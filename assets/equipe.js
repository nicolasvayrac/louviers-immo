/* louviers.immo — questionnaire de l'équipe : photos réduites avant l'envoi (Netlify Forms, 8 Mo par envoi) */
(function () {
  'use strict';
  var form = document.getElementById('eq-form'); if (!form) return;
  var st = document.getElementById('eq-st'), btn = document.getElementById('eq-send');
  function shrink(file) {
    return new Promise(function (res) {
      if (!file || !file.size || !/^image\//.test(file.type)) return res(null);
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () {
        var m = 1600, k = Math.min(1, m / Math.max(img.width, img.height));
        var c = document.createElement('canvas'); c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height); URL.revokeObjectURL(url);
        c.toBlob(function (b) { res(b ? new File([b], file.name.replace(/\.[^.]+$/, '') + '.jpg', { type: 'image/jpeg' }) : file); }, 'image/jpeg', 0.82);
      };
      img.onerror = function () { URL.revokeObjectURL(url); res(file); };
      img.src = url;
    });
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.personne.value) { st.textContent = 'Choisissez votre nom en haut du questionnaire.'; form.personne.focus(); return; }
    if (!form.accord_publication.checked) { st.textContent = 'Cochez la dernière case pour pouvoir envoyer.'; return; }
    var files = form.querySelectorAll('input[type=file]'), hasPhoto = false;
    files.forEach(function (f) { if (f.files.length) hasPhoto = true; });
    if (hasPhoto && !form.accord_photos.checked) { st.textContent = 'Cochez la case sur les photos pour pouvoir les envoyer.'; return; }
    btn.disabled = true; st.textContent = hasPhoto ? 'Préparation des photos…' : 'Envoi…';
    var fd = new FormData(form);
    Promise.all(Array.prototype.map.call(files, function (f) {
      return shrink(f.files[0]).then(function (x) { fd.delete(f.name); if (x) fd.append(f.name, x); });
    })).then(function () {
      st.textContent = 'Envoi…';
      return fetch(form.getAttribute('action'), { method: 'POST', body: fd });
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      form.hidden = true; document.getElementById('eq-done').hidden = false; window.scrollTo(0, 0);
    }).catch(function () {
      btn.disabled = false;
      st.textContent = 'L’envoi n’a pas abouti. Vérifiez votre connexion et réessayez ; si cela recommence, envoyez vos réponses à Nicolas par e-mail.';
    });
  });
})();
