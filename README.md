# Gerador-KML-Focos-Queimadas

Esse projeto foi desenvolvido no **INPE - Instituto Nacional de Pesquisas Espaciais**, e aborda a aplicação do Python com bibliotecas relacionadas a Geoprocessamento. <br>

Tendo em vista isso, este repositório aborda sobre a criação de KMLs, que consiste num formato de arquivo baseado em XML, para fazer a representação de dados geográficos em aplicativos, como por exemplo o Google Earth. <br>
*Mais informações sobre o formato KML [aqui](https://developers.google.com/kml/documentation).*

Dessa forma, apesar de todos os testes no **Jupyter Notebook** estarem utilizando a biblioteca FastKML, foi estudado diferentes formas de ingestão de dados e criação do arquivo, seja por meio do Pandas atuando com um CSV, ou realizando consultas ao banco de dados PostgreSQL.

<img src=https://i.imgur.com/tvz3RWF.jpeg>

***Pontos coloridos:** Focos de Queimadas, com cor baseada no intervalo desde que ocorreu (legenda).*

<img src=https://i.imgur.com/R5WmvV6.jpeg>

***Área em laranja:** Frente de Fogo Ativo do dia atual (área de 500m ao redor do foco). <br>
**Área em preto:** Frente de Fogo Ativo do dia anterior.*

## Requisitos

- **Python** com versão entre **3.6** e **3.9**
- **Bibliotecas**: 
  - *fastkml* ([documentação](https://fastkml.readthedocs.io/en/latest/))
  - *psycopg2* ([documentação](https://www.psycopg.org/docs/))
  - *SQLAlchemy* ([documentação](https://docs.sqlalchemy.org/en/14/))
  - *geopandas* ou *pandas*, dependendo da versão escolhida. ([documentação pandas](https://pandas.pydata.org/docs/)) ([documentação geopandas](https://geopandas.org/en/stable/docs.html))

## Notebooks de Estudo

Atualmente o projeto conta com três Notebooks, correspondentes aos testes de geração do arquivo KML:

- Gerar por meio de um CSV com os dados preestabelecidos, utilizando a biblioteca Pandas para a leitura, montagem e filtragem do dataframe;
- Gerar por meio de consultas no banco de dados, operação que foi feita usando a biblioteca SQLAlchemy;
- Gerar por meio de consultas no banco de dados, em que não só é obtido os pontos dos focos mas também é feito a criação de um buffer (frente de fogo ativo).

## Desenvolvimento dos notebooks

Com os dados obtidos (em que foi estudado diferentes formas para essa obtenção), construiu-se o KML a partir do FastKML, em que a geração é feita num formato semelhante a estar adicionando itens numa lista, por meio do **append**. <br>

### Pandas-CSV

A construção do projeto teve como início a leitura de um arquivo CSV gerado por meio do sistema de monitoramento **BDQueimadas**, desenvolvido pelo **INPE**. Dessa forma, por meio da biblioteca Pandas filtrou-se as colunas desejadas e trabalhou-se com os dados adquiridos. <br>

### Pandas-SQLAlchemy

Desenvolvida posteriormente à supracitada, foi construido o KML por meio de uma conexão e consulta a um banco de dados, utilizando um método nativo do pandas chamado **read_sql**, no qual foi necessário a biblioteca SQLAlchemy em conjunto com a psycopg2 para coletar os dados desejados. <br>

### GeoPandas-SQLAlchemy

Como forma de otimizar o trabalho com objetos Geo, utilizou-se a biblioteca GeoPandas que, além do pandas que está incluído nela, possui também novas libraries com classes e métodos que auxiliam as operações que precisam ser desenvolvidas.

O arquivo **gerador.py** utiliza como base essa versão, e dentro dele ela está constantemente sendo melhorada, adicionando-se funcionalidades e realizando otimizações. 

## Execução 

É necessário realizar a instalação das bibliotecas requisitadas, que podem ser feitas de duas maneiras:
  - criação de um ambiente virtual com a biblioteca **virtualenv** e usando o **pip**
  - criação de um ambiente de desenvolvimento pelo **conda**, instalando as bibliotecas posteriormente

Após a instalação das bibliotecas, fazer as modificações, dependendo da versão a ser executada:

### Pandas-CSV
Com tudo necessário instalado, alterar o arquivo CSV lido na pasta **csv**, se desejar: <br>

    file = r'csv\Focos_2021-11-01_2021-11-03.csv'

### Pandas-SQLAlchemy e GeoPandas-SQLAlchemy
Alterar as informações para o acesso ao banco de dados:

    engine = create_engine(f'postgresql+psycopg2://USER:PASS@HOST:PORT/DATABASE', poolclass=pool.NullPool)

