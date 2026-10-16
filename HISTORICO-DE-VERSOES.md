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
git checkout arena/557fb81d-iaracostaoficial
```

Para consultar apenas um arquivo de uma versão antiga, sem mudar nada:

```bash
git show v0.1.0:seu-projeto/index.html
```

**Nada é perdido ao voltar.** O Git guarda todo o histórico; a troca de versão
apenas mostra os arquivos como estavam naquele momento.

---

## Versões registradas

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
| v0.1.1 | Ajustes no protótipo a partir da conferência visual da equipe |
| v0.2.0 | Bloco B: JSONs de templates para Elementor |
| v0.3.0 | Bloco C: kit ZIP, produtos.csv, posts.csv e guias de instalação |
| v1.0.0 | Go-live: site publicado com dados reais e revisão jurídica concluída |

Estas previsões são referência de planejamento e podem mudar. O que vale é o
que estiver registrado como versão entregue neste arquivo.
