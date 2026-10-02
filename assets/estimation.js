/* louviers.immo — Estimation rapide : fourchette à partir des ventes DVF autour d'une adresse */
(function () {
  'use strict';
  function q(arr, p) {
    var a = arr.slice().sort(function (x, y) { return x - y; });
    var i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
    return a[lo] + (a[hi] - a[lo]) * (i - lo);
  }
  function euros(n) { return LI.fmt(Math.round(n / 1000) * 1000) + ' €'; }

  document.addEventListener('DOMContentLoaded', function () {
    var f = document.getElementById('estim-form'), out = document.getElementById('estim-out');
    if (!f) return;
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var adr = document.getElementById('e-adr').value.trim();
      var type = document.getElementById('e-type').value;
      var surf = parseFloat(document.getElementById('e-surf').value);
      if (!adr || !(surf >= 10 && surf <= 600)) {
        out.innerHTML = '<p class="muted">Indiquez une adresse et une surface entre 10 et 600 m².</p>';
        return;
      }
      out.innerHTML = '<p class="muted"><span class="loader"></span>Calcul en cours…</p>';
      Promise.all([LI.geocode(adr, 1, false), LI.loadDVF()]).then(function (res) {
        var g = res[0][0], d = res[1];
        if (!g) { out.innerHTML = '<p class="muted">Adresse introuvable. Vérifiez le numéro, la rue et la commune.</p>'; return; }
        var same = d.sales.filter(function (s) { return s.type === type; });
        var radius = 0, near = [];
        [500, 1000, 2000].some(function (rad) {
          near = same.filter(function (s) { return LI.dist(g.lat, g.lon, s.lat, s.lon) <= rad; });
          radius = rad;
          return near.length >= 8;
        });
        if (near.length < 5) {
          out.innerHTML = '<p><strong>Pas assez de ventes comparables</strong> autour de cette adresse pour calculer une fourchette.</p>' +
            '<a class="btn btn-gold plausible-event-name=Estimation+Rapide" href="https://www.cvimmobilier.fr/estimation">Demander une estimation à un négociateur</a>';
          return;
        }
        var pm = near.map(function (s) { return s.pm2; });
        var lo = q(pm, 0.25) * surf, mid = q(pm, 0.5) * surf, hi = q(pm, 0.75) * surf;
        var per = d.meta.period ? LI.monthFR(d.meta.period.from) + ' – ' + LI.monthFR(d.meta.period.to) : '';
        out.innerHTML =
          '<p class="estim-adr">' + LI.esc(g.label) + ' · ' + (type === 'M' ? 'maison' : 'appartement') + ' de ' + LI.fmt(surf) + ' m²</p>' +
          '<p class="estim-range">' + euros(lo) + ' <span>à</span> ' + euros(hi) + '</p>' +
          '<p class="muted">Valeur médiane : ' + euros(mid) + ' · calculée sur ' + near.length + ' ventes de ' + (type === 'M' ? 'maisons' : 'appartements') +
          ' à moins de ' + (radius >= 1000 ? (radius / 1000) + ' km' : radius + ' m') + (per ? ' (' + per + ')' : '') + '.</p>' +
          '<p class="estim-warn">Ce n’est pas une estimation : la moitié des ventes comparables se situent dans cette fourchette. L’état, le terrain, l’exposition ou les travaux peuvent faire varier le prix de 30 % ou plus.</p>' +
          '<a class="btn btn-gold plausible-event-name=Estimation+Rapide" href="https://www.cvimmobilier.fr/estimation">Affiner avec un négociateur</a>';
      }).catch(function () {
        out.innerHTML = '<p class="muted">Le service d’adresses ne répond pas pour le moment. Réessayez dans un instant.</p>';
      });
    });
  });
})();
