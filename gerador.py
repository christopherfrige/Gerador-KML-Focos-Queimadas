import geopandas as gpd
from fastkml import kml, styles
from sqlalchemy import create_engine, pool
from datetime import datetime, timedelta
import sys

class Arquivo:
    def __init__(self, kml_file):
        self.arquivo = kml_file
        self.logo_url = "http://queimadas.dgi.inpe.br/queimadas/portal-static/kml/images/logo.png"
        self.legenda_url = "http://queimadas.dgi.inpe.br/queimadas/portal-static/kml/images/legend.png"

    def iniciaArquivo(self):
        self.arquivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    
    # Funções abaixo necessárias pois a biblioteca FastKML não possui a propriedade "ScreenOverlay"    
    def montarLogo(self):
        logo = f"""
    <ScreenOverlay>
      <name>Logo</name>
      <Icon>
        <href>{self.logo_url}</href>
      </Icon>
      <overlayXY x="1" y="1" xunits="fraction" yunits="fraction"/>
      <screenXY x="0.99" y="0.7" xunits="fraction" yunits="fraction"/>
      <size x="0" y="0" xunits="fraction" yunits="fraction"/>
    </ScreenOverlay>"""
        self.arquivo.writelines(logo)

    def montarLegenda(self):
        legenda = f"""
    <ScreenOverlay>
      <name>Legenda</name>
      <Icon>
        <href>{self.legenda_url}</href>
      </Icon>
      <overlayXY x="1" y="1" xunits="fraction" yunits="fraction"/>
      <screenXY x="0.99" y="0.55" xunits="fraction" yunits="fraction"/>
      <size x="0" y="0" xunits="fraction" yunits="fraction"/>
    </ScreenOverlay>"""
        self.arquivo.writelines(legenda)
        
    def finalizarArquivo(self):
        fim = """
  </Document>
</kml>
        """
        self.arquivo.writelines(fim)


NOME_ARQUIVO_KML = f"kml_geopandas_com_db.kml"
# Entrada de dados por meio de argumento
if sys.argv[-1][:2] == "20":
    DATA_ATUAL = sys.argv[-1].replace("-", "")
    NOME_ARQUIVO_KML = f"kml_geopandas_com_db-{DATA_ATUAL}.kml"
    DATA_ATUAL = datetime.strptime(DATA_ATUAL, "%Y%m%d")
else:
    DATA_ATUAL = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
DATA_INICIAL = DATA_ATUAL - timedelta(days=1)

# Lista de satélites e cores correspondentes
SATELITES = ['AQUA_M-M', 'AQUA_M-T', 'GOES-16', 'METOP-B', 'METOP-C', 'MSG-03',
            'NOAA-18', 'NOAA-19', 'NOAA-20', 'NPP-375', 'TERRA_M-M', 'TERRA_M-T']
CORES = ('ff00ff00', 'ff00ff00', 'ffff1d00', 'ff14f0ff', 'ffcc3cf0', 'ffffff00',
            'ff0099ff', 'ff003399', 'ff6666ff', 'FFda01C1', 'ffccffcc', 'ffccffcc')

k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'

# SEÇÃO DOS ESTILOS

# Estilos Buffers
estilos = []
poly_normal = styles.PolyStyle(ns=ns, color='4614B4FF')
line_normal = styles.LineStyle(ns=ns, color='FFFFFFFF', width=1)
style_polygon_normal = styles.Style(styles = [poly_normal, line_normal])

poly_highlight = styles.PolyStyle(ns=ns, color='1e14B4FF')
line_highlight = styles.LineStyle(ns=ns, color='FF0000FF', width=1)
style_polygon_highlight = styles.Style(styles = [poly_highlight, line_highlight])

stylemap_polygon = styles.StyleMap(normal=style_polygon_normal, highlight=style_polygon_highlight, id='poly-foco')

estilos.append(stylemap_polygon)

# Estilos Focos
for i in range(len(SATELITES)):
    icon_style = styles.IconStyle(icon_href='http://maps.google.com/mapfiles/kml/shapes/placemark_square.png', scale=0.8, color=CORES[i])
    label_style = styles.LabelStyle(ns=ns, scale=0)
    lista_styles = styles.Style(styles = [icon_style, label_style], id=SATELITES[i])
    estilos.append(lista_styles)

