# Guia de go-live: a virada, item a item, sem volta escondida

O go-live é a sequência de viradas abaixo, **nesta ordem**, executada pela
equipe e registrada com data e responsável. Nada aqui foi executado por mim.
Se um item da lista falhar, a virada para: loja fechada mais um dia é melhor
que loja aberta vendendo errado.

> Pré-condição: GUIA-TESTES.md inteiro marcado, com o pedido de teste
> apagado; desempenho medido (GUIA-DESEMPENHO.md); e-mails autenticados
> (GUIA-EMAIL-SMTP.md); nota fiscal resolvida (GUIA-NFE.md).

---

## 1. Congelar e copiar

- [ ] Backup completo do staging aprovado e do que for produzido, com
      restauração testada (GUIA-SEGURANCA.md).
- [ ] Janela de virada combinada (dia e hora de pouco movimento) e quem fica
      de plantão nas primeiras 24 horas [A DEFINIR].
- [ ] Lista de diferenças entre staging e produção anotada (domínio,
      credenciais do gateway, e-mails): é aqui que mora o esquecimento.

## 2. Conteúdo e loja

- [ ] Nenhum `[PREENCHER]`, `[PROPOSTA]` ou `[CONFERIR]` publicado: buscar
      os termos no painel, página por página, produto por produto.
- [ ] Nenhum produto, post ou depoimento de exemplo no ar; estoque, preço,
      peso e dimensões reais em tudo que está publicado.
- [ ] Páginas legais **aprovadas pelo jurídico** e publicadas (privacidade,
      termos e cookies), com razão social, CNPJ e endereço do rodapé iguais
      aos documentos da empresa (Decreto 7.962/2013).
- [ ] Banner de cookies funcionando, com recusar de verdade.
- [ ] Cupom BEMVINDO10 ativo e conferido de novo em produção com um pedido
      real pequeno da própria equipe (e estornado/apagado conforme a regra
      combinada), frete grátis em R$ 299 valendo e gateway em produção.

## 3. A virada técnica

- [ ] Domínio final apontado, HTTPS válido no domínio final e e-mails do
      domínio autenticados (SPF, DKIM e DMARC).
- [ ] **Tirar o `noindex`**: Configurações > Leitura desmarcado e Yoast
      liberando o que deve indexar. Manter `noindex` e fora do sitemap em
      sacola, finalizar compra, minha conta e pedido recebido.
- [ ] Sitemap enviado ao Search Console e uma compra de conferência
      encontrada de ponta a ponta (página, pedido, e-mail, nota).
- [ ] Cache ligado fora do funil de compra; desempenho medido de novo no
      domínio final e registrado na tabela do guia de desempenho.
- [ ] Analítica e pixels [A DEFINIR: quais] só com consentimento do banner,
      nada disparando antes da escolha da cliente.

## 4. Primeiras 24 horas e primeira semana

- [ ] Plantão olhando: pedidos, e-mails, erros 404 e a busca do site.
- [ ] Search Console: cobertura e erros na primeira semana.
- [ ] Relatório simples ao fim da primeira semana: o que vendeu, o que
      travou, o que ajustar. Erro encontrado vira item de lista, não boato.

## 5. Os 30 dias seguintes

- [ ] Atualizações só com teste em staging antes (a rotina do guia de
      segurança), backup conferido toda semana.
- [ ] Relatório mensal de SEO e de desempenho, com a mesma tabela de antes.
- [ ] Revisão das páginas legais se qualquer regra da loja mudar (prazo,
      troca, frete): página legal desatualizada é problema jurídico, não
      detalhe de texto.
- [ ] Fechamento do projeto: este guia marcado, os relatórios guardados e o
      diário de bordo com a data do go-live.

---

## Sobre plugin próprio (`plugin-iara-custom.zip`)

Avaliação ao fim do Bloco C: **nenhum plugin próprio é indispensável** para
o que foi desenhado. Variações, desejos, checkout, formulários e SEO são
cobertos por WooCommerce, Elementor Pro, Yoast e os dois plugins gratuitos
aprovados. A regra continua valendo: se um dia algo exigir código próprio,
ele nasce como plugin isolado, versionado neste repositório, com guia de
instalação próprio. `functions.php` e o núcleo seguem intocados.
