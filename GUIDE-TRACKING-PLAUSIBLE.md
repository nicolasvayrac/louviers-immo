# Guide tracking Plausible — louviers.immo

## ✅ Ce qui a été fait dans le code

Les 3 fichiers HTML (`index.html`, `contact.html`, `reglement.html`) ont été mis à jour avec :

1. **Script Plausible** ajouté dans le `<head>` de chaque page
2. **Tous les boutons "Estimation offerte"** taggés pour tracking (9 boutons au total) :
   - `index.html` : nav, hero, bottom CTA, footer
   - `contact.html` : nav, hero, footer
   - `reglement.html` : nav, footer
3. **Tracking automatique des liens sortants** activé (cvimmobilier.fr, FNAIM, Google Maps, etc.)

---

## 🚀 Étapes côté Plausible (15 minutes)

### 1. Créer ton compte Plausible

1. Va sur [plausible.io](https://plausible.io/register)
2. Crée un compte avec ton email pro
3. Choisis le plan **Growth** (~9€ HT/mois pour ≤10k visites/mois)
   - Tu as **30 jours d'essai gratuit**, pas de CB demandée

### 2. Ajouter ton domaine

1. Dans le dashboard Plausible → **Add a website**
2. Domain : `louviers.immo` (sans `https://` ni `www`)
3. Timezone : `Europe/Paris`
4. Reporting currency : `EUR`
5. Clique **Add site**

### 3. Vérifier l'installation

1. Plausible te montre une page "Verify your installation"
2. **Ne fais rien sur cette page** — le script est déjà dans ton code
3. Ouvre `https://louviers.immo` dans un nouvel onglet (ou la version netlify si DNS pas encore propagé)
4. Reviens sur Plausible → **Verify** → ça devrait passer au vert

### 4. Configurer les "Goals" (objectifs de conversion)

Dans le dashboard Plausible → **Site Settings** → **Goals** → **Add Goal**

**Goal 1 — Click sur Estimation**
- Goal trigger : **Custom event**
- Event name : `Estimation Click`
- Display name : `🎯 Clic Estimation`
- **Add goal**

**Goal 2 — Trafic depuis QR codes**
- Goal trigger : **Custom event**
- Event name : `Outbound Link: Click` (déjà tracké par le script outbound-links)

(Plausible va auto-détecter les UTM params dans Sources → Acquisition.)

---

## 📱 URLs à mettre dans les QR codes

Voici les 4 URLs exactes à utiliser pour générer tes QR codes. **Chacune est différente** pour pouvoir distinguer les supports dans Plausible :

### QR Presse (annonces journaux locaux, etc.)
```
https://louviers.immo/?utm_source=presse&utm_medium=qr&utm_campaign=taxe2026
```

### QR Set de table (restaurants, brasseries partenaires)
```
https://louviers.immo/?utm_source=settable&utm_medium=qr&utm_campaign=taxe2026
```

### QR Vitrine (vitrines des 2 agences)
```
https://louviers.immo/?utm_source=vitrine&utm_medium=qr&utm_campaign=taxe2026
```

### QR Flyers (boîtage, distribution)
```
https://louviers.immo/?utm_source=flyer&utm_medium=qr&utm_campaign=taxe2026
```

### Comment générer les QR codes

1. Va sur [qr-code-generator.com](https://www.qr-code-generator.com) (gratuit)
2. Choisis "URL" comme type
3. Colle l'URL UTM du support
4. Personnalise au besoin (couleurs CV IMMOBILIER : navy `#0B2C4D` + or `#C8A865`)
5. Télécharge en PNG haute résolution (pour impression) et SVG (pour le print pro)
6. **Important** : teste chaque QR code avec ton iPhone avant impression !

---

## 📊 Comment lire ton dashboard Plausible

Une fois Plausible installé et qu'il y a du trafic, tu verras :

### Vue principale
- **Visitors** : nombre de visiteurs uniques
- **Pageviews** : nombre total de pages vues
- **Bounce rate** : % de visiteurs qui sont partis après 1 seule page
- **Visit duration** : temps moyen passé

### Section "Sources" — Pour mesurer le ROI des supports
- Filtre par **UTM source** : tu verras `presse`, `settable`, `vitrine`, `flyer`
- Tu sauras combien de visiteurs sont venus de chaque support
- Tu sauras combien ont cliqué sur "Estimation" (= conversion)

### Section "Goal Conversions"
- **🎯 Clic Estimation** : nombre total de clics
- Tu pourras voir : *"Le set de table a généré 47 visites et 8 clics estimation = 17% de taux de conversion"*

### Calcul du ROI
Pour chaque support :
```
Taux de conversion = (Clics Estimation / Visiteurs du support) × 100
```

Exemple :
- Set de table : 100€ d'impression × 200 exemplaires = 100€
  → 47 visites, 8 clics estimation
  → 1 mandat exclusif signé (~10 000€ d'honoraires moyens)
  → **ROI = 100x sur l'investissement**

---

## 🔎 Tester que tout fonctionne (avant de te lancer)

1. Va sur ton site `louviers.immo` (ou `louviers-immo.netlify.app` en attendant le DNS)
2. Ouvre la console développeur (Cmd+Opt+I sur Mac, F12 sur PC)
3. Onglet **Network** → filtre `plausible`
4. Recharge la page → tu devrais voir une requête `event` envoyée à `plausible.io`
5. Clique sur le bouton "Estimation offerte" → une seconde requête `event` doit apparaître

Si tu vois ces 2 requêtes, c'est nickel ✅

---

## ⚠️ RGPD — Pas besoin de bandeau cookie

Plausible est **conçu pour être RGPD-compliant sans bandeau cookie** :
- Pas de cookie déposé
- Pas de tracking individuel (pas de fingerprinting)
- IP visiteur anonymisée et non stockée
- Données hébergées en UE (Allemagne)

Tu n'as **rien à ajouter** côté juridique. C'est l'un des gros avantages de Plausible vs GA4.

---

## 💡 Idées d'évolution (plus tard)

Quand tu seras à l'aise avec le dashboard, tu pourras :

1. **Ajouter des goals supplémentaires** :
   - Clic sur le bouton "Tel" (appel direct depuis le site)
   - Clic sur "Itinéraire" (Google Maps)
   - Clic sur le règlement (= visiteur très engagé)

2. **Brancher Plausible sur Slack ou Email** :
   - Site Settings → Email reports → recevoir un récap hebdo automatique

3. **Comparer les périodes** :
   - Filtre "Last 30 days vs Previous 30 days" pour voir les évolutions

---

## 📞 Si tu bloques

- Doc Plausible : [plausible.io/docs](https://plausible.io/docs)
- Support Plausible : très réactif par mail (hello@plausible.io)
- Ou demande-moi, je peux te débugger ce que tu veux