# Cria o documento e anexa nele a lista de estilos anteriormente criada
documento = kml.Document(ns=ns, name='Monitoramento de Queimadas Focos e Buffers', description='Monitoramento de queimadas em tempo Real', styles=estilos)
k.append(documento)

engine = create_engine(f'postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE', poolclass=pool.NullPool)

sql = f"""
select 
    to_char(f.latitude, '999D999999') as latitude, 
    to_char(f.longitude, '999D999999') as longitude, 
    f.cod_sat, 
    f.data_pas,
    f.name_1 as estado,
    f.name_2 as municipio,
    f.versao,
    f.geom as geom,
    st_buffer(f.geom, 0.005, 'endcap=square') as geom_buffer
from
    public.focos_operacao as f
where
    id_0 = 33 and
    (f.data_pas>='{DATA_INICIAL}' and f.data_pas::date <= '{DATA_ATUAL}') 
"""

# Faz a query, monta um dataframe com o resultado e converte a coluna "geom" para objeto geometry
df = gpd.GeoDataFrame.from_postgis(sql=sql, con=engine, geom_col='geom', crs=4326)
# Converte a coluna geom_buffer para objeto geometry
df['geom_buffer'] = gpd.GeoSeries.from_wkb(df['geom_buffer'])

# Cria a Folder principal
mainFolder = kml.Folder(ns=ns, name='Focos por Satélite', description='Focos do último dia categorizado pelo satélite que o captou')
documento.append(mainFolder)

bufferFolder = kml.Folder(ns=ns, name='Buffers', description='Área de cobertura em torno de determinado foco')
pontoFolder = kml.Folder(ns=ns, name='Pontos', description='Local onde o satélite registrou o foco')

mainFolder.append(bufferFolder)
mainFolder.append(pontoFolder)

satelites_folders_names = []
ponto_objects = []
buffer_objects = []
for foco in df.itertuples():
    # Para organizar os focos em pastas, e não recriá-las
    if not foco.cod_sat in satelites_folders_names:
        satelite_ponto_folder = kml.Folder(ns=ns, name=foco.cod_sat)
        pontoFolder.append(satelite_ponto_folder)
        ponto_objects.append(satelite_ponto_folder)
        
        satelite_buffer_folder = kml.Folder(ns=ns, name=foco.cod_sat)
        bufferFolder.append(satelite_buffer_folder)
        buffer_objects.append(satelite_buffer_folder)

        satelites_folders_names.append(foco.cod_sat)

    descricao = f"""LAT = {foco.latitude}
    LONG = {foco.longitude}
    DATA = {foco.data_pas}
    SATÉLITE = {foco.cod_sat}
    ESTADO = {foco.estado}
    MUNICÍPIO = {foco.municipio}
    VERSÃO = {foco.versao}
    """
        
    ponto = kml.Placemark(ns=ns, name=foco.cod_sat, description=descricao, styleUrl=foco.cod_sat)
    ponto.geometry = foco.geom

    buffer = kml.Placemark(ns=ns, name=foco.cod_sat, styleUrl='poly-foco')
    buffer.geometry = foco.geom_buffer
    
    pasta_atual_ponto = ponto_objects[satelites_folders_names.index(foco.cod_sat)]  
    pasta_atual_ponto.append(ponto)
    
    pasta_atual_buffer = buffer_objects[satelites_folders_names.index(foco.cod_sat)] 
    pasta_atual_buffer.append(buffer)

with open(NOME_ARQUIVO_KML, 'w+') as kml_file:
    arquivo = Arquivo(kml_file)
    arquivo.iniciaArquivo()
    # slicing de -22 para remover as propriedades </Document> e </kml>
    # para tornar possível a adição de Screens Overlays (manualmente)
    kml_file.writelines(k.to_string(prettyprint=True)[:-22])
    arquivo.montarLogo()
    arquivo.montarLegenda()
    arquivo.finalizarArquivo()