/* ==========================================================
   louviers.immo — Observatoire des prix (données DVF)
   ========================================================== */
(function () {
  'use strict';
  var LI = window.LI;
  var $ = function (id) { return document.getElementById(id); };
  var S = { all: [], meta: {}, map: null, layer: null, focus: null, gj: null, quartier: '', qLayer: null };
  var C = { low: '#4F7F98', mid: '#C9A961', high: '#6B5420' };

  function q(arr, p) {
    if (!arr.length) return null;
    var a = arr.slice().sort(function (x, y) { return x - y; });
    var i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
    return a[lo] + (a[hi] - a[lo]) * (i - lo);
  }
  function round10(x) { return Math.round(x / 10) * 10; }

  function filtered() {
    var type = $('f-type').value, com = $('f-commune').value, per = $('f-period').value;
    var last = S.meta.period && S.meta.period.to;
    var cutoff = '';
    var year = per.charAt(0) === 'y' ? per.slice(1) : '';
    if (!year && per !== 'all' && last) {
      var y = parseInt(last.slice(0, 4), 10), m = parseInt(last.slice(5, 7), 10);
      var back = parseInt(per, 10);
      var tot = y * 12 + (m - 1) - back + 1;
      cutoff = Math.floor(tot / 12) + '-' + String(tot % 12 + 1).padStart(2, '0');
    }
    return S.all.filter(function (s) {
      return (type === 'all' || s.type === type) &&
        (com === 'all' || s.commune === com) &&
        (!S.quartier || com !== 'Louviers' || s.q === S.quartier) &&
        (!cutoff || s.ym >= cutoff) &&
        (!year || s.ym.slice(0, 4) === year);
    });
  }

  function render() {
    var list = filtered();
    var pm = list.map(function (s) { return s.pm2; });
    var t1 = q(pm, 1 / 3), t2 = q(pm, 2 / 3);

    // Chiffres clés
    var mh = LI.median(list.filter(function (s) { return s.type === 'M'; }).map(function (s) { return s.pm2; }));
    var ma = LI.median(list.filter(function (s) { return s.type === 'A'; }).map(function (s) { return s.pm2; }));
    $('k-maison').textContent = mh ? LI.fmt(round10(mh)) + ' €' : '—';
    $('k-appart').textContent = ma ? LI.fmt(round10(ma)) + ' €' : '—';
    $('k-ventes').textContent = LI.fmt(list.length);
    $('lg-low').textContent = t1 ? 'moins de ' + LI.fmt(round10(t1)) + ' €/m²' : 'moins cher';
    $('lg-high').textContent = t2 ? 'plus de ' + LI.fmt(round10(t2)) + ' €/m²' : 'plus cher';

    // Carte
    if (S.map) {
      S.layer.clearLayers();
      var renderer = L.canvas({ padding: 0.3 });
      list.forEach(function (s) {
        var col = s.pm2 < t1 ? C.low : (s.pm2 > t2 ? C.high : C.mid);
        L.circleMarker([s.lat, s.lon], { renderer: renderer, radius: 6, color: '#FFFFFF', weight: 1.2, fillColor: col, fillOpacity: 0.92 })
          .bindPopup('<strong>' + (s.type === 'M' ? 'Maison' : 'Appartement') + ' · ' + LI.fmt(s.surf) + ' m²' + (s.rooms ? ' · ' + s.rooms + ' p.' : '') + '</strong><br>' +
            LI.esc(s.commune) + ' · ' + LI.monthFR(s.ym) + '<br>' + LI.fmt(s.price) + ' € · <strong>' + LI.fmt(round10(s.pm2)) + ' €/m²</strong>')
          .addTo(S.layer);
      });
    }

    drawQuartiers();
    if (S.map && S.quartier && $('f-commune').value === 'Louviers' && S.qSel) {
      S.map.stop(); S.map.fitBounds(S.qSel.getBounds(), { padding: [30, 30], animate: false });
    } else if (S.map && !S.focus && list.length) {
      var bb = L.latLngBounds(list.map(function (s) { return [s.lat, s.lon]; }));
      S.map.fitBounds(bb, { padding: [30, 30], maxZoom: 15 });
    }

        // Tableau par commune
    var by = {};
    list.forEach(function (s) { (by[s.commune] = by[s.commune] || []).push(s); });
    var rows = Object.keys(by).sort(function (a, b) { return by[b].length - by[a].length; }).map(function (c) {
      var arr = by[c];
      var h = arr.filter(function (s) { return s.type === 'M'; }), a = arr.filter(function (s) { return s.type === 'A'; });
      var f = function (x) { return x.length >= 5 ? LI.fmt(round10(LI.median(x.map(function (s) { return s.pm2; })))) + ' €' : '<span class="muted">—</span>'; };
      return '<tr><td>' + LI.esc(c) + '</td><td class="num">' + arr.length + '</td><td class="num">' + f(h) + '</td><td class="num">' + f(a) + '</td></tr>';
    }).join('');
    $('t-body').innerHTML = rows || '<tr><td colspan="4" class="muted">Aucune vente pour ces critères.</td></tr>';
  }

  /* ---------- Quartiers de Louviers ---------- */
  function drawQuartiers() {
    if (!S.map || !S.gj) return;
    if (S.qLayer) { S.map.removeLayer(S.qLayer); S.qLayer = null; }
    S.qSel = null;
    if ($('f-commune').value !== 'Louviers') return;
    S.qLayer = L.geoJSON(S.gj, {
      interactive: false,
      style: function (f) {
        var on = f.properties.slug === S.quartier;
        return on ? { color: '#C9A961', weight: 3.5, fill: false } : { color: '#1B2E40', weight: 1, opacity: S.quartier ? 0.35 : 0.6, dashArray: '4 4', fill: false };
      },
      onEachFeature: function (f, l) { if (f.properties.slug === S.quartier) S.qSel = l; }
    }).addTo(S.map);
    S.qLayer.bringToBack();
  }
  function setQuartier(slug, opts) {
    opts = opts || {};
    S.quartier = slug || '';
    if (S.quartier && $('f-commune').value !== 'Louviers') $('f-commune').value = 'Louviers';
    ['f-quartier', 'f-quartier-top'].forEach(function (id) { if ($(id)) $(id).value = S.quartier; });
    document.querySelectorAll('.pq-panel').forEach(function (p) { p.hidden = p.getAttribute('data-slug') !== S.quartier; });
    document.querySelectorAll('.pq-row').forEach(function (r) { r.classList.toggle('on', r.getAttribute('data-slug') === S.quartier); });
    try {
      var u = new URL(location.href);
      if (S.quartier) u.searchParams.set('quartier', S.quartier); else u.searchParams.delete('quartier');
      history.replaceState(null, '', u.pathname + u.search + u.hash);
    } catch (e) {}
    syncQuartierField();
    render();
    if (opts.scroll) { var el = document.querySelector('.pq-panel:not([hidden])') || $('prix-quartiers'); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    if (S.quartier && window.plausible && !opts.silent) window.plausible('Prix Quartier Choisi', { props: { quartier: S.quartier } });
  }
  function syncQuartierField() {
    var w = $('f-quartier-w'); if (w) w.hidden = $('f-commune').value !== 'Louviers' || !S.gj;
  }
  function initQuartiers() {
    if (!LI.loadVillages || !$('f-quartier')) return Promise.resolve();
    return LI.loadVillages().then(function (gj) {
      S.gj = gj;
      S.all.forEach(function (s) { if (s.commune === 'Louviers') { var v = LI.villageDe(gj, s.lat, s.lon); s.q = v ? v.properties.slug : ''; } });
      var top = $('f-quartier-top');
      if (top) gj.features.slice().sort(function (a, b) { return a.properties.n - b.properties.n; }).forEach(function (f) {
        var o = document.createElement('option'); o.value = f.properties.slug; o.textContent = f.properties.n + '. ' + f.properties.nom; top.appendChild(o);
      });
      ['f-quartier', 'f-quartier-top'].forEach(function (id) { if ($(id)) $(id).addEventListener('change', function () { setQuartier(this.value, { scroll: id === 'f-quartier' }); }); });
      document.querySelectorAll('.pq-row').forEach(function (r) {
        r.addEventListener('click', function (e) { if (e.target.closest('a')) return; setQuartier(r.getAttribute('data-slug'), { scroll: true }); });
      });
    }).catch(function () {});
  }

  document.addEventListener('DOMContentLoaded', function () {
    var u = new URLSearchParams(location.search);
    var flat = parseFloat(u.get('lat')), flon = parseFloat(u.get('lon'));
    var hasFocus = isFinite(flat) && isFinite(flon);
    S.focus = hasFocus;
    var c = hasFocus ? { lat: flat, lon: flon } : LI.center;

    if (window.L) {
      S.map = LI.makeMap($('map'), c.lat, c.lon, hasFocus ? 16 : 14);
      S.layer = L.layerGroup().addTo(S.map);
      if (hasFocus) {
        L.circle([flat, flon], { radius: 500, color: '#1B2E40', weight: 1.5, dashArray: '4 6', fill: false, interactive: false }).addTo(S.map);
        L.marker([flat, flon], { icon: LI.divIcon('<div class="pin-me"></div>', '', 22), zIndexOffset: 1000 }).addTo(S.map);
      }
    }

    LI.loadDVF().then(function (d) {
      S.all = d.allSales || d.sales; S.meta = d.metaAll || d.meta || {};
      if (!S.all.length) {
        $('no-data').hidden = false;
        $('t-body').innerHTML = '<tr><td colspan="4" class="muted">Les données seront affichées dès leur intégration.</td></tr>';
        return;
      }
      if (S.meta.period) $('period').textContent = LI.monthFR(S.meta.period.from) + ' – ' + LI.monthFR(S.meta.period.to);
      if (S.meta.generated) $('updated').textContent = S.meta.generated;
      var communes = {};
      S.all.forEach(function (s) { communes[s.commune] = (communes[s.commune] || 0) + 1; });
      var sel = $('f-commune');
      Object.keys(communes).sort(function (a, b) { return a.localeCompare(b, 'fr'); }).forEach(function (cm) {
        var o = document.createElement('option'); o.value = cm; o.textContent = cm; sel.appendChild(o);
      });
      if (!hasFocus && communes.Louviers) sel.value = 'Louviers';
      // Une option par année disponible
      var years = {}; S.all.forEach(function (s) { years[s.ym.slice(0, 4)] = 1; });
      var ys = Object.keys(years).sort().reverse(), fp = $('f-period');
      var allOpt = fp.querySelector('option[value="all"]');
      if (allOpt && ys.length > 1) allOpt.textContent = 'Toute la période (' + ys[ys.length - 1] + '–' + ys[0] + ')';
      ys.forEach(function (y) {
        var o = document.createElement('option'); o.value = 'y' + y;
        o.textContent = 'Année ' + y + (S.meta.period && S.meta.period.to.slice(0, 4) === y && S.meta.period.to.slice(5) !== '12' ? ' (jusqu’à ' + LI.monthFR(S.meta.period.to) + ')' : '');
        fp.appendChild(o);
      });
      var py = u.get('periode'); if (py && fp.querySelector('option[value="' + py + '"]')) fp.value = py;
      ['f-type', 'f-period'].forEach(function (id) { $(id).addEventListener('change', render); });
      $('f-commune').addEventListener('change', function () { syncQuartierField(); render(); });
      syncQuartierField();
      if (!u.get('quartier')) render();
      initQuartiers().then(function () {
        var qs = u.get('quartier');
        var ok = qs && S.gj && S.gj.features.some(function (f) { return f.properties.slug === qs; });
        if (ok) setQuartier(qs, { silent: true }); else { syncQuartierField(); render(); }
      });
    });
  });
})();
