# Guia de SEO com Yoast: ser encontrada sem prometer posição

Isto é **INSTRUÇÃO**. SEO não se declara pronto num documento: ele se confere
página por página no Yoast e, depois do go-live, no Search Console. Nenhuma
posição em buscador é garantida por ninguém.

---

## 1. Base (uma vez)

- [ ] Yoast SEO instalado e o assistente inicial concluído como organização,
      com nome da loja, logo e perfis sociais [PREENCHER: endereços reais].
- [ ] Título e separador do site no padrão: `Página | Iara Costa`.
- [ ] Staging inteiro com `noindex` (Configurações > Leitura desmarcado só no
      go-live; ver o guia de go-live para a virada).
- [ ] Sitemap do Yoast ativo e conferido: entram páginas, produtos e posts.
      **Fora do sitemap e com `noindex`**: sacola, finalizar compra, minha
      conta e pedido recebido.
- [ ] Endereços (slugs) iguais aos do protótipo: `/loja/`, `/colecao/`,
      `/guia-de-medidas/`, `/diario/` e os demais da tabela do Bloco B.

## 2. Por tipo de página

### Páginas institucionais e de conteúdo

- [ ] Título e descrição únicos por página, escritos a partir do texto real
      de `pages-conteudo.md`, sem repetir a mesma frase em páginas diferentes.
- [ ] Um só H1 por página (vem do template); H2 na ordem do texto.
- [ ] Frase-chave do Yoast usada como conferência de leitura, não como
      enchimento de palavra repetida.

### Produtos

- [ ] Título do produto limpo (nome da peça) e descrição curta própria: é ela
      que vira o resumo nos buscadores e nas redes.
- [ ] Categoria certa, foto 1:1 com texto alternativo que descreve a peça
      (não o nome do arquivo), e preço/estoque reais para o Yoast e para o
      WooCommerce gerarem os dados estruturados de produto.
- [ ] Produto sem estoque fora de promoção: nada de empurrar o que não vende.

### Diário (posts do Gutenberg)

- [ ] Título, resumo e imagem de capa por post; categoria do diário certa.
- [ ] Link interno de cada post para a peça ou guia citado no texto.
- [ ] Autor definido e página de autor simples, sem biografia inventada
      [PREENCHER: quem assina].

## 3. Dados estruturados e compartilhamento

- [ ] Conferir no validador de resultados ricos [CONFERIR ferramenta atual do
      Google] um produto, um artigo e a loja: produto precisa de preço e
      disponibilidade; artigo, de data e autor.
- [ ] Imagem de compartilhamento (Open Graph) padrão da loja [PREENCHER:
      imagem oficial] e a de cada lançamento.
- [ ] Trilha de navegação (breadcrumbs) visível nas páginas de loja e produto:
      ela também alimenta o resultado de busca.

## 4. O que não fazer

- Nada de texto escondido, palavra-chave repetida à força ou página duplicada
  com a palavra trocada.
- Nada de publicar produto ou post de exemplo com título chamativo: além de
  errado para a cliente, indexa lixo com o nome da marca.
- Nada de prometer prazo de indexação ou posição. O combinado é: técnico
  conferido, conteúdo real e medição depois do go-live.

## 5. Depois do go-live (medição, não promessa)

- [ ] Search Console conectado, sitemap enviado e erros de cobertura olhados
      na primeira semana e depois uma vez por mês.
- [ ] Páginas que o Google não indexou: primeiro conferir se deveriam ser
      indexadas; as do funil de compra ficam de fora de propósito.
- [ ] Relatório simples mensal: páginas mais visitadas, termos que trouxeram
      visita e o que será ajustado no mês seguinte. Sem relatório, SEO vira
      opinião.
