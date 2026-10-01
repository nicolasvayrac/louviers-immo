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
     mapName   (facultatif) nom affiché sur les cartes et dans l'annuaire
     listed    (facultatif) false pour une seconde boutique : sur les cartes,
               mais pas en double dans la liste des portraits
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
    photo: "assets/img/portraits/maison-barbe-facade.jpg",
    mapName: "Maison Barbé - Charcuterie du Parvis",
    chapo: "Rue du Maréchal Foch, Sylvie et Patrice Barbé perpétuent une charcuterie artisanale, entièrement repensée après de gros travaux.",
    quartier: "Centre-ville",
    category: "Charcutier-traiteur",
    rubrique: "bouche",
    commune: "Louviers",
    address: "43 rue du Maréchal Foch 27400 Louviers",
    phone: "02 32 40 02 77",
    website: "https://www.maison-barbe.com/"
  },
  {
    name: "Institut des Portes de l'Eau",
    title: "la beauté au naturel en centre-ville",
    url: "portraits/institut-des-portes-de-l-eau.html",
    photo: "assets/img/portraits/portes-eau-accueil.jpg",
    chapo: "Place de la Porte de l’Eau, Élodie, esthéticienne depuis plus de vingt-trois ans, a ouvert un institut tourné vers les soins bio.",
    quartier: "Centre-ville",
    category: "Institut de beauté",
    kind: "beauty",
    rubrique: "beaute",
    commune: "Louviers",
    address: "1 place de la Porte de l'Eau 27400 Louviers",
    phone: "09 82 52 92 16",
    website: "https://institutdesportesdeleau.fr/"
  },
  {
    name: "Aux Délices de Louviers",
    aliases: ["Aux délices de Louviers", "Maison Guincêtre", "Maison Guincetre", "Boulangerie Guincêtre"],
    mapName: "Aux Délices de Louviers - Maison Guincêtre",
    title: "une histoire de famille, de Louviers au Vaudreuil",
    url: "portraits/aux-delices-de-louviers.html",
    photo: "assets/img/portraits/guincetre-facades.jpg",
    chapo: "Rue du Maréchal Foch, la famille Guincêtre, finaliste de La Meilleure Boulangerie de France sur M6, fait tout sur place depuis 1996.",
    quartier: "Centre-ville",
    category: "Boulanger-pâtissier",
    kind: "bakery",
    rubrique: "boulangeries",
    commune: "Louviers",
    address: "38 rue du Maréchal Foch 27400 Louviers",
    phone: "02 32 40 04 63",
    website: "https://auxdelicesdelouviers.fr/"
  },
  {
    // Seconde boutique : apparaît sur les cartes et dans l'annuaire du Vaudreuil, pas dans la liste des portraits
    name: "Maison Guincêtre",
    listed: false,
    aliases: ["Maison Guincetre", "Aux Délices de Louviers"],
    url: "portraits/aux-delices-de-louviers.html",
    category: "Boulanger-pâtissier",
    kind: "bakery",
    rubrique: "boulangeries",
    commune: "Le Vaudreuil",
    address: "10 place du Général de Gaulle 27100 Le Vaudreuil",
    phone: "02 32 40 04 63",
    website: "https://auxdelicesdelouviers.fr/maison-guincetre/"
  }
];
