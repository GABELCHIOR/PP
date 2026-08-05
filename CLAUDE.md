# PP_estudo — Montgomery, Design and Analysis of Experiments (9ª ed.)

Projeto de estudo autodidata de Delineamento e Análise de Experimentos (DOE).
Toda a produção é **em português (pt-BR)**.

## O livro

- Arquivo: `DesignandAnalysisofExperiments9thEditionPDFDrive.pdf` (107 MB, 749 páginas)
- Montgomery, D. C. — *Design and Analysis of Experiments*, 9ª edição, Wiley, 2017
- **Versão completa e verificada**: 15 capítulos + Apêndice (Tabelas I–VII) + Bibliografia + Índice
- Gerado em LaTeX/hyperref: **camada de texto íntegra**, extração limpa, sem necessidade de OCR
- **Offset de página: página do PDF = página do livro + 15**
  (ex.: seção 3.3 na p.69 do livro está na p.84 do PDF)

Uma versão anterior e incompleta (8 MB, 629 pág., sem os cap. 10, 12, 15 nem o apêndice)
foi substituída por esta. Se aparecer um PDF pequeno na pasta de novo, é a versão errada.

## Preferências de estudo definidas

| Item | Decisão |
|---|---|
| Objetivo | Autodidata, base sólida. Percurso **linear do cap. 1 ao 15**, sem prazo. Ênfase em entender a lógica por trás de cada delineamento, não em decorar receita. |
| Software | **R**. Incluir código dos exemplos com `agricolae`, `FrF2`, `rsm`, `lme4`, `car`. |
| Formato | **Arquivos HTML locais** em `estudo/`. Offline, abertos direto no navegador. Matemática em **MathML nativo** (sem CDN, sem JS). |
| Idioma | Português (pt-BR). Termos técnicos com o original em inglês entre parênteses na primeira ocorrência. |

## Como trabalhar aqui

**Geração sob demanda, seção por seção.** Não converter o livro inteiro — a cada sessão o
usuário escolhe uma seção e eu gero uma página de estudo focada.

Cada página de estudo contém, nesta ordem:

1. **Objetivo da seção** — o que se deve saber fazer ao final
2. **Conceito** em português, com a derivação matemática em MathML
3. **Figuras e tabelas** recortadas do PDF (`ferramentas/extrair.py recorte`)
4. **Exemplo do livro resolvido passo a passo**, com o código em R e a saída comentada
5. **Cartões de recall ativo** — pergunta com resposta escondida (`<details>`)
6. **Exercícios selecionados** do fim do capítulo, com gabarito comentado

**Tom das aulas:** professor dando aula, não resumo. O usuário está aprendendo a matéria
do zero — explicar o *porquê* de cada resultado, mostrar as derivações, antecipar as
armadilhas profissionais e ligar cada conceito a onde ele reaparece nos capítulos seguintes.
Nunca comprimir a ponto de virar lista de fórmulas.

**Regra dos números:** todo resultado numérico das resoluções deve ser *calculado*
(scipy/numpy no scratchpad), nunca copiado de memória. Conferir contra o livro quando houver.

## Ferramentas

`ferramentas/extrair.py` — localiza o PDF sozinho (por tamanho, na raiz da pasta).
`ferramentas/figuras.py` — detecta e recorta figuras automaticamente (agrupa desenhos
vetoriais + rótulos de texto, excluindo a legenda "F I G U R E"/"T A B L E").

```bash
python ferramentas/figuras.py listar 84          # candidatos a figura na página
python ferramentas/figuras.py salvar 84 fig.png  # salva o maior candidato
```

```bash
python ferramentas/extrair.py texto --livro 69 78      # texto pela numeração do livro
python ferramentas/extrair.py texto 84 93              # texto pela numeração do PDF
python ferramentas/extrair.py pagina 84 out.png        # página inteira em PNG 200dpi
python ferramentas/extrair.py recorte 84 100 200 500 400 fig.png   # recorte 300dpi
python ferramentas/extrair.py imagens 84 pasta/        # imagens embutidas
python ferramentas/extrair.py buscar "Latin square"    # localiza um termo
```

Dependências: `pymupdf` (instalado), `pypdf`, `pdfplumber`. Python 3.13.9.

**R não está instalado no PATH.** O código em R vai nas páginas de estudo para leitura e
execução manual pelo usuário; não tente rodá-lo aqui sem antes verificar `Rscript`.

## Convenção de nomes

Tudo ordena alfabeticamente na ordem do livro e o nome do arquivo sozinho já diz de
onde veio. **Números sempre com dois dígitos**, minúsculas, sem acento, hífen entre
palavras.

| O quê | Padrão | Exemplo |
|---|---|---|
| Pasta do capítulo | `capNN/` | `cap03/` |
| Página de uma seção | `NN-SS-titulo-kebab.html` | `cap03/03-02-analise-variancia.html` |
| Página do capítulo inteiro | `NN-00-titulo.html` (`00` = visão geral) | `cap01/01-00-introducao.html` |
| Figura | `img/fig-NN-MM.png` | `cap03/img/fig-03-01.png` |
| Tabela recortada | `img/tab-NN-MM.png` | `cap03/img/tab-03-04.png` |

