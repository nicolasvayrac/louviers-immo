/* louviers.immo — « Mon adresse » : votre rue, hier et aujourd'hui
   Comparaison de photographies aériennes IGN (deux périodes au choix, curseur à glisser)
   et histoire de la rue quand elle est connue (data/rues.js). */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var WMTS = 'https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}';
  var P = {
    '1950': { label: '1950–1965', q: '&LAYER=ORTHOIMAGERY.ORTHOPHOTOS.1950-1965&STYLE=BDORTHOHISTORIQUE&FORMAT=image/png' },
    '1965': { label: '1965–1980', q: '&LAYER=ORTHOIMAGERY.ORTHOPHOTOS.1965-1980&STYLE=BDORTHOHISTORIQUE&FORMAT=image/png' },
    '1980': { label: '1980–1995', q: '&LAYER=ORTHOIMAGERY.ORTHOPHOTOS.1980-1995&STYLE=BDORTHOHISTORIQUE&FORMAT=image/png' },
    'now':  { label: 'Aujourd’hui', q: '&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&FORMAT=image/jpeg' }
  };
  var S = { map: null, left: null, right: null, me: null };

  function layer(key, pane) {
    return L.tileLayer(WMTS + P[key].q, { pane: pane, maxZoom: 18, attribution: 'Photographies aériennes © <a href="https://www.ign.fr/" target="_blank" rel="noopener">IGN</a>' });
  }
  function clip() {
    var map = S.map; if (!map) return;
    var size = map.getSize(), x = size.x * $('av-range').value / 100;
    var nw = map.containerPointToLayerPoint([0, 0]), se = map.containerPointToLayerPoint(size);
    map.getPane('avG').style.clip = 'rect(' + [nw.y, nw.x + x, se.y, nw.x].join('px,') + 'px)';
    $('av-bar').style.left = x + 'px';
  }
  function setSide(side) {
    var sel = $(side === 'G' ? 'av-g' : 'av-d'), key = sel.value;
    var cur = side === 'G' ? S.left : S.right;
    if (cur) S.map.removeLayer(cur);
    var l = layer(key, side === 'G' ? 'avG' : 'avD').addTo(S.map);
    if (side === 'G') S.left = l; else S.right = l;
    $(side === 'G' ? 'av-lg' : 'av-ld').textContent = P[key].label;
  }
  function init(lat, lon) {
    var el = $('av-map');
    S.map = L.map(el, { zoomControl: false, scrollWheelZoom: false, minZoom: 12, maxZoom: 18 }).setView([lat, lon], 17);
    L.control.zoom({ position: 'topright', zoomInTitle: 'Zoomer', zoomOutTitle: 'Dézoomer' }).addTo(S.map);
    S.map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    S.map.createPane('avD').style.zIndex = 240;
    S.map.createPane('avG').style.zIndex = 250;
    setSide('D'); setSide('G');
    $('av-g').addEventListener('change', function () { setSide('G'); clip(); });
    $('av-d').addEventListener('change', function () { setSide('D'); clip(); });
    $('av-range').addEventListener('input', clip);
    S.map.on('move zoom resize', clip);
    var bar = $('av-bar'), drag = false;
    bar.addEventListener('pointerdown', function (e) { drag = true; bar.setPointerCapture(e.pointerId); S.map.dragging.disable(); });
    bar.addEventListener('pointermove', function (e) {
      if (!drag) return;
      var r = el.getBoundingClientRect();
      $('av-range').value = Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100)); clip();
    });
    bar.addEventListener('pointerup', function () { drag = false; S.map.dragging.enable(); });
    clip();
  }

  function rueFor(label) {
    var n = ' ' + LI.norm(label) + ' ';
    if (!/ louviers /.test(n) && !/ 27400 /.test(n)) return null;
    var best = null;
    (window.LI_RUES || []).forEach(function (r) {
      [r.nom].concat(r.aliases || []).forEach(function (nm) {
        var k = LI.norm(nm);
        if (n.indexOf(' ' + k + ' ') >= 0 && (!best || k.length > best.k)) best = { r: r, k: k.length };
      });
    });
    return best && best.r;
  }
  function renderRue(label) {
    var box = $('av-rue'), r = rueFor(label);
    box.hidden = !r;
    if (!r) return;
    $('av-plaque').textContent = r.nom;
    $('av-texte').textContent = '« ' + r.texte + ' »';
    $('av-src').textContent = 'Source : ' + r.source;
    $('av-voir').innerHTML = (r.voir || []).map(function (v) { return '<li>' + LI.esc(v) + '</li>'; }).join('');
    $('av-voir-w').hidden = !(r.voir && r.voir.length);
  }

  LI.renderAvant = function (lat, lon, label) {
    if (!$('av-map') || !window.L) return;
    renderRue(label || '');
    if (!S.map) init(lat, lon);
    else { S.map.invalidateSize(); S.map.setView([lat, lon], 17); }
    if (S.me) S.map.removeLayer(S.me);
    S.me = L.marker([lat, lon], { pane: 'markerPane', icon: LI.divIcon('<div class="pin-me"></div>', '', 22), interactive: false }).addTo(S.map);
    setTimeout(function () { S.map.invalidateSize(); clip(); }, 60);
  };
})();
