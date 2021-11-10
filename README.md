# Gerador-KML-Jupyter-Testes

Esse projeto aborda a aplicação da linguagem Python para Geoprocessamento. Com mais especificidade, a criação de KMLs, que consiste num formato de arquivo baseado em XML, para poder ser exibir dados geográficos em aplicativos, como por exemplo o Google Earth. 
*Mais informações sobre o formato KML [aqui](https://developers.google.com/kml/documentation).*

Dessa forma, apesar de todos os testes estarem utilizando o FastKML, foi estudado diferentes formas de trabalhar os dados e de gerar o arquivo, seja por meio do Pandas atuando com um CSV de dados predefinidos, ou utilizando informações obtidas por meio de consultas a um banco de dados PostgreSQL.

## Requisitos

- **Python** com versão entre **3.6.X** e **3.9.X**
- **Bibliotecas**: 
  - *fastkml* ([documentação](https://fastkml.readthedocs.io/en/latest/))
  - *psycopg2* ([documentação](https://www.psycopg.org/docs/))
  - *SQLAlchemy* ([documentação](https://docs.sqlalchemy.org/en/14/))
  - *geopandas* ou *pandas*, dependendo da versão. ([documentação pandas](https://pandas.pydata.org/docs/)) ([documentação geopandas](https://geopandas.org/en/stable/docs.html))

## Versões

Atualmente o projeto conta com três Notebooks, correspondentes aos testes:

- Gerar o arquivo KML por meio de um CSV com os dados preestabelecidos, utilizando a biblioteca Pandas para a leitura, montagem e filtragem do dataframe
- Gerar o arquivo KML por meio de consultas no banco de dados, operação que foi feita usando a biblioteca SQLAlchemy, 
- Gerar o arquivo KML por meio de consultas no banco de dados, em que não só é obtido os pontos dos focos mas também é feito a criação de um buffer (frente de fogo).

## Desenvolvimento

A maior peculiaridade envolvida nessa biblioteca KML (FastKML), e que diverge da SimpleKML (outra biblioteca amplamente utilizada, mas com seus pontos fracos), é que a utilizada nesse projeto não possui um método para a inclusão da **Logo** e **Legenda**, essa última sendo uma característica importante na hora da análise geográfica, seja pelo Google Earth ou por qualquer outra ferramenta. Assim, foi necessário desenvolver uma classe Arquivo, para atuar nessa parte da criação.

Com os dados obtidos (em que foi estudado diferentes formas para essa obtenção), construiu-se o KML a partir do FastKML, em que a geração é feita num formato semelhante a estar adicionando itens numa lista, por meio do **append**. <br>

### Pandas-CSV

A construção do projeto teve como início a leitura de um arquivo CSV gerado por meio do sistema de monitoramento BDQueimadas, desenvolvido pelo INPE. Dessa forma, por meio da biblioteca Pandas filtrou-se as colunas desejadas e trabalhou-se com os dados adquiridos. <br>

### Pandas-SQLAlchemy

Desenvolvida posteriormente à supracitada, foi construido o KML por meio de uma conexão e consulta a um banco de dados, utilizando um método nativo do pandas chamado **read_sql**, no qual foi necessário a biblioteca SQLAlchemy em conjunto com a psycopg2 para coletar os dados desejados. <br>

### GeoPandas-SQLAlchemy

Como forma de otimizar o trabalho com objetos Geo, utilizou-se a biblioteca GeoPandas que, além do pandas que está incluído nela, possui também novas libraries com classes e métodos que auxiliam as operações que precisam ser desenvolvidas.

É a versão atual e que constantemente está sendo melhorada, adicionando mais funcionalidades e realizando otimizações. O arquivo **gerador.py** é o que utiliza como base essa versão.

## Execução 

É necessário realizar a instalação das bibliotecas, que podem ser feitas de duas maneiras:
  - criação de um ambiente virtual com a biblioteca *virtualenv* e usando o *pip*
  - criação de um ambiente de desenvolvimento pelo *conda*, instalando as bibliotecas posteriormente

Após a instalação das bibliotecas, fazer as modificações, dependendo da versão a ser executada:

### Pandas-CSV
Com tudo necessário instalado, alterar o arquivo CSV lido na pasta **csv**, se desejar: <br>

    file = r'csv\Focos_2021-11-01_2021-11-03.csv'

### Pandas-SQLAlchemy e GeoPandas-SQLAlchemy
Alterar as informações para o acesso ao banco de dados:

    engine = create_engine(f'postgresql+psycopg2://USER:PASS@HOST:PORT/DATABASE', poolclass=pool.NullPool)


## Registro de Mudanças (Changelog)

Tomando como base o arquivo **gerador.py**, que contém a última versão lançada.

*Em construção*
