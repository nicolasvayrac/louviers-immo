/* Fond de carte commun : Plan IGN (Géoplateforme, Licence Ouverte Etalab) */
(function () {
  'use strict';
  var LI = window.LI = window.LI || {};
  LI.makeMap = function (el, lat, lon, zoom) {
    var map = L.map(el, { scrollWheelZoom: false, zoomControl: false, attributionControl: true })
      .setView([lat, lon], zoom || 15);
    L.control.zoom({ position: 'topright', zoomInTitle: 'Zoomer', zoomOutTitle: 'Dézoomer' }).addTo(map);
    L.tileLayer(
      'https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0' +
      '&LAYER=GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2&STYLE=normal&TILEMATRIXSET=PM' +
      '&FORMAT=image/png&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
      { maxZoom: 19, minZoom: 9, attribution: '&copy; <a href="https://www.ign.fr/" target="_blank" rel="noopener">IGN</a> · Plan IGN' }
    ).addTo(map);
    // Une tuile IGN qui échoue (coupure passagère) est redemandée une fois, au lieu de laisser un carré gris
    map.eachLayer(function (l) {
      if (!l.on || !l.getTileUrl) return;
      l.on('tileerror', function (e) {
        var t = e.tile;
        if (t.getAttribute('data-retry')) return;
        t.setAttribute('data-retry', '1');
        setTimeout(function () { t.src = e.tile.src.split('&_r=')[0] + '&_r=' + Date.now(); }, 700);
      });
    });
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    // Molette active seulement après un clic (évite de « piéger » le défilement de la page)
    map.on('click', function () { map.scrollWheelZoom.enable(); });
    map.on('mouseout', function () { map.scrollWheelZoom.disable(); });
    return map;
  };
  LI.divIcon = function (html, cls, size) {
    var s = size || 28;
    return L.divIcon({ html: html, className: cls || '', iconSize: [s, s], iconAnchor: [s / 2, s / 2] });
  };
})();
