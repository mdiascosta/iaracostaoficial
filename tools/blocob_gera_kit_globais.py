#!/usr/bin/env python3
"""
Gera bloco-b/globais/iara-costa-globais.zip: o pacote de importacao das
configuracoes do site (cores e fontes globais) no formato Kit do Elementor.

Por que este arquivo existe
---------------------------
O `cores-e-fontes.json` NAO e um template: importa-lo em Templates da erro
("Tipo de modelo invalido"). A importacao de configuracoes do Elementor usa
outro caminho, o Importar/Exportar Kit, que espera um .zip com:

    manifest.json          (nome, titulo, version "2.0" e as abas presentes)
    site-settings.json     (o conteudo das configuracoes do site)

Formato conferido no codigo-fonte do Elementor:
  - app/modules/import-export/module.php (FORMAT_VERSION = "2.0");
  - app/modules/import-export/processes/export.php (manifest e add_json_file:
    o arquivo entra na raiz do zip como site-settings.json);
  - app/modules/import-export/runners/import/site-settings.php: a importacao
    cria um kit novo, mistura as configuracoes antigas com as novas e anexa
    cores e fontes personalizadas mantendo o _id de cada uma. E por manter o
    _id que os templates, que apontam para "iara-papel" etc., nascem certos
    sem precisar do tools/ajusta-ids.py.

O que entra (de proposito, so isto):
  system_colors, custom_colors, system_typography, custom_typography,
  container_width, space_between_widgets e o fundo do corpo. Nome do site,
  logo e demais ajustes ficam fora: este pacote e so de cor, fonte e largura.

Uso:
    python3 tools/blocob_gera_kit_globais.py
"""

import json
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import blocob_gera  # noqa: E402  (fonte unica das cores e fontes)

RAIZ = pathlib.Path(__file__).resolve().parents[1]
DESTINO = RAIZ / 'bloco-b' / 'globais' / 'iara-costa-globais.zip'
DATA_FIXA = (2026, 10, 19, 12, 0, 0)

ABAS = [
    'global-colors', 'global-typography', 'settings-background',
    'settings-layout', 'theme-style-typography', 'theme-style-buttons',
    'theme-style-form-fields', 'theme-style-images',
]

CHAVES = [
    'system_colors', 'custom_colors', 'system_typography', 'custom_typography',
    'container_width', 'space_between_widgets',
    'body_background_background', 'body_background_color',
]


def manifesto():
    return {
        'name': 'iara-costa-globais',
        'title': 'Iara Costa: cores e fontes',
        'description': ('Cores e fontes globais do site da Iara Costa '
                        '(15 cores e 11 fontes), para importar pelo '
                        'Importar/Exportar Kit do Elementor.'),
        'version': '2.0',
        'site-settings': ABAS,
    }


def main():
    completas = blocob_gera.site_settings()['settings']
    settings = {chave: completas[chave] for chave in CHAVES}
    site_settings = {'content': [], 'settings': settings}

    with zipfile.ZipFile(DESTINO, 'w', zipfile.ZIP_DEFLATED) as z:
        for nome, dados in (
            ('manifest.json', manifesto()),
            ('site-settings.json', site_settings),
        ):
            info = zipfile.ZipInfo(nome, DATA_FIXA)
            info.external_attr = 0o644 << 16
            z.writestr(info, json.dumps(dados, ensure_ascii=False, indent=2) + '\n')

    n_cores = len(settings['system_colors']) + len(settings['custom_colors'])
    n_fontes = len(settings['system_typography']) + len(settings['custom_typography'])
    print(f'  ok  iara-costa-globais.zip  {n_cores} cores, {n_fontes} fontes, '
          f'{DESTINO.stat().st_size} bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
