/* louviers.immo — Prototypes « labo » : Louviers d'hier et d'aujourd'hui, l'histoire de votre rue, l'école de secteur */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };

  /* ================= 1. Louviers d'hier et d'aujourd'hui ================= */
  function initHier() {
    var el = $('hier-map');
    if (!el || !window.L) return;
    var IGN = 'https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}';
    var map = L.map(el, { zoomControl: false, scrollWheelZoom: false, minZoom: 12, maxZoom: 18 }).setView([49.2154, 1.1659], 17);
    L.control.zoom({ position: 'topright', zoomInTitle: 'Zoomer', zoomOutTitle: 'Dézoomer' }).addTo(map);
    L.tileLayer(IGN + '&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&FORMAT=image/jpeg',
      { maxZoom: 18, attribution: 'Photographies aériennes &copy; <a href="https://www.ign.fr/" target="_blank" rel="noopener">IGN</a>' }).addTo(map);
    map.createPane('old'); map.getPane('old').style.zIndex = 250;
    L.tileLayer(IGN + '&LAYER=ORTHOIMAGERY.ORTHOPHOTOS.1950-1965&STYLE=BDORTHOHISTORIQUE&FORMAT=image/png',
      { pane: 'old', maxZoom: 18, attribution: 'IGN, photographies 1950-1965' }).addTo(map);
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');

    var range = $('hier-range'), bar = $('hier-bar'), pane = map.getPane('old');
    function clip() {
      var size = map.getSize(), x = size.x * range.value / 100;
      var nw = map.containerPointToLayerPoint([0, 0]), se = map.containerPointToLayerPoint(size);
      pane.style.clip = 'rect(' + [nw.y, nw.x + x, se.y, nw.x].join('px,') + 'px)';
      bar.style.left = x + 'px';
    }
    range.addEventListener('input', clip);
    map.on('move zoom resize', clip);
    clip();
    // Glisser directement sur la carte avec la poignée
    var drag = false;
    bar.addEventListener('pointerdown', function (e) { drag = true; bar.setPointerCapture(e.pointerId); map.dragging.disable(); });
    bar.addEventListener('pointermove', function (e) {
      if (!drag) return;
      var r = el.getBoundingClientRect();
      range.value = Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100)); clip();
    });
    bar.addEventListener('pointerup', function () { drag = false; map.dragging.enable(); });

    document.querySelectorAll('[data-go]').forEach(function (b) {
      b.addEventListener('click', function () {
        var p = b.getAttribute('data-go').split(',');
        map.setView([+p[0], +p[1]], +p[2] || 17);
        document.querySelectorAll('[data-go]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      });
    });
    var form = document.querySelector('form.search');
    if (form) form._onChoose = function (r) {
      map.setView([r.lat, r.lon], 17);
      document.querySelectorAll('[data-go]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    };
  }

  /* ================= 3. L'histoire de votre rue ================= */
  var RUES = {
    'rue-du-quai': {
      nom: 'Rue du Quai', q: 'Rue du Quai 27400 Louviers',
      origine: 'Elle conduisait aux quais du bassin de Bigards, port principal, d’où son nom. Au n°18, on découvre une très belle manufacture du XVIIIe siècle.',
      voir: ['La manufacture du XVIIIe siècle, au n°18', 'Les bras de l’Eure, qui faisaient tourner les moulins et les ateliers']
    },
    'rue-ternaux': {
      nom: 'Rue Ternaux', q: 'Rue Ternaux 27400 Louviers',
      origine: 'Du nom d’un célèbre manufacturier du début du XIXe siècle, propriétaire de nombreux ateliers à Louviers et à Sedan, cette rue était à l’origine celle des tanneurs, puis des tisseurs.',
      voir: ['Les façades des anciens ateliers textiles', 'La place de la Halle, à deux pas']
    }
  };
  var SRC = 'Office de tourisme Seine-Eure, circuit « Louviers, cité drapière »';
  function initRue() {
    var box = $('rue');
    if (!box) return;
    var key = new URLSearchParams(location.search).get('r');
    if (!RUES[key]) key = 'rue-du-quai';
    document.querySelectorAll('[data-rue]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-rue') === key ? 'true' : 'false');
    });
    var R = RUES[key];
    $('rue-nom').textContent = R.nom;
    $('rue-origine').textContent = '« ' + R.origine + ' »';
    $('rue-src').textContent = SRC;
    $('rue-voir').innerHTML = R.voir.map(function (v) { return '<li>' + LI.esc(v) + '</li>'; }).join('');
    $('rue-adr').href = LI.root + 'adresse.html?q=' + encodeURIComponent(R.q);
    $('rue-ventes').innerHTML = '<p class="muted"><span class="loader"></span>Chargement des ventes…</p>';
    Promise.all([LI.geocode(R.q, 1, false), LI.loadDVF()]).then(function (res) {
      var g = res[0][0], d = res[1];
      if (!g) throw new Error('adresse');
      var near = d.sales.filter(function (s) { return LI.dist(g.lat, g.lon, s.lat, s.lon) <= 150; })
        .sort(function (a, b) { return a.ym < b.ym ? 1 : -1; });
      if (!near.length) { $('rue-ventes').innerHTML = '<p class="muted">Aucune vente enregistrée à moins de 150 m sur la période.</p>'; return; }
      var pm = LI.median(near.map(function (s) { return s.pm2; }));
      $('rue-ventes').innerHTML =
        '<p class="lb-big">' + near.length + ' <span>vente' + (near.length > 1 ? 's' : '') + ' à moins de 150 m · médiane ' + LI.fmt(Math.round(pm / 10) * 10) + ' €/m²</span></p>' +
        '<table class="lb-table"><thead><tr><th>Date</th><th>Bien</th><th>Surface</th><th>Prix</th></tr></thead><tbody>' +
        near.slice(0, 5).map(function (s) {
          return '<tr><td>' + LI.monthFR(s.ym) + '</td><td>' + (s.type === 'M' ? 'Maison' : 'Appartement') + (s.rooms ? ', ' + s.rooms + ' p.' : '') + '</td><td>' + LI.fmt(s.surf) + ' m²</td><td>' + LI.fmt(s.price) + ' €</td></tr>';
        }).join('') + '</tbody></table>';
    }).catch(function () { $('rue-ventes').innerHTML = '<p class="muted">Les ventes ne peuvent pas être chargées pour le moment.</p>'; });
  }

  /* ================= 6. L'école de secteur ================= */
  function initEcole() {
    var out = $('ec-out');
    if (!out || !LI.adr) return;
    var A = LI.adr;
    function kind(p) {
      var n = LI.norm(p.name);
      if (A.schoolType(p) !== 'ecole') return A.schoolType(p);
      if (/maternelle/.test(n)) return 'mat';
      if (/elementaire|primaire/.test(n)) return 'elem';
      return 'ecole';
    }
    function card(title, p, mode) {
      if (!p) return '<div class="ec-card"><span class="ec-k">' + title + '</span><p class="muted">Aucun établissement trouvé à proximité.</p></div>';
      var m = A.minutes(mode, p.d);
      return '<div class="ec-card"><span class="ec-k">' + title + '</span><b class="ec-n">' + LI.esc(p.name || 'Établissement') + '</b>' +
        '<span class="ec-t">' + A.fmtMin(m) + (mode === 'walk' ? ' à pied' : ' en voiture') + ' · ' + A.fmtDist(p.d) + '</span></div>';
    }
    function run(g) {
      $('ec-adr').textContent = g.label;
      out.innerHTML = '<p class="muted"><span class="loader"></span>Recherche des écoles…</p>';
      A.getPois(g.lat, g.lon).then(function (P) {
        var mat = A.nearest(P, function (p) { var k = kind(p); return k === 'mat' || k === 'ecole'; });
        var elem = A.nearest(P, function (p) { var k = kind(p); return k === 'elem' || k === 'ecole'; });
        var col = A.nearest(P, function (p) { return kind(p) === 'college'; });
        var lyc = A.nearest(P, function (p) { return kind(p) === 'lycee'; });
        out.innerHTML = card('Maternelle', mat, 'walk') + card('Élémentaire', elem, 'walk') +
          card('Collège', col, A.minutes('walk', col ? col.d : 0) > 20 ? 'car' : 'walk') + card('Lycée', lyc, 'car');
      }).catch(function () { out.innerHTML = '<p class="muted">Les données ne répondent pas pour le moment.</p>'; });
    }
    var form = document.querySelector('form.search');
    if (form) form._onChoose = run;
    run({ label: 'Place de la Halle aux Drapiers, 27400 Louviers', lat: 49.2154, lon: 1.1659 });
  }

  document.addEventListener('DOMContentLoaded', function () { initHier(); initRue(); initEcole(); });
})();
