/* ==========================================================
   louviers.immo — Calculateurs (frais de notaire, capacité d'emprunt)
   Estimations indicatives : seul le notaire / la banque font foi.
   ========================================================== */
(function () {
  'use strict';
  var LI = window.LI;
  var $ = function (id) { return document.getElementById(id); };
  function num(id) { var v = parseFloat(String($(id).value).replace(/\s/g, '').replace(',', '.')); return isFinite(v) ? v : 0; }
  function eur(x) { return LI.fmt(Math.round(x)) + ' €'; }

  /* ---------- Paramètres (à mettre à jour si la loi change) ---------- */
  var P = {
    dmto: 0.0632,          // Eure, depuis le 1er avril 2026 : 5 % département + 1,2 % commune + frais d'assiette
    dmtoPrimo: 0.0581,     // Primo-accédants (résidence principale) : taux départemental maintenu à 4,5 %
    tpfNeuf: 0.00715,      // Taxe de publicité foncière dans le neuf (VEFA)
    csi: 0.001,            // Contribution de sécurité immobilière
    debours: 1200,         // Débours et formalités (forfait indicatif)
    tva: 0.20,
    bareme: [[6500, 0.03870], [17000, 0.01596], [60000, 0.01064], [Infinity, 0.00799]] // émoluments proportionnels HT
  };

  function emoluments(prix) {
    var tot = 0, prev = 0;
    P.bareme.forEach(function (t) {
      if (prix > prev) tot += (Math.min(prix, t[0]) - prev) * t[1];
      prev = t[0];
    });
    return tot;
  }

  function notaire() {
    var prix = num('n-prix');
    var neuf = document.querySelector('input[name="n-type"]:checked').value === 'neuf';
    var primo = $('n-primo').checked;
    var taxes = prix * (neuf ? P.tpfNeuf : (primo ? P.dmtoPrimo : P.dmto));
    var emo = emoluments(prix) * (1 + P.tva);
    var csi = Math.max(15, prix * P.csi);
    var total = prix > 0 ? taxes + emo + csi + P.debours : 0;
    $('n-total').textContent = eur(total);
    $('n-pct').textContent = prix > 0 ? 'soit environ ' + LI.fmt(total / prix * 100, 1) + ' % du prix' : '';
    $('n-taxes').textContent = eur(taxes);
    $('n-taxes-l').textContent = neuf ? 'Taxe de publicité foncière (0,715 %)' : 'Droits de mutation (' + LI.fmt((primo ? P.dmtoPrimo : P.dmto) * 100, 2) + ' %)';
    $('n-emo').textContent = eur(prix > 0 ? emo : 0);
    $('n-csi').textContent = eur(prix > 0 ? csi : 0);
    $('n-deb').textContent = eur(prix > 0 ? P.debours : 0);
    $('n-cout').textContent = eur(prix + total);
    $('n-primo-row').hidden = neuf;
  }

  function emprunt() {
    var rev = num('e-rev'), chg = num('e-chg'), apport = num('e-apport');
    var years = parseInt($('e-duree').value, 10), rate = num('e-taux') / 100, ass = num('e-ass') / 100;
    var maxPay = Math.max(0, rev * 0.35 - chg);           // taux d'endettement de 35 %, assurance comprise
    var n = years * 12, r = rate / 12;
    var factor = r > 0 ? r / (1 - Math.pow(1 + r, -n)) : 1 / n;
    var capital = maxPay / (factor + ass / 12);
    var payAss = capital * ass / 12;
    // Budget achat : (capital + apport) = prix × (1 + frais de notaire ≈ 7,8 % dans l'ancien)
    var budget = (capital + apport) / 1.078;
    $('e-capital').textContent = eur(capital);
    $('e-mensu').textContent = eur(maxPay);
    $('e-mensu-d').textContent = eur(maxPay - payAss) + ' de crédit + ' + eur(payAss) + ' d’assurance';
    $('e-budget').textContent = eur(budget);
    $('e-cout').textContent = eur(Math.max(0, (maxPay - payAss) * n - capital) + payAss * n);
    var lk = $('e-link');
    if (lk) lk.href = 'prix.html';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var fn = $('form-notaire'), fe = $('form-emprunt');
    if (fn) { fn.addEventListener('input', notaire); fn.addEventListener('change', notaire); fn.addEventListener('submit', function (e) { e.preventDefault(); }); notaire(); }
    if (fe) { fe.addEventListener('input', emprunt); fe.addEventListener('change', emprunt); fe.addEventListener('submit', function (e) { e.preventDefault(); }); emprunt(); }
  });
})();
