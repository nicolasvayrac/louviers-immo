/* ==========================================================
   louviers.immo — Annuaire des commerçants
   Source : OpenStreetMap (Overpass), par commune (code INSEE).
   Les commerces ayant un portrait (data/portraits.js) passent en tête.
   ========================================================== */
(function () {
  'use strict';
  var LI = window.LI;
  var $ = function (id) { return document.getElementById(id); };

  var COMMUNES = [
    ['27375', 'Louviers'], ['27598', 'Saint-Pierre-du-Vauvray'], ['27528', 'Le Vaudreuil'], ['27701', 'Val-de-Reuil'],
    ['27351', 'Incarville'], ['27469', "Pont-de-l'Arche"], ['27003', 'Acquigny'], ['27015', 'Andé'],
    ['27537', 'Saint-Étienne-du-Vauvray'], ['27456', 'Pinterville']
  ];

  // Rubriques : [id, titre, description, valeurs OSM (shop / amenity / craft)]
  var RUB = [
    ['restaurer', 'Se restaurer', 'Restaurants, brasseries, tables du midi et du soir', ['restaurant']],
    ['snacking', 'Snacking', 'Pour le midi : sur le pouce, à emporter', ['fast_food', 'food_court', 'sandwich', 'caterer']],
    ['cafes', 'Cafés & bars', 'Un café en terrasse, un verre en fin de journée', ['cafe', 'bar', 'pub', 'ice_cream', 'tea', 'coffee']],
    ['boulangeries', 'Boulangeries & pâtisseries', 'Le pain du matin et les douceurs du dimanche', ['bakery', 'pastry', 'confectionery', 'chocolate']],
    ['bouche', 'Métiers de bouche', 'Charcutiers, bouchers, fromagers, primeurs, cavistes', ['butcher', 'cheese', 'greengrocer', 'seafood', 'deli', 'wine', 'alcohol', 'farm', 'organic', 'beverages', 'frozen_food', 'spices']],
    ['courses', 'Courses du quotidien', 'Supermarchés et épiceries', ['supermarket', 'convenience', 'general']],
    ['habiller', 'S’habiller', 'Mode, chaussures, accessoires et bijoux', ['clothes', 'shoes', 'boutique', 'fashion_accessories', 'bag', 'jewelry', 'watches', 'leather', 'tailor', 'fabric', 'baby_goods']],
    ['beaute', 'Beauté & bien-être', 'Coiffeurs, instituts, parfumeries', ['hairdresser', 'beauty', 'cosmetics', 'perfumery', 'massage', 'tattoo', 'barber']],
    ['maison', 'Maison & déco', 'Décoration, fleurs, ameublement, bricolage', ['furniture', 'interior_decoration', 'houseware', 'florist', 'garden_centre', 'hardware', 'doityourself', 'kitchen', 'bed', 'paint', 'lighting', 'antiques', 'second_hand', 'carpet', 'curtain', 'tiles', 'bathroom_furnishing']],
    ['loisirs', 'Culture & loisirs', 'Livres, jeux, sport, cadeaux', ['books', 'music', 'art', 'toys', 'games', 'sports', 'bicycle', 'outdoor', 'photo', 'stationery', 'gift', 'craft', 'video_games', 'newsagent', 'tobacco', 'pet']],
    ['sante', 'Santé', 'Pharmacies, opticiens, audioprothésistes', ['pharmacy', 'optician', 'hearing_aids', 'medical_supply', 'chemist']],
    ['services', 'Services', 'Banques, poste, pressing, téléphonie, garages', ['bank', 'post_office', 'laundry', 'dry_cleaning', 'travel_agency', 'copyshop', 'mobile_phone', 'electronics', 'computer', 'car_repair', 'car', 'funeral_directors', 'insurance', 'locksmith', 'shoe_repair', 'repair']]
  ];
  var LABEL = {
    restaurant: 'Restaurant', fast_food: 'Restauration rapide', food_court: 'Restauration', sandwich: 'Sandwicherie', caterer: 'Traiteur',
    cafe: 'Café', bar: 'Bar', pub: 'Pub', ice_cream: 'Glacier', tea: 'Salon de thé', coffee: 'Torréfacteur',
    bakery: 'Boulangerie', pastry: 'Pâtisserie', confectionery: 'Confiserie', chocolate: 'Chocolatier',
    butcher: 'Boucherie-charcuterie', cheese: 'Fromagerie', greengrocer: 'Primeur', seafood: 'Poissonnerie', deli: 'Épicerie fine', wine: 'Caviste', alcohol: 'Caviste', farm: 'Produits fermiers', organic: 'Bio', beverages: 'Boissons', frozen_food: 'Surgelés', spices: 'Épices',
    supermarket: 'Supermarché', convenience: 'Épicerie', general: 'Épicerie',
    clothes: 'Vêtements', shoes: 'Chaussures', boutique: 'Boutique', fashion_accessories: 'Accessoires', bag: 'Maroquinerie', jewelry: 'Bijouterie', watches: 'Horlogerie', leather: 'Maroquinerie', tailor: 'Retouches', fabric: 'Tissus', baby_goods: 'Puériculture',
    hairdresser: 'Coiffeur', beauty: 'Institut de beauté', cosmetics: 'Cosmétiques', perfumery: 'Parfumerie', massage: 'Massage', tattoo: 'Tatouage', barber: 'Barbier',
    furniture: 'Ameublement', interior_decoration: 'Décoration', houseware: 'Arts de la table', florist: 'Fleuriste', garden_centre: 'Jardinerie', hardware: 'Quincaillerie', doityourself: 'Bricolage', kitchen: 'Cuisines', bed: 'Literie', paint: 'Peinture', lighting: 'Luminaires', antiques: 'Antiquités', second_hand: 'Dépôt-vente', carpet: 'Tapis', curtain: 'Rideaux', tiles: 'Carrelage', bathroom_furnishing: 'Salles de bain',
    books: 'Librairie', music: 'Musique', art: 'Galerie', toys: 'Jouets', games: 'Jeux', sports: 'Sport', bicycle: 'Vélos', outdoor: 'Plein air', photo: 'Photo', stationery: 'Papeterie', gift: 'Cadeaux', craft: 'Loisirs créatifs', video_games: 'Jeux vidéo', newsagent: 'Presse', tobacco: 'Tabac-presse', pet: 'Animalerie',
    pharmacy: 'Pharmacie', optician: 'Opticien', hearing_aids: 'Audioprothésiste', medical_supply: 'Matériel médical', chemist: 'Droguerie',
    bank: 'Banque', post_office: 'Bureau de poste', laundry: 'Laverie', dry_cleaning: 'Pressing', travel_agency: 'Agence de voyages', copyshop: 'Reprographie', mobile_phone: 'Téléphonie', electronics: 'Électronique', computer: 'Informatique', car_repair: 'Garage', car: 'Automobile', funeral_directors: 'Pompes funèbres', insurance: 'Assurance', locksmith: 'Serrurier', shoe_repair: 'Cordonnier', repair: 'Réparation'
  };
  var KIND2RUB = {};
  RUB.forEach(function (r) { r[3].forEach(function (k) { if (!KIND2RUB[k]) KIND2RUB[k] = r[0]; }); });

  var S = { insee: '27375', all: [], rub: 'all', q: '', map: null, layer: null };

  function kindOf(t) {
    if (t.amenity && KIND2RUB[t.amenity]) return t.amenity;
    if (t.shop && KIND2RUB[t.shop]) return t.shop;
    if (t.craft && KIND2RUB[t.craft]) return t.craft;
    return t.shop || t.amenity || t.craft || '';
  }
  function addrOf(t) {
    var a = [t['addr:housenumber'], t['addr:street']].filter(Boolean).join(' ');
    return a;
  }
  function safeUrl(u) {
    if (!u) return '';
    u = String(u).trim();
    if (!/^https?:\/\//i.test(u)) u = 'https://' + u;
    return /^https?:\/\/[^\s"'<>]+$/i.test(u) ? u : '';
  }

  /* ---------- Chargement ---------- */
  function fromElement(id, la, lo, t) {
    if (la == null || !t.name || t.office) return null;
    var k = kindOf(t), r = KIND2RUB[k];
    if (!r) return null;
    return { id: id, name: t.name, lat: la, lon: lo, kind: k, rub: r, addr: addrOf(t), web: safeUrl(t.website || t['contact:website']), phone: t.phone || t['contact:phone'] || '' };
  }
  function dedupe(list) {
    var seen = {};
    return list.filter(function (s) {
      var k = LI.norm(s.name) + '|' + Math.round(s.lat * 2000) + '|' + Math.round(s.lon * 2000);
      if (seen[k]) return false; seen[k] = 1; return true;
    });
  }
  function query(insee) {
    return LI.loadPOIs().then(function (c) {
      if (c && c.pois.some(function (p) { return p.c === insee; })) {
        return dedupe(c.pois.filter(function (p) { return p.c === insee; }).map(function (p) { return fromElement(p.id, p.lat, p.lon, p.t); }).filter(Boolean));
      }
      return queryLive(insee);
    });
  }
  function queryLive(insee) {
    var key = 'li-commerces-' + insee;
    try {
      var c = JSON.parse(sessionStorage.getItem(key) || 'null');
      if (c && Date.now() - c.t < 3600e3) return Promise.resolve(c.d);
    } catch (e) { /* stockage indisponible */ }
    var q = '[out:json][timeout:30];area["ref:INSEE"="' + insee + '"]["boundary"="administrative"]->.a;(' +
      'nwr(area.a)[shop][name][shop!~"^(vacant|estate_agent)$"];' +
      'nwr(area.a)[amenity~"^(restaurant|fast_food|food_court|cafe|bar|pub|ice_cream|pharmacy|bank|post_office)$"][name];' +
      'nwr(area.a)[craft~"^(bakery|caterer|confectionery|butcher|shoe_repair|tailor|locksmith)$"][name];' +
      ');out center tags;';
    var urls = ['https://overpass-api.de/api/interpreter', 'https://overpass.private.coffee/api/interpreter', 'https://overpass.kumi.systems/api/interpreter'];
    function attempt(i) {
      return LI.fetchJSON(urls[i], { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'data=' + encodeURIComponent(q) }, 20000)
        .catch(function (e) { if (i + 1 < urls.length) return attempt(i + 1); throw e; });
    }
    return attempt(0).then(function (j) {
      var seen = {};
      var d = (j.elements || []).map(function (e) {
        var la = e.lat != null ? e.lat : (e.center && e.center.lat), lo = e.lon != null ? e.lon : (e.center && e.center.lon);
        var t = e.tags || {};
        if (la == null || !t.name || t.office) return null;
        var k = kindOf(t), r = KIND2RUB[k];
        if (!r) return null;
        var key2 = LI.norm(t.name) + '|' + Math.round(la * 2000) + '|' + Math.round(lo * 2000);
        if (seen[key2]) return null; seen[key2] = 1;
        return { id: e.type + '/' + e.id, name: t.name, lat: la, lon: lo, kind: k, rub: r, addr: addrOf(t), web: safeUrl(t.website || t['contact:website']), phone: t.phone || t['contact:phone'] || '' };
      }).filter(Boolean);
      try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), d: d })); } catch (e) { /* plein ou bloqué */ }
      return d;
    });
  }

  function attachPortraits(list) {
    return LI.resolvePortraits().then(function (ps) {
      var com = (COMMUNES.filter(function (c) { return c[0] === S.insee; })[0] || [])[1];
      ps.forEach(function (p) {
        var names = [p.name].concat(p.aliases || []).map(LI.norm);
        var hit = null;
        list.forEach(function (s) {
          if (hit) return;
          if (p.osm && p.osm === s.id) { hit = s; return; }
          var near = p.lat != null && LI.dist(p.lat, p.lon, s.lat, s.lon) < 120;
          if (names.indexOf(LI.norm(s.name)) >= 0 && (near || p.lat == null)) hit = s;
          else if (p.lat != null && LI.dist(p.lat, p.lon, s.lat, s.lon) < 15) hit = s;
        });
        if (hit) {
          hit.portrait = p;
          if (p.rubrique) hit.rub = p.rubrique;
          if (p.website && !hit.web) hit.web = p.website;
          if (p.address && !hit.addr) hit.addr = p.address.replace(/\s*\d{5}.*$/, '');
        } else if (p.commune === com && p.lat != null) {
          list.push({ id: 'portrait/' + p.url, name: p.name, lat: p.lat, lon: p.lon, kind: p.kind || '', rub: p.rubrique || 'bouche',
            addr: (p.address || '').replace(/\s*\d{5}.*$/, ''), web: p.website || '', phone: p.phone || '', portrait: p, label: p.category });
        }
      });
      return list;
    });
  }

  /* ---------- Affichage ---------- */
  function card(s) {
    var lab = s.label || (s.portrait && s.portrait.category) || LABEL[s.kind] || 'Commerce';
    var links = [];
    if (s.portrait) links.push('<a class="pt" href="' + LI.esc(LI.root + s.portrait.url) + '">Lire son portrait <span class="arrow">→</span></a>');
    if (s.web) links.push('<a class="cx" href="' + LI.esc(s.web) + '" target="_blank" rel="noopener">Site web ↗</a>');
    links.push('<a class="cx" href="' + LI.esc(LI.root + 'adresse.html?q=' + encodeURIComponent(s.name + (s.addr ? ', ' + s.addr : '')) + '&lat=' + s.lat.toFixed(6) + '&lon=' + s.lon.toFixed(6)) + '">Voir le quartier</a>');
    return '<article class="biz' + (s.portrait ? ' has-portrait' : '') + '">' +
      '<div class="k">' + LI.esc(lab) + (s.portrait ? ' · <span class="star">Portrait</span>' : '') + '</div>' +
      '<h3 class="nm">' + LI.esc(s.name) + '</h3>' +
      (s.addr ? '<div class="ds">' + LI.esc(s.addr) + '</div>' : '') +
      (s.phone ? '<div class="ds"><a href="tel:' + LI.esc(s.phone.replace(/[^\d+]/g, '')) + '">' + LI.esc(s.phone) + '</a></div>' : '') +
      '<div class="lk">' + links.join('') + '</div></article>';
  }

  function render() {
    var q = LI.norm(S.q);
    var list = S.all.filter(function (s) {
      return (S.rub === 'all' || s.rub === S.rub) && (!q || LI.norm(s.name + ' ' + (LABEL[s.kind] || '') + ' ' + s.addr).indexOf(q) >= 0);
    });
    // Compteurs
    RUB.forEach(function (r) {
      var el = document.querySelector('.rub[data-rub="' + r[0] + '"] .n');
      if (el) el.textContent = S.all.filter(function (s) { return s.rub === r[0]; }).length;
    });
    var tot = document.querySelector('.rub[data-rub="all"] .n'); if (tot) tot.textContent = S.all.length;

    var sortFn = function (a, b) { return (b.portrait ? 1 : 0) - (a.portrait ? 1 : 0) || a.name.localeCompare(b.name, 'fr'); };
    var html = RUB.filter(function (r) { return S.rub === 'all' || r[0] === S.rub; }).map(function (r) {
      var items = list.filter(function (s) { return s.rub === r[0]; }).sort(sortFn);
      if (!items.length) return '';
      return '<section class="rub-sec" id="r-' + r[0] + '"><div class="rub-head"><h2>' + LI.esc(r[1]) + '</h2><p>' + LI.esc(r[2]) + ' · ' + items.length + '</p></div>' +
        '<div class="biz-grid">' + items.map(card).join('') + '</div></section>';
    }).join('');
    $('dir').innerHTML = html || '<div class="state">Aucun commerce ne correspond à cette recherche.</div>';
    $('count').textContent = list.length + ' commerce' + (list.length > 1 ? 's' : '');

    if (S.map) {
      S.layer.clearLayers();
      var pts = [];
      list.forEach(function (s) {
        L.circleMarker([s.lat, s.lon], { radius: s.portrait ? 8 : 6, color: '#FFFFFF', weight: 1.5, fillColor: s.portrait ? '#C9A961' : '#1B2E40', fillOpacity: 0.95 })
          .bindPopup('<strong>' + LI.esc(s.name) + '</strong><br>' + LI.esc(LABEL[s.kind] || s.label || '') + (s.addr ? '<br>' + LI.esc(s.addr) : '') +
            (s.portrait ? '<br><a href="' + LI.esc(LI.root + s.portrait.url) + '">Lire son portrait →</a>' : ''))
          .addTo(S.layer);
        pts.push([s.lat, s.lon]);
      });
      if (pts.length) S.map.fitBounds(pts, { padding: [30, 30], maxZoom: 16 });
    }
  }

  function load() {
    $('dir').innerHTML = '<div class="state"><span class="loader"></span>Chargement des commerces…</div>';
    query(S.insee).then(function (d) {
      return attachPortraits(d.slice());
    }).then(function (d) {
      S.all = d;
      render();
    }).catch(function () {
      $('dir').innerHTML = '<div class="state">Les données OpenStreetMap ne répondent pas pour le moment. <button type="button" class="btn btn-line" id="retry" style="margin-top:14px">Réessayer</button></div>';
      var b = $('retry'); if (b) b.addEventListener('click', load);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var sel = $('c-commune');
    COMMUNES.forEach(function (c) { var o = document.createElement('option'); o.value = c[0]; o.textContent = c[1]; sel.appendChild(o); });
    var u = new URLSearchParams(location.search);
    if (u.get('commune') && COMMUNES.some(function (c) { return c[0] === u.get('commune'); })) S.insee = u.get('commune');
    sel.value = S.insee;
    var h = (location.hash || '').replace('#', '');
    if (RUB.some(function (r) { return r[0] === h; })) S.rub = h;

    // Boutons de rubriques
    var bar = $('rubs');
    bar.innerHTML = '<button type="button" class="rub" data-rub="all" aria-pressed="true">Tout <span class="n"></span></button>' +
      RUB.map(function (r) { return '<button type="button" class="rub" data-rub="' + r[0] + '" aria-pressed="false">' + LI.esc(r[1]) + ' <span class="n"></span></button>'; }).join('');
    function setRub(id) {
      S.rub = id;
      bar.querySelectorAll('.rub').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-rub') === id ? 'true' : 'false'); });
      history.replaceState(null, '', location.pathname + location.search + (id === 'all' ? '' : '#' + id));
      if (S.all.length) render();
    }
    bar.addEventListener('click', function (e) { var b = e.target.closest('.rub'); if (b) setRub(b.getAttribute('data-rub')); });
    setRub(S.rub);

    sel.addEventListener('change', function () { S.insee = sel.value; history.replaceState(null, '', '?commune=' + S.insee + location.hash); load(); });
    var t = null;
    $('c-q').addEventListener('input', function (e) { clearTimeout(t); t = setTimeout(function () { S.q = e.target.value; render(); }, 150); });

    if (window.L) {
      S.map = LI.makeMap($('map'), LI.center.lat, LI.center.lon, 15);
      S.layer = L.layerGroup().addTo(S.map);
      S.map.attributionControl.addAttribution('Commerces &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">contributeurs OpenStreetMap</a>');
    }
    load();
  });
})();
