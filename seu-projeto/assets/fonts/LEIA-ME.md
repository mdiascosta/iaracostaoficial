# Fontes da marca: como hospedar localmente

**Por que esta pasta existe:** no protótipo, as fontes Jost e Playfair Display
são carregadas do Google Fonts. Isso funciona, mas envia o endereço IP de cada
visitante para um servidor de terceiro. Em produção, o projeto prevê servir as
fontes do próprio domínio, o que melhora a privacidade (LGPD), tira uma
requisição externa e costuma acelerar o carregamento.

---

## 1. Quais pesos são usados

Só estes. Carregar peso que ninguém usa é peso morto na página.

| Fonte            | Peso | Onde é usada                                          |
|------------------|------|-------------------------------------------------------|
| Jost             | 400  | Todo o texto de interface: menus, corpo, preços, botões |
| Jost             | 600  | Botões, rótulos, destaques                            |
| Playfair Display | 400  | Logo, títulos H1 e H2, citações                       |

## 2. Licença

Ambas são distribuídas sob a **SIL Open Font License (OFL)**, que permite usar,
modificar e redistribuir, inclusive em site comercial, desde que os arquivos de
licença sejam mantidos junto.

**[CONFERIR]** Antes de subir, confirme a licença atual na página oficial de cada
família. Guarde o arquivo de licença (`OFL.txt`) dentro desta pasta, junto com as
fontes. A equipe da Iara Costa é responsável por manter essa comprovação.

## 3. Como obter os arquivos

Baixe apenas de fonte oficial:

1. Página da família no **Google Fonts**.
2. Baixe o pacote da família (o botão de download entrega `Jost.zip` e
   `PlayfairDisplay.zip`, ou a família variável).
3. Descompacte e localize os arquivos `.woff2` (formato web, o mais leve) e, se
   houver, `.ttf` (formato de reserva).

Nomes esperados aqui dentro, já no padrão da pasta:

```
assets/fonts/
├── LEIA-ME.md
├── OFL.txt                  (licença das duas famílias)
├── jost-400.woff2
├── jost-600.woff2
└── playfairdisplay-400.woff2
```

Se você baixar a versão variável (um único arquivo com todos os pesos), mantenha
o nome `jost-variable.woff2` para não confundir a equipe.

**[CONFERIR]** Este projeto não inclui os arquivos `.woff2` porque o download
precisa ser feito pela equipe, na origem oficial. Não use fontes baixadas de
sites de agregadores desconhecidos.

## 4. O que a equipe precisa fazer no elemento <head>

Aqui no protótipo, mantenha como está para visualizar. **Em produção**, troque as
três linhas do Google pelo bloco abaixo, e apague a linha de `fonts.googleapis.com`:

```html
<link rel="preload" href="assets/fonts/jost-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/playfairdisplay-400.woff2" as="font" type="font/woff2" crossorigin>
```

E acrescente isto no arquivo de CSS da marca:

```css
@font-face {
  font-family: "Jost";
  src: url("../fonts/jost-400.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Jost";
  src: url("../fonts/jost-600.woff2") format("woff2");
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Playfair Display";
  src: url("../fonts/playfairdisplay-400.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

O `font-display: swap` faz o texto aparecer com a fonte de reserva enquanto a
fonte baixa, evitando a tela em branco.

## 5. No Elementor (Bloco B)

O Elementor Pro e o Elementor Free recentes têm a opção de servir Google Fonts
localmente. Se usar esse caminho:

1. Painel do WordPress, **Elementor** e depois **Configurações** e depois **Avançado**.
2. Ative **Carregar Google Fonts localmente**.
3. Salve e limpe o cache.
4. Confirme no navegador, na aba Rede, que nenhuma requisição vai para
   `fonts.gstatic.com`.

Se preferir controle total, mantenha a opção desligada e use o `@font-face` do
item 4 diretamente no template.

## 6. Como conferir se deu certo

- Abra o site com a internet do celular e verifique se as fontes aparecem
  corretamente, sem "pulo" de layout ao carregar.
- Na aba Rede do navegador, filtre por `font`. Os arquivos devem vir do seu
  domínio, não do Google.
- Teste no celular, porque o Safari do iPhone costuma ser o mais exigente com
  formato e cache de fonte.

## 7. Se algo der errado

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Texto aparece na fonte de reserva (Arial, Segoe UI) | Caminho do arquivo errado | Confira se a pasta é `assets/fonts/` e se o nome do arquivo bate exatamente |
| Aviso de CORS no console | Falta `crossorigin` no `preload` | Acrescente o atributo, como no item 4 |
| Fonte funciona no desktop e não no celular | Arquivo `.ttf` em vez de `.woff2`, ou cache antigo | Use `.woff2` e limpe o cache do navegador |
| Layout "pula" ao carregar | `font-display` ausente | Inclua `font-display: swap` |

## 8. Aviso para o Diário de Bordo

Quando a equipe concluir esta etapa, registre no `DIARIO-DE-BORDO.md`:

- Data da troca para fontes locais.
- Nomes e origem dos arquivos usados.
- Onde está guardado o comprovante de licença.
- Resultado do teste no celular.
