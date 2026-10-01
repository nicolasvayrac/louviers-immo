/* ==========================================================
   louviers.immo — scripts communs
   Navigation, apparitions, recherche d'adresse (Base Adresse
   Nationale via la Géoplateforme IGN), chiffres DVF, portraits.
   ========================================================== */
(function () {
  'use strict';

  var LI = window.LI = window.LI || {};
  LI.root = document.documentElement.getAttribute('data-root') || '';
  LI.center = { lat: 49.2153, lon: 1.1655 }; // Louviers

  /* ---------- Utilitaires ---------- */
  LI.esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  LI.fmt = function (n, dec) {
    return Number(n).toLocaleString('fr-FR', { maximumFractionDigits: dec || 0, minimumFractionDigits: dec || 0 }).replace(/[\u202f\u2009]/g, '\u00a0');
  };
  LI.median = function (arr) {
    if (!arr.length) return null;
    var a = arr.slice().sort(function (x, y) { return x - y; });
    var m = Math.floor(a.length / 2);
    return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
  };
  LI.dist = function (lat1, lon1, lat2, lon2) {
    var R = 6371000, toR = Math.PI / 180;
    var dLat = (lat2 - lat1) * toR, dLon = (lon2 - lon1) * toR;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * toR) * Math.cos(lat2 * toR) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * R * Math.asin(Math.sqrt(a));
  };
  LI.norm = function (s) {
    return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  };
  LI.fetchJSON = function (url, opts, ms) {
    var ctrl = 'AbortController' in window ? new AbortController() : null;
    var t = ctrl ? setTimeout(function () { ctrl.abort(); }, ms || 12000) : null;
    var o = opts || {};
    if (ctrl) o.signal = ctrl.signal;
    return fetch(url, o).then(function (r) {
      if (t) clearTimeout(t);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }, function (e) { if (t) clearTimeout(t); throw e; });
  };
  LI.monthFR = function (ym) {
    var M = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
    var p = String(ym || '').split('-');
    return p.length >= 2 ? M[parseInt(p[1], 10) - 1] + ' ' + p[0] : ym;
  };

  /* ---------- Géocodage : Base Adresse Nationale ---------- */
  var GEO = [
    'https://data.geopf.fr/geocodage/search',
    'https://api-adresse.data.gouv.fr/search/'
  ];
  LI.geocode = function (q, limit, autocomplete) {
    var qs = '?q=' + encodeURIComponent(q) + '&limit=' + (limit || 5) +
      '&lat=' + LI.center.lat + '&lon=' + LI.center.lon +
      (autocomplete ? '&autocomplete=1' : '');
    function attempt(i) {
      var base = GEO[i];
      var url = base + qs + (i === 0 ? '&index=address' : '');
      return LI.fetchJSON(url, null, 8000).then(function (j) {
        return (j.features || []).map(function (f) {
          var p = f.properties || {};
          return {
            label: p.label, name: p.name, city: p.city, postcode: p.postcode,
            context: p.context, type: p.type,
            lon: f.geometry.coordinates[0], lat: f.geometry.coordinates[1]
          };
        });
      }).catch(function (e) {
        if (i + 1 < GEO.length) return attempt(i + 1);
        throw e;
      });
    }
    return attempt(0);
  };

  /* ---------- Champ d'adresse avec suggestions ---------- */
  LI.addressUrl = function (r) {
    return LI.root + 'adresse.html?q=' + encodeURIComponent(r.label) +
      '&lat=' + r.lat.toFixed(6) + '&lon=' + r.lon.toFixed(6);
  };

  function bindSearch(form) {
    var input = form.querySelector('input[type="search"], input[type="text"]');
    var list = form.querySelector('.suggest');
    if (!input || !list) return;
    var items = [], active = -1, timer = null, seq = 0;

    function close() { list.classList.remove('show'); input.setAttribute('aria-expanded', 'false'); active = -1; }
    function render() {
      if (!items.length) { close(); return; }
      list.innerHTML = items.map(function (r, i) {
        var sub = [r.postcode, r.city].filter(Boolean).join(' ');
        return '<li role="option" id="' + list.id + '-' + i + '" aria-selected="' + (i === active) + '" data-i="' + i + '">' +
          LI.esc(r.name || r.label) + (sub && r.type !== 'municipality' ? '<small>' + LI.esc(sub) + '</small>' : '') + '</li>';
      }).join('');
      list.classList.add('show');
      input.setAttribute('aria-expanded', 'true');
      if (active >= 0) input.setAttribute('aria-activedescendant', list.id + '-' + active);
      else input.removeAttribute('aria-activedescendant');
    }
    function choose(r) {
      close();
      input.value = r.label;
      if (typeof form._onChoose === 'function') form._onChoose(r);
      else window.location.href = LI.addressUrl(r);
    }
    input.addEventListener('input', function () {
      var q = input.value.trim();
      clearTimeout(timer);
      if (q.length < 3) { items = []; close(); return; }
      timer = setTimeout(function () {
        var my = ++seq;
        LI.geocode(q, 5, true).then(function (res) {
          if (my !== seq) return;
          items = res; active = -1; render();
        }).catch(function () { items = []; close(); });
      }, 220);
    });
    input.addEventListener('keydown', function (e) {
      if (!list.classList.contains('show')) return;
      if (e.key === 'ArrowDown') { active = Math.min(items.length - 1, active + 1); render(); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { active = Math.max(0, active - 1); render(); e.preventDefault(); }
      else if (e.key === 'Escape') { close(); }
      else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); choose(items[active]); }
    });
    list.addEventListener('mousedown', function (e) {
      var li = e.target.closest('li');
      if (li) { e.preventDefault(); choose(items[+li.getAttribute('data-i')]); }
    });
    input.addEventListener('blur', function () { setTimeout(close, 150); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = input.value.trim();
      if (!q) { input.focus(); return; }
      if (items.length) { choose(items[Math.max(0, active)]); return; }
      var btn = form.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;
      LI.geocode(q, 1, false).then(function (res) {
        if (btn) btn.disabled = false;
        if (res.length) choose(res[0]);
        else window.location.href = LI.root + 'adresse.html?q=' + encodeURIComponent(q);
      }).catch(function () {
        if (btn) btn.disabled = false;
        window.location.href = LI.root + 'adresse.html?q=' + encodeURIComponent(q);
      });
    });
  }

  /* ---------- Données DVF (chargées une seule fois) ---------- */
  var dvfPromise = null;
  LI.loadDVF = function () {
    if (!dvfPromise) {
      dvfPromise = LI.fetchJSON(LI.root + 'data/dvf.json', null, 15000).then(function (j) {
        var sales = (j.sales || []).map(function (s) {
          return { lat: s[0], lon: s[1], ym: s[2], price: s[3], surf: s[4], type: s[5], rooms: s[6], commune: s[7], pm2: s[3] / s[4] };
        });
        return { meta: j, sales: sales };
      }).catch(function () { return { meta: {}, sales: [] }; });
    }
    return dvfPromise;
  };

  /* ---------- Lieux OpenStreetMap pré-téléchargés (data/pois.json) ---------- */
  var poisPromise = null;
  LI.loadPOIs = function () {
    if (!poisPromise) {
      poisPromise = LI.fetchJSON(LI.root + 'data/pois.json', null, 15000)
        .then(function (j) { return j && j.pois && j.pois.length ? j : null; })
        .catch(function () { return null; });
    }
    return poisPromise;
  };
  LI.inBBox = function (b, lat, lon, margin) {
    var m = margin || 0;
    return b && lat >= b[0] - m && lat <= b[2] + m && lon >= b[1] - m && lon <= b[3] + m;
  };

  /* ---------- Portraits (data/portraits.js) ---------- */
  LI.portraits = function () { return (window.LI_PORTRAITS || []).filter(function (p) { return p && p.url && p.name; }); };
  // Complète les coordonnées manquantes à partir de l'adresse (une seule fois par page)
  var resolved = null;
  LI.resolvePortraits = function () {
    if (!resolved) {
      var ps = LI.portraits();
      resolved = Promise.all(ps.map(function (p) {
        if (p.lat != null || !p.address) return Promise.resolve(p);
        return LI.geocode(p.address, 1, false).then(function (r) {
          if (r[0]) { p.lat = r[0].lat; p.lon = r[0].lon; }
          return p;
        }).catch(function () { return p; });
      }));
    }
    return resolved;
  };

  /* ---------- Agences et partenaires (data/partenaires.js) ---------- */
  var agResolved = null;
  LI.resolveAgences = function () {
    if (!agResolved) {
      var list = (window.LI_PARTENAIRES || []).filter(function (a) { return a && a.name && a.address; });
      agResolved = Promise.all(list.map(function (a) {
        if (!a.addr) a.addr = a.address.replace(/\s*\d{5}.*$/, '');
        if (a.lat != null) return Promise.resolve(a);
        return LI.geocode(a.address, 1, false).then(function (r) {
          if (r[0]) { a.lat = r[0].lat; a.lon = r[0].lon; }
          return a;
        }).catch(function () { return a; });
      }));
    }
    return agResolved;
  };
  /* ---------- Commerces masqués (data/exclusions.js) ---------- */
  var exclu = null;
  LI.isExclu = function (name) {
    if (!exclu) {
      exclu = {};
      (window.LI_EXCLUS || []).forEach(function (n) { if (n) exclu[LI.norm(n)] = 1; });
    }
    return !!exclu[LI.norm(name || '')];
  };

  /* ---------- Clubs sportifs (data/clubs.js) ---------- */
  var clubsResolved = null;
  LI.resolveClubs = function () {
    if (!clubsResolved) {
      var list = (window.LI_CLUBS || []).filter(function (c) { return c && c.name; });
      var byAddr = {};
      list.forEach(function (c) { if (c.address) (byAddr[c.address] = byAddr[c.address] || []).push(c); });
      clubsResolved = Promise.all(Object.keys(byAddr).map(function (a) {
        return LI.geocode(a, 1, false).then(function (r) {
          if (r[0]) byAddr[a].forEach(function (c) { c.lat = r[0].lat; c.lon = r[0].lon; });
        }).catch(function () { /* club affiché sans position */ });
      })).then(function () { return list; });
    }
    return clubsResolved;
  };

  LI.partnerLink = function (u) {
    return /^https?:/i.test(u) ? u : LI.root + u;
  };

  function renderHomePortraits() {
    var box = document.getElementById('home-portraits');
    if (!box) return;
    var all = LI.portraits().filter(function (p) { return p.listed !== false; });
    var ps = box.hasAttribute('data-all') ? all : all.slice(0, 3);
    if (!ps.length) return; // le message « à venir » est déjà dans le HTML
    box.innerHTML = ps.map(function (p, i) {
      return '<a class="p-card" href="' + LI.esc(LI.root + p.url) + '">' +
        (p.photo ? '<div class="ph"><img src="' + LI.esc(LI.root + p.photo) + '" alt="" loading="lazy"></div>'
          : '<div class="ph ph-type"><span>' + LI.esc(p.name) + '</span><small>' + LI.esc(p.category || '') + '</small></div>') +
        '<span class="eyebrow">Portrait n°' + String(i + 1).padStart(2, '0') + (p.quartier ? ' · ' + LI.esc(p.quartier) : '') + '</span>' +
        '<span class="t">' + LI.esc(p.name) + (p.title ? ' — ' + LI.esc(p.title) : '') + '</span>' +
        (p.chapo ? '<p>' + LI.esc(p.chapo) + '</p>' : '') + '</a>';
    }).join('');
  }

  function fillKpis() {
    var els = document.querySelectorAll('[data-kpi]');
    if (!els.length) return;
    LI.loadDVF().then(function (d) {
      if (!d.sales.length) return;
      var lv = d.sales.filter(function (s) { return LI.norm(s.commune) === 'louviers'; });
      var last = lv.map(function (s) { return s.ym; }).sort().pop();
      var cutoff = last ? (parseInt(last.slice(0, 4), 10) - 1) + last.slice(4) : '';
      var yr = lv.filter(function (s) { return s.ym > cutoff; });
      var vals = {
        maison: LI.median(lv.filter(function (s) { return s.type === 'M'; }).map(function (s) { return s.pm2; })),
        appart: LI.median(lv.filter(function (s) { return s.type === 'A'; }).map(function (s) { return s.pm2; })),
        ventes: yr.length
      };
      els.forEach(function (el) {
        var k = el.getAttribute('data-kpi');
        if (vals[k] != null) el.textContent = k === 'ventes' ? LI.fmt(vals[k]) : LI.fmt(Math.round(vals[k] / 10) * 10) + ' €';
      });
      var per = document.querySelector('[data-kpi-period]');
      if (per && d.meta.period) per.textContent = 'Ventes ' + LI.monthFR(d.meta.period.from) + ' – ' + LI.monthFR(d.meta.period.to) + ' · source DVF';
    });
  }

  /* ---------- Démarrage ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('.nav');
    var burger = document.querySelector('.burger');
    if (nav && burger) {
      burger.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
    document.querySelectorAll('form.search').forEach(bindSearch);

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.08 });
      document.querySelectorAll('.rv, .stagger').forEach(function (el) { io.observe(el); });
    } else {
      document.querySelectorAll('.rv, .stagger').forEach(function (el) { el.classList.add('in'); });
    }
    renderHomePortraits();
    fillKpis();
  });
})();
