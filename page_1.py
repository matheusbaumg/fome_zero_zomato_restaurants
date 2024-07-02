#------------------------------------------------------------
#bibliotecas
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from utils import data_process
from filtros import filtro_paises, filtro_notas

# carregamento dos dados 
df = pd.read_csv('zomato.csv')
df1 = df.copy()
# processamento dos dados
df1 = data_process(df1)

#========================================================================
# -------------------- Início configuração Streamlit --------------------

# -------------------- Barra Lateral -------------------- 

with st.sidebar.container():
    col1, col2 = st.columns(2, vertical_alignment='center')

    with col1:
        col1.image('logo5.png', width=130)

    with col2:
        st.markdown('# Fome Zero!')
        
st.sidebar.divider()

# Definindo Filtros

st.sidebar.markdown('## Países')
paises = filtro_paises(df1, 'Altera os restaurantes exibidos no mapa')

st.sidebar.markdown('## Notas')
notas = filtro_notas('Altera os restaurantes exibidos no mapa')

st.sidebar.divider()

# rodapé da Barra Lateral
st.sidebar.markdown('##### Desenvolvido por')
st.sidebar.markdown('##### Matheus Maranho Baumguertner')
st.sidebar.markdown('##### @matheusbaumg')
#-------------------------------------------------------------------

# Aplicando filtros da barra lateral

# o filtro vai ser aplicado apenas ao mapa, nos numeros apresentados no topo não interfere
df2 = df1.loc[df1['country'].isin(paises), :]
df2 = df2.loc[df2['aggregate_rating'].between(notas[0], notas[1]), :]

#========================================================================

# linha 1
with st.container():
    st.title('Fome Zero!')
    st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.divider()

# linha 2
with st.container():
    st.subheader('Temos as seguintes marcas dentro da nossa plataforma:')

    col1, col2, col3, col4, col5 = st.columns(5)

    # linha 2, coluna 1
    with col1:
        nrestaurantes = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', f'{nrestaurantes:,}'.replace(',', '.'))

    #linha 2, coluna 2
    with col2:
        npaises = df1['country'].nunique()
        col2.metric('Paises Cadastrados', npaises)

    #linha 2, coluna 3
    with col3:
        ncidades = df1['city'].nunique()
        col3.metric('Cidades Cadastradas', ncidades)

    # linha 2, coluna 4
    with col4:
        navaliacoes = df1['votes'].sum()
        col4.metric('Avaliações feitas na plataforma', f'{navaliacoes:,}'.replace(',', '.'))

    # linha 2, coluna 5
    with col5:
        nculinarias = df1['cuisines'].nunique()
        col5.metric('Tipos de Culinárias Oferecidas', nculinarias)

st.divider()

# linha 3 - mapa
with st.container():
    # usa o df2, df filtrado pelo filtro de países da barra lateral
    df_aux = df2.loc[:, ['latitude', 'longitude', 'restaurant_name', 'average_cost_for_two', 'currency', 'cuisines', 'aggregate_rating', 'rating_color']]
    # cria o mapa centralizado na latitude e longitude média dos pontos do dataframe
    map=folium.Map(location=[df_aux['latitude'].mean(), df_aux['longitude'].mean()], zoom_start=2)
    # marcadores agrupados
    marker_cluster = MarkerCluster().add_to(map)
    for index, location_info in df_aux.iterrows():
        popup_text = ('<h3><b>' + location_info['restaurant_name'] + '</b></h3>' + '<br>' + 
                      '<b>Price: </b>' + f'{location_info['average_cost_for_two']}' + ' ' + '(' + location_info['currency'] + ')' + ' para dois' + '<br>' + 
                      '<b>Type: </b>' + location_info['cuisines'] + '<br>' + 
                      '<b>Aggregate Rating: </b>' + f'{location_info['aggregate_rating']}' + '/5.0')

        folium.Marker([location_info['latitude'], 
                       location_info['longitude']], 
                       popup=folium.Popup(popup_text,
                                           max_width=300), 
                       icon=folium.Icon(color=location_info['rating_color'], 
                                        icon='home')).add_to(marker_cluster)
# mapa
folium_static(map, width=1024, height=600)