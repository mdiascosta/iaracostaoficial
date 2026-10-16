# Lista de imagens a produzir: Iara Costa

> **Atualizado na v0.1.1.** Na v0.1.0 este documento descrevia 47 retângulos de
> exemplo em SVG espalhados pelo protótipo. Eles **não existem mais**: foram
> removidos e, no lugar, entraram **31 fotos em JPG** vindas do template de
> referência enviado pela cliente. O protótipo agora se parece com uma loja de
> verdade, e é justamente por isso que este documento mudou de função: ele
> deixou de ser a lista do que falta para virar a **lista de conferência das
> fotos de produção**.

**Antes de publicar, três coisas precisam estar resolvidas:**

1. **Direitos das 31 fotos do template** `[CONFERIR]`: de onde vieram, quem
   fotografou, existe licença para uso comercial? Se não houver, todas precisam
   ser substituídas.
2. **Fotos reais dos produtos** que a Iara Costa vai vender. As fotos atuais são
   de exemplo.
3. **Dados legais e fiscais** (fora do escopo deste arquivo, ver o rodapé).

**Regra de ouro:** o site só vai ao ar quando nenhuma foto de exemplo estiver no
ar. O `tools/check.py` não detecta isso, então a conferência é visual, feita
pela equipe.

---

## 0. O que existe hoje (v0.1.1)

31 arquivos JPG, 5,0 MB no total. O maior tem 326 KB (alvo de produção: até
300 KB). Nenhum deles está otimizado para web ainda: na produção, converter
para WebP e redimensionar.

| Grupo | Arquivos |
|---|---|
| Produtos e modelagens | `blusa-terracota`, `vestido-salvia`, `camisa-branca`, `vestido-cerrado`, `cropped-tricot`, `saia-cru`, `pantalona-salvia`, `blazer-areia`, `kimono-fluido`, `vestido-terra` |
| Acessórios | `colar-ceramica`, `brinco-argila`, `bolsa-palha`, `sandalia-couro`, `lenco-algodao` |
| Categorias | `cat-vestidos`, `cat-blusas`, `cat-saias-calcas` |
| Ocasiões | `oc-diadia`, `oc-trabalho`, `oc-festa`, `oc-acessorios` |
| Editorial e ateliê | `hero-editorial`, `tingimento`, `costura`, `atelie-bancada`, `detalhe-botoes`, `ceramica-seca` |
| Campanhas | `cap-terracota`, `cap-cru`, `cap-salvia` |

Arquivo que se chama assim nas páginas: `assets/img/<nome>.jpg`. Para trocar uma
foto, basta subir a definitiva com o mesmo nome e o site inteiro acompanha.

---

## 1. Convenções obrigatórias

- **Nomes:** minúsculas, sem acento, sem espaço. Separe com hífen. Exemplo:
  `vestido-salvia-frente.webp`.
- **Formato:** `.webp` quando o servidor suportar (recomendado). `.jpg` como
  alternativa.
- **Peso:** até 300 KB por arquivo. Imagem de produto quadrada com 1600x1600
  pixels abaixo de 300 KB é o alvo.
- **Alt:** toda imagem precisa de texto alternativo descritivo em português, que
  descreva o que aparece. Não use "imagem de vestido", use "Vestido midi de linho
  terracota, visto de frente, em corpo inteiro".
- **Direitos:** só entre imagens com autorização. Fotos próprias, contratadas, ou
  banco de imagens com licença comercial. Se houver modelo, termo de uso de
  imagem assinado **antes** da publicação. Registre autoria e licença no Diário
  de Bordo.
- **Nunca:** imagem com marca de terceiro, logotipo visível de outra empresa,
  pessoa famosa ou foto baixada de busca de imagem.

---

## 2. Fotos de produto (a prioridade)

O catálogo de exemplo do protótipo tem **12 peças** e cada uma usa **1 foto**
hoje. Na produção, o padrão recomendado é de **3 ângulos por peça** (36 fotos
no total), em formato quadrado 1:1, por exemplo 1600x1600 pixels, com fundo
consistente entre todos os produtos.

| Arquivo hoje | Peça de exemplo | Ângulos que faltam produzir |
|---|---|---|
| `blusa-terracota.jpg` | Blusa de Linho Terracota | costas, detalhe do acabamento |
| `vestido-salvia.jpg` | Vestido Midi Sálvia | costas, detalhe da costura |
| `camisa-branca.jpg` | Camisa Branca de Linho | lateral, detalhe do colarinho |
| `vestido-cerrado.jpg` | Vestido Longo Cerrado | costas, movimento do tecido |
| `cropped-tricot.jpg` | Cropped de Tricot Areia | costas, detalhe do tricô |
| `saia-cru.jpg` | Saia Midi de Linho Cru | lateral, detalhe das pregas |
| `pantalona-salvia.jpg` | Calça Pantalona Sálvia | costas, detalhe do cós |
| `blazer-areia.jpg` | Blazer de Linho Areia | costas, detalhe da lapela |
| `colar-ceramica.jpg` | Colar de Cerâmica | detalhe das contas, fecho |
| `brinco-argila.jpg` | Brinco de Argila Torneado | par montado, detalhe |
| `bolsa-palha.jpg` | Bolsa Artesanal em Palha | interior, alça |
| `sandalia-couro.jpg` | Sandália de Couro Natural | sola, detalhe da fivela |

**Atenção:** as fotos precisam mostrar a cor real da peça. Se a foto mostrar uma
cor e a cliente receber outra, gera troca e reclamação. Ajuste de cor é diferente
de filtro de estética.

### Cores por variação

