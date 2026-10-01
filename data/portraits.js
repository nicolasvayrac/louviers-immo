/* ==========================================================
   Portraits publiés sur louviers.immo
   ----------------------------------------------------------
   Ajoutez un bloc par portrait publié. Ils apparaissent alors
   automatiquement : sur l'accueil, la page Portraits, et dans
   « Mon adresse » (badge « Lire son portrait » sur le commerce).

   Champs :
     name      Nom du commerce (tel qu'affiché sur la devanture)
     title     Titre du portrait
     url       Chemin de la page, ex. "portraits/boulangerie-dupont.html"
     photo     Photo de couverture, ex. "assets/img/portraits/dupont.jpg"
     chapo     Une ou deux phrases d'accroche
     quartier  Quartier, ex. "Centre-ville"
     category  Catégorie affichée, ex. "Boulangerie"
     address   Adresse complète : la position est retrouvée automatiquement
     lat, lon  (facultatif) coordonnées exactes, si l'adresse ne suffit pas
     aliases   Autres noms du commerce (enseigne, ancien nom)
     website   Site du commerce
     commune   Commune, ex. "Louviers"
     rubrique  Rubrique de l'annuaire : restaurer, snacking, cafes, boulangeries,
               bouche, courses, habiller, beaute, maison, loisirs, sante, services

   Exemple (à dupliquer, sans les // en début de ligne) :

   // {
   //   name: "Boulangerie Exemple",
   //   title: "Le pain au levain depuis trois générations",
   //   url: "portraits/boulangerie-exemple.html",
   //   photo: "assets/img/portraits/boulangerie-exemple.jpg",
   //   chapo: "Rue du Général de Gaulle, la famille X pétrit chaque nuit depuis 1985.",
   //   quartier: "Centre-ville",
   //   category: "Boulangerie",
   //   lat: 49.2150, lon: 1.1650
   // },
   ========================================================== */
window.LI_PORTRAITS = [
  {
    name: "Maison Barbé",
    aliases: ["Charcuterie du Parvis", "Maison Barbé - Charcuterie du Parvis"],
    title: "la charcuterie du Parvis fait peau neuve",
    url: "portraits/maison-barbe.html",
    chapo: "Rue du Maréchal Foch, Sylvie et Patrice Barbé perpétuent une charcuterie artisanale, entièrement repensée après de gros travaux.",
    quartier: "Centre-ville",
    category: "Charcutier-traiteur",
    rubrique: "bouche",
    commune: "Louviers",
    address: "43 rue du Maréchal Foch 27400 Louviers",
    phone: "02 32 40 02 77",
    website: "https://www.maison-barbe.com/"
  }
];
