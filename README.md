# Gerador-KML-Jupyter-Testes

Testando a criação de KMLs por meio da biblioteca FastKML.

Esse projeto é uma segunda abordagem da forma de criar KMLs, com uma biblioteca diferente da anteriormente utilizada, que antes era a SimpleKML e agora passou a ser a FastKML. <br>
*Mais informações sobre o formato KML [aqui](https://developers.google.com/kml/documentation).*

## Desenvolvimento

A costrução do projeto teve como início a leitura de um arquivo CSV gerado por meio do sistema de monitoramento BDQueimadas, desenvolvido pelo INPE. Dessa forma, por meio da biblioteca Pandas filtrou-se as colunas desejadas e as transformou numa lista de tuplas, em que cada índice corresponde a uma linha. <br>

Com os dados obtidos, construiu-se o KML a partir da biblioteca FastKML, em que a geração do KML é feita num formato semelhante a estar adicionando itens numa lista, por meio do **append**. <br>

A maior peculiaridade envolvida nessa biblioteca KML (FastKML), e que diverge da SimpleKML, é que a utilizada nesse projeto não possui um método para a inclusão da **Logo** e **Legenda**, essa última sendo uma característica importante na hora da análise geográfica, seja pelo Google Earth ou por qualquer outra ferramenta.

## Requisitos

- **Python** com versão entre **3.6.X** e **3.9.X**
- Biblioteca **pandas** ([documentação](https://pandas.pydata.org/docs/))
- Biblioteca **fastkml** ([documentação](https://simplekml.readthedocs.io/en/latest/))

## Execução

Por conta desse projeto ter sido construído por meio do **Jupyter Notebook**, não é necessário criar um ambiente virtual. Assim, para instalar as bibliotecas necessárias (pandas e fastKML), executar no terminal:

    pip install -r requirements.txt

Com tudo necessário instalado, alterar o arquivo CSV lido na pasta **csv**, se desejar: <br>
![](https://i.imgur.com/qPpMSH9.png)

Agora resta fazer a execução, em que nesse caso foi utilizado o Jupyter Notebook.
