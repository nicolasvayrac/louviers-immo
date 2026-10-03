/* ==========================================================
   Corrections de l'annuaire des commerces
   ----------------------------------------------------------
   1. Commerces à ne pas afficher (fermés, hors sujet)
   Les commerces dont le nom figure ci-dessous n'apparaissent
   ni dans l'annuaire, ni dans « Mon adresse ».

   Pour MASQUER un commerce : ajouter son nom entre guillemets,
   suivi d'une virgule, tel qu'il s'affiche sur le site.
   Les majuscules et les accents ne comptent pas.
   Pour le RÉAFFICHER : supprimer sa ligne.

   Exemple :
     "Nom du commerce",
   ========================================================== */
window.LI_EXCLUS = [
  "Le Beau Bar",
  "Au Bon Coin",
  "Lolotte Pastry",
  "Caramel",
  "Éram",
  "Manufacture Hermès",
];

/* ----------------------------------------------------------
   Commerces à classer dans une autre rubrique de l'annuaire
   "Nom du commerce": "rubrique"
   Rubriques : restaurer, snacking, cafes, boulangeries, bouche,
   courses, habiller, beaute, maison, loisirs, tabac, sante,
   artisans, services
   ---------------------------------------------------------- */
window.LI_RUBRIQUES = {
  "Collet traiteur": "restaurer",
  "West Phone": "services",
};

/* ----------------------------------------------------------
   Commerces à AJOUTER (absents d'OpenStreetMap)
   Même format que data/partenaires.js, sans badge doré.
   ---------------------------------------------------------- */
window.LI_AJOUTS = [
  {
    name: "Bonobo",
    category: "Vêtements",
    kind: "clothes",
    rubrique: "habiller",
    address: "34 rue du Général de Gaulle 27400 Louviers",
    insee: "27375"
  },
  {
    name: "Du Pareil au Même",
    category: "Vêtements enfants",
    kind: "clothes",
    rubrique: "habiller",
    address: "37 rue du Général de Gaulle 27400 Louviers",
    insee: "27375"
  },
  {
    name: "Adopt'",
    category: "Parfumerie, cosmétiques",
    kind: "perfumery",
    rubrique: "beaute",
    address: "40 rue du Matrey 27400 Louviers",
    insee: "27375"
  },
];
