/* ==========================================================
   Agences CV Immobilier et partenaires
   ----------------------------------------------------------
   Ces fiches apparaissent toujours, mises en avant en doré :
   - dans l'annuaire des commerces (rubrique indiquée) ;
   - dans « Mon adresse », si elles sont à moins de 1,5 km.

   Pour AJOUTER un partenaire : copier un bloc { … }, le coller
   avant le « ]; » final et modifier les informations.
   Pour RETIRER un partenaire : supprimer son bloc { … },
   y compris la virgule qui le suit.

   Champs :
     name      Nom affiché
     category  Petite ligne au-dessus du nom (type d'activité)
     badge     Mention dorée : « Éditeur du guide », « Partenaire »…
               (laisser "" pour une fiche simple, sans encadré doré)
     rubrique  Rubrique de l'annuaire : immobilier, financement, notaires,
               ou une rubrique existante (restaurer, bouche…)
     address   Adresse complète (la position est trouvée seule)
     insee     Code de la commune : Louviers 27375,
               Saint-Pierre-du-Vauvray 27598, Le Vaudreuil 27528,
               Val-de-Reuil 27701, Incarville 27351,
               Pont-de-l'Arche 27469, Acquigny 27003, Andé 27015
     phone     Téléphone
     web       Site internet
     links     (facultatif) boutons : [{ label: "…", url: "…" }]
   ========================================================== */
window.LI_PARTENAIRES = [
  {
    name: "CV Immobilier — Louviers",
    category: "Agence immobilière",
    badge: "Éditeur du guide",
    rubrique: "immobilier",
    address: "27 rue du Général de Gaulle 27400 Louviers",
    insee: "27375",
    phone: "02 32 40 22 28",
    web: "https://www.cvimmobilier.fr/",
    links: [
      { label: "Faire estimer un bien", url: "https://www.cvimmobilier.fr/estimation" },
      { label: "L’équipe", url: "a-propos.html" }
    ]
  },
  {
    name: "CV Immobilier — Saint-Pierre-du-Vauvray",
    category: "Agence immobilière",
    badge: "Éditeur du guide",
    rubrique: "immobilier",
    address: "15 Grande Rue 27430 Saint-Pierre-du-Vauvray",
    insee: "27598",
    phone: "02 79 49 21 71",
    web: "https://www.cvimmobilier.fr/",
    links: [
      { label: "Faire estimer un bien", url: "https://www.cvimmobilier.fr/estimation" },
      { label: "L’équipe", url: "a-propos.html" }
    ]
  },
  {
    name: "La Centrale de Financement Louviers",
    category: "Courtier en crédit immobilier",
    badge: "Partenaire",
    rubrique: "financement",
    address: "4 place de la Porte de l'Eau 27400 Louviers",
    insee: "27375",
    phone: "02 79 09 00 00",
    web: "https://www.lacentraledefinancement.fr/"
  },
  {
    name: "Meilleurtaux Louviers",
    category: "Courtier en crédit immobilier",
    badge: "Partenaire",
    rubrique: "financement",
    address: "52 place du Parvis Notre-Dame 27400 Louviers",
    insee: "27375",
    phone: "02 79 06 02 80",
    web: "https://www.meilleurtaux.com/"
  },
  {
    name: "Office notarial Pelfrene & Potentier",
    category: "Notaires · Me Stéphane Pelfrene, Me Thibault Potentier",
    badge: "",
    rubrique: "notaires",
    address: "26 rue du Maréchal Foch 27400 Louviers",
    insee: "27375",
    phone: "02 32 40 17 91",
    web: "https://potentier-pelfrene-louviers.notaires.fr/"
  },
  {
    name: "Office notarial Legros & Bricnet",
    category: "Notaires · Me Yann Legros",
    badge: "",
    rubrique: "notaires",
    address: "1 square Albert 1er 27400 Louviers",
    insee: "27375",
    phone: "02 32 40 00 58",
    web: "https://legros-bricnet-louviers.notaires.fr/"
  },
  {
    name: "Office notarial Paty, Pelletier, Cherif & Erkul",
    category: "Notaires · Me Olfa Cherif, Me Zeynep Erkul",
    badge: "",
    rubrique: "notaires",
    address: "33 bis boulevard de Crosne 27400 Louviers",
    insee: "27375",
    phone: "02 32 40 22 16",
    web: "https://blot-chartier-louviers.notaires.fr/"
  }
];
