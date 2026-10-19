# Iara Costa · loja online

Loja de moda feminina e acessorios da Iara Costa (Cerquilho, SP). O site e
construido em **modo manual**: arquivos autocontidos, guias e verificacoes
automaticas, sem acesso ao painel do WordPress e sem automacao externa.

A entrega acontece em blocos. O **Bloco A esta fechado na versao 0.1.20**: e o
prototipo HTML estatico completo, que valida visual, conteudo e acessibilidade
antes de qualquer coisa ir para o WordPress. Ele fica congelado em
`template-v0.1.20/`, e o que ainda depende de informacao da empresa esta em
`PENDENCIAS.md`.

O **Bloco B esta completo na versao 0.2.5**: os 24 templates do
Elementor em `bloco-b/`, com as cores e as fontes globais do site.

O **Bloco C esta em andamento (versao 0.3.1)**: comeca pelos arquivos que
alimentam a loja e o diario (`bloco-c/produtos.csv` e `bloco-c/posts.csv`),
o conteudo das paginas em `bloco-c/pages-conteudo.md` e o kit da equipe em
`bloco-c/iara-costa-kit.zip`. O guia de importacao
do Bloco B esta em `bloco-b/GUIA-IMPORTACAO.md`.

---

## Como o repositorio esta organizado

| Pasta ou arquivo | O que e |
|---|---|
| `seu-projeto/` | A versao em desenvolvimento do template. E daqui que sai o site |
| `template-v0.1.20/` | Copia congelada da versao em que o Bloco A fechou (0.1.20), para conferencia |
| `template-v0.1.18/` | Copia congelada da versao 0.1.18, guardada tambem. Uma pasta por versao fechada |
| `PENDENCIAS.md` | O que ainda depende de informacao da empresa, por assunto |
| `bloco-b/` | Templates do Elementor (Bloco B): os `.json` de importacao e o guia |
| `bloco-c/` | Dados e guias de instalacao (Bloco C): CSVs, kit e guias |
| `tools/` | Gerador das paginas e as verificacoes (Python e Node) |
| `VERSION` | Numero da versao atual do template |
| `HISTORICO-DE-VERSOES.md` | O que mudou em cada versao, com a data e o pedido que originou |
| `DIARIO-DE-BORDO.md` | Registro de cada rodada de trabalho |
| `package.json` | Dependencias das verificacoes (jsdom). O site nao depende disto |

Cada versao fechada tambem tem uma etiqueta (tag) no Git, de `v0.1.0` ate
`v0.1.20`, que guarda os arquivos exatamente como estavam naquele dia.

---

## Como ver o site

**Do jeito mais simples:** de dois cliques em `seu-projeto/index.html`.

**Com servidor local** (recomendado):

```bash
python3 -m http.server 8080 --directory seu-projeto
```

Depois abra `http://localhost:8080`.

Para abrir a versao congelada, troque a pasta:

```bash
python3 -m http.server 8080 --directory template-v0.1.20
```

---

## Como rodar as verificacoes

```bash
python3 tools/build.py      # gera as 22 paginas em seu-projeto/
python3 tools/check.py      # confere o que foi gerado
node tools/test.js          # 1043 verificacoes automaticas
python3 tools/pente-fino.py # varredura de HTML, CSS e JavaScript
```

O `tools/test.js` precisa das dependencias instaladas uma vez:

```bash
npm install
```

---

## Avisos

- O prototipo **nao vai para producao** e nada dele e importado no WordPress.
  Ele serve de referencia aprovada para a construcao no Elementor.
- Textos legais (privacidade, termos e cookies) sao **rascunhos** para revisao
  juridica.
- As imagens sao de referencia, com direitos a conferir antes de publicar.
- Nada aqui deve ser declarado como instalado, testado ou medido no WordPress
  sem a verificacao da equipe.
