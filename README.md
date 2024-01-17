# Covid-19 Dashboard

## EN
_In this repository, you will find various files related to a completed project. These include a detailed project report, a file containing the necessary libraries to run the code, a geojson file with identification of all countries in the world, the dashboard logo, and the Python code for the project implementation._

Files:
* Water Potability.ipynb: contains the Jupyter notebook with the project code
* water_potability.xls: contains the data used in the project
* Water Quality Prediction Report.pdf: project report in English
* Relatório da Previsão da Qualidade da Água.pdf: project report in Portuguese
  
**Objective:**
This project primary objective is to build a Dashboard using the Dash library in Python. The Dashboard aims to illustrate active/total cases or deaths for the selected date, vaccination data, and global or country-specific hospitalizations. The user can choose the country, and the Dashboard will regularly update its data accordingly.

**Description of the Dataset:**
Coronaviruses are a family of viruses that can cause diseases in humans, ranging from mild flu-like symptoms to severe conditions such as pneumonia. The chosen dataset has 51 columns, but not all are necessary for the Dashboard. Therefore, some columns were eliminated to make the dataset manageable. The final dataset includes the following columns: iso_code, continent, location, date, population, total cases, new cases, total deaths, new deaths, ICU patients, hospitalized patients, vaccinated people, fully vaccinated people, and new vaccinations.

**Project Description:**
The project went through various stages, including:

_Design concept creation:_ Selection of visualizations to be presented, layout for displaying the visualizations, and choosing colors for each visualization.

_Implementation:_ Creation of a title consisting of an eye-catching logo, name, and a button displaying the user's chosen location. An interactive calendar was implemented, along with an interactive map using the choropleth mapbox from the plotly.express library, using a geojson file corresponding to all countries worldwide. Informative cards, a bar plot about vaccination, a pie chart showing the top 10 countries with new cases for the selected date, and finally, a scatter plot with RadioItems were also created.

## PT

_Neste repositório, encontrar-se-ão diversos ficheiros relacionados com um projeto concluído. Incluem-se um relatório detalhado do projeto, um ficheiro com as bibliotecas necessárias para correr o código, um ficheiro geojson com identificação de todos os paises do mundo, o logotipo da dashboard e o código em Python da implementação do projeto._

Ficheiros:
* Water Potability.ipynb: contém o jupyter notebook com o código do projeto
* water_potability.xls: contém os dados usados no projeto
* Water Quality Prediction Report.pdf: relatório do projeto em inglês
* Relatório da Previsão da Qualidade da Água.pdf: relatório do projeto em português
**Objetivo:**
O objetivo deste projeto é construir uma Dashboard, através da biblioteca dash do python, que visa ilustrar casos ou mortes ativos/totais/para data selecionada, vacinação e internados globalmente ou para determinado país que o utilizador escolha e que atualize os seus dados regularmente.
Como tal, foi escolhido um dataset que responde ao resultado pretendido.

**Descrição do Dataset:**
Os Coronavírus são uma família de vírus que podem causar doenças no ser humano. A infeção pode ser semelhante a uma gripe comum ou apresentar-se como doença mais grave, como pneumonia.
O dataset escolhido possui 51 colunas. No entanto, como nem todas são necessárias/úteis para a realização da Dashboard optei por eliminar algumas de forma a tornar o dataset viável. Como tal, o dataset final possui as seguintes colunas: iso_code, continente, localização, data, população, casos totais, novos casos, total de mortes, novas mortes, pacientes icu, pacientes hospitalizados, pessoas vacinadas, pessoas totalmente vacinadas, novas vacinações. 

**Descrição do Projeto:**
O projeto seguiu várias etapas, incluindo:

_Criação de ideia de design:_ Escolha de visualizações a apresentar, esquema de apresentação das visualizações e cores a usar para cada visualização.

_Implementação:_ Criação de um título composto por um logótipo chamativo, nome e botão que apresenta a localização escolhida pelo utilizador, realização de um calendário interativo, criação de um mapa interativo usando o choropleth mapbox da biblioteca plotly.express utilizando um geojson correspondente a todos os países do mundo. Foram ainda criados cartões informativos, um barplot acerca da vacinação, um pie chart com os 10 paises com mais novos casos para a data selecionada e por fim um scatter plot com um RadioItems.
