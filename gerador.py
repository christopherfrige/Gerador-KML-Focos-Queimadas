from time import time
import geopandas as gpd
from fastkml import kml, styles
from sqlalchemy import create_engine, pool
from datetime import datetime, timedelta
import sys

class Arquivo:
    def __init__(self, kml_file):
        self.arquivo = kml_file
        self.logo_url = "http://queimadas.dgi.inpe.br/queimadas/portal-static/kml/images/logo.png"
        self.legenda_url = "http://queimadas.dgi.inpe.br/queimadas/portal-static/kml/images/legend_hora.png"

    def iniciar(self):
        self.arquivo.writelines('<?xml version="1.0" encoding="UTF-8"?>')

    def finalizar(self):
        self.arquivo.writelines(f'''
    <ScreenOverlay>
      <name>Logo</name>
      <Icon>
        <href>{self.logo_url}</href>
      </Icon>
      <overlayXY x="1" y="1" xunits="fraction" yunits="fraction"/>
      <screenXY x="0.96" y="0.84" xunits="fraction" yunits="fraction"/>
      <size x="0" y="0" xunits="fraction" yunits="fraction"/>
    </ScreenOverlay>
    <ScreenOverlay>
      <name>Legenda</name>
      <Icon>
        <href>{self.legenda_url}</href>
      </Icon>
      <overlayXY x="1" y="1" xunits="fraction" yunits="fraction"/>
      <screenXY x="0.99" y="0.74" xunits="fraction" yunits="fraction"/>
      <size x="0" y="0" xunits="fraction" yunits="fraction"/>
    </ScreenOverlay>
  </Document>
</kml>
''')

ENGINE = create_engine(f'postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE', poolclass=pool.NullPool)
CORES = ('ff00008b', 'ff2222b2', 'ff0000ff', 'ff4763ff', 'ff507fff', 'ff7aa0ff',
    'ff13458b', 'ff0b86b8', 'ff20a5da', 'ff60a4f4', 'ff87b8de', 'ffb3def5',
    'ffe16941', 'ffffbf00', 'ffffff00', 'ffd1ce00', 'ffd0e040', 'ffd4ff7f',
    'ff008000', 'ff32cd32', 'ff2fffad', 'ff9afa00', 'ff7fff00', 'ff90ee90', 'ff98fb98')
NOME_ARQUIVO_KML = f"kmls/kml_geopandas_com_db"

# Entrada de dados por meio de argumento
if sys.argv[-1][:2] == "20":
    DATA_ATUAL = sys.argv[-1].replace("-", "")
    NOME_ARQUIVO_KML = NOME_ARQUIVO_KML+"-"+DATA_ATUAL
    DATA_ATUAL = datetime.strptime(DATA_ATUAL, "%Y%m%d")
    DATA_ATUAL = DATA_ATUAL.replace(hour=23, minute=59, second=0)
else:
    DATA_ATUAL = datetime.utcnow()
DATA_INICIAL = (DATA_ATUAL - timedelta(days=1)).replace(hour=0, minute=0, second=0)

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'

# SEÇÃO DOS ESTILOS // cores em AA-GG-BB-RR
# Estilos Buffers
def criar_estilo_polygon(cor_polygon, cor_line, largura):
    polygon_style = styles.PolyStyle(ns=ns, color=cor_polygon)
    line_style = styles.LineStyle(ns=ns, color=cor_line, width=largura)
    return styles.Style(styles = [polygon_style, line_style])

style_polygon_normal = criar_estilo_polygon('B300A5FF', 'FF4763FF', 1)
style_polygon_highlight = criar_estilo_polygon('4D00A5FF', 'FF0000FF', 1)
style_polygon_normal_anterior = criar_estilo_polygon('CC000000', 'FF000000', 1)
style_polygon_highlight_anterior = criar_estilo_polygon('4D000000', 'FF000000', 1)

stylemap_polygon = styles.StyleMap(normal=style_polygon_normal, highlight=style_polygon_highlight, id='poly-foco')
stylemap_polygon_anterior = styles.StyleMap(normal=style_polygon_normal_anterior, highlight=style_polygon_highlight_anterior, id='poly-foco-anterior')
estilos = [stylemap_polygon, stylemap_polygon_anterior]

# Estilos Focos
for i in range(len(CORES)):
    horario = (DATA_ATUAL - timedelta(hours=i)).strftime("%Y-%m-%d %H")
    icon_style = styles.IconStyle(icon_href='http://maps.google.com/mapfiles/kml/shapes/placemark_square.png', scale=1, color=CORES[i])    
    label_style = styles.LabelStyle(ns=ns, scale=0)
    style_list = styles.Style(styles = [icon_style, label_style], id=horario)
    estilos.append(style_list)

# Cria o documento e anexa nele a lista de estilos anteriormente criada
documento = kml.Document(ns=ns, name='Monitoramento de Queimadas Focos e Buffers', description='Monitoramento de queimadas em tempo real.', styles=estilos)
k.append(documento)

