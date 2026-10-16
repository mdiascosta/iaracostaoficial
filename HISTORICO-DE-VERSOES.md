# Histórico de versões: Iara Costa E-commerce

Este arquivo registra **o que mudou em cada versão** do projeto. Serve para duas
coisas: saber o que foi entregue quando, e poder voltar a uma versão anterior
sem depender da memória de ninguém.

---

## Como o versionamento funciona

Cada versão aprovada vira uma **etiqueta (tag)** no Git. A etiqueta é um marco
permanente: nada é sobrescrito, as versões antigas continuam acessíveis para
sempre.

### Formato: `vMAJOR.MINOR.PATCH`

| Parte | Muda quando | Exemplo |
|---|---|---|
| **MAJOR** | Um bloco inteiro é entregue ou o escopo muda de verdade | Bloco A pronto, Bloco B pronto, site publicado |
| **MINOR** | Novas páginas, novas seções ou ajustes visuais aprovados pela equipe | Header refeito, 9 páginas novas |
| **PATCH** | Correções pequenas, textos, ajustes de acessibilidade | Cor do ícone, tamanho do logo, erro de digitação |

### Exemplos de leitura das etiquetas

- `v0.1.0` significa: primeira versão antes do lançamento, primeiro conjunto de
  entregas. O zero inicial indica que o projeto ainda não foi publicado.
- `v0.1.1` seria uma correção pequena sobre a mesma base.
- `v1.0.0` será a **primeira versão publicada em produção**, no go-live.

---

## Como voltar a uma versão anterior

Se em algum momento você precisar ver como o site estava em uma versão antiga:

```bash
# Ver a lista de todas as versões guardadas
git tag -l

# Abrir uma versão específica para conferir (não apaga nada do que existe)
git checkout v0.1.0

# Voltar para a versão mais recente do trabalho
git checkout main
```

A v0.1.0 foi integrada à `main` pelo pull request #1 (16/10/2026). A partir
dela, cada nova versão nasce em uma branch própria e é integrada por pull
request, para a equipe poder comparar antes de aceitar.

Para consultar apenas um arquivo de uma versão antiga, sem mudar nada:

```bash
git show v0.1.0:seu-projeto/index.html
```

**Nada é perdido ao voltar.** O Git guarda todo o histórico; a troca de versão
apenas mostra os arquivos como estavam naquele momento.

---

## Versões registradas

### v0.1.1 · 2026-10-16 · Super layout com fotos e faixa de benefícios centralizada

**O que mudou em relação à v0.1.0:**

- **Faixa de benefícios centralizada** (pedido da cliente): os quatro itens
  (frete grátis, troca fácil, pagamento, do P ao GG) passam a ficar agrupados no
  centro da faixa, com fio de separação entre eles, em vez de esticados de ponta
  a ponta.
- **Fotos de exemplo de verdade**: as 47 imagens de exemplo em SVG (retângulos
  cinza escritos "SUBSTITUIR") saíram do projeto. Entraram 31 fotos em JPG
  extraídas do template de referência enviado pela cliente. Direitos e origem
  destas fotos: `[CONFERIR]` antes de qualquer uso em produção.
- **Home no padrão do template**: hero com selo numerado, categorias numeradas,
  vitrine por ocasião, editorial "Um ateliê, três gestos" com pilares numerados,
  coleção "Terra & Linho" em bloco duplo, depoimentos e faixa verde sálvia de
  lista de espera.
- **Card de produto completo**: selo (Novo, Mais vendida, Oferta), coração de
  lista de desejos, nota com avaliações, preço promocional riscado, tamanhos e
  link "Adicionar à sacola".
- **Mini-sacola lateral (drawer)** com barra de progresso do frete grátis,
  subtotal, aviso rápido (toast) e circulação de foco por teclado.
- **Rodapé em 4 colunas**, newsletter com nota de consentimento, selos de
  pagamento ilustrativos e identificação da empresa.
- **Catálogo de exemplo ampliado** de 10 para 12 peças, alinhado ao template.
  Decisão pendente com a cliente: `[A DEFINIR]` manter 12 ou voltar a 10.
- **Regra de frete grátis unificada em R$ 299** em todo o protótipo (o dossiê
  previa R$ 199 e o header aprovado diz R$ 299). Confirmar qual vale:
  `[CONFIRMAR COM A EMPRESA]`.

**Arquivos novos:** `assets/css/comercio.css`, `assets/js/loja.js`,
`tools/produtos.json`, `tools/partials/drawer.html`.

**Verificado nesta versão:** 22 páginas sem erro de estrutura (`check.py`),
1.250 links internos e imagens conferidos, mini-sacola, coração de desejos,
busca e menu mobile testados por script, 1 H1 por página, alt em todas as
imagens não decorativas.

**Ainda não verificado:** conferência visual em navegador (é o próximo passo,
com a cliente) e direitos das fotos.

---

### v0.1.0 · 2026-10-16 · Bloco A concluído (protótipo HTML)

**O que está nesta versão:**

- Protótipo com **22 páginas** HTML, estáticas, navegáveis sem servidor.
- Identidade visual aplicada: 4 cores de sistema, 9 customizadas, Jost e
  Playfair Display.
- Header no padrão de site de moda: logo à esquerda, navegação ao centro,
  lupa, coração, conta e sacola à direita. Busca expansível ao clicar na lupa.
- Todos os estados de interface exigidos pelo dossiê: carregando, busca sem
  resultado, produto esgotado, sacola vazia, pagamento recusado, pedido
  confirmado e 404.
- Acessibilidade WCAG 2.2 AA: skip link, foco visível, área de toque de 44px,
  menu com ESC e controle de foco, `prefers-reduced-motion`, 16px no celular.
- Gerador de páginas (`tools/build.py`) com header e footer em um só lugar.
- Verificador automático (`tools/check.py`) e teste funcional do header.
- 47 imagens de exemplo em SVG, todas marcadas para substituição.
- Documentos: README do protótipo, lista de imagens a produzir, guia de fontes
  locais e os 3 rascunhos legais marcados para revisão jurídica.

**Verificado nesta versão:** 22 páginas sem erro de estrutura, 1.100 links
internos funcionando, 1 H1 por página, alt em todas as imagens, 22 páginas
respondendo 200 no servidor local.

**Ainda não verificado:** conferência visual em navegador, feita pela equipe.

**O que trava o lançamento:** imagens reais, dados legais da empresa, gateway
de pagamento, solução de frete, dados reais dos produtos e revisão jurídica das
páginas legais.

---

## Próximas versões previstas

| Versão | Conteúdo esperado |
|---|---|
| v0.1.2 | Ajustes finos no super layout a partir da conferência visual da cliente |
| v0.2.0 | Bloco B: JSONs de templates para Elementor |
| v0.3.0 | Bloco C: kit ZIP, produtos.csv, posts.csv e guias de instalação |
| v1.0.0 | Go-live: site publicado com dados reais e revisão jurídica concluída |

Estas previsões são referência de planejamento e podem mudar. O que vale é o
que estiver registrado como versão entregue neste arquivo.
