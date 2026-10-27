# Encargo: tradução para o português do Brasil – Wallace D. Wattles, Obras Reunidas

Pasta de trabalho: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/
- Texto-fonte autorizado (inglês, revisado e conferido com os fac-símiles): `eng/<obra>.md`
- Saída: `por/parts/<arquivo indicado no seu encargo>.md`
- Ferramentas auxiliares: crie-as SOMENTE numa subpasta nova e própria de /tmp/claude-0/-home-user/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/

Objetivo: uma tradução completa, fiel e pronta para impressão, num português do Brasil impecável, culto e natural
(Novo Acordo Ortográfico, norma-padrão brasileira). Nada de resumos nem omissões: CADA parágrafo, cada frase.

## Método
1. Traduza seção por seção (`## `) e PARÁGRAFO POR PARÁGRAFO. A sequência de parágrafos deve coincidir exatamente com a
   do inglês (mesmo número de parágrafos por capítulo). Grave o arquivo em etapas se for longo (por exemplo, capítulo a
   capítulo, acrescentando ao arquivo), para não perder trabalho.
2. Ao terminar, releia o arquivo inteiro de corrido e corrija ortografia, gramática, pontuação e estilo.
3. Verifique: `python3 check_pt.py eng/<obra>.md por/parts/<arquivo>.md <primeiro_índice> <último_índice>`
   (os índices de capítulo do seu encargo, começando em 0). Deve dar `problems: 0`. A proporção de palavras é só um
   indício de omissões: NUNCA alongue o texto para aumentá-la; o que importa é que nada falte e que o português seja natural.
4. Relatório breve: capítulos, palavras, decisões e passagens duvidosas.

## Regras comuns (OBRIGATÓRIAS para o livro inteiro)
- Tratamento do leitor: **você** (plural: vocês), como é usual nos livros de desenvolvimento pessoal no Brasil.
  Exceções: diálogos do romance (ver encargo) e citações bíblicas (vós).
- Pronomes referentes a Deus e a Jesus em **minúscula** (ele, seu, lhe).
- Citações bíblicas: no estilo da tradução clássica de **João Ferreira de Almeida** (Revista e Corrigida antiga, domínio
  público), ajustadas à redação que Wattles cita.
- «man»/«men» genérico: «o homem», «os homens» ou «o ser humano», conforme o contexto; não neutralize sistematicamente.

### Glossário fixo
| inglês | português |
|---|---|
| Right Way | a Maneira Correta (para não confundir com «a Certa Maneira») |
| Certain Way / a Certain Way | a Certa Maneira / de uma Certa Maneira (com maiúsculas, como no original) |
| formless substance / Formless Stuff | substância sem forma / matéria sem forma (com maiúsculas onde o original as tem) |
| Thinking Substance / thinking stuff | Substância Pensante / matéria pensante |
| Original Substance / Intelligent Substance | Substância Original / Substância Inteligente |
| the Formless | a Substância sem Forma |
| increase | crescimento (the impression of increase = a impressão de crescimento) |
| use value / cash value | valor de uso / valor monetário |
| creative plane / competitive plane | plano criativo / plano competitivo |
| competitive mind / creative mind | mentalidade competitiva / mentalidade criativa |
| the Advancing Man / advancing | o homem que avança / que avança |
| Principle of Health / of Life / of Power | Princípio da Saúde / Princípio da Vida / Princípio do Poder |
| New Thought | Novo Pensamento |
| mind / spirit | mente / espírito (spiritual = espiritual) |
| the Supreme / Intelligence | o Supremo / Inteligência |
| supply / Formless Supply | a provisão / a Provisão sem Forma |
| All-Mind / All-Health / All-Power | a Mente Total / a Saúde Total / Todo o Poder |
| Living Substance / the Living One | Substância Viva / o Vivente |
| work-power / vital power | poder de trabalho / poder vital |
| will / faith / gratitude / purpose | vontade / fé / gratidão / propósito |
| Mental Science / Christian Science | Ciência Mental / Ciência Cristã |

Credo de *A Ciência de Ficar Rico* (use-o literalmente onde Wattles o repete):
- Existe uma matéria pensante da qual todas as coisas são feitas e que, em seu estado original, permeia, penetra e preenche os interstícios do universo.
- Um pensamento, nessa substância, produz a coisa cuja imagem é formada pelo pensamento.
- O homem pode formar coisas em seu pensamento e, imprimindo seu pensamento na substância sem forma, pode fazer com que seja criada a coisa em que pensa.

### Títulos das obras (também quando citados no texto, em itálico)
- The Science of Getting Rich → *A Ciência de Ficar Rico*
- The Science of Being Well → *A Ciência de Ser Saudável*
- The Science of Being Great → *A Ciência de Ser Grande*
- How to Get What You Want → *Como Conseguir o que Você Quer*
- Making the Man Who Can → *Formando o Homem que Pode*
- The New Science of Living and Healing → *A Nova Ciência de Viver e Curar*
- What Is Truth? → *O que É a Verdade?*
- A New Christ → *Um Novo Cristo*
- Jesus: The Man and His Work → *Jesus: o Homem e Sua Obra*
- Hell-Fire Harrison → *Harrison, o Infernal* (o apelido do protagonista é sempre «Harrison, o Infernal»;
  the Hell-Fire Club = o Clube do Fogo do Inferno)
- The Nautilus: fica em inglês, em itálico.
- Quando o texto fala da ciência em si (não do livro): «a ciência de ficar rico», sem itálico.

### Tipografia (padrão brasileiro)
- Aspas: “…”; dentro delas ‘…’. Nunca aspas retas " '. Não use « » nem „ “.
- Travessão (—) para incisos: «texto — inciso — texto», com espaços. No ROMANCE, os diálogos vão com travessão,
  segundo a norma brasileira: — Bom dia — disse Harrison. — Como vai o senhor?
- Reticências com o caractere … ; números e datas conforme a norma.
- Itálicos do original: *itálico*. Palavras em VERSAIS usadas como ênfase podem ir em itálico.

### Formato (igual a eng/)
- `## <título do capítulo em português>` sem número, com inicial maiúscula só na primeira palavra e nos nomes próprios.
  Prefácio do autor: `## Prefácio`. Prefácio de 1905 de *Jesus*: `## Prefácio dos editores (1905)`. Capítulos do
  romance: `## Capítulo um` … `## Capítulo oito`.
- Parágrafos separados por uma linha em branco; `> ` citações em bloco (linha de fonte: `> — Autor`); `| ` versos;
  `### ` subtítulos; `%% ` linhas de sumário sob os títulos (como em eng/); notas de rodapé como em eng/ (¹ sobrescrito
  no texto e linha `~~ ¹ …` no fim do capítulo); `^^` e `=>` como em eng/ se aparecerem.
- Nenhum capítulo «About This Work», nenhuma nota do tradutor.
