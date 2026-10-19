# Guia de nota fiscal: o que decidir antes de vender a primeira peça

Este guia **não emite nota fiscal** e não substitui contador. Ele organiza
as decisões e os dados que a empresa precisa fechar com a contabilidade
antes do go-live, para a emissão entrar no fluxo certo desde o primeiro
pedido. Tudo aqui é [CONFIRMAR COM A EMPRESA] junto ao contador.

> Vender sem nota não é uma opção de lançamento que este projeto assine.
> Se a emissão não estiver resolvida, o go-live espera.

---

## 1. Dados da empresa que travam tudo [PREENCHER]

| Dado | Para que serve |
|---|---|
| Razão social e CNPJ (os mesmos do rodapé do site) | identificação em todos os documentos |
| Inscrição estadual e regime tributário | define o tipo de nota e os impostos |
| Endereço fiscal completo | emissor e cálculo |
| Certificado digital (modelo e validade) | assinatura da nota; **fica com a empresa, nunca no repositório** |
| Contador responsável e contato | quem valida classificação fiscal e CFOP |

## 2. Decisões com o contador

- [ ] **Modelo de nota** para venda ao consumidor pela internet
      (NFC-e ou NF-e, conforme o estado e o regime da empresa).
- [ ] **Classificação fiscal das peças** (NCM de vestuário e acessórios) e
      CFOP de venda interestadual e dentro do estado.
- [ ] **Quando a nota nasce** no fluxo: na confirmação do pagamento ou na
      postagem, e como ela chega à cliente (e-mail e Minha conta).
- [ ] **Troca e devolução**: nota de devolução e estorno combinados com o
      processo da página de trocas, sem improviso quando acontecer.
- [ ] **Cupom BEMVINDO10 e Pix com desconto**: como o desconto aparece na
      nota, conferido com o contador.

## 3. Emissão: pelo WooCommerce ou pelo sistema da empresa?

| Caminho | Quando faz sentido | Cuidado |
|---|---|---|
| Plugin emissor ligado ao WooCommerce [CONFERIR candidatos] | volume baixo e tudo dentro da loja | plugin novo pede aprovação prévia e teste em staging com nota de homologação |
| Sistema/ERP da empresa emitindo a partir do pedido | quando a empresa já tem emissor ou contador que exige um | conferir quem digita o quê: retrabalho manual é onde o erro mora |

A decisão é da empresa com o contador. O que este projeto exige é só que
ela esteja tomada e testada antes do go-live, com **nota de homologação**
emitida e cancelada em ambiente de teste, nunca nota real para testar.

## 4. Conferência antes do go-live

- [ ] Pedido de teste completo gerando a nota de homologação certa
      (valores, desconto e frete batendo com o pedido).
- [ ] Nota acessível à cliente (e-mail e Minha conta) e guardada pela
      empresa pelo prazo que o contador indicar.
- [ ] Processo escrito de devolução com nota, na página de trocas, sem
      prometer prazo que a operação não cumpre.
- [ ] Quem emite, quem confere e quem resolve erro de emissão: nomes e
      canais registrados fora do site.
