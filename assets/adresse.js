/* ==========================================================
   louviers.immo — « Mon adresse »
   1. Géocode l'adresse (Base Adresse Nationale)
   2. Interroge OpenStreetMap (Overpass) autour du point
   3. Estime les temps de trajet et liste les commerces proches,
      en reliant ceux qui ont un portrait (data/portraits.js)
   4. Affiche les prix DVF autour de l'adresse (data/dvf.json)
   ========================================================== */
(function () {
  'use strict';
  var LI = window.LI;
  var $ = function (id) { return document.getElementById(id); };

  /* ---------- Paramètres des estimations ---------- */
  // Distance réelle ≈ distance à vol d'oiseau × détour moyen en ville
  var DETOUR = 1.3;
  var SPEED = { walk: 80, bike: 250 };                  // mètres par minute (4,8 km/h et 15 km/h)
  function carMinutes(m) {                               // ville lente, puis route
    var d = m * DETOUR;
    var t = d < 3000 ? d / 420 : 3000 / 420 + (d - 3000) / 900;
    return Math.max(2, Math.round(t + 1));
  }
  function minutes(mode, m) {
    if (mode === 'car') return carMinutes(m);
    return Math.max(1, Math.round(m * DETOUR / SPEED[mode]));
  }
  function fmtMin(n) {
    if (n >= 60) { var h = Math.floor(n / 60), r = n % 60; return h + ' h' + (r ? ' ' + String(r).padStart(2, '0') : ''); }
    return n + ' min';
  }
  function fmtDist(m) { return m < 1000 ? (Math.round(m / 10) * 10) + ' m' : LI.fmt(m / 1000, 1) + ' km'; }

  /* ---------- Overpass (OpenStreetMap) ---------- */
  var OVERPASS = ['https://overpass-api.de/api/interpreter', 'https://overpass.private.coffee/api/interpreter', 'https://overpass.kumi.systems/api/interpreter'];
  function overpass(lat, lon) {
    var p = lat.toFixed(6) + ',' + lon.toFixed(6);
    var q = '[out:json][timeout:25];(' +
      'nwr(around:1500,' + p + ')[shop][shop!~"vacant|estate_agent"][name];' +
      'nwr(around:1500,' + p + ')[amenity~"^(pharmacy|restaurant|cafe|bar|pub|fast_food|ice_cream|bank|post_office|doctors|dentist|clinic|library|marketplace|townhall)$"];' +
      'nwr(around:1500,' + p + ')[leisure~"^(park|playground|sports_centre|swimming_pool|pitch)$"][name];' +
      'node(around:1500,' + p + ')[highway=bus_stop];' +
      'nwr(around:6000,' + p + ')[amenity~"^(school|kindergarten|college)$"];' +
      'nwr(around:6000,' + p + ')[shop=supermarket];' +
      'node(around:20000,' + p + ')[railway~"^(station|halt)$"][station!~"subway|light_rail"];' +
      'node(around:20000,' + p + ')[highway=motorway_junction];' +
      ');out center tags;';
    function attempt(i) {
      return LI.fetchJSON(OVERPASS[i], {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'data=' + encodeURIComponent(q)
      }, 20000).catch(function (e) {
        if (i + 1 < OVERPASS.length) return attempt(i + 1);
        throw e;
      });
    }
    return attempt(0).then(function (j) {
      var seen = {};
      return (j.elements || []).map(function (e) {
        var la = e.lat != null ? e.lat : (e.center && e.center.lat);
        var lo = e.lon != null ? e.lon : (e.center && e.center.lon);
        if (la == null) return null;
        var id = e.type + '/' + e.id;
        if (seen[id]) return null;
        seen[id] = 1;
        var t = e.tags || {};
        return { id: id, lat: la, lon: lo, t: t, name: t.name || '', d: LI.dist(lat, lon, la, lo) };
      }).filter(Boolean);
    });
  }

  // Lieux autour du point : fichier pré-téléchargé si l'adresse est dans la zone, sinon OpenStreetMap en direct
  function getPois(lat, lon) {
    return LI.loadPOIs().then(function (c) {
      if (!c || !LI.inBBox(c.bbox, lat, lon, -0.02)) return overpass(lat, lon);
      return c.pois.map(function (p) {
        var t = p.t, d = LI.dist(lat, lon, p.lat, p.lon), max = 1500;
        if (t.railway || t.highway === 'motorway_junction') max = 20000;
        else if (/^(school|kindergarten|college)$/.test(t.amenity || '') || t.shop === 'supermarket') max = 6000;
        if (d > max) return null;
        if (t.shop && !t.name) return null;
        return { id: p.id, lat: p.lat, lon: p.lon, t: t, name: t.name || '', d: d };
      }).filter(Boolean);
    });
  }

  /* ---------- Catégories ---------- */
  var SHOP_FR = {
    bakery: 'Boulangerie', pastry: 'Pâtisserie', butcher: 'Boucherie', greengrocer: 'Primeur', cheese: 'Fromagerie',
    supermarket: 'Supermarché', convenience: 'Épicerie', deli: 'Traiteur', wine: 'Caviste', alcohol: 'Caviste',
    chocolate: 'Chocolatier', confectionery: 'Confiserie', seafood: 'Poissonnerie', coffee: 'Torréfacteur', tea: 'Thé',
    farm: 'Produits fermiers', organic: 'Bio', frozen_food: 'Surgelés', beverages: 'Boissons',
    estate_agent: 'Agence immobilière', hairdresser: 'Coiffeur', beauty: 'Institut de beauté', florist: 'Fleuriste', laundry: 'Laverie', dry_cleaning: 'Pressing',
    optician: 'Opticien', hearing_aids: 'Audioprothésiste', medical_supply: 'Matériel médical',
    clothes: 'Vêtements', shoes: 'Chaussures', books: 'Librairie', gift: 'Cadeaux', jewelry: 'Bijouterie',
    furniture: 'Ameublement', hardware: 'Quincaillerie', doityourself: 'Bricolage', newsagent: 'Presse', tobacco: 'Tabac',
    toys: 'Jouets', sports: 'Sport', bicycle: 'Vélos', electronics: 'Électronique', mobile_phone: 'Téléphonie',
    interior_decoration: 'Décoration', variety_store: 'Bazar', garden_centre: 'Jardinerie', pet: 'Animalerie',
    car_repair: 'Garage', car: 'Automobile', tattoo: 'Tatouage', copyshop: 'Reprographie', travel_agency: 'Agence de voyages',
    second_hand: 'Dépôt-vente', computer: 'Informatique', kitchen: 'Cuisines', bed: 'Literie', art: 'Galerie',
    photo: 'Photographe', music: 'Musique', stationery: 'Papeterie', cosmetics: 'Parfumerie', perfumery: 'Parfumerie',
    massage: 'Massage', funeral_directors: 'Pompes funèbres', paint: 'Peinture', houseware: 'Arts de la table'
  };
  var AMENITY_FR = {
    pharmacy: 'Pharmacie', restaurant: 'Restaurant', cafe: 'Café', bar: 'Bar', pub: 'Pub', fast_food: 'Restauration rapide',
    ice_cream: 'Glacier', bank: 'Banque', post_office: 'Bureau de poste', doctors: 'Médecin', dentist: 'Dentiste',
    clinic: 'Centre médical', library: 'Bibliothèque', marketplace: 'Marché', townhall: 'Mairie'
  };
  var FAMILY = {
    alim: ['bakery', 'pastry', 'butcher', 'greengrocer', 'cheese', 'supermarket', 'convenience', 'deli', 'wine', 'alcohol', 'chocolate', 'confectionery', 'seafood', 'coffee', 'tea', 'farm', 'organic', 'frozen_food', 'beverages', 'marketplace'],
    resto: ['restaurant', 'cafe', 'bar', 'pub', 'fast_food', 'ice_cream'],
    sante: ['pharmacy', 'optician', 'hearing_aids', 'medical_supply', 'doctors', 'dentist', 'clinic'],
    serv: ['estate_agent', 'notary', 'hairdresser', 'beauty', 'florist', 'laundry', 'dry_cleaning', 'bank', 'post_office', 'travel_agency', 'copyshop', 'tattoo', 'massage', 'car_repair', 'funeral_directors', 'library']
  };
  function kindOf(t) {
    if (t.shop) return t.shop;
    if (t.amenity) return t.amenity;
    return '';
  }
  function labelOf(k) { return SHOP_FR[k] || AMENITY_FR[k] || 'Commerce'; }
  function familyOf(k) {
    for (var f in FAMILY) if (FAMILY[f].indexOf(k) >= 0) return f;
    return 'shop';
  }

  function nearest(list, pred) {
    var best = null;
    list.forEach(function (p) { if (pred(p) && (!best || p.d < best.d)) best = p; });
    return best;
  }
  function schoolType(p) {
    var n = LI.norm(p.name), t = p.t;
    if (/\blycee\b/.test(n) || t['isced:level'] === '3' || t.amenity === 'college') return 'lycee';
    if (/\bcollege\b/.test(n) || t['isced:level'] === '2') return 'college';
    if (t.amenity === 'kindergarten') return 'creche';
    if (t.amenity === 'school') return 'ecole';
    return '';
  }

  /* ---------- État ---------- */
  var S = { lat: null, lon: null, label: '', pois: [], mode: 'walk', fam: 'all', map: null, layers: null, shopsShown: [] };

  /* ---------- Trajets ---------- */
  function buildTrips() {
    var P = S.pois;
    var pt = function (k) { return function (p) { return p.t.shop === k || p.t.amenity === k; }; };
    var station = nearest(P, function (p) { return !!p.t.railway; });
    var junction = nearest(P, function (p) { return p.t.highway === 'motorway_junction'; });
    var groups = [
      { title: 'Au quotidien', rows: [
        ['Boulangerie', nearest(P, pt('bakery'))],
        ['Pharmacie', nearest(P, pt('pharmacy'))],
        ['Supermarché', nearest(P, pt('supermarket'))],
        ['Médecin', nearest(P, pt('doctors'))],
        ['Bureau de poste', nearest(P, pt('post_office'))]
      ] },
      { title: 'Écoles', rows: [
        ['Crèche ou multi-accueil', nearest(P, function (p) { return schoolType(p) === 'creche'; })],
        ['École', nearest(P, function (p) { return schoolType(p) === 'ecole'; })],
        ['Collège', nearest(P, function (p) { return schoolType(p) === 'college'; })],
        ['Lycée', nearest(P, function (p) { return schoolType(p) === 'lycee'; })]
      ] },
      { title: 'Se déplacer', rows: [
        ['Arrêt de bus', nearest(P, function (p) { return p.t.highway === 'bus_stop'; })],
        ['Gare' + (station && station.name ? ' — ' + station.name : ''), station, true],
        ['Accès autoroute' + (junction ? (junction.t.ref ? ' — sortie ' + junction.t.ref : '') + (junction.name ? ' (' + junction.name + ')' : '') : ''), junction, true]
      ] },
      { title: 'Loisirs', rows: [
        ['Parc ou jardin', nearest(P, function (p) { return p.t.leisure === 'park'; })],
        ['Aire de jeux', nearest(P, function (p) { return p.t.leisure === 'playground'; })],
        ['Équipement sportif', nearest(P, function (p) { return /sports_centre|swimming_pool|pitch/.test(p.t.leisure || ''); })]
      ] }
    ];
    var html = groups.map(function (g) {
      var rows = g.rows.map(function (r) {
        var lbl = r[0], p = r[1];
        if (!p) {
          return '<div class="trow na"><div><div class="lbl">' + LI.esc(lbl) + '</div><div class="sub">Rien de référencé à proximité</div></div><div class="bar"></div><div class="tm">—</div></div>';
        }
        var m = minutes(S.mode, p.d);
        var tooFar = S.mode === 'walk' && m > 45;
        var w = Math.min(100, Math.round(m / 40 * 100));
        var sub = (p.name && lbl.indexOf(p.name) < 0 ? p.name + ' · ' : '') + fmtDist(p.d) + ' à vol d’oiseau';
        return '<div class="trow' + (tooFar ? ' na' : '') + '"><div><div class="lbl">' + LI.esc(lbl) + '</div><div class="sub">' + LI.esc(sub) + '</div></div>' +
          '<div class="bar"><i style="width:' + (tooFar ? 100 : w) + '%"></i></div>' +
          '<div class="tm">' + (tooFar ? '+45 min' : fmtMin(m)) + '</div></div>';
      }).join('');
      return '<div class="tgroup"><h3>' + LI.esc(g.title) + '</h3>' + rows + '</div>';
    }).join('');
    $('trips').innerHTML = html;
    var lbl = { walk: 'à pied', bike: 'à vélo', car: 'en voiture' }[S.mode];
    $('mode-label').textContent = lbl;

    // Arrêts de bus et lignes
    var stops = P.filter(function (p) { return p.t.highway === 'bus_stop'; }).sort(function (a, b) { return a.d - b.d; });
    var uniq = [], names = {};
    stops.forEach(function (s) { var k = LI.norm(s.name) || s.id; if (!names[k] && uniq.length < 3) { names[k] = 1; uniq.push(s); } });
    $('bus').innerHTML = uniq.length ? uniq.map(function (s) {
      var lines = s.t.route_ref ? '<span class="tag" style="margin-left:8px">Ligne' + (/[;,]/.test(s.t.route_ref) ? 's ' : ' ') + LI.esc(s.t.route_ref.replace(/;/g, ', ')) + '</span>' : '';
      return '<div class="trow"><div><div class="lbl">' + LI.esc(s.name || 'Arrêt sans nom') + lines + '</div><div class="sub">' + fmtDist(s.d) + '</div></div><div class="bar"></div><div class="tm">' + fmtMin(minutes('walk', s.d)) + '</div></div>';
    }).join('') : '<p class="muted small" style="padding:12px 0">Aucun arrêt référencé à moins de 1,5 km.</p>';
  }

  /* ---------- Commerces ---------- */
  function shopsAll() {
    var P = S.pois.filter(function (p) {
      var k = kindOf(p.t);
      if (!k || !p.name) return false;
      if (p.t.shop === 'estate_agent' || p.t.shop === 'vacant' || p.t.office) return false; // pas d'agences immobilières
      if (p.t.shop) return true;
      return !!AMENITY_FR[k] && ['library', 'townhall'].indexOf(k) < 0 && p.d <= 1500;
    }).filter(function (p) { return p.d <= 1500; });
    var portraits = LI.portraits();
    var used = {};
    P.forEach(function (p) {
      var hit = null;
      portraits.forEach(function (pr, i) {
        if (hit) return;
        if (pr.osm && pr.osm === p.id) hit = i;
        else if (pr.lat != null && pr.lon != null) {
          var dd = LI.dist(pr.lat, pr.lon, p.lat, p.lon);
          var names = [pr.name].concat(pr.aliases || []).map(LI.norm);
          if (dd < 15 || (dd < 150 && names.indexOf(LI.norm(p.name)) >= 0)) hit = i;
        }
      });
      if (hit != null) { p.portrait = portraits[hit]; used[hit] = 1; }
    });
    // Portraits absents d'OpenStreetMap mais situés dans le périmètre
    portraits.forEach(function (pr, i) {
      if (used[i] || pr.lat == null) return;
      var d = LI.dist(S.lat, S.lon, pr.lat, pr.lon);
      if (d <= 1500) P.push({ id: 'portrait/' + i, lat: pr.lat, lon: pr.lon, name: pr.name, d: d, t: { shop: pr.kind || '' }, portrait: pr, label: pr.category });
    });
    (S.agences || []).forEach(function (a) {
      if (a.lat == null) return;
      var d = LI.dist(S.lat, S.lon, a.lat, a.lon);
      if (d <= 1500) P.push({ id: 'partenaire/' + a.name, lat: a.lat, lon: a.lon, name: a.name, d: d, t: { shop: a.rubrique === 'immobilier' ? 'estate_agent' : (a.rubrique === 'notaires' ? 'notary' : 'bank') }, label: a.category || '', own: a });
    });
    P.sort(function (a, b) { return a.d - b.d; });
    return P;
  }
  function renderShops() {
    var all = shopsAll();
    var list = all.filter(function (p) {
      if (S.fam === 'all') return true;
      var f = familyOf(kindOf(p.t));
      return S.fam === 'shop' ? f === 'shop' : f === S.fam;
    }).slice(0, 12);
    S.shopsShown = list;
    var box = $('shops');
    if (!list.length) {
      box.innerHTML = '<div class="state" style="grid-column:1/-1">Aucun commerce de cette catégorie référencé à moins de 1,5 km.</div>';
    } else {
      box.innerHTML = list.map(function (p, i) {
        var lab = p.label || labelOf(kindOf(p.t));
        var pt = p.portrait ? '<a class="pt" href="' + LI.esc(LI.root + p.portrait.url) + '">Lire son portrait <span class="arrow">→</span></a>' : '';
        if (p.own) {
          var l0 = (p.own.links && p.own.links[0]) || (p.own.web ? { label: 'Site web', url: p.own.web } : null);
          pt = (p.own.badge ? '<span class="pt" style="margin-right:8px">' + LI.esc(p.own.badge) + '</span>' : '') +
            (l0 ? '<a class="pt" href="' + LI.esc(LI.partnerLink(l0.url)) + '"' + (/^https?:/i.test(l0.url) ? ' target="_blank" rel="noopener"' : '') + '>' + LI.esc(l0.label) + ' <span class="arrow">→</span></a>' : '');
        }
        return '<div class="shop' + (p.portrait || (p.own && p.own.badge) ? ' has-portrait' : '') + '"><div class="num" aria-hidden="true">' + (i + 1) + '</div><div>' +
          '<div class="k">' + LI.esc(lab) + '</div><div class="nm">' + LI.esc(p.name) + '</div>' +
          '<div class="ds">' + fmtMin(minutes('walk', p.d)) + ' à pied · ' + fmtDist(p.d) + '</div>' + pt + '</div></div>';
      }).join('');
    }
    drawShopMarkers();
  }

  /* ---------- Carte ---------- */
  function initMap() {
    if (!window.L) return;
    if (!S.map) {
      S.map = LI.makeMap($('map'), S.lat, S.lon, 15);
      S.layers = L.layerGroup().addTo(S.map);
      S.shopLayer = L.layerGroup().addTo(S.map);
      S.map.attributionControl.addAttribution('Lieux &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">contributeurs OpenStreetMap</a>');
    } else {
      S.map.setView([S.lat, S.lon], 15);
    }
    S.layers.clearLayers();
    // Cercles ≈ 5, 10 et 15 min à pied
    [5, 10, 15].forEach(function (m) {
      var r = m * SPEED.walk / DETOUR;
      L.circle([S.lat, S.lon], { radius: r, color: '#9C7C33', weight: 1.5, dashArray: '4 6', fill: m === 5, fillColor: '#C9A961', fillOpacity: 0.08, interactive: false }).addTo(S.layers);
      var lab = L.latLng(S.lat + (r / 111320), S.lon);
      L.marker(lab, { icon: L.divIcon({ className: '', html: '<span class="ring-label">≈ ' + m + ' MIN</span>', iconSize: [70, 20], iconAnchor: [35, 10] }), interactive: false, keyboard: false }).addTo(S.layers);
    });
    L.marker([S.lat, S.lon], { icon: LI.divIcon('<div class="pin-me"></div>', '', 22), title: S.label, zIndexOffset: 1000 })
      .bindPopup('<strong>' + LI.esc(S.label) + '</strong>').addTo(S.layers);
    setTimeout(function () { S.map.invalidateSize(); }, 50);
  }
  function drawShopMarkers() {
    if (!S.map) return;
    S.shopLayer.clearLayers();
    var bounds = [[S.lat, S.lon]];
    S.shopsShown.forEach(function (p, i) {
      L.marker([p.lat, p.lon], { icon: LI.divIcon('<div class="pin-n' + (p.portrait || (p.own && p.own.badge) ? ' star' : '') + '">' + (i + 1) + '</div>', '', 28), title: p.name })
        .bindPopup('<strong>' + LI.esc(p.name) + '</strong><br>' + LI.esc(p.label || labelOf(kindOf(p.t))) + ' · ' + fmtMin(minutes('walk', p.d)) + ' à pied' +
          (p.portrait ? '<br><a href="' + LI.esc(LI.root + p.portrait.url) + '">Lire son portrait →</a>' : ''))
        .addTo(S.shopLayer);
      bounds.push([p.lat, p.lon]);
    });
    if (bounds.length > 1) S.map.fitBounds(bounds, { padding: [40, 40], maxZoom: 16 });
  }

  /* ---------- Prix DVF ---------- */
  function renderPrices() {
    LI.loadDVF().then(function (d) {
      var box = $('prices');
      if (!d.sales.length) {
        box.innerHTML = '<div class="kpi light"><div class="l">Prix au m²</div><div class="v">Bientôt</div><div class="u">Données DVF en cours d’intégration</div></div>';
        return;
      }
      var near = d.sales.filter(function (s) { return LI.dist(S.lat, S.lon, s.lat, s.lon) <= 500; });
      var mh = LI.median(near.filter(function (s) { return s.type === 'M'; }).map(function (s) { return s.pm2; }));
      var ma = LI.median(near.filter(function (s) { return s.type === 'A'; }).map(function (s) { return s.pm2; }));
      var nh = near.filter(function (s) { return s.type === 'M'; }).length;
      var na = near.filter(function (s) { return s.type === 'A'; }).length;
      function v(x, n) { return x && n >= 3 ? LI.fmt(Math.round(x / 10) * 10) + ' €' : '—'; }
      box.innerHTML =
        '<div class="kpi light"><div class="l">Maison</div><div class="v">' + v(mh, nh) + '</div><div class="u">€/m² médian · ' + nh + ' vente' + (nh > 1 ? 's' : '') + '</div></div>' +
        '<div class="kpi light"><div class="l">Appartement</div><div class="v">' + v(ma, na) + '</div><div class="u">€/m² médian · ' + na + ' vente' + (na > 1 ? 's' : '') + '</div></div>' +
        '<div class="kpi light"><div class="l">Ventes à 500 m</div><div class="v">' + LI.fmt(near.length) + '</div><div class="u">' + (d.meta.period ? LI.monthFR(d.meta.period.from) + ' – ' + LI.monthFR(d.meta.period.to) : 'source DVF') + '</div></div>';
      $('prices-link').href = LI.root + 'prix.html?lat=' + S.lat.toFixed(5) + '&lon=' + S.lon.toFixed(5);
    });
  }

  /* ---------- Chargement d'une adresse ---------- */
  function setLoading() {
    var sk = '<div class="tgroup">' + [1, 2, 3, 4, 5].map(function () { return '<div class="trow"><div class="skel" style="width:70%"></div><div class="skel"></div><div class="skel"></div></div>'; }).join('') + '</div>';
    $('trips').innerHTML = sk;
    $('bus').innerHTML = '';
    $('shops').innerHTML = '<div class="state" style="grid-column:1/-1"><span class="loader"></span>Recherche des commerces autour de l’adresse…</div>';
  }
  function showError() {
    var msg = '<div class="state">Les données OpenStreetMap ne répondent pas pour le moment. <button type="button" class="btn btn-line" id="retry" style="margin-top:14px">Réessayer</button></div>';
    $('trips').innerHTML = msg;
    $('shops').innerHTML = '';
    var b = $('retry'); if (b) b.addEventListener('click', loadPlace);
  }
  function loadPlace() {
    $('res-title').textContent = S.label;
    document.title = S.label + ' — vivre ici · louviers.immo';
    var far = LI.dist(S.lat, S.lon, LI.center.lat, LI.center.lon) > 25000;
    $('far').hidden = !far;
    initMap();
    renderPrices();
    setLoading();
    Promise.all([getPois(S.lat, S.lon), LI.resolvePortraits(), LI.resolveAgences()]).then(function (res) {
      S.pois = res[0];
      S.agences = res[2];
      buildTrips();
      renderShops();
    }).catch(showError);
  }
  function go(r) {
    S.lat = r.lat; S.lon = r.lon; S.label = r.label;
    var sub = [r.postcode, r.city].filter(Boolean).join(' ');
    $('res-city').textContent = r.type === 'municipality' ? (r.context || '') : sub;
    history.replaceState(null, '', 'adresse.html?q=' + encodeURIComponent(r.label) + '&lat=' + r.lat.toFixed(6) + '&lon=' + r.lon.toFixed(6));
    $('results').hidden = false;
    $('intro').hidden = true;
    loadPlace();
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Boutons de mode
    document.querySelectorAll('.mode').forEach(function (b) {
      b.addEventListener('click', function () {
        S.mode = b.getAttribute('data-mode');
        document.querySelectorAll('.mode').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        if (S.pois.length) buildTrips();
      });
    });
    document.querySelectorAll('.cat').forEach(function (b) {
      b.addEventListener('click', function () {
        S.fam = b.getAttribute('data-fam');
        document.querySelectorAll('.cat').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        if (S.pois.length || LI.portraits().length) renderShops();
      });
    });
    // La recherche de cette page recharge les résultats sans changer de page
    var form = document.querySelector('form.search');
    if (form) form._onChoose = go;

    var u = new URLSearchParams(location.search);
    var q = u.get('q'), lat = parseFloat(u.get('lat')), lon = parseFloat(u.get('lon'));
    if (q && isFinite(lat) && isFinite(lon)) {
      go({ label: q, lat: lat, lon: lon, city: '', postcode: '' });
      LI.geocode(q, 1, false).then(function (r) {
        if (r[0] && LI.dist(r[0].lat, r[0].lon, lat, lon) < 200) {
          $('res-city').textContent = r[0].type === 'municipality' ? (r[0].context || '') : [r[0].postcode, r[0].city].filter(Boolean).join(' ');
        }
      }).catch(function () {});
    } else if (q) {
      LI.geocode(q, 1, false).then(function (r) {
        if (r.length) go(r[0]);
        else { $('intro-msg').textContent = 'Adresse introuvable : « ' + q + ' ». Essayez avec le nom de la rue et la commune.'; }
      }).catch(function () { $('intro-msg').textContent = 'Le service d’adresses ne répond pas. Réessayez dans un instant.'; });
    }
  });
})();
