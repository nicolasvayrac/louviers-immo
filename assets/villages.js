/* louviers.immo — Les 18 quartiers (« Les villages dans la ville », Ville de Louviers)
   Carte des quartiers (quartiers.html), carte d'un quartier et de ses ventes (quartiers/*.html),
   et quartier d'une adresse (adresse.html). Données : data/villages.json (généré par scripts/gen.py). */
(function () {
  'use strict';
  var LI = window.LI = window.LI || {};
  var $ = function (id) { return document.getElementById(id); };
  var promise = null;
  LI.loadVillages = function () {
    if (!promise) promise = LI.fetchJSON(LI.root + 'data/villages.json', null, 15000);
    return promise;
  };
  function inRing(lat, lon, ring) {
    var c = false;
    for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
      if (((yi > lat) !== (yj > lat)) && (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi)) c = !c;
    }
    return c;
  }
  function distRing(lat, lon, ring) {
    var kx = Math.cos(lat * Math.PI / 180) * 111320, ky = 110574, best = 1e9;
    for (var i = 0; i < ring.length - 1; i++) {
      var ax = (ring[i][0] - lon) * kx, ay = (ring[i][1] - lat) * ky, bx = (ring[i + 1][0] - lon) * kx, by = (ring[i + 1][1] - lat) * ky;
      var dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-9, t = Math.max(0, Math.min(1, -(ax * dx + ay * dy) / l2));
      best = Math.min(best, Math.hypot(ax + t * dx, ay + t * dy));
    }
    return best;
  }
  // Quartier d'un point : celui qui le contient, sinon le plus proche à moins de 250 m
  LI.villageDe = function (gj, lat, lon) {
    var best = null, bd = 250;
    for (var i = 0; i < gj.features.length; i++) {
      var f = gj.features[i], ring = f.geometry.coordinates[0];
      if (inRing(lat, lon, ring)) return f;
      var d = distRing(lat, lon, ring); if (d < bd) { bd = d; best = f; }
    }
    return best;
  };
  var fmt = function (v) { return v ? Math.round(v).toLocaleString('fr-FR') + ' €' : '—'; };
  function mix(a, b, k) {
    var pa = [1, 3, 5].map(function (i) { return parseInt(a.substr(i, 2), 16); }), pb = [1, 3, 5].map(function (i) { return parseInt(b.substr(i, 2), 16); });
    return '#' + pa.map(function (x, i) { return ('0' + Math.round(x + (pb[i] - x) * k).toString(16)).slice(-2); }).join('');
  }
  function ramp(k) { return k < 0.5 ? mix('#E8F0E9', '#C9A961', k * 2) : mix('#C9A961', '#7E3B2B', (k - 0.5) * 2); }
  function popup(p, root) {
    var s = p.s;
    return '<strong style="font-size:16px;color:#1B2E40">' + p.n + '. ' + LI.esc(p.nom) + '</strong><br>' +
      s.n + ' ventes<br>Maisons : ' + (s.M[0] ? fmt(s.M[0]) + '/m²' : 'pas assez de ventes') + '<br>Appartements : ' + (s.A[0] ? fmt(s.A[0]) + '/m²' : 'pas assez de ventes') +
      '<br><a href="' + root + 'quartiers/' + p.slug + '.html">Voir le quartier</a>';
  }

  /* ---------- quartiers.html : carte des 18 quartiers ---------- */
  function initListe(el) {
    LI.loadVillages().then(function (gj) {
      var map = LI.makeMap(el, 49.212, 1.168, 14), mode = 'q', layer;
      function style(f) {
        var c = f.properties.c, v;
        if (mode !== 'q') {
          var vals = gj.features.map(function (g) { return g.properties.s[mode][0]; }).filter(Boolean);
          var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
          v = f.properties.s[mode][0];
          c = v ? ramp((v - lo) / (hi - lo || 1)) : '#D9D4C8';
          $('vl-lo').textContent = fmt(lo); $('vl-hi').textContent = fmt(hi);
        }
        return { color: '#1B2E40', weight: 1.5, fillColor: c, fillOpacity: mode === 'q' ? 0.42 : (v ? 0.72 : 0.35) };
      }
      layer = L.geoJSON(gj, {
        style: style,
        onEachFeature: function (f, l) {
          l.bindPopup(popup(f.properties, ''));
          l.bindTooltip(String(f.properties.n), { permanent: true, direction: 'center', className: 'vl-lbl' });
          l.on('mouseover', function () { l.setStyle({ weight: 3 }); }); l.on('mouseout', function () { l.setStyle({ weight: 1.5 }); });
        }
      }).addTo(map);
      map.options.zoomSnap = 0.25; map.fitBounds(layer.getBounds(), { padding: [10, 10] });
      document.querySelectorAll('.vl-modes button').forEach(function (b) {
        b.addEventListener('click', function () {
          mode = b.getAttribute('data-mode');
          document.querySelectorAll('.vl-modes button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          layer.setStyle(style); $('vl-leg').hidden = mode === 'q';
        });
      });
    }).catch(function () { el.innerHTML = '<p class="empty-data" style="margin:24px">La carte n’a pas pu se charger. Rechargez la page.</p>'; });
  }
  function initTri(tbl) {
    var dir = {};
    tbl.querySelectorAll('th button').forEach(function (b) {
      b.addEventListener('click', function () {
        var c = +b.getAttribute('data-c'), tb = tbl.tBodies[0], rows = Array.prototype.slice.call(tb.rows);
        dir[c] = !dir[c];
        rows.sort(function (x, y) { var a = +x.cells[c].getAttribute('data-v'), z = +y.cells[c].getAttribute('data-v'); return dir[c] ? z - a : a - z; });
        rows.forEach(function (r) { tb.appendChild(r); });
      });
    });
  }

  /* ---------- quartiers/*.html : le quartier, ses voisins et ses ventes ---------- */
  function initQuartier(el) {
    var n = +el.getAttribute('data-n');
    Promise.all([LI.loadVillages(), LI.loadDVF()]).then(function (r) {
      var gj = r[0], dvf = r[1], me = null;
      var map = LI.makeMap(el, 49.212, 1.168, 15);
      var layer = L.geoJSON(gj, {
        style: function (f) {
          var on = f.properties.n === n;
          return { color: on ? '#1B2E40' : '#5B6B78', weight: on ? 3 : 1, fillColor: f.properties.c, fillOpacity: on ? 0.28 : 0.08, dashArray: on ? null : '4 4' };
        },
        onEachFeature: function (f, l) {
          if (f.properties.n === n) me = l;
          else {
            l.bindTooltip(f.properties.n + '. ' + f.properties.nom, { sticky: true });
            l.on('click', function () { location.href = f.properties.slug + '.html'; });
          }
        }
      }).addTo(map);
      map.fitBounds(me.getBounds(), { padding: [16, 16] });
      var sales = dvf.sales.filter(function (s) {
        if (s.commune !== 'Louviers' || !s.surf || s.pm2 < 400 || s.pm2 > 6000) return false;
        var v = LI.villageDe(gj, s.lat, s.lon); return v && v.properties.n === n;
      });
      var m2 = sales.map(function (s) { return s.pm2; }).sort(function (a, b) { return a - b; });
      var lo = m2[Math.floor(m2.length * 0.1)] || 1000, hi = m2[Math.floor(m2.length * 0.9)] || 3000;
      sales.forEach(function (s) {
        var k = Math.max(0, Math.min(1, (s.pm2 - lo) / (hi - lo || 1)));
        L.circleMarker([s.lat, s.lon], { radius: 6, color: '#1B2E40', weight: 1, fillColor: ramp(k), fillOpacity: 0.95 })
          .bindPopup('<strong>' + (s.type === 'M' ? 'Maison' : 'Appartement') + '</strong> · ' + s.surf + ' m²' + (s.rooms ? ' · ' + s.rooms + ' p.' : '') +
            '<br>' + fmt(s.price) + ' · ' + fmt(s.pm2) + '/m²<br><span style="color:#5B5F63">' + s.ym.split('-').reverse().join('/') + '</span>')
          .addTo(map);
      });
    }).catch(function () { el.innerHTML = '<p class="empty-data" style="margin:24px">La carte n’a pas pu se charger. Rechargez la page.</p>'; });
  }

  /* ---------- adresse.html : le quartier de l'adresse ---------- */
  LI.renderQuartier = function (lat, lon) {
    var box = $('q-badge'); if (!box) return;
    box.hidden = true;
    LI.loadVillages().then(function (gj) {
      var f = LI.villageDe(gj, lat, lon); if (!f) return;
      var p = f.properties, s = p.s;
      box.innerHTML = '<span class="qb-n" style="background:' + p.c + '">' + p.n + '</span><span><span class="qb-l">Votre quartier</span><strong>' + LI.esc(p.nom) + '</strong>' +
        '<span class="qb-s">' + s.n + ' ventes · maisons ' + (s.M[0] ? fmt(s.M[0]) + '/m²' : '—') + ' · appartements ' + (s.A[0] ? fmt(s.A[0]) + '/m²' : '—') + '</span></span>' +
        '<span class="qb-go">Voir le quartier</span>';
      box.href = LI.root + 'quartiers/' + p.slug + '.html';
      box.hidden = false;
    }).catch(function () {});
  };

  document.addEventListener('DOMContentLoaded', function () {
    if ($('vl-map')) initListe($('vl-map'));
    if ($('vl-tbl')) initTri($('vl-tbl'));
    if ($('vq-map')) initQuartier($('vq-map'));
  });
})();