Ao criar uma aula nova, acrescentar o link em **três** lugares de `estudo/index.html`:
a lista da aba lateral, o cartão em "Aulas disponíveis" e a linha da tabela do percurso.
E acertar o `.nav-rodape` (anterior/próxima) da aula vizinha.

## Layout das páginas

O CSS está separado em dois arquivos e essa separação é para valer:

- `estudo/assets/tema.css` — **única** fonte de cores, fontes e medidas, tudo em
  variáveis CSS, com bloco `@media (prefers-color-scheme: dark)`. É o arquivo que o
  usuário vai trocar quando mudar de tema.
- `estudo/assets/estilo.css` — só estrutura. **Nunca escrever cor literal aqui**,
  sempre `var(--…)`. Precisa de uma cor nova? Declare-a em `tema.css` (nos dois modos)
  e use a variável. Única exceção tolerada: o `@media print`, que força fundo branco.

O `<head>` de toda página de aula é este — os dois CSS nesta ordem, e o `noindex`
obrigatório (o site é público no GitHub Pages, mas as figuras são do livro):

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Cap. N — Título</title>
<link rel="stylesheet" href="../assets/tema.css?v=3">
<link rel="stylesheet" href="../assets/estilo.css?v=3">
```

`estilo.css` define uma **grade de quebra de coluna**. A prosa fica numa coluna
de 46rem (`--largura-leitura`, leitura confortável), e estes elementos avançam para as
bordas quando são filhos diretos de `.pagina`:

`.topo` · `figure` · `.rolagem` (tabelas) · `pre` · `.cartoes` · `.exercicio` · `.nav-rodape`

Os nomes das linhas da grade **precisam** terminar em `-start`/`-end` — só assim o atalho
`grid-column: texto` resolve. (Já quebrou uma vez por usar `-inicio`/`-fim`.)

Dentro de `.exercicio` há a mesma grade em miniatura: prosa e equações na coluna de
leitura, `pre` e `.rolagem` ocupando a caixa inteira.

Toda página tem uma **aba lateral fixa** (`<details class="menu-lateral">`) logo depois
de `<body>`, com o índice das seções. É `<details>` puro — funciona sem JavaScript; o
script no fim do arquivo só fecha o painel ao clicar num link. A coluna esquerda da grade
reserva 3.25rem para a aba não cobrir o texto.

Ao editar qualquer um dos dois CSS, **incrementar o `?v=` nos dois `<link>` de todas as
páginas**, senão o navegador serve a versão em cache. Estão em `?v=3`.

## Estrutura

```
PP_estudo/
├── DesignandAnalysisofExperiments9thEditionPDFDrive.pdf   (fora do git: .gitignore)
├── index.html              redireciona para estudo/ — serve ao GitHub Pages
├── README.md               documentação pública do repositório
├── CLAUDE.md               este arquivo
├── .gitignore  .gitattributes
├── ferramentas/
│   ├── extrair.py
│   └── figuras.py
└── estudo/
    ├── index.html          painel com o percurso e o progresso
    ├── assets/
    │   ├── tema.css        cores, fontes, medidas
    │   └── estilo.css      estrutura e layout
    └── capNN/
        ├── NN-SS-secao.html
        └── img/fig-NN-MM.png
```

O repositório é git desde 2026-08-05, pensado para ir ao GitHub. O PDF (107 MB) está no
`.gitignore` — passa do limite de 100 MB por arquivo do GitHub e é material com direitos
autorais. Ao mudar a estrutura, atualizar `README.md` **e** este arquivo.

## Progresso

**Capítulos 1 e 2 prontos** (gerados em 2026-08-05). Próximo: capítulo 3 (ANOVA).

Ao gerar o cap. 3, retomar os ganchos já plantados nas aulas anteriores:
o problema das comparações múltiplas (por que não fazer vários testes *t* dois a dois),
`SQ/σ² ~ χ²` como base da decomposição, e a contagem de graus de liberdade por restrições.

| Cap. | Título | Livro p. | PDF p. | Status |
|---|---|---|---|---|
| 1 | Introduction | 1 | 16 | ✅ `estudo/cap01/01-00-introducao.html` |
| 2 | Simple Comparative Experiments | 23 | 38 | ✅ `estudo/cap02/02-00-experimentos-comparativos.html` |
| 3 | Experiments with a Single Factor: ANOVA | 65 | 80 | — |
| 4 | Randomized Blocks, Latin Squares | 135 | 150 | — |
| 5 | Introduction to Factorial Designs | 179 | 194 | — |
| 6 | The 2^k Factorial Design | 230 | 245 | — |
| 7 | Blocking and Confounding in the 2^k | 308 | 323 | — |
| 8 | Two-Level Fractional Factorial Designs | 328 | 343 | — |
| 9 | Additional Topics for Factorial Designs | 406 | 421 | — |
| 10 | Fitting Regression Models | 460 | 475 | — |
| 11 | Response Surface Methods and Designs | 489 | 504 | — |
| 12 | Robust Parameter Design | 569 | 584 | — |
| 13 | Experiments with Random Factors | 589 | 604 | — |
| 14 | Nested and Split-Plot Designs | 618 | 633 | — |
| 15 | Other Design and Analysis Topics | 657 | 672 | — |
| — | Apêndice (Tabelas I–VII) | 697 | 712 | — |
