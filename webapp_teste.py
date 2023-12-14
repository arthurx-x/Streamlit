import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import plotly.express as px
import folium as folium
from streamlit_folium import folium_static
import altair as alt

#1 Configurando o layout e o título da página
st.set_page_config(page_title='SINASC Rondônia', layout='wide')
# Display image with specified width and height using HTML
custom_height = 300  # Set your desired custom height
st.markdown(f'<img src="https://media.giphy.com/media/FtlUfrq3pVZXVNjoxf/giphy.gif" style="width:100%; height:{custom_height}px;">', unsafe_allow_html=True)
st.title('Explorando o Streamlit - Análise SINASC 🤓👆📊')


#2 Função para carregar os dados com cache para melhorar o desempenho
@st.cache_data # Usando o decorador st.cache para aplicar o cache aos dados
def carregar_dados(caminho):
    return pd.read_csv(caminho, parse_dates=['DTNASC'])

#3 Lendo o arquivo csv e mostrando um dataframe na tela
caminho_dados = r'C:\\Users\\Arthu\\OneDrive\\Área de Trabalho\\Data Science\\notebooks\\SINASC_RO_2019.csv'
dados_nascimentos = carregar_dados(caminho_dados) # Usando um nome de variável mais descritivo

#4 Criando uma barra de progresso e uma mensagem de carregamento
with st.spinner('Carregando dados...'):
    # Inicializando a barra de progresso com 0% e um texto
    progress_bar = st.progress(0, text='Progresso: 0%')
    # Criando um espaço reservado para o texto de progresso
    progress_text = st.empty()
    # Simulando um processo demorado de 10 segundos, atualizando a barra de progresso a cada segundo
    for percent_complete in range(0, 101, 10):
        # Esperando 1 segundo
        time.sleep(1)
        # Atualizando o valor e o texto da barra de progresso
        progress_bar.progress(percent_complete)
        progress_text.text(f'Progresso: {percent_complete}%')
   
#5 Mostrando uma mensagem de sucesso quando os dados forem carregados
st.success('Dados carregados com sucesso!')

st.header('Contexto sobre o assunto 🕵')
st.video('https://www.youtube.com/watch?v=8j4pOqbPgw8')
st.markdown(f'<iframe src="https://pt.wikipedia.org/wiki/Sistema_de_informa%C3%A7%C3%A3o_em_sa%C3%BAde" width="100%" height="500"></iframe>', unsafe_allow_html=True)
st.markdown(f'<iframe src="https://cidades.ibge.gov.br/brasil/ro/panorama" width="100%" height="500"></iframe>', unsafe_allow_html=True)

#6 Limpando o texto de progresso
progress_bar.empty()
progress_text.empty()

#7 # Criando um checkbox para mostrar ou ocultar o DataFrame na barra lateral
st.sidebar.checkbox('Mostrar / Ocultar DataFrame', value=True, key='show_dataframe')
# Mostrando o dataframe na tela se o checkbox estiver marcado
if st.session_state.show_dataframe:
    st.dataframe(dados_nascimentos)
   
#8 Criando uma barra lateral com alguns widgets
st.sidebar.header('Filtro')
# Criando um slider para escolher o peso mínimo ao nascer
peso_min = st.sidebar.slider('Peso mínimo ao nascer (em gramas)', min_value=0, max_value=6000, value=0, step=100)
dados_nascimentos = dados_nascimentos[dados_nascimentos['PESO'] >= peso_min]
       
#9 Criando um gráfico de pizza com os dados de nascimentos por sexo
st.header('Visualziando os dados')
# Criando um gráfico de pizza com os dados de nascimentos por sexo usando a função st.pyplot
st.subheader('Escolaridade Mãe')
fig, ax = plt.subplots()
ax.pie(dados_nascimentos['SEXO'].value_counts(), labels=['Feminino', 'Masculino'], autopct='%1.1f%%')
ax.set_title('Distribuição dos nascimentos por sexo')
# Adicionando um texto divertido ao gráfico
ax.text(0, -1.4, 'Parabéns aos pais!', fontsize=16, color='green', ha='center')
# Mostrando o gráfico na tela com ajuste automático de largura
st.pyplot(fig, use_container_width=True)

#10 Criando alguns gráficos interativos com os dados de nascimentos por sexo, idade da mãe, peso ao nascer, etc.
st.header('Gráficos de nascimentos por variáveis')
# Criando um gráfico de pizza com os dados de nascimentos por sexo usando a função st.plotly_chart
st.subheader('Escolaridade Mãe')
fig1 = px.pie(dados_nascimentos, names='ESCMAE', title='Distribuição da escolaridade da mãe')
st.plotly_chart(fig1, use_container_width=True)

#11 Criando um gráfico de histograma com os dados de idade da mãe usando a função st.plotly_chart
st.subheader('Idade da mãe - Histograma Interativo')
fig2 = px.histogram(dados_nascimentos, x='IDADEMAE', title='Distribuição da idade da mãe', color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig2, use_container_width=True)

#12 Criando um gráfico de dispersão com os dados de peso ao nascer e idade gestacional usando a função st.plotly_chart
st.subheader('Peso ao nascer e idade gestacional - Scatter Plot Interativo')
fig3 = px.scatter(dados_nascimentos, x='GESTACAO', y='PESO', title='Relação entre peso ao nascer e idade gestacional', color_discrete_sequence=px.colors.sequential.RdBu, marginal_x="histogram", marginal_y="histogram")
st.plotly_chart(fig3, use_container_width=True)