Se o produto tem mais de uma cor, **cada cor precisa das suas próprias fotos.**
Isso multiplica a lista acima. Quando o orçamento de produção for limitado, a
prioridade é: foto principal de cada cor primeiro, detalhes depois.

---

## 3. Categorias e navegação

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `cat-vestidos.jpg` | 800x1000 (4:5) | Peça de destaque da categoria, atmosfera da marca |
| `cat-blusas.jpg` | 800x1000 | Idem |
| `cat-saias-calcas.jpg` | 800x1000 | Idem |
| `oc-acessorios.jpg` | 800x1000 | Idem |

---

## 4. Home e banners

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `cap-terracota.jpg` / `cap-cru.jpg` / `cap-salvia.jpg` | 1200x1500 | Campanhas da coleção. Sem texto dentro da foto |
| `hero-editorial.jpg` | 1200x1400 | Foto principal da home, a que aparece primeiro |
| `tingimento.jpg`, `costura.jpg`, `atelie-bancada.jpg`, `detalhe-botoes.jpg`, `ceramica-seca.jpg` | 1100x1300 | Ateliê e processo. Alimentam o editorial "Um ateliê, três gestos" |
| *(a produzir)* imagem de compartilhamento | 1200x630 | Usada quando o site é compartilhado em redes e WhatsApp. Logo mais foto. Ainda não existe no protótipo |

**Sobre o banner:** evite texto dentro da imagem. No celular ele desaparece ou
corta. O texto do banner deve ficar em HTML, sobre a imagem.

---

## 5. Marca

| Arquivo | Formato | Observação |
|---|---|---|
| Logo principal | SVG de preferência, ou PNG com fundo transparente | Para fundo claro |
| Logo versão clara | SVG ou PNG transparente | Para fundo escuro, se a marca usar |
| favicon | SVG ou PNG 512x512 | Já existe um provisório com as iniciais "IC" |

O logo em texto (Playfair Display na fonte) está funcionando bem no header. A
logo em imagem só entra se a Iara Costa tiver uma marca desenhada. Se tiver,
avise: o header precisa de ajuste para trocar texto por imagem.

---

## 6. Coleção (capítulos)

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `cap-terracota.jpg`, `cap-salvia.jpg`, `cap-cru.jpg` | 768x1376 (9:16) | Abertura dos três capítulos: corpo inteiro, mesmo tom de fundo nos três |
| `oc-diadia.jpg`, `oc-trabalho.jpg`, `oc-festa.jpg`, `vestido-terra.jpg` | 1200x1500 (4:5) | Looks completos, corpo inteiro. Fora da página de coleção desde a v0.1.16; ficam para vitrines e o Diário |

Cada capítulo leva, embaixo do texto, duas peças do catálogo com foto 4:5
(as mesmas da loja). Detalhes de produção estão na própria página
`lookbook.html`, seção final.

---

## 7. Blog

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `lenco-algodao.jpg` | 1600x900 (16:9) | Cuidados com as peças, tecidos |
| `cap-salvia.jpg` | 1600x900 | Tamanhos, medidas, guia |
| `blazer-areia.jpg` | 1600x900 | Estilo, combinações |
| `kimono-fluido.jpg`, `cap-cru.jpg`, `sandalia-couro.jpg`, `atelie-bancada.jpg` | 1600x900 | Demais posts, reaproveitados por tema |

Cada post precisa da sua imagem de destaque. Com 8 posts previstos no projeto,
considere produzir de 6 a 8 imagens e reaproveitar as que fizerem sentido,
sempre relacionadas ao tema do texto.

---

## 8. Sobre

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `atelie-bancada.jpg`, `ceramica-seca.jpg` | 1600x900 | História da marca, ambiente de trabalho. Falta foto da equipe |

---

## 9. Resumo do volume de produção

| Grupo | Arquivos |
|---|---|
| Produtos (12 x 3 ângulos, descontando as 12 fotos que já existem) | 24 a produzir |
| Categorias | 1 a produzir (3 das 4 já existem) |
| Campanhas e editoriais | 1 imagem de compartilhamento social |
| Marca (logo e favicon) | 2 a 3 |
| Lookbook | 5 já existem, revisar |
| Blog | 4 já existem, revisar |
| Sobre | 2 já existem, falta a equipe |
| **Já no projeto** | **31 fotos de exemplo** |
| **Total a produzir** | **cerca de 30 arquivos, além da conferência de direitos dos 31 atuais** |

Se a produção for feita em etapas, esta é a ordem de prioridade:

1. **Logo e favicon.** Destravam a identidade em todo o site.
2. **Produtos.** Sem eles a loja não vende. São a maior parte do trabalho e o
   maior impacto.
3. **Banner da home.** Primeira impressão do visitante.
4. **Categorias.** Melhoram a navegação.
5. **Blog e lookbook.** Conteúdo, pode entrar depois do lançamento.
6. **Sobre.** Pode usar foto provisória do ateliê por mais tempo.

---

## 10. Checklist de conferência antes de publicar

- [ ] Nenhum arquivo com a etiqueta "SUBSTITUIR POR FOTO REAL" no site.
- [ ] Todos os nomes em minúsculas, com hífen, sem acento.
- [ ] Toda imagem com alt descritivo em português.
- [ ] Nenhum arquivo acima de 2000 pixels na maior dimensão.
- [ ] Nenhum arquivo acima de 300 KB.
- [ ] Hero da home sem carregamento preguiçoso (lazy load desligado).
- [ ] Demais imagens com lazy load ligado.
- [ ] Cor da foto conferida contra a peça real, lado a lado.
- [ ] Termo de uso de imagem assinado, se houver modelo.
- [ ] Autoria e licença de cada imagem registradas no Diário de Bordo.
- [ ] Direitos das imagens documentados em um só lugar.
