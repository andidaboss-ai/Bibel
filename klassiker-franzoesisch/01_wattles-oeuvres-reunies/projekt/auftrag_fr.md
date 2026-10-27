# Mission : traduction française – Wallace D. Wattles, Œuvres réunies

Dossier de travail : /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/
- Texte source de référence (anglais, révisé et collationné sur les fac-similés) : `eng/<œuvre>.md`
- Sortie : `fra/parts/<fichier indiqué dans votre mission>.md`
- Outils auxiliaires : créez-les UNIQUEMENT dans un nouveau sous-dossier à vous de /tmp/claude-0/-home-user/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/

Objectif : une traduction intégrale, fidèle et prête pour l'impression, dans un français impeccable, soutenu et naturel
(orthographe de référence : Le Robert / Larousse ; rectifications de 1990 non obligatoires, mais soyez cohérent).
Ni résumé ni omission : CHAQUE paragraphe, chaque phrase.

## Méthode
1. Traduisez section par section (`## `) et PARAGRAPHE PAR PARAGRAPHE. La suite des paragraphes doit correspondre
   exactement à l'anglais (même nombre de paragraphes par chapitre). Enregistrez le fichier par étapes s'il est long
   (chapitre par chapitre, en ajoutant au fichier), pour ne rien perdre.
2. À la fin, relisez tout le fichier d'une traite et corrigez orthographe, grammaire, accords, ponctuation et style.
3. Vérifiez : `python3 check_fr.py eng/<œuvre>.md fra/parts/<fichier>.md <premier_indice> <dernier_indice>`
   (les indices de chapitre de votre mission, à partir de 0). Résultat attendu : `problems: 0`. Le rapport de mots
   n'est qu'un indice d'omission : n'allongez JAMAIS le texte pour l'augmenter.
4. Rapport bref : chapitres, nombre de mots, décisions et passages douteux.

## Règles communes (OBLIGATOIRES pour tout le livre)
- On s'adresse au lecteur par **vous**. Exceptions : dialogues du roman (voir mission) et citations bibliques
  (tutoiement de Dieu, vouvoiement collectif « vous » comme chez Segond).
- Pronoms se rapportant à Dieu et à Jésus en **minuscule** (il, lui, son).
- Citations bibliques : dans le style de la **Bible Louis Segond 1910** (domaine public), ajustées à la formulation que
  cite Wattles. Références au format « Jean 10.30 », « Marc 11.23-24 ».
- « man »/« men » au sens générique : « l'homme », « les hommes » ou « l'être humain » selon le contexte ; pas de
  neutralisation systématique.

### Glossaire fixe
| anglais | français |
|---|---|
| Certain Way / a Certain Way | la Certaine Manière / d'une Certaine Manière (avec majuscules, comme dans l'original) |
| Right Way | la Juste Manière (pour ne pas la confondre avec la Certaine Manière) |
| formless substance / Formless Stuff / the Formless | substance informe / matière informe / la Substance informe (majuscule là où l'original en a) |
| Thinking Substance / thinking stuff | Substance Pensante / matière pensante |
| Original Substance / Intelligent Substance | Substance Originelle / Substance Intelligente |
| Living Substance / the Living One | Substance Vivante / le Vivant |
| increase | accroissement (the impression of increase = l'impression d'accroissement) |
| use value / cash value | valeur d'usage / valeur marchande |
| creative plane / competitive plane | plan créatif / plan compétitif |
| competitive mind / creative mind | mentalité compétitive / mentalité créatrice |
| the Advancing Man / advancing | l'homme qui progresse / qui progresse |
| Principle of Health / of Life / of Power | Principe de Santé / Principe de Vie / Principe de Puissance |
| New Thought | Nouvelle Pensée |
| mind / spirit | esprit ou mental selon le contexte / Esprit (spiritual = spirituel) |
| All-Mind / All-Health / All-Power | l'Esprit Total / la Santé Totale / la Toute-Puissance |
| the Supreme / Intelligence | le Suprême / Intelligence |
| supply / Formless Supply | la provision / la Provision informe |
| work-power / vital power / vital energy | puissance de travail / puissance vitale / énergie vitale |
| will / faith / gratitude / purpose | volonté / foi / gratitude / intention ferme (PURPOSE = INTENTION) |
| Mental Science / Christian Science | Science mentale / Science chrétienne |

Credo de *La Science de l'enrichissement* (à reprendre mot pour mot là où Wattles le répète) :
- Il existe une matière pensante dont toutes choses sont faites et qui, dans son état originel, imprègne, pénètre et remplit les interstices de l'univers.
- Une pensée, dans cette substance, produit la chose dont l'image est formée par la pensée.
- L'homme peut former des choses dans sa pensée et, en imprimant sa pensée sur la substance informe, peut faire que soit créée la chose à laquelle il pense.

### Titres des œuvres (en italique aussi quand ils sont cités dans le texte)
- The Science of Getting Rich → *La Science de l'enrichissement*
- The Science of Being Well → *La Science de la santé*
- The Science of Being Great → *La Science de la grandeur*
- How to Get What You Want → *Comment obtenir ce que vous voulez*
- Making the Man Who Can → *Former l'homme qui peut*
- The New Science of Living and Healing → *La Nouvelle Science de la vie et de la guérison*
- What Is Truth? → *Qu'est-ce que la vérité ?*
- A New Christ → *Un nouveau Christ*
- Jesus: The Man and His Work → *Jésus : l'homme et son œuvre*
- Hell-Fire Harrison → *Harrison l'Infernal* (le surnom du héros est toujours « Harrison l'Infernal » ;
  the Hell-Fire Club = le Club du Feu de l'Enfer)
- The Nautilus : reste en anglais, en italique.
- Quand le texte parle de la science elle-même (et non du livre) : « la science de l'enrichissement », sans italique.

### Typographie
- Guillemets français « … » ; à l'intérieur, “ … ”. Jamais de guillemets droits " '. Apostrophe typographique ’.
- Écrivez les espaces devant ; : ! ? et à l'intérieur des guillemets comme des espaces NORMALES (« texte », mot ;) :
  elles seront converties automatiquement en espaces insécables. N'oubliez jamais ces espaces.
- Tiret cadratin (—) pour les incises. Dans le ROMAN, dialogues au tiret : — Bonjour, dit Harrison. (une réplique
  peut aussi s'ouvrir par « et continuer au tiret, selon l'usage français).
- Points de suspension avec le caractère … ; majuscules accentuées (À, É, Ç…) ; ligatures œ, Œ, æ.
- Italiques de l'original : *italique*. Les mots en CAPITALES d'insistance peuvent être mis en italique.

### Format (identique à eng/)
- `## <titre du chapitre en français>` sans numéro, majuscule au seul premier mot et aux noms propres. Préface de
  l'auteur : `## Préface`. Préface de 1905 de *Jésus* : `## Préface des éditeurs (1905)`. Chapitres du roman :
  `## Chapitre premier`, `## Chapitre deux` … `## Chapitre huit`.
- Paragraphes séparés par une ligne vide ; `> ` citations en bloc (ligne de source : `> — Auteur`) ; `| ` vers ;
  `### ` intertitres ; `%% ` lignes de sommaire sous les titres (comme dans eng/) ; notes de bas de page comme dans
  eng/ (¹ en exposant dans le texte et ligne `~~ ¹ …` en fin de chapitre) ; `^^` et `=>` comme dans eng/.
- Aucun chapitre « About This Work », aucune note du traducteur.
