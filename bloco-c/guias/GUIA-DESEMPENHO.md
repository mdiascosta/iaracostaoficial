# Guia de desempenho: medir antes e depois, sem chute

Desempenho se **mede**, não se promete. Este guia diz onde medir, o que olhar
e como registrar. As metas do projeto são as do dossiê: **LCP abaixo de 2,5s,
CLS abaixo de 0,1 e INP abaixo de 200ms**, no celular, que é onde a cliente
compra. Nada foi medido por mim: não há site no ar.

---

## 1. Onde medir

- **PageSpeed Insights** (laboratório e, quando houver tráfego, dados de
  campo): home, loja, produto, sacola e uma página do diário.
- **WebPageTest** ou o relatório de desempenho da hospedagem [CONFERIR o que
  o ambiente oferece] para a sequência de carregamento (o que trava o quê).
- Medir sempre no **celular simulado** e repetir 3 vezes, ficando com a
  mediana; uma medição só é retrato do acaso.

## 2. Antes e depois (a comparação que importa)

1. Medir o site recém-montado, antes de qualquer otimização. Anotar.
2. Ajustar um item por vez (a lista da seção 3) e medir de novo.
3. Guardar as duas colunas na tabela da seção 5. Otimização sem antes e
   depois é só trabalho, não é resultado.

## 3. A lista de ajustes, na ordem de impacto comum

- [ ] **Imagens**: fotos de produto 1:1, redimensionadas para o tamanho em que
      aparecem (nada de foto de 4000px em cartão de 400px), comprimidas
      [CONFERIR ferramenta da hospedagem ou do fluxo de subida], com a foto da
      home marcada como prioritária e as demais com carregamento preguiçoso.
- [ ] **Fontes hospedadas localmente** (Jost e Playfair Display), com
      `font-display: swap` equivalente e só os pesos usados (400 e 600).
- [ ] **Cache de página** da hospedagem ou plugin aprovado [CONFERIR]:
      nunca em sacola, checkout e minha conta.
- [ ] **Plugins**: a lista mínima do guia de instalação; medir o peso antes
      e depois de cada plugin novo (a regra já está no guia de segurança).
- [ ] **Elementor**: CSS e JS gerados pelo próprio Elementor, sem widget
      repetido à toa; a home não pode virar um museu de blocos dinâmicos.
- [ ] **Banco e cron**: revisões de produto e post sob controle
      [CONFERIR recurso do WordPress/hospedagem], sem plugin novo por
      enquanto.

## 4. Sinais de alerta durante a medição

| Sinal | Suspeita primeiro |
|---|---|
| LCP alto na home | foto do hero pesada ou fonte trocando tarde |
| CLS alto na loja | imagem sem proporção reservada ou banner entrando depois |
| INP alto no produto | script de variação ou de filtro pesado na troca de opção |
| Servidor lento (TTFB) | hospedagem ou cache desligado; não é culpa do layout |

## 5. Registro (preencher com a medição real)

| Página | Quando | LCP | CLS | INP | O que foi ajustado |
|---|---|---|---|---|---|
| Home | antes |  |  |  |  |
| Home | depois |  |  |  |  |
| Loja | antes |  |  |  |  |
| Loja | depois |  |  |  |  |
| Produto | antes |  |  |  |  |
| Produto | depois |  |  |  |  |

Sem número medido, a frase certa no relatório é "não medido", nunca
"rápido". Site aprovado em desempenho é o que tem esta tabela preenchida
abaixo das metas, no celular.
