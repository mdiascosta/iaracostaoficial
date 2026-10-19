# Guia de instalação: do zero ao site montado em staging

Este guia é a ordem completa de montagem do site, costurando os Blocos B e C.
Ele é **INSTRUÇÃO**: nada aqui foi executado por mim. Quem executa é a equipe,
em staging, marcando cada item. Onde a informação depende do ambiente, está
`[CONFERIR]`; onde depende da empresa, `[PREENCHER]`.

> Regra de ouro: staging com `noindex` ligado do primeiro ao último dia.
> Nada vai ao ar antes do go-live (ver `GUIA-GO-LIVE.md`).

---

## 1. Ambiente

| Item | O que conferir | Situação |
|---|---|---|
| Hospedagem com PHP 8.2 ou superior | versão no painel da hospedagem | [CONFERIR] |
| WordPress atualizado | Painel > Atualizações | [CONFERIR] |
| Certificado HTTPS ativo | cadeado no navegador, sem aviso | [CONFERIR] |
| Backup antes de começar | ferramenta da hospedagem ou plugin aprovado | [CONFERIR] |
| Fuso horário America/Sao_Paulo | Configurações > Geral | ajustar |
| Idioma pt_BR e moeda BRL | Configurações > Geral e WooCommerce | ajustar |
| Links permanentes em "Nome do post" | Configurações > Links permanentes | ajustar |

## 2. Tema e plugins (o mínimo, todos oficiais)

Instalar nesta ordem e **testar o site depois de cada um**:

1. Tema **Hello Elementor**.
2. **Elementor** (gratuito) e **Elementor Pro** (licença oficial da empresa).
3. **WooCommerce**.
4. **TI WooCommerce Wishlist** (gratuito, aprovado em 16/10/2026).
5. **Variation Swatches for WooCommerce**, da GetWooPlugins (gratuito, aprovado).
6. **Yoast SEO** (ver `GUIA-SEO-YOAST.md`).

Nada de plugin nulo ou pirata. Qualquer plugin além desta lista pede aprovação
prévia e entra no registro do diário de bordo.

## 3. Configurações do site (Site Settings)

1. Elementor > Configurações do site: criar as **15 cores** e as **10 fontes**
   globais exatamente com os nomes e valores da seção 3 de
   `bloco-b/GUIA-IMPORTACAO.md`.
2. Exportar só as configurações do site e rodar
   `python3 tools/ajusta-ids.py <site-settings.json>` para acertar os ids nos
   templates; conferir com `python3 tools/blocob_confere.py`.
3. Logo em Aparência > Personalizar > Identidade do site.
4. Fontes hospedadas localmente antes do go-live [CONFERIR no Bloco C].

## 4. Templates do Elementor

1. Importar os 24 arquivos de `bloco-b/json/`, um por vez, na ordem da seção 8
   do `GUIA-IMPORTACAO.md` do Bloco B.
2. Theme Builder: cabeçalho e rodapé com condição **Entire Site**; loja como
   arquivo de produtos; produto como produto único; 404 como página de erro.
3. Fazer os ajustes de editor listados na seção 4.3 do mesmo guia (menu
   `principal`, busca em lupa, sacola só com ícone, fotos da home, produtos em
   destaque, posts recentes).
4. Gerar a página da lista de desejos pelo TI Wishlist em
   `/lista-de-desejos/` e apontar o widget da página `10-desejos.json` para ela.
5. Configurar os atributos globais **Cor** (tipo cor) e **Tamanho** (tipo
   botão) no Variation Swatches; conferir variação esgotada riscada ou
   esmaecida.

## 5. Loja (WooCommerce)

1. Assistente do WooCommerce: Brasil, BRL, vírgula decimal, produtos físicos,
   fuso America/Sao_Paulo, peso em kg e medidas em cm.
2. Páginas da loja em WooCommerce > Configurações > Avançado: sacola,
   finalizar compra, minha conta e pedido recebido apontando para as páginas
   criadas com os templates `06` a `09`.
3. `noindex` e fora do sitemap em sacola, finalizar compra e minha conta
   (Yoast, página por página).
4. Compra como visitante ligada (Configurações > Contas e privacidade).
   Estoque ligado, com baixa automática e aviso de estoque baixo.
5. Cupom **BEMVINDO10**: 10% na primeira compra. A limitação técnica de
   "primeira compra" do WooCommerce é por e-mail e conta; registrar no guia
   de testes como ela foi configurada e qual é o limite real dela, sem
   prometer o que a ferramenta não faz. [A DEFINIR: teto de desconto]
6. Gateway **Mercado Pago** [CONFERIR conta e credenciais da empresa]:
   Pix com 5% de desconto, cartão em até 6x sem juros e boleto, conforme o
   que estiver ativo na conta. Nenhum pagamento real em staging.
7. Frete: PAC pelos Correios [CONFERIR integração], frete grátis a partir de
   R$ 299 e peso/dimensões reais por produto (o cálculo depende deles).
8. Importar `bloco-c/produtos.csv` (ver `IMPORTACAO-CSV.md`): 12 produtos em
   rascunho. Só publicar com descrição, composição, foto 1:1, peso, dimensões
   e estoque reais.
9. Categorias reais criadas; apontar os cartões da home para cada categoria.
10. Filtros da loja: decidir o caminho da seção 4.4 do guia do Bloco B
    (blocos do WooCommerce, plugin aprovado ou links por atributo).

## 6. Conteúdo

1. Criar as páginas nos endereços da tabela do guia do Bloco B, colando os
   textos revisados de `bloco-c/pages-conteudo.md`.
2. Páginas legais como **rascunho** até o jurídico aprovar.
3. Criar os 8 posts de `bloco-c/posts.csv` no Gutenberg (rascunho), com autor
   definido [PREENCHER: quem assina].
4. Menus: principal (Início, Loja, Coleção, Sobre, Contato) e os links do
   rodapé conferidos página por página.
5. Botão de WhatsApp por Floating Elements, com o número oficial
   [PREENCHER: número com DDI] e entrada depois da rolagem.
6. E-mail da newsletter e dos formulários [PREENCHER: destino] e endereços
   das redes sociais [PREENCHER].

## 7. Conferência rápida antes dos testes

- [ ] Cabeçalho e rodapé em todas as páginas, no celular e no computador.
- [ ] Nenhuma página publicada com `[PREENCHER]`, `[PROPOSTA]` ou texto de exemplo.
- [ ] Nenhum produto de exemplo publicado.
- [ ] Busca com resultado, busca sem resultado e um endereço inexistente (404).
- [ ] `python3 tools/blocob_confere.py` e `tools/blococ_confere.py` verdes no
      repositório (eles conferem os arquivos, não o site).

Com tudo montado, a próxima etapa é segurança (`GUIA-SEGURANCA.md`), depois
SEO, testes, desempenho, e-mail e go-live.
