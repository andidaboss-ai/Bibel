# Encargo: traducción al español – Wallace D. Wattles, Obras reunidas

Carpeta de trabajo: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/
- Texto fuente autorizado (inglés, depurado y cotejado con los facsímiles): `eng/<obra>.md`
- Salida: `spa/parts/<archivo indicado en tu encargo>.md`
- Herramientas auxiliares: créalas SOLO en una subcarpeta nueva y propia de /tmp/claude-0/-home-user/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/

Objetivo: una traducción completa, fiel y lista para imprenta, en un español impecable, culto y natural (norma RAE,
español neutro, comprensible en España y en América). Nada de resúmenes ni omisiones: CADA párrafo, cada frase.

## Método
1. Traduce sección por sección (`## `) y PÁRRAFO POR PÁRRAFO. La secuencia de párrafos debe coincidir exactamente con
   la del inglés (mismo número de párrafos por capítulo). Escribe el archivo por tramos si es largo (p. ej. capítulo a
   capítulo, añadiendo al archivo), para no perder trabajo.
2. Al terminar, relee todo el archivo de corrido y corrige ortografía, gramática, puntuación y estilo.
3. Comprueba: `python3 check_es.py eng/<obra>.md spa/parts/<archivo>.md <primer_índice> <último_índice>`
   (los índices de capítulo de tu encargo, empezando en 0). Debe dar `problems: 0`. La ratio de palabras es solo un indicio de omisiones: NUNCA alargue el texto para subirla; lo que cuenta es que no falte nada y que el español sea natural.
4. Informe breve: capítulos, palabras, decisiones y pasajes dudosos.

## Reglas comunes (OBLIGATORIAS para todo el libro)
- Tratamiento al lector: **usted** (plural: ustedes). Excepciones: diálogos de la novela, citas bíblicas (vosotros, como
  en la Reina-Valera).
- Pronombres referidos a Dios y a Jesús en **minúscula** (él, su, le), como en la Reina-Valera 1909.
- Citas bíblicas: seguir el tenor de la **Reina-Valera 1909** (dominio público), ajustado a la redacción que cita Wattles.
- Wattles escribe «man»/«men» en sentido genérico: tradúzcalo como «el hombre», «los hombres» o «el ser humano» según
  el contexto; no lo neutralice sistemáticamente.

### Glosario fijo
| inglés | español |
|---|---|
| Certain Way / a Certain Way | la Cierta Manera / de una Cierta Manera (con mayúsculas, como en el original) |
| formless substance / Formless Stuff | sustancia sin forma / materia sin forma |
| Thinking Substance / thinking stuff | Sustancia Pensante / materia pensante |
| Original Substance | Sustancia Original |
| increase | incremento (the impression of increase = la impresión de incremento) |
| use value / cash value | valor de uso / valor monetario |
| creative plane / competitive plane | plano creativo / plano competitivo |
| competitive mind / creative mind | mentalidad competitiva / mentalidad creativa |
| the Advancing Man / advancing | el hombre que avanza / que avanza |
| Principle of Health / of Life / of Power | Principio de Salud / Principio de Vida / Principio de Poder |
| New Thought | Nuevo Pensamiento |
| mind / spirit | mente / espíritu (spiritual = espiritual) |
| the Supreme / Intelligence | el Supremo / Inteligencia |
| will / faith / gratitude / purpose | voluntad / fe / gratitud / propósito |
| Mental Science / Christian Science | Ciencia Mental / Ciencia Cristiana |
| supply / Formless Supply | la provisión / la Provisión sin Forma |
| Formless Substance / Formless Stuff (con mayúscula) / the Formless | Sustancia sin Forma / Materia sin Forma / la Sustancia sin Forma |
| It (referido a la Sustancia, con mayúscula en el original) | Ella |

Credo de *La ciencia de hacerse rico* (fijado; úselo literalmente donde Wattles lo cite):
- Hay una materia pensante de la que están hechas todas las cosas y que, en su estado original, impregna, penetra y llena los intersticios del universo.
- Un pensamiento, en esta sustancia, produce la cosa cuya imagen se forma en el pensamiento.
- El hombre puede formar cosas en su pensamiento y, al imprimir su pensamiento en la sustancia sin forma, puede hacer que se cree la cosa en que piensa.

### Títulos de las obras (también cuando se citan dentro del texto, en cursiva)
- The Science of Getting Rich → *La ciencia de hacerse rico*
- The Science of Being Well → *La ciencia de estar bien*
- The Science of Being Great → *La ciencia de ser grande*
- How to Get What You Want → *Cómo conseguir lo que se desea*
- Making the Man Who Can → *Formar al hombre que puede*
- The New Science of Living and Healing → *La nueva ciencia de vivir y sanar*
- What Is Truth? → *¿Qué es la verdad?*
- A New Christ → *Un nuevo Cristo*
- Jesus: The Man and His Work → *Jesús: el hombre y su obra*
- Hell-Fire Harrison → *Harrison el Infernal* (el apodo del protagonista es siempre «Harrison el Infernal»;
  the Hell-Fire Club = el Club del Fuego Infernal)
- The Nautilus: se deja en inglés, en cursiva.

### Tipografía
- Comillas: «…»; dentro de ellas “…”, y dentro de estas ‘…’. Nunca comillas rectas " '.
- Signos de apertura ¿ ¡ siempre.
- Raya (—) para incisos, pegada al inciso: «texto —inciso— texto». En la NOVELA los diálogos van con raya, según la
  norma española: —Buenos días —dijo Harrison—. ¿Cómo está usted?
- Puntos suspensivos con el carácter … ; números y fechas según la RAE.
- Cursivas del original: *cursiva*. Palabras en VERSALES usadas como énfasis pueden ir en cursiva.

### Formato (igual que eng/)
- `## <título del capítulo en español>` sin número. Prefacio del autor: `## Prefacio`. Prólogo de 1905 de *Jesús*:
  `## Prólogo de los editores (1905)`. Capítulos de la novela: `## Capítulo primero` … `## Capítulo octavo`.
- Párrafos separados por una línea en blanco; `> ` citas en bloque (línea de fuente: `> — Autor`); `| ` versos;
  `### ` subtítulos; `%% ` líneas de sumario bajo los títulos (como en eng/); notas al pie como en eng/ (¹ voladita en
  el texto y línea `~~ ¹ …` al final del capítulo); `^^` y `=>` como en eng/ si aparecen.
- Ningún capítulo «About This Work», ninguna nota del traductor.