# Cria a Folder principal
mainFolder = kml.Folder(ns=ns, name='Focos por Data', description='Focos de queimadas organizados por data.')
documento.append(mainFolder)

datas = [data.strftime("%Y-%m-%d") for data in [DATA_ATUAL, DATA_INICIAL]]
for data in datas:
    dateFolder = kml.Folder(ns= ns, name=data)
    mainFolder.append(dateFolder)

    sql_pontos = f"""
        SELECT 
            to_char(latitude, '999D999999') as latitude, 
            to_char(longitude, '999D999999') as longitude, 
            cod_sat, 
            data_pas,
            name_1 as estado,
            name_2 as municipio,
            geom
            FROM
                public.focos_operacao
            WHERE
                data_pas::date = '{data}'
                and id_0 = 33
                and id_1 = 50
                and id_tipo_area_industrial is null;
        """

    sql_buffers = f"""
        SELECT 
            (ST_Dump(st_union( st_buffer(geom, 0.005, 'endcap=square')))).geom as geom, 
            st_area((ST_Dump(st_union(st_buffer(geom, 0.005, 'endcap=square')))).geom::geography)/10000 as hectare,
            data_pas::date as data_pas
            FROM
                public.focos_operacao 
            WHERE
                data_pas::date = '{data}'
                and id_0 = 33
                and id_1 = 50
                and id_tipo_area_industrial is null
            GROUP BY data_pas::date
            ORDER BY data_pas;
        """



    if data == DATA_ATUAL.strftime("%Y-%m-%d"):
        focosFolder = kml.Folder(ns=ns, name='Focos', description='Local onde o satélite registrou o foco.')
        dateFolder.append(focosFolder)

        # Faz a query, monta um dataframe com o resultado e converte a coluna "geom" para objeto geometry
        df_pontos = gpd.GeoDataFrame.from_postgis(sql=sql_pontos, con=ENGINE, geom_col='geom', crs=4326)

        hourFolder_nomes = []
        hourFolder_objetos = []
        for foco in df_pontos.itertuples():
            #if foco.data_pas.hour == df_pontos.data_pas.dt.hour.max(): Para mostrar apenas a ultima passagem
            data_styleUrl = foco.data_pas.strftime("%Y-%m-%d %H")
            intervalo = f"{DATA_ATUAL.hour - foco.data_pas.hour}h"
    
            descricao = f"""<b>LAT =</b> {foco.latitude}<br>
            <b>LONG =</b> {foco.longitude}<br>
            <b>DATA =</b> {foco.data_pas}<br>
            <b>SATÉLITE =</b> {foco.cod_sat}<br>
            <b>ESTADO =</b> {foco.estado}<br>
            <b>MUNICÍPIO =</b> {foco.municipio}<br>
            <b>INTERVALO =</b> {intervalo} (UTC: {DATA_ATUAL.strftime('%H:%M:%S')})<br>   
            """
            
            ponto = kml.Placemark(ns=ns, name=data, description=descricao, styleUrl=data_styleUrl)
            ponto.geometry = foco.geom

            if not intervalo in hourFolder_nomes:
                hourFolder = kml.Folder(ns=ns, name=intervalo)
                focosFolder.append(hourFolder)
                hourFolder.append(ponto)
                hourFolder_nomes.append(intervalo)
                hourFolder_objetos.append(hourFolder)
            else:
                hourFolder_objetos[hourFolder_nomes.index(intervalo)].append(ponto)

    # Faz a query, monta um dataframe com o resultado e converte a coluna "geom" para objeto geometry
    df_buffers = gpd.GeoDataFrame.from_postgis(sql=sql_buffers, con=ENGINE, geom_col='geom', crs=4326)

    bufferFolder = kml.Folder(ns=ns, name='Frentes de Fogo Ativo', description='Área de cobertura em torno de determinado foco.')
    dateFolder.append(bufferFolder)

    for foco_buffer in df_buffers.itertuples():
        buffer = kml.Placemark(
        ns = ns, 
        name = 'Frente de Fogo Ativo', 
        description = f'''<b>Data de ocorrência:</b> <br>{data}<br><br>
        <b>Área:</b> {round(foco_buffer.hectare)} ha''', 
        styleUrl = 'poly-foco' if data == DATA_ATUAL.strftime("%Y-%m-%d") else 'poly-foco-anterior')

        buffer.geometry = foco_buffer.geom
        bufferFolder.append(buffer)

with open(f"{NOME_ARQUIVO_KML}.kml", 'w+') as kml_file:
    arquivo = Arquivo(kml_file)
    arquivo.iniciar()
    # slicing de -22 para remover as propriedades </Document> e </kml>, tornando possível a adição de Screens Overlays
    kml_file.writelines(k.to_string(prettyprint=True)[:-22])
    arquivo.finalizar()