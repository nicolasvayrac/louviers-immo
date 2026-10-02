/* Chiffres DVF autour d'un point de référence du quartier (attribut data-ref sur #q-prices) */
(function () {
  'use strict';
  var LI = window.LI;
  document.addEventListener('DOMContentLoaded', function () {
    var box = document.getElementById('q-prices');
    if (!box) return;
    var ref = box.getAttribute('data-ref'), radius = parseInt(box.getAttribute('data-radius') || '600', 10);
    Promise.all([LI.geocode(ref, 1, false), LI.loadDVF()]).then(function (r) {
      var pt = r[0][0], d = r[1];
      if (!pt || !d.sales.length) return;
      var near = d.sales.filter(function (s) { return LI.dist(pt.lat, pt.lon, s.lat, s.lon) <= radius; });
      function med(t) {
        var x = near.filter(function (s) { return s.type === t; }).map(function (s) { return s.pm2; });
        return x.length >= 3 ? LI.fmt(Math.round(LI.median(x) / 10) * 10) + ' €' : '—';
      }
      box.querySelector('[data-k="M"]').textContent = med('M');
      box.querySelector('[data-k="A"]').textContent = med('A');
      box.querySelector('[data-k="N"]').textContent = LI.fmt(near.length);
      var per = box.querySelector('[data-k="P"]');
      if (per && d.meta.period) per.textContent = LI.monthFR(d.meta.period.from) + ' – ' + LI.monthFR(d.meta.period.to) + ' · DVF';
      var lk = document.getElementById('q-prices-link');
      if (lk) lk.href = LI.root + 'prix.html?lat=' + pt.lat.toFixed(5) + '&lon=' + pt.lon.toFixed(5);
    }).catch(function () { /* chiffres laissés à « — » */ });
  });
})();
