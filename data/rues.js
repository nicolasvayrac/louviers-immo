/* ==========================================================
   Histoires de rues de Louviers
   ----------------------------------------------------------
   Apparaissent sur « Mon adresse » quand l'adresse tapée est
   dans l'une de ces rues. N'écrire que des faits sourcés :
   citation exacte entre guillemets et source indiquée.

   Champs :
     nom      Nom de la voie, tel qu'écrit dans les adresses
     aliases  Autres écritures (facultatif)
     texte    Citation exacte de la source
     source   D'où vient la citation
     voir     (facultatif) ce qu'on peut voir en passant
   ========================================================== */
window.LI_RUES_SOURCE_OT = 'Office de tourisme Seine-Eure, circuit « Louviers, cité drapière »';
window.LI_RUES = [
  {
    nom: 'Rue du Quai',
    texte: 'Elle conduisait aux quais du bassin de Bigards, port principal, d’où son nom. Au n°18, on découvre une très belle manufacture du XVIIIe siècle.',
    source: window.LI_RUES_SOURCE_OT,
    voir: ['La manufacture du XVIIIe siècle, au n°18']
  },
  {
    nom: 'Rue Ternaux',
    texte: 'Du nom d’un célèbre manufacturier du début du XIXe siècle, propriétaire de nombreux ateliers à Louviers et à Sedan, cette rue était à l’origine celle des tanneurs, puis des tisseurs.',
    source: window.LI_RUES_SOURCE_OT
  },
  {
    nom: 'Rue des Grands Carreaux',
    texte: 'Cette rue […] doit son nom aux grandes dalles faisant autrefois office de pavage.',
    source: window.LI_RUES_SOURCE_OT
  },
  {
    nom: 'Place de la Halle aux Drapiers',
    aliases: ['Place de la Halle'],
    texte: 'La place de la Halle, occupée autrefois par l’église Saint-Martin et la Halle aux Drapiers, devenue place du marché hebdomadaire.',
    source: window.LI_RUES_SOURCE_OT
  },
  {
    nom: 'Place du Pilori',
    texte: 'La place du Pilori, où l’on pratiquait jadis les exécutions publiques.',
    source: window.LI_RUES_SOURCE_OT
  }
];
