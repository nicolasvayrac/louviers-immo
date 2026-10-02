/* louviers.immo — Comparateur de deux adresses : prix, écoles, gare, A13 */
(function () {
  'use strict';
  var A = LI.adr;

  function prices(sales, lat, lon) {
    var near = sales.filter(function (s) { return LI.dist(lat, lon, s.lat, s.lon) <= 500; });
    function med(t) {
      var v = near.filter(function (s) { return s.type === t; }).map(function (s) { return s.pm2; });
      return v.length >= 3 ? LI.fmt(Math.round(LI.median(v) / 10) * 10) + ' €/m²' : '—';
    }
    return { maison: med('M'), appart: med('A'), n: near.length };
  }
  function row(label, value, sub) {
    return '<div class="cmp-row"><span class="cmp-l">' + label + '</span><span class="cmp-v">' + value + (sub ? '<small>' + sub + '</small>' : '') + '</span></div>';
  }
  function one(n, dvf) {
    var input = document.getElementById('cmp-q' + n), box = document.getElementById('cmp-r' + n);
    var v = input.value.trim();
    if (!v) { box.innerHTML = '<p class="muted">Indiquez une adresse.</p>'; return Promise.resolve(); }
    box.innerHTML = '<p class="muted"><span class="loader"></span>Recherche…</p>';
    return LI.geocode(v, 1, false).then(function (res) {
      var g = res[0];
      if (!g) { box.innerHTML = '<p class="muted">Adresse introuvable.</p>'; return; }
      return A.getPois(g.lat, g.lon).then(function (P) {
        var pr = prices(dvf.sales, g.lat, g.lon);
        var ecole = A.nearest(P, function (p) { return A.schoolType(p) === 'ecole'; });
        var college = A.nearest(P, function (p) { return A.schoolType(p) === 'college'; });
        var lycee = A.nearest(P, function (p) { return A.schoolType(p) === 'lycee'; });
        var gare = A.nearest(P, function (p) { return !!p.t.railway; });
        var a13 = A.nearest(P, function (p) { return p.t.highway === 'motorway_junction'; });
        function sch(p) { if (!p) return '—'; var w = A.minutes('walk', p.d); return w <= 20 ? A.fmtMin(w) + ' à pied' : A.fmtMin(A.minutes('car', p.d)) + ' en voiture'; }
        box.innerHTML =
          '<p class="cmp-title">' + LI.esc(g.label) + '</p>' +
          row('Maison', pr.maison) + row('Appartement', pr.appart) + row('Ventes à 500 m', LI.fmt(pr.n)) +
          row('École', sch(ecole), ecole ? LI.esc(ecole.name) : '') +
          row('Collège', sch(college), college ? LI.esc(college.name) : '') +
          row('Lycée', lycee ? A.fmtMin(A.minutes('car', lycee.d)) + ' en voiture' : '—', lycee ? LI.esc(lycee.name) : '') +
          row('Gare', gare ? A.fmtMin(A.minutes('car', gare.d)) + ' en voiture' : '—', gare ? LI.esc(gare.name) : '') +
          row('Autoroute A13', a13 ? A.fmtMin(A.minutes('car', a13.d)) + ' en voiture' : '—', a13 && a13.t.ref ? 'sortie ' + LI.esc(a13.t.ref) : '') +
          '<a class="link-u" href="' + LI.esc(LI.root + 'adresse.html?q=' + encodeURIComponent(g.label) + '&lat=' + g.lat.toFixed(6) + '&lon=' + g.lon.toFixed(6)) + '">Tout voir autour de cette adresse</a>';
      });
    }).catch(function () { box.innerHTML = '<p class="muted">Les services de données ne répondent pas pour le moment. Réessayez dans un instant.</p>'; });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var f = document.getElementById('cmp-form');
    if (!f) return;
    var u = new URLSearchParams(location.search);
    if (u.get('a')) document.getElementById('cmp-q1').value = u.get('a');
    if (u.get('b')) document.getElementById('cmp-q2').value = u.get('b');
    function run() {
      LI.loadDVF().then(function (dvf) { return Promise.all([one(1, dvf), one(2, dvf)]); });
    }
    f.addEventListener('submit', function (e) { e.preventDefault(); run(); });
    if (u.get('a') && u.get('b')) run();
  });
})();
