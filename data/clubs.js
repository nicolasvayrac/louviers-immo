/* ==========================================================
   Clubs et associations sportives de Louviers
   ----------------------------------------------------------
   Source : annuaire des associations de la Ville de Louviers
   (édition 2024). Les clubs apparaissent dans l'annuaire, rubrique
   « Clubs sportifs », quand la commune choisie est Louviers.

   Pour AJOUTER un club : copier un bloc { … }, le coller avant
   le « ]; » final et modifier les informations.
   Pour RETIRER un club : supprimer son bloc { … } et la virgule
   qui le suit.

   Champs :
     name     Nom du club
     sport    Discipline(s), affichée au-dessus du nom
     lieu     Lieu de pratique, en clair
     address  Adresse du lieu, pour le placer sur la carte
              (laisser "" si le lieu n'a pas d'adresse précise)
     web      Site internet (facultatif)
     email    Adresse mail du club (facultatif)
   ========================================================== */
window.LI_CLUBS = [
  { name: "Louviers Tennis Club", sport: "Tennis", lieu: "5 rue Alexandre Dumas",
    address: "5 rue Alexandre Dumas 27400 Louviers", web: "https://louviers-tennis-club.com/", email: "info@louviers-tennis-club.com" },
  { name: "Louviers Volley-Ball", sport: "Volley-ball", lieu: "Gymnase Maxime Marchand",
    address: "12 avenue du Maréchal Leclerc 27400 Louviers", web: "https://www.louviersvolleyball.com/", email: "louviersvolleyball@gmail.com" },
  { name: "Louviers Pétanque", sport: "Pétanque", lieu: "Rue Roger Salengro",
    address: "rue Roger Salengro 27400 Louviers", web: "", email: "" },
  { name: "Association Sportive Boules Lyonnaises", sport: "Boules lyonnaises", lieu: "Boulodrome, rue du Canal",
    address: "rue du Canal 27400 Louviers", web: "", email: "" },
  { name: "Ice Skating Club Louviers", sport: "Patinage, curling", lieu: "Patinoire Glacéo, 13 rue du Canal",
    address: "13 rue du Canal 27400 Louviers", web: "https://www.iscl-clubpatinage-louviers.fr/", email: "president.iscl@gmail.com" },
  { name: "Loups Hockey'Eure", sport: "Hockey sur glace", lieu: "Patinoire Glacéo, 13 rue du Canal",
    address: "13 rue du Canal 27400 Louviers", web: "", email: "loups.hockey.eure@gmail.com" },
  { name: "Roller Louviers Club", sport: "Roller", lieu: "Le Kolysé",
    address: "avenue François Mitterrand 27400 Louviers", web: "https://www.rollerlouviersclub.fr/", email: "rollerlouviersclub@gmail.com" },
  { name: "Bowling Club Louviers", sport: "Bowling", lieu: "Le Kolysé",
    address: "avenue François Mitterrand 27400 Louviers", web: "", email: "" },
  { name: "Entente Natation Louviers", sport: "Natation, water-polo, natation artistique", lieu: "Complexe aquatique Caséo",
    address: "rue du Canal 27400 Louviers", web: "https://www.enl27.com/", email: "" },
  { name: "AONES Plongée", sport: "Plongée, apnée, nage en eaux vives", lieu: "Piscine Caséo",
    address: "rue du Canal 27400 Louviers", web: "https://aonesplongee.fr/", email: "" },
  { name: "AONES Canoë-Kayak", sport: "Canoë-kayak", lieu: "Pont de Folleville",
    address: "", web: "https://aonescanoekayak.fr/", email: "aonescanoekayak@gmail.com" },
  { name: "AONES Aviron", sport: "Aviron", lieu: "Lac du Mesnil, Poses",
    address: "", web: "https://aonesaviron27.net/", email: "aonesaviron27@gmail.com" },
  { name: "Football Club Seine-Eure", sport: "Football", lieu: "Stade Paul Coudray",
    address: "95 rue Roger Salengro 27400 Louviers", web: "https://football-club-seine-eure.com/", email: "" },
  { name: "U.S. Louviers", sport: "Football", lieu: "Stade Paul Coudray",
    address: "95 rue Roger Salengro 27400 Louviers", web: "", email: "" },
  { name: "Entente Handball Louviers – Val-de-Reuil", sport: "Handball", lieu: "Gymnase Colette Besson",
    address: "15 boulevard Jules Ferry 27400 Louviers", web: "https://evdrlhandball.fr/", email: "evdrlhandball@gmail.com" },
  { name: "Association Louviers Hamelet Basket (ALHBCI)", sport: "Basket-ball", lieu: "Gymnases Colette Besson, Anatole France, Paul Morin et Saint-Louis",
    address: "15 boulevard Jules Ferry 27400 Louviers", web: "https://alhbci.jimdofree.com/", email: "alhbcibasket@gmail.com" },
  { name: "Badminton Louviers – Val-de-Reuil", sport: "Badminton", lieu: "Gymnase Paul Morin",
    address: "rue Georges Guynemer 27400 Louviers", web: "https://bvrl.fr/", email: "" },
  { name: "Wallabies Baseball Club Louviers", sport: "Baseball, softball", lieu: "Parc des sports Annette Sergent",
    address: "sente de la Plaquette 27400 Louviers", web: "https://wallabies.fr/", email: "contact@wallabies.fr" },
  { name: "Étoile Athlétique Lovérienne", sport: "Course sur route, trail, marche nordique", lieu: "Complexe Maxime Marchand et stade Carrington",
    address: "12 avenue du Maréchal Leclerc 27400 Louviers", web: "https://ealouviers.athle.org/", email: "" },
  { name: "Cyclos Touristes Lovériens", sport: "Cyclotourisme", lieu: "Départ parking des Tisserands",
    address: "", web: "https://cyclotourlouviers.sportsregions.fr/", email: "" },
  { name: "Union Vélocipédique de Louviers", sport: "VTT, cyclisme", lieu: "Louviers",
    address: "", web: "https://uvlouviers.wifeo.com/", email: "u.v.louviers@gmail.com" },
  { name: "Cercle d'Escrime Lovérien", sport: "Escrime", lieu: "Gymnase de la Roquette",
    address: "rue du Point du Jour 27400 Louviers", web: "https://www.escrimelouviers.com/", email: "escrimelouviers@gmail.com" },
  { name: "Judo Club Louviers", sport: "Judo, taïso, ju-jitsu", lieu: "Dojo, avenue du Maréchal Leclerc",
    address: "avenue du Maréchal Leclerc 27400 Louviers", web: "", email: "" },
  { name: "Sen Karaté Louviers", sport: "Karaté, body karaté", lieu: "Gymnase Colette Besson",
    address: "15 boulevard Jules Ferry 27400 Louviers", web: "https://www.sen-karate-louviers.fr/", email: "senkaratelouviers@gmail.com" },
  { name: "Aïkido Kobayashi Ryu", sport: "Aïkido", lieu: "Gymnase Colette Besson",
    address: "15 boulevard Jules Ferry 27400 Louviers", web: "https://seine-eure.aikido.fr/", email: "" },
  { name: "Louviers Full Boxing", sport: "Kick-boxing, full contact, muay-thaï", lieu: "9 rue au Coq",
    address: "9 rue au Coq 27400 Louviers", web: "", email: "louviersfullboxing@gmail.com" },
  { name: "Team Vince Art Muay Thaï", sport: "Boxe thaïlandaise", lieu: "Gymnase Maxime Marchand",
    address: "12 avenue du Maréchal Leclerc 27400 Louviers", web: "", email: "team.vince.amt@gmail.com" },
  { name: "Capoeira Biriba Brasil", sport: "Capoeira", lieu: "Maison des sports et gymnase Paul Morin",
    address: "rue Georges Guynemer 27400 Louviers", web: "https://www.biribabrasil.com/", email: "" },
  { name: "Taï Chi Chuan Louviers", sport: "Taï-chi-chuan", lieu: "Gymnase Colette Besson",
    address: "15 boulevard Jules Ferry 27400 Louviers", web: "", email: "taichichuanlouviers@gmail.com" },
  { name: "La Fraternelle Louviers", sport: "Gymnastique", lieu: "Gymnase Maxime Marchand",
    address: "12 avenue du Maréchal Leclerc 27400 Louviers", web: "", email: "lafratlouviers@gmail.com" },
  { name: "Gym Plaisir", sport: "Gymnastique d'entretien", lieu: "Salle des colonnes, mairie de Louviers",
    address: "", web: "", email: "" },
  { name: "Twirling Sportif Louviers", sport: "Twirling bâton", lieu: "Gymnase Maxime Marchand",
    address: "12 avenue du Maréchal Leclerc 27400 Louviers", web: "", email: "twirlinglouviersclub@gmail.com" },
  { name: "Créart'Danses", sport: "Danse, yoga, pilates", lieu: "Le Moulin, rue des Anciens Combattants d'Afrique du Nord",
    address: "rue des Anciens Combattants d'Afrique du Nord 27400 Louviers", web: "https://creartdanses.com/", email: "" },
  { name: "Cirk'ulaire", sport: "École de cirque", lieu: "Gymnase Paul Morin",
    address: "rue Georges Guynemer 27400 Louviers", web: "https://cirkulaire.com/", email: "contact@cirkulaire.com" },
  { name: "Yogaïa", sport: "Yoga", lieu: "Maison des sports et des associations",
    address: "avenue du Maréchal Leclerc 27400 Louviers", web: "https://associationyogaia.blogspot.com/", email: "" },
  { name: "Force Athlétique Lovérienne", sport: "Force athlétique", lieu: "Maison des sports et des associations",
    address: "avenue du Maréchal Leclerc 27400 Louviers", web: "", email: "" },
  { name: "Billard Amical Club Lovérien", sport: "Billard français, snooker", lieu: "3 rue Saint-Jean",
    address: "3 rue Saint-Jean 27400 Louviers", web: "", email: "baclouviers@gmail.com" },
  { name: "Aile Roi Échecs", sport: "Échecs", lieu: "Salle Pierre Quemin",
    address: "", web: "https://www.aileroi-louviers.fr/", email: "" },
  { name: "Sport Impulzz", sport: "Teqball", lieu: "Louviers",
    address: "", web: "", email: "sport.impulzzz@gmail.com" },
  { name: "AAPPMA de Louviers Seine & Eure", sport: "Pêche", lieu: "Rivière l'Eure et étang",
    address: "", web: "https://www.eure-peche.com/aappma", email: "" }
];
