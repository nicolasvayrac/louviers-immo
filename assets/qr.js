/* louviers.immo — Outil interne : code QR « Vivre ici » vers la page d'une adresse */
(function () {
  'use strict';
  var SITE = 'https://louviers.immo/';
  function build(url) {
    var qr = qrcode(0, 'M');
    qr.addData(url);
    qr.make();
    return qr;
  }
  function svgOf(qr, cell, margin) {
    var n = qr.getModuleCount(), size = n * cell + margin * 2, d = '';
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++)
      if (qr.isDark(r, c)) d += 'M' + (c * cell + margin) + ' ' + (r * cell + margin) + 'h' + cell + 'v' + cell + 'h-' + cell + 'z';
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + size + ' ' + size + '" width="' + size + '" height="' + size + '">' +
      '<rect width="100%" height="100%" fill="#ffffff"/><path d="' + d + '" fill="#1B2E40"/></svg>';
  }
  function pngOf(qr, px) {
    var n = qr.getModuleCount(), margin = 4, cell = Math.floor(px / (n + margin * 2));
    var size = cell * (n + margin * 2), cv = document.createElement('canvas');
    cv.width = cv.height = size;
    var x = cv.getContext('2d');
    x.fillStyle = '#ffffff'; x.fillRect(0, 0, size, size);
    x.fillStyle = '#1B2E40';
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (qr.isDark(r, c)) x.fillRect((c + margin) * cell, (r + margin) * cell, cell, cell);
    return cv.toDataURL('image/png');
  }
  document.addEventListener('DOMContentLoaded', function () {
    var f = document.getElementById('qr-form');
    if (!f) return;
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('qr-msg'), v = document.getElementById('qr-adr').value.trim();
      if (!v) { msg.textContent = 'Indiquez une adresse.'; return; }
      msg.textContent = 'Recherche de l’adresse…';
      LI.geocode(v, 1, false).then(function (res) {
        var g = res[0];
        if (!g) { msg.textContent = 'Adresse introuvable. Vérifiez le numéro, la rue et la commune.'; return; }
        var url = SITE + 'adresse.html?q=' + encodeURIComponent(g.label) + '&lat=' + g.lat.toFixed(6) + '&lon=' + g.lon.toFixed(6) + '&utm_source=qr-annonce';
        var qr = build(url), svg = svgOf(qr, 8, 32);
        document.getElementById('qr-svg').innerHTML = svg;
        document.getElementById('qr-url').textContent = g.label;
        document.getElementById('qr-svgdl').href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
        document.getElementById('qr-png').href = pngOf(qr, 1200);
        var slug = LI.norm(g.label).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60);
        document.getElementById('qr-svgdl').setAttribute('download', 'qr-' + slug + '.svg');
        document.getElementById('qr-png').setAttribute('download', 'qr-' + slug + '.png');
        document.getElementById('qr-out').hidden = false;
        msg.textContent = 'Code QR prêt pour : ' + g.label;
      }).catch(function () { msg.textContent = 'Le service d’adresses ne répond pas pour le moment.'; });
    });
  });
})();
