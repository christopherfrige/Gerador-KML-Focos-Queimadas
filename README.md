# Gerador-KML-Jupyter-Testes

Testando a criação de KMLs por meio da biblioteca FastKML.

Esse projeto é uma segunda abordagem da forma de criar KMLs, com uma biblioteca diferente da anteriormente utilizada, que antes era a SimpleKML e agora passou a ser a FastKML. <br>
*Mais informações sobre o formato KML [aqui](https://developers.google.com/kml/documentation).*

Dessa forma, apesar de todos os testes estarem utilizando a FastKML, foi estudado diferentes formas de gerar o arquivo, seja por meio de um CSV com dados predefinidos, ou utilizando informações dentro de um banco de dados.

## Desenvolvimento

### Versão Pandas-CSV

A costrução do projeto teve como início a leitura de um arquivo CSV gerado por meio do sistema de monitoramento BDQueimadas, desenvolvido pelo INPE. Dessa forma, por meio da biblioteca Pandas filtrou-se as colunas desejadas e trabalhou-se com os dados adquiridos. <br>

Com os dados obtidos, construiu-se o KML a partir da biblioteca FastKML, em que a geração do KML é feita num formato semelhante a estar adicionando itens numa lista, por meio do **append**. <br>

### Versão Pandas-SQLAlchemy

Desenvolvida posteriormente à supracitada, foi construido o KML por meio de uma conexão e consulta a um banco de dados, utilizando um método nativo do pandas chamado **read_sql**, no qual foi preciso a biblioteca SQLAlchemy em conjunto com a psycopg2 para coletar os dados desejados. <br>

A maior peculiaridade envolvida nessa biblioteca KML (FastKML), e que diverge da SimpleKML, é que a utilizada nesse projeto não possui um método para a inclusão da **Logo** e **Legenda**, essa última sendo uma característica importante na hora da análise geográfica, seja pelo Google Earth ou por qualquer outra ferramenta.

## Versões

Atualmente o projeto conta com dois Notebooks, correspondentes a dois testes:

- Gerar o arquivo KML por meio de um CSV com os dados preestabelecidos, utilizando a biblioteca Pandas para a leitura, montagem e filtragem do dataframe
- Gerar o arquivo KML por meio de consultas no banco de dados, operação que foi feita usando a biblioteca SQLAlchemy, 

## Requisitos

- **Python** com versão entre **3.6.X** e **3.9.X**
- Biblioteca **pandas** ([documentação](https://pandas.pydata.org/docs/))
- Biblioteca **fastkml** ([documentação](https://fastkml.readthedocs.io/en/latest/))
- Biblioteca **psycopg2** ([documentação](https://www.psycopg.org/docs/))
- Biblioteca **SQLAlchemy** ([documentação](https://docs.sqlalchemy.org/en/14/))

## Execução

Por conta desse projeto ter sido construído por meio do **Jupyter Notebook**, não é necessário criar um ambiente virtual. Assim, para instalar as bibliotecas necessárias basta seguir o passo a passo descrito no caderno.

Após a instalação das bibliotecas, fazer as modificações, dependendo da versão a ser executada:

### Versão Pandas-CSV
Com tudo necessário instalado, alterar o arquivo CSV lido na pasta **csv**, se desejar: <br>

    [9] file = r'csv\Focos_2021-11-01_2021-11-03.csv'

### Versão Pandas-SQLAlchemy
Alterar as informações para o acesso ao banco de dados:

    [10] engine = create_engine(f'postgresql+psycopg2://USER:PASS@HOST:PORT/DATABASE', poolclass=pool.NullPool)

