# Delineamento e Análise de Experimentos — caderno de estudo

Aulas em português (pt-BR) sobre **Montgomery, D. C., _Design and Analysis of
Experiments_, 9ª ed., Wiley, 2017**, escritas seção por seção ao longo de um
percurso linear do capítulo 1 ao 15.

Cada página é um **arquivo HTML estático, offline, sem nenhuma dependência
externa** — sem CDN, sem JavaScript de terceiros, sem build. A matemática usa
**MathML nativo**, que os navegadores atuais renderizam sozinhos. Basta abrir o
arquivo no navegador (ou publicar a pasta em qualquer servidor estático).

👉 **Comece por [`estudo/index.html`](estudo/index.html)** — é o painel com o
percurso e o progresso.

## O que tem em cada aula

1. **Objetivo da seção** — o que se deve saber fazer ao final
2. **Conceito** com a derivação matemática completa
3. **Figuras e tabelas** recortadas do livro
4. **Exemplo resolvido passo a passo**, à mão e em R (`agricolae`, `FrF2`,
   `rsm`, `lme4`, `car`)
5. **Cartões de recall ativo** — pergunta com a resposta escondida
6. **Exercícios do fim do capítulo** com gabarito comentado

## Estrutura

```
PP_estudo/
├── index.html              redireciona para estudo/ (serve ao GitHub Pages)
├── README.md
├── CLAUDE.md               instruções de trabalho do projeto
├── .gitignore              o PDF do livro fica de fora — ver abaixo
├── ferramentas/
│   ├── extrair.py          texto, páginas e recortes do PDF
│   └── figuras.py          detecta e recorta figuras automaticamente
└── estudo/
    ├── index.html          painel: percurso, aulas prontas, progresso
    ├── assets/
    │   ├── tema.css        cores, fontes e medidas  ← mexa aqui para trocar o visual
    │   └── estilo.css      estrutura e layout       ← não contém cor literal
    ├── cap01/
    │   ├── 01-00-introducao.html
    │   └── img/fig-01-01.png …
    └── cap02/
        ├── 02-00-experimentos-comparativos.html
        └── img/fig-02-01.png …
```

### Convenção de nomes

Pensada para continuar legível com dezenas de arquivos — tudo ordena
alfabeticamente na ordem do livro, e o nome do arquivo sozinho já diz de onde
ele veio (útil na aba do editor e na busca por nome).

| O quê | Padrão | Exemplo |
|---|---|---|
| Pasta do capítulo | `capNN/` | `cap03/` |
| Página de uma seção | `NN-SS-titulo-em-kebab-case.html` | `cap03/03-02-analise-variancia.html` |
| Página do capítulo inteiro | `NN-00-titulo.html` (seção `00` = visão geral) | `cap01/01-00-introducao.html` |
| Figura | `img/fig-NN-MM.png` | `cap03/img/fig-03-01.png` |
| Tabela recortada | `img/tab-NN-MM.png` | `cap03/img/tab-03-04.png` |

Regras: números **sempre com dois dígitos** (`03`, não `3`) — senão o capítulo
10 aparece antes do 2 na listagem; tudo em **minúsculas, sem acento e sem
espaço**, com hífen separando palavras — nomes assim sobrevivem a qualquer
sistema de arquivos e viram URL sem escape.

## Trocando o tema

O CSS está separado em dois arquivos com responsabilidades que não se
misturam:

- **`estudo/assets/tema.css`** — a única fonte de cores, fontes e medidas.
  Declara tudo como variáveis CSS (`--realce`, `--serif`,
  `--largura-leitura`…), com um bloco `@media (prefers-color-scheme: dark)`
  para o modo escuro.
- **`estudo/assets/estilo.css`** — só estrutura: grade, espaçamentos,
  componentes. **Nenhuma cor literal**, apenas `var(--…)`.

Para um tema novo, copie `tema.css` para `assets/temas/<nome>.css`, mude os
valores e troque o `href` do primeiro `<link>` das páginas. `estilo.css`
continua idêntico.

> ⚠️ Ao editar qualquer um dos dois, **incremente o `?v=` nos dois `<link>`
> de todas as páginas** — o navegador serve a versão em cache caso contrário.
> Hoje as páginas estão em `?v=3`.

## O PDF do livro não está aqui

O arquivo tem 107 MB — acima do limite de 100 MB por arquivo do GitHub — e é
obra protegida por direitos autorais. Ele está no `.gitignore` (`*.pdf`).

Para usar as ferramentas de extração, coloque a sua própria cópia do PDF na
raiz da pasta: `ferramentas/extrair.py` o localiza sozinho, pelo tamanho.
As figuras já recortadas que estão versionadas são reproduções pontuais do
original, para fins de estudo pessoal.

**Offset de página: página do PDF = página do livro + 15.**

```bash
python ferramentas/extrair.py texto --livro 69 78          # texto pela numeração do livro
python ferramentas/extrair.py buscar "Latin square"        # localiza um termo
python ferramentas/extrair.py recorte 84 100 200 500 400 fig.png
python ferramentas/figuras.py listar 84                    # candidatos a figura na página
python ferramentas/figuras.py salvar 84 fig.png
```

Dependências: `pymupdf`, `pypdf`, `pdfplumber` (Python 3.13).

## Publicando no GitHub Pages

Em **Settings → Pages**, escolha a branch `main` e a pasta **`/ (root)`**. O
`index.html` da raiz redireciona para `estudo/index.html`. Nada precisa ser
compilado — o site é o próprio repositório. O objetivo é ler as aulas em
qualquer aparelho (tablet, celular) sempre na versão mais recente; o CSS já é
responsivo.

### Fora dos buscadores, de propósito

O repositório é público porque o GitHub Pages gratuito só publica repositórios
públicos, mas o conteúdo **não deve ser indexado** — reproduz figuras do livro.
Duas camadas cuidam disso:

- `<meta name="robots" content="noindex, nofollow">` em toda página — é o que os
  buscadores obedecem para não indexar. **Toda aula nova precisa dele.**
- [`robots.txt`](robots.txt) na raiz com `Disallow: /` — pede que nada seja
  sequer baixado, o que também afasta arquivadores e raspadores bem-comportados.

## Licença

O código das ferramentas e o texto das aulas são de uso pessoal e livre. As
figuras, tabelas e enunciados de exercícios pertencem a Montgomery / Wiley e
estão reproduzidos aqui apenas para estudo — não redistribua o livro.
