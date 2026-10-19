# Guia de e-mail e SMTP: a confirmação do pedido tem que chegar

E-mail de loja não é detalhe: é onde chegam confirmação de pedido,
rastreio, recuperação de senha e a resposta do contato. Este guia é
INSTRUÇÃO; nada foi configurado por mim. Nunca cole senha de e-mail ou
chave de API em documento ou conversa.

---

## 1. Endereços da loja (decidir e registrar)

| Uso | Endereço sugerido | Situação |
|---|---|---|
| Remetente dos e-mails automáticos | o e-mail oficial da loja [PREENCHER] | [A DEFINIR] |
| Destino do formulário de contato | atendimento [PREENCHER] | [CONFERIR] |
| Destino da newsletter | a ferramenta escolhida [PREENCHER] | [A DEFINIR] |
| Responder para (reply-to) | o atendimento que lê de verdade | [A DEFINIR] |

Nome do remetente: **Iara Costa**. Nada de "WordPress" ou do domínio cru
aparecendo para a cliente.

## 2. Autenticação do domínio (SPF, DKIM e DMARC)

Sem estes três registros no DNS, o e-mail da loja cai em spam ou é
falsificado em nome da marca:

- [ ] **SPF**: registro TXT autorizando quem pode enviar pelo domínio
      (hospedagem do site, serviço de e-mail e ferramenta de newsletter,
      cada um com o seu trecho, sem duplicar registro).
- [ ] **DKIM**: chave gerada pelo serviço de e-mail e publicada no DNS;
      conferir "assinado por" nos e-mails de teste.
- [ ] **DMARC**: começar em monitoramento (`p=none` com relatório) e subir
      para quarentena ou rejeição depois de conferir que nada legítimo
      quebra. Endereço dos relatórios [PREENCHER].
- [ ] Conferir os três em ferramenta de consulta de DNS [CONFERIR] e
      guardar a data da conferência.

## 3. Envio pelo site (SMTP)

- [ ] O WordPress **não** deve enviar pela função simples do servidor:
      configurar o envio autenticado pelo serviço de e-mail da empresa
      (recurso da hospedagem ou plugin aprovado; **plugin novo pede
      aprovação prévia**, como todo plugin do projeto).
- [ ] Credencial de envio guardada no cofre da empresa, nunca no repositório
      e nunca neste guia.
- [ ] E-mail de teste do próprio WordPress chegando em duas caixas
      diferentes (por exemplo Gmail e Outlook), fora da pasta de spam.

## 4. E-mails do WooCommerce (conferir um por um)

Ativar e revisar o texto de cada um, com o nome da loja e sem sobra em
inglês: pedido recebido, pedido em processamento, pedido concluído, nota
ao cliente, reembolso, conta criada e redefinição de senha.

- [ ] Fazer o pedido de teste do GUIA-TESTES.md e conferir os e-mails que
      ele gera, na caixa certa e fora do spam.
- [ ] Código de rastreio no e-mail de envio assim que a peça é postada
      [CONFERIR como o rastreio entra: campo do plugin de frete ou manual].
- [ ] Newsletter: dupla confirmação (opt-in com clique no e-mail) e link de
      cancelamento funcionando, como pede a LGPD. Um clique para sair.

## 5. Sinais de problema e o que olhar primeiro

| Sintoma | Olhar primeiro |
|---|---|
| Confirmação não chega | spam da cliente; depois SPF/DKIM; depois o envio SMTP |
| Chega como "via outro domínio" | DKIM ou SPF do serviço de envio |
| Só o formulário de contato falha | destino `[PREENCHER]` e o registro do formulário |
| E-mail da loja sendo falsificado | DMARC ainda em `p=none`: subir a política |
