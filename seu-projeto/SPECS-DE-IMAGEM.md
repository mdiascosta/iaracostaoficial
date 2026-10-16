# Lista de imagens a produzir: Iara Costa

Este documento é a **lista de compras de fotos** do projeto. Cada linha
corresponde a um arquivo que hoje é um retângulo de exemplo com a etiqueta
"SUBSTITUIR POR FOTO REAL". Quando a foto definitiva entrar no lugar, com o
mesmo nome de arquivo, o site fica pronto visualmente.

**Regra de ouro:** o site só vai ao ar quando nenhum arquivo desta lista for
imagem de exemplo. O `tools/check.py` não detecta isso, então a conferência é
visual, feita pela equipe.

---

## 1. Convenções obrigatórias

- **Nomes:** minúsculas, sem acento, sem espaço. Separe com hífen. Exemplo:
  `produto-01-frente.webp`.
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

Dez produtos, mínimo de 3 ângulos cada: **30 arquivos**. Formato quadrado 1:1,
por exemplo 1600x1600 pixels. Fundo consistente entre todos os produtos.

| Arquivo | Produto de exemplo | Ângulo |
|---|---|---|
| produto-01-a | Vestido Midi Linho Terracota | Frente, corpo inteiro |
| produto-01-b | Vestido Midi Linho Terracota | Costas |
| produto-01-c | Vestido Midi Linho Terracota | Detalhe do tecido ou acabamento |
| produto-02-a, -b, -c | Vestido Longo Fluido Off-White | Frente, detalhe, corpo inteiro |
| produto-03-a, -b, -c | Vestido Chemise Botões | Frente, lateral, detalhe |
| produto-04-a, -b, -c | Blusa Canelada Manga Longa | Frente, costas, detalhe |
| produto-05-a, -b, -c | Camisa Oversized Algodão | Frente, lateral, detalhe |
| produto-06-a, -b, -c | Calça Wide Leg Alfaiataria | Frente, costas, detalhe |
| produto-07-a, -b, -c | Calça Jeans Reta Cintura Alta | Frente, costas, detalhe |
| produto-08-a, -b, -c | Saia Midi Plissada | Frente, detalhe da plissagem, movimento |
| produto-09-a, -b, -c | Bolsa Tote Couro Vegano | Frente, interior, detalhe |
| produto-10-a, -b, -c | Brinco Argola Dourada | Par, unitário, detalhe |

**Atenção:** as fotos precisam mostrar a cor real da peça. Se a foto mostrar uma
cor e o cliente receber outra, gera troca e reclamação. Ajuste de cor é diferente
de filtro de estética.

### Cores por variação

Se o produto tem mais de uma cor, cada cor precisa das suas próprias fotos. Isso
multiplica a lista acima. Quando o orçamento de produção for limitado, a
prioridade é: foto principal de cada cor primeiro, detalhes depois.

---

## 3. Categorias e navegação

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| categoria-vestidos | 800x1000 (4:5) | Peça de destaque da categoria, atmosfera da marca |
| categoria-blusas | 800x1000 | Idem |
| categoria-calcas | 800x1000 | Idem |
| categoria-acessorios | 800x1000 | Idem |

---

## 4. Home e banners

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| banner-home-desktop | 1920x800 | Campanha atual. Sem muito texto sobre a foto |
| banner-home-mobile | 800x1000 | Versão vertical do mesmo banner, enquadramento fechado |
| editorial-atelie | 1200x1200 | Detalhe de tecido, mão trabalhando, peça no cabide. Alimenta o bloco "Como escolher" |
| compartilhamento-social | 1200x630 | Usada quando o site é compartilhado em redes e WhatsApp. Logo mais foto |

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

## 6. Lookbook

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| lookbook-01 a 04 | 1200x1500 (4:5) | Quatro a seis looks completos, corpo inteiro |

Detalhes de produção estão na própria página `lookbook.html`, seção final.

---

## 7. Blog

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| blog-destaque-01 | 1600x900 (16:9) | Cuidados com as peças, tecidos |
| blog-destaque-02 | 1600x900 | Tamanhos, medidas, guia |
| blog-destaque-03 | 1600x900 | Estilo, combinações |

Cada post precisa da sua imagem de destaque. Com 8 posts previstos no projeto,
considere produzir de 6 a 8 imagens e reaproveitar as que fizerem sentido,
sempre relacionadas ao tema do texto.

---

## 8. Sobre

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| sobre-atelie | 1600x900 | História da marca, ambiente de trabalho, equipe |

---

## 9. Resumo do volume de produção

| Grupo | Arquivos |
|---|---|
| Produtos (10 x 3 ângulos) | 30 |
| Categorias | 4 |
| Banners e editoriais | 4 |
| Marca (logo e favicon) | 2 a 3 |
| Lookbook | 4 a 6 |
| Blog | 3 a 8 |
| Sobre | 1 |
| **Total estimado** | **48 a 56 arquivos** |

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