#13 Function to create a Folium map with a HeatMap layer
dados_nascimentos['TOTAL_FILHOS'] = dados_nascimentos[['QTDFILVIVO', 'QTDFILMORT']].sum(axis=1)
dados_nascimentos.dropna(subset=['munResLat', 'munResLon', 'TOTAL_FILHOS'], inplace=True)
# Set Mapbox access token
mapbox_access_token = 'YOUR_MAPBOX_ACCESS_TOKEN'  # Replace with your actual token
# Display the heat map using plotly.express with Mapbox
st.header('Mapa de nascimentos por município')
fig = px.scatter_mapbox(
    dados_nascimentos,
    lat='munResLat',
    lon='munResLon',
    color='TOTAL_FILHOS',
    size='TOTAL_FILHOS',
    mapbox_style='carto-darkmatter',
    zoom=5,
    color_continuous_scale='reds',
    title='Heatmap de nascimentos por município',
).update_layout(mapbox=dict(accesstoken=mapbox_access_token))
st.plotly_chart(fig, use_container_width=True)

#14 Convertendo a coluna DTNASC para objetos datetime
DTNASC = pd.to_datetime(dados_nascimentos['DTNASC'], format='%d%m%Y')
# Criando seletor de intervalo de datas na barra lateral
date_selector_expander = st.sidebar.date_input("Selecione a Data Inicial", min_value=DTNASC.min(), max_value=DTNASC.max(), value=DTNASC.min(), key='date_selector', format="DD/MM/YYYY")
end_date = st.sidebar.date_input("Selecione a Data Final", min_value=DTNASC.min(), max_value=DTNASC.max(), value=DTNASC.max(), key='end_date', format="DD/MM/YYYY")
# Convertendo as datas selecionadas para objetos datetime
start_date, end_date = pd.to_datetime(date_selector_expander, format="%Y-%m-%d"), pd.to_datetime(end_date, format="%Y-%m-%d")
# Filtrando os dados com base no intervalo de datas selecionado
filtered_data = dados_nascimentos[(DTNASC >= start_date) & (DTNASC <= end_date)]
# Exibindo informações do intervalo de datas na barra lateral
date_info = f"**Intervalo de Datas Selecionado:**\n\nInício: {start_date.strftime('%d/%m/%Y')}\n\nFim: {end_date.strftime('%d/%m/%Y')}"
st.sidebar.info(date_info)
# Estilizando o fundo do texto na barra lateral para verde
st.markdown(
    """
    <style>
    div[data-testid="stSidebar"] .stAlert {
        background-color: green;
    }
    </style>
    """,
    unsafe_allow_html=True)

#15 Mostrando uma mensagem de aviso se as datas selecionadas estiverem fora do intervalo disponível
if start_date < DTNASC.min() or end_date > DTNASC.max():
    st.warning('Atenção: Certifique-se de que as datas selecionadas estão dentro do intervalo disponível.')
    
#16 Gerador de Gráfico
st.title('Gerador de Gráfico')
st.write("Selecione as colunas para o gráfico:")
coluna_categoria = st.selectbox("Selecione a coluna de categoria", dados_nascimentos.columns, key='coluna_categoria')
coluna_valor = st.selectbox("Selecione a coluna de valor", dados_nascimentos.columns, key='coluna_valor')
# Function for plotting a bar chart with Altair
def plot_grafico(df, categoria_col, valor_col):
    df[categoria_col] = df[categoria_col].astype(str)
    chart = alt.Chart(df).mark_bar().encode(
        x=categoria_col,
        y=valor_col,
        tooltip=[categoria_col, valor_col]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
# Button click event to generate the chart
if st.button("Gerar Gráfico"):
    # Check if selected columns are valid
    if coluna_categoria in dados_nascimentos.columns and coluna_valor in dados_nascimentos.columns:
        plot_grafico(dados_nascimentos, coluna_categoria, coluna_valor)
    else:
        st.error("Selecione colunas válidas para o gráfico.")
      
#17 Espaço reservado para GIF no final
st.title('Por hoje é isso!✌')
custom_height = 300  # Set your desired custom height
st.markdown(f'<img src="https://i.kym-cdn.com/photos/images/newsfeed/002/054/274/08a.gif" style="width:100%; height:{custom_height}px;">', unsafe_allow_html=True)

#18 Sugestões de Melhoria/ Solicitações
with st.expander('Sugestões de Melhoria/ Solicitações'):
    # Function to add a task to the list
    def adicionar_tarefa(tarefa, lista_tarefas):
        lista_tarefas.append(tarefa)
    # Function to display tasks in a numbered list
    def exibir_tarefas(lista_tarefas):
        st.write("Lista:")
        # Use st.text instead of st.markdown for simplicity
        for i, tarefa in enumerate(lista_tarefas, start=1):
            st.text(f"{i}. {tarefa}")
    lista_tarefas = []
    tarefa = st.text_input("Digite")
    # Button click event to add a task
    if st.button("Adicionar") and tarefa:
        adicionar_tarefa(tarefa, lista_tarefas)
    # Display the list of tasks
    exibir_tarefas(lista_tarefas)
