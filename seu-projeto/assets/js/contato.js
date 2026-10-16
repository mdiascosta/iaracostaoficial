/* ============================================================================
   VALIDAÇÃO DO FORMULÁRIO DE CONTATO (v0.1.19)

   Por que existe: o formulário tem `novalidate` e campos obrigatórios, então,
   sem este arquivo, clicar em "Enviar mensagem" não mostrava nada. A pessoa
   achava que o site tinha travado.

   O que faz, seguindo o padrão que já existe no checkout (seção de referência
   de erro): marca o campo com problema, escreve a mensagem embaixo do campo,
   liga a mensagem ao campo por aria-describedby e leva o foco ao primeiro
   campo que precisa de conserto. Quando está tudo certo, mostra um recado na
   tela dizendo que o envio é simulado neste protótipo.

   Sem JavaScript, o formulário volta ao comportamento do HTML: os campos
   `required` são cobrados pelo próprio navegador. Nada aqui é essencial para
   ler ou navegar na página.
   ========================================================================== */
(function () {
  'use strict';

  var formulario = document.querySelector('[data-form-contato]');
  if (!formulario) { return; }

  var recado = document.querySelector('[data-contato-msg]');

  /* Cada campo obrigatório tem a sua mensagem, escrita para dizer o que fazer. */
  var REGRAS = [
    { id: 'ct-nome', mensagem: 'Escreva seu nome para a gente saber com quem falar.' },
    { id: 'ct-email', mensagem: 'Confira o e-mail: ele é por onde respondemos.' },
    { id: 'ct-assunto', mensagem: 'Escolha o assunto da mensagem.' },
    { id: 'ct-msg', mensagem: 'Conte o que você precisa na mensagem.' },
    { id: 'ct-consent', mensagem: 'Marque a autorização de uso dos dados para podermos responder.' }
  ];

  function caixaDo(campo) {
    return campo.closest('.field') || campo.closest('.checkbox') || campo.parentElement;
  }

  function erroDo(campo) {
    return document.getElementById(campo.id + '-erro');
  }

  function limpar(campo) {
    var caixa = caixaDo(campo);
    if (caixa) { caixa.classList.remove('field--invalid'); }

    campo.removeAttribute('aria-invalid');

    var aviso = erroDo(campo);
    if (aviso && aviso.parentElement) { aviso.parentElement.removeChild(aviso); }

    /* A descrição volta a ser só a que o HTML já tinha (dica, contador, etc.). */
    var descricao = (campo.getAttribute('aria-describedby') || '')
      .split(/\s+/)
      .filter(function (id) { return id && id !== campo.id + '-erro'; })
      .join(' ');
    if (descricao) { campo.setAttribute('aria-describedby', descricao); }
    else { campo.removeAttribute('aria-describedby'); }
  }

  function marcarErro(campo, texto) {
    var caixa = caixaDo(campo);
    if (caixa) { caixa.classList.add('field--invalid'); }

    campo.setAttribute('aria-invalid', 'true');

    var aviso = erroDo(campo);
    if (!aviso) {
      aviso = document.createElement('p');
      aviso.className = 'field__error';
      aviso.id = campo.id + '-erro';
      var onde = caixa ? (caixa.querySelector('.field__hint') || null) : null;
      if (onde && onde.parentElement === caixa) { caixa.insertBefore(aviso, onde); }
      else if (caixa) { caixa.appendChild(aviso); }
    }
    aviso.textContent = texto;

    var descricao = (campo.getAttribute('aria-describedby') || '').split(/\s+/)
      .filter(function (id) { return id && id !== aviso.id; });
    descricao.push(aviso.id);
    campo.setAttribute('aria-describedby', descricao.join(' '));
  }

  function problema(campo) {
    if (campo.type === 'checkbox') {
      return campo.checked ? '' : 'Obrigatório';
    }

    var valor = (campo.value || '').trim();

    if (!valor) { return 'Obrigatório'; }

    if (campo.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(valor)) {
      return 'E-mail incompleto';
    }

    return '';
  }

  formulario.addEventListener('submit', function (evento) {
    evento.preventDefault();

    var primeiro = null;

    REGRAS.forEach(function (regra) {
      var campo = document.getElementById(regra.id);
      if (!campo) { return; }

      limpar(campo);

      if (problema(campo)) {
        marcarErro(campo, regra.mensagem);
        if (!primeiro) { primeiro = campo; }
      }
    });

    if (primeiro) {
      if (recado) {
        recado.textContent = 'Falta preencher um campo ou mais. Os campos com problema estão marcados abaixo.';
      }
      primeiro.focus();
      return;
    }

    if (recado) {
      recado.textContent = 'Mensagem de exemplo recebida. Este protótipo não envia e-mail: no site, '
        + 'quem recebe é contato@iaracosta.com.br e a resposta sai em até 24 horas úteis.';
    }
  });

  /* Ao corrigir um campo, o aviso daquele campo sai da tela na hora. */
  formulario.addEventListener('input', function (evento) {
    var campo = evento.target;
    if (!campo || !campo.id) { return; }
    if (campo.hasAttribute('aria-invalid')) { limpar(campo); }
  });

  formulario.addEventListener('change', function (evento) {
    var campo = evento.target;
    if (!campo || !campo.id) { return; }
    if (campo.hasAttribute('aria-invalid')) { limpar(campo); }
  });
})();
