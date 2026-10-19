#!/usr/bin/env python3
"""
Gera bloco-b/iara-costa-kit-completo.zip: o KIT COMPLETO do Elementor.

Por que este arquivo existe
---------------------------
Pedido da cliente (v0.3.12): "não tem como criar algo que possa apenas
importar, pois cada alteração tenho que ficar fazendo isso". Tinha razão:
importar 24 JSONs um por um, a cada correção, é inviável. O Elementor tem
um formato próprio para isso, o Kit (Elementor > Ferramentas >
Importar/Exportar Kit): um .zip só que, numa importação, traz as
configurações do site (cores e fontes globais) E todos os templates de
uma vez, já com as condições do Theme Builder (Entire Site etc.).

Formato conferido no código-fonte (Elementor gratuito + espelho público
do Pro, lidos em 2026-10-19):
  - module.php: FORMAT_VERSION = "2.0";
  - processes/export.php: manifest.json na raiz, com name/title/
    description/version e a seção "templates"; cada template entra como
    templates/<id>.json (add_json_file acrescenta o .json);
  - runners/export/templates.php: cada arquivo de template é o
    get_export_data() do documento: {content, settings, metadata};
  - documents/theme-document.php (Pro): o resumo no manifesto ganha
    "location" e "conditions" (primeira condição include, sem sub_id);
    na importação, conditions[0] vira a condição do template. Sem
    conditions, a importação de header/footer/archive/single FALHA;
  - conditions/*.php (Pro): Entire Site = include/general; loja =
    include/archive/product_archive; blog = include/archive/post_archive;
    produto = include/singular/product; post = include/singular/post;
    busca = include/archive/search; 404 =
    include/singular/not_found404.

O que entra:
  - manifest.json          (com a seção templates, 24 itens)
  - site-settings.json     (o mesmo conteúdo do iara-costa-globais.zip)
  - templates/91NN.json    (24 arquivos: content dos bloco-b/json/*.json,
                            settings vazios e metadata com o tipo)

Limites honestos (também estão no guia, seção 3.0):
  - Reimportar CRIA CÓPIAS novas dos templates: antes de reimportar uma
    versão nova, apague os templates "Iara Costa" anteriores em
    Templates, senão eles se acumulam (o Elementor funciona assim para
    qualquer kit, não é deste arquivo).
  - Se já existir um template com a mesma condição (ex.: um cabeçalho
    Entire Site antigo), a importação pode manter a condição no antigo;
    apagar os antigos antes resolve.
  - Templates pedem Elementor Pro (a cliente tem): o runner de templates
    do kit só roda com Pro ativo.

Uso:
    python3 tools/blocob_gera_kit_completo.py
"""

import json
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import blocob_gera  # noqa: E402
import blocob_gera_kit_globais as kit_globais  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA_JSON = RAIZ / 'bloco-b' / 'json'
DESTINO = RAIZ / 'bloco-b' / 'iara-costa-kit-completo.zip'
DATA_FIXA = (2026, 10, 19, 12, 0, 0)

# Condições do Theme Builder por arquivo (conferidas no código, ver acima).
# Arquivos 'page' não são documentos de tema: sem location/conditions,
# como num export real de template de página.
CONDICOES = {
    '01-cabecalho.json': ('header', ('general', '', '')),
    '02-rodape.json': ('footer', ('general', '', '')),
    '04-loja.json': ('archive', ('archive', 'product_archive', '')),
    '05-produto.json': ('single', ('singular', 'product', '')),
    '11-blog.json': ('archive', ('archive', 'post_archive', '')),
    '12-post.json': ('single', ('singular', 'post', '')),
    '13-busca.json': ('archive', ('archive', 'search', '')),
    '14-404.json': ('single', ('singular', 'not_found404', '')),
}

ID_BASE = 9100


def condicao(nome_arquivo):
    location, (nome, sub_nome, sub_id) = CONDICOES[nome_arquivo]
    return location, [{
        'type': 'include',
        'name': nome,
        'sub_name': sub_nome,
        'sub_id': sub_id,
    }]


def main():
    arquivos = sorted(PASTA_JSON.glob('*.json'))
    if len(arquivos) != 24:
        print(f'esperados 24 templates, achei {len(arquivos)}')
        return 1

    templates_manifest = {}
    arquivos_templates = []  # (nome no zip, dados)
    for indice, caminho in enumerate(arquivos, 1):
        doc_id = str(ID_BASE + indice)
        dados = json.loads(caminho.read_text(encoding='utf-8'))
        resumo = {
            'title': dados['title'],
            'doc_type': dados['type'],
            'thumbnail': None,
        }
        if caminho.name in CONDICOES:
            location, conditions = condicao(caminho.name)
            resumo['location'] = location
            resumo['conditions'] = conditions
        templates_manifest[doc_id] = resumo
        arquivos_templates.append((f'templates/{doc_id}.json', {
            'content': dados['content'],
            'settings': dados['page_settings'] if dados['page_settings'] else {},
            'metadata': {'_elementor_template_type': dados['type']},
        }))

    # site-settings: o mesmo conteúdo do pacote de globais
    completas = blocob_gera.site_settings()['settings']
    settings = {chave: completas[chave] for chave in kit_globais.CHAVES}
    site_settings = {'content': [], 'settings': settings}

    manifesto = {
        'name': 'iara-costa-kit-completo',
        'title': 'Iara Costa: kit completo do site',
        'description': ('Kit completo da Iara Costa: configuracoes globais '
                        '(15 cores, 11 fontes) e os 24 templates (cabecalho, '
                        'rodape e as 22 paginas), ja com as condicoes do '
                        'Theme Builder. Importar em Elementor > '
                        'Ferramentas > Importar/Exportar Kit.'),
        'author': 'Iara Costa',
        'version': '2.0',
        'site-settings': kit_globais.ABAS,
        'templates': templates_manifest,
    }

    with zipfile.ZipFile(DESTINO, 'w', zipfile.ZIP_DEFLATED) as z:
        def gravar(nome, dados):
            info = zipfile.ZipInfo(nome, DATA_FIXA)
            z.writestr(info, json.dumps(dados, ensure_ascii=False, indent=2))

        gravar('manifest.json', manifesto)
        gravar('site-settings.json', site_settings)
        for nome, dados in arquivos_templates:
            gravar(nome, dados)

    print(f'  ok  {DESTINO.relative_to(RAIZ)}  24 templates + globais, '
          f'{DESTINO.stat().st_size} bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
