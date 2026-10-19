# Guia de segurança: o mínimo sério antes do go-live

Isto é **INSTRUÇÃO** para a equipe executar e registrar. Eu não tenho acesso
ao servidor, ao painel nem ao banco de dados, então **não declaro o site
seguro**: quem declara é a conferência item a item, com data e responsável.

> Nunca cole senha, chave, token ou dado de cartão em documento, e-mail ou
> conversa. Credencial se guarda no cofre da empresa, com acesso por pessoa.

---

## 1. Acessos

- [ ] Cada pessoa com login próprio no WordPress; nada de usuário "admin"
      compartilhado. Quem não precisa de administrador, não é administrador.
- [ ] Senhas fortes e diferentes das de outros serviços; gerenciador de senhas
      da empresa [A DEFINIR: qual].
- [ ] Autenticação em duas etapas para administradores [CONFERIR: recurso da
      hospedagem ou plugin aprovado; plugin novo pede aprovação].
- [ ] Revisar a lista de usuários depois da montagem e apagar contas de teste.
- [ ] Acesso à hospedagem, ao domínio e ao Mercado Pago com donos nomeados
      (nada preso ao e-mail pessoal de uma pessoa só).

## 2. Atualização e backup

- [ ] WordPress, tema, Elementor, WooCommerce e plugins com atualização
      acompanhada: testar em staging antes de atualizar produção.
- [ ] Apagar temas e plugins que não estão em uso (plugin parado também é
      porta).
- [ ] Backup automático com retenção definida [A DEFINIR: frequência e dias] e
      **um teste de restauração feito de verdade**, com data registrada.
      Backup que nunca foi restaurado é só uma esperança.
- [ ] Cópia do kit (`iara-costa-kit.zip`), dos CSVs e das configurações
      exportadas do Elementor fora do servidor, no repositório do projeto.

## 3. Servidor e WordPress

- [ ] HTTPS em tudo, com redirecionamento de HTTP para HTTPS e HSTS se a
      hospedagem oferecer [CONFERIR].
- [ ] PHP 8.2 ou superior e versão do MySQL/MariaDB suportada [CONFERIR].
- [ ] `functions.php` e arquivos do núcleo intocados (regra do projeto:
      código próprio só em plugin isolado, e até aqui nenhum foi necessário).
- [ ] Editor de arquivos do painel desligado, se a hospedagem permitir
      [CONFERIR], e listagem de diretórios bloqueada.
- [ ] Permissões de arquivo padrão da hospedagem, sem pasta pública de upload
      executando script [CONFERIR com a hospedagem].

## 4. Loja e dados pessoais (LGPD)

- [ ] Banner de cookies com aceitar e recusar de verdade (recusar não pode ser
      só enfeite), apontando para a Política de Cookies aprovada pelo jurídico.
- [ ] Formulários só com os campos necessários; consentimento registrado onde
      a lei pede (newsletter e contato).
- [ ] Dados de cartão **nunca** passam pelo site: quem processa é o gateway
      (Mercado Pago). Se algum relatório mostrar dado de cartão, parar tudo.
- [ ] E-mails da loja com SPF, DKIM e DMARC (ver `GUIA-EMAIL-SMTP.md`): é
      segurança da entrega e contra falsificação do remetente.
- [ ] Política de Privacidade publicada só depois do jurídico, com encarregado
      e canal de contato [PREENCHER].

## 5. Rotina depois do go-live

| Quando | O quê |
|---|---|
| Semanal | olhar atualizações pendentes e o relatório de pedidos estranhos |
| Mensal | revisar usuários, backups e o teste de restauração |
| A cada plugin novo | aprovação prévia, instalar em staging, medir o peso e registrar no diário |
| A cada incidente | registrar o que houve, o que foi feito e o que mudou na rotina |

## 6. O que falta decidir

- [ ] Ferramenta de backup e de duas etapas, se não forem da hospedagem.
- [ ] Quem é o responsável técnico que recebe alerta de site fora do ar.
- [ ] Telefone e canal de emergência da hospedagem anotados fora do site.
