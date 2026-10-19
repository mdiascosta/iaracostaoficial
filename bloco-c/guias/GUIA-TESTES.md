# Guia de testes: conferir antes de qualquer pessoa comprar

Este é o roteiro que a equipe executa em staging e registra, item a item,
com data e quem testou. Nada aqui foi executado por mim. Critério de aceite:
o item só passa se funcionar **no celular e no computador**; se falhar, volta
para a lista com o que aconteceu escrito, sem "mais ou menos".

> Regra do ambiente: **nenhum pagamento real em staging**. Cartão de teste do
> gateway, transferência simulada ou pedido manual; dinheiro de verdade, só
> depois do go-live, no primeiro pedido de conferência.

---

## 1. Navegação e páginas

- [ ] Menu principal e menu do celular abrem e levam às páginas certas.
- [ ] Busca com resultado, busca sem resultado e busca vazia.
- [ ] Endereço inexistente abre a página 404 com saída para a loja.
- [ ] Cabeçalho e rodapé iguais em todas as páginas; coração de desejos com
      contador certo depois de salvar uma peça.
- [ ] Nenhuma página publicada com `[PREENCHER]`, `[PROPOSTA]`, texto ou
      produto de exemplo. Procurar por esses termos no painel antes de seguir.

## 2. Loja e produto

- [ ] Grade na ordem certa, paginação de 9 em 9 e as 5 ordenações mudando a
      ordem de verdade (recentes, populares, menor preço, maior preço,
      melhor avaliados).
- [ ] Filtros pelo caminho decidido (guia do Bloco B, seção 4.4) filtrando de
      verdade, inclusive limpar filtros.
- [ ] Produto variável: trocar cor e tamanho muda preço, foto e estoque;
      tamanho esgotado aparece riscado ou esmaecido e não entra na sacola.
- [ ] Produto sem estoque não vende; produto simples (acessório) compra direto.
- [ ] Tabela de medidas da peça abre e bate com o produto cadastrado.
- [ ] Relacionados ("Combina com") mostram peças da mesma conversa, não
      produtos aleatórios do catálogo.

## 3. Sacola, checkout e pedido (o teste central)

Executar nesta ordem, como visitante e depois logado:

1. [ ] Adicionar peça com variação à sacola; mudar quantidade; remover item.
2. [ ] Aplicar **BEMVINDO10**: desconto de 10% aparece uma vez. Tentar aplicar
       de novo no mesmo pedido e em um segundo pedido com o mesmo e-mail:
       registrar o que o WooCommerce fez (a limitação é por e-mail e conta;
       anotar o comportamento real, não o desejado).
3. [ ] Calcular frete com CEP abaixo de R$ 299 (cobra) e acima de R$ 299
       (grátis no PAC), conferindo se o total acompanha.
4. [ ] Fechar o pedido como **visitante** pagando por transferência ou meio de
       teste do Mercado Pago. Nenhum campo obrigatório sem sentido; erro de
       formulário explicado em português, campo por campo.
5. [ ] Tela de **pedido recebido** mostra número, itens e total; e-mail de
       confirmação chega na caixa certa (ver também GUIA-EMAIL-SMTP.md).
6. [ ] Pedido aparece em Minha conta com o estado certo; baixar nota ou boleto
       de teste, se o meio tiver.
7. [ ] **Apagar o pedido de teste** e os clientes de teste criados. Staging
       limpo é parte do teste.
8. [ ] Registrar: data, quem testou, meios usados e qualquer desvio.

## 4. Conta, desejos e formulários

- [ ] Criar conta, entrar, sair, recuperar senha e editar endereço.
- [ ] Salvar e remover peça dos desejos (TI Wishlist); a página da lista abre
      pelo coração do cabeçalho.
- [ ] Contato envia e chega no e-mail certo; newsletter assina e confirma;
      nenhum dos dois guarda dado além do pedido (LGPD).

## 5. Acessibilidade (conferência manual, WCAG 2.2 AA como meta)

- [ ] Navegar a loja inteira só com o teclado: foco visível, sem armadilha,
      sanfona do FAQ e seletores de variação alcançáveis.
- [ ] Aumentar o zoom para 200% sem perder compra nem menu.
- [ ] `prefers-reduced-motion` ligado no sistema: animações param.
- [ ] Leitor de tela em uma compra completa, ao menos uma vez, no celular.
- [ ] Contraste de qualquer texto novo conferido contra as cores globais.
      Registro honesto: ornamento decorativo não é texto; o que é texto
      precisa passar.

## 6. Registro

Guardar no repositório ou na pasta do projeto: a lista acima marcada, os
desvios encontrados com a correção aplicada e a data do pedido de teste
apagado. Sem esse registro, "testamos" é só uma lembrança.
