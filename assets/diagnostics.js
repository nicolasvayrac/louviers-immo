/* louviers.immo — Diagnostics : liste personnalisée selon le logement */
(function () {
  'use strict';
  var AGGLO = 'https://formulaires.demarches.seine-eure.fr/cycle-de-l-eau/demande-de-diagnostic-assainissement/';

  function val(f, n) { var el = f.querySelector('input[name="' + n + '"]:checked'); return el ? el.value : ''; }
  function on(f, n) { var el = f.querySelector('input[name="' + n + '"]'); return !!(el && el.checked); }

  function compute(f) {
    var vente = val(f, 'projet') === 'vente', maison = val(f, 'type') === 'maison';
    var annee = val(f, 'annee'), dpe = val(f, 'dpe'), fosse = val(f, 'eaux') === 'fosse', agglo = on(f, 'agglo');
    var L = [], extra = [], alert = '';
    function add(id, name, valid, why) { L.push({ id: id, name: name, valid: valid, why: why }); }

    add('dpe', 'DPE, performance énergétique', '10 ans', 'Obligatoire pour tous les logements.');
    if (vente && maison && (dpe === 'E' || dpe === 'F' || dpe === 'G'))
      add('audit', 'Audit énergétique', '5 ans', 'Maison classée ' + dpe + ' : à remettre dès la première visite.');
    if ((annee === '1949' || annee === '1997') && (vente || !maison))
      add('amiante', vente ? 'Repérage amiante' : 'Dossier amiante des parties privatives', vente ? 'Illimitée si absence' : 'À tenir à disposition',
        'Permis de construire antérieur au 1er juillet 1997.');
    if (annee === '1949')
      add('plomb', 'Plomb (CREP)', vente ? '1 an, illimitée si absence' : '6 ans', 'Logement construit avant 1949.');
    if (on(f, 'elec15')) add('elec', 'Électricité', vente ? '3 ans' : '6 ans', 'Installation de plus de 15 ans.');
    if (on(f, 'gaz15')) add('gaz', 'Gaz', vente ? '3 ans' : '6 ans', 'Installation de plus de 15 ans.');
    add('erp', 'État des risques (ERP)', 'Moins de 6 mois', 'Obligatoire pour tous les logements.');
    if (vente && !maison) add('carrez', 'Surface loi Carrez', 'Tant que la surface ne change pas', 'Vente d’un lot de copropriété.');
    if (!vente) add('carrez', 'Surface habitable (loi Boutin)', 'Tant que la surface ne change pas', 'Elle figure au bail.');
    if (vente && fosse)
      add('assaini', 'Contrôle de l’assainissement individuel', 'Moins de 3 ans', 'Réalisé par le service public d’assainissement non collectif (SPANC).');
    else if (vente && agglo)
      add('assaini', 'Contrôle de raccordement à l’égout', '3 ans', 'Obligation propre à l’Agglomération Seine-Eure, réalisée par un agent de l’Agglo (100 € pour un logement).');

    if (vente && maison && dpe === '?')
      extra.push('Si l’étiquette énergie de la maison est E, F ou G, un <a href="#d-audit">audit énergétique</a> sera aussi demandé.');
    if (vente && !maison)
      extra.push('En copropriété, réunissez aussi les documents du syndic : pré-état daté, règlement de copropriété, procès-verbaux des trois dernières assemblées, fiche synthétique.');
    if (!vente && dpe === 'G')
      alert = 'Un logement classé G ne peut plus faire l’objet d’un nouveau bail depuis le 1er janvier 2025. Des travaux de rénovation sont nécessaires avant de le louer.';
    else if (!vente && dpe === 'F')
      alert = 'Un logement classé F ne pourra plus être proposé à la location à partir de 2028, et son loyer ne peut pas être augmenté en cours ou en renouvellement de bail.';
    if (vente && agglo && !fosse)
      extra.push('<a href="' + AGGLO + '" target="_blank" rel="noopener">Demander le contrôle d’assainissement à l’Agglo</a> dès la mise en vente : comptez quelques semaines.');
    return { list: L, extra: extra, alert: alert, vente: vente };
  }

  function render(f) {
    var r = compute(f);
    document.getElementById('dg-count').textContent = r.list.length;
    document.getElementById('dg-title').textContent = 'diagnostics à prévoir pour ' + (r.vente ? 'vendre' : 'louer');
    document.getElementById('dg-list').innerHTML = r.list.map(function (d) {
      return '<li class="dg-' + d.id + '"><a href="#d-' + d.id + '"><b>' + LI.esc(d.name) + '</b></a><span class="dg-v">' + LI.esc(d.valid) + '</span><span class="dg-w">' + LI.esc(d.why) + '</span></li>';
    }).join('');
    var cta = document.getElementById('dg-cta'); if (cta) cta.hidden = !r.vente;
    var a = document.getElementById('dg-alert');
    a.hidden = !r.alert; a.textContent = r.alert;
    document.getElementById('dg-extra').innerHTML = r.extra.map(function (t) { return '<p>' + t + '</p>'; }).join('');
    var out = document.querySelector('.dg-out');
    out.classList.remove('flash'); void out.offsetWidth; out.classList.add('flash');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var f = document.getElementById('dg-form');
    if (!f) return;
    f.addEventListener('change', function () { render(f); });
    render(f);
  });
})();

/* Diagnostiqueurs partenaires : ordre tiré au hasard à chaque visite, pour qu'aucun ne soit toujours en premier */
(function () {
  var grid = document.getElementById('pt-grid');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.children);
  for (var i = cards.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1)), t = cards[i]; cards[i] = cards[j]; cards[j] = t;
  }
  cards.forEach(function (c) { grid.appendChild(c); });
})();
