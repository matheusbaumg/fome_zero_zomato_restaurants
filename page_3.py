#------------------------------------------------------------
# bibliotecas
import pandas as pd
import plotly.express as px
import streamlit as st

from utils import data_process
from filtros import filtro_paises

# carregando dados
df = pd.read_csv('zomato.csv')
df1 = df.copy()
# processamento dos dados
df1 = data_process(df1)

#========================================================================
# -------------------- Início configuração Streamlit --------------------

# -------------------- Barra Lateral --------------------

# Definindo Filtros

st.sidebar.markdown('## Países')
paises = filtro_paises(df1, 'Este filtro altera todas as visualizações desta página')

st.sidebar.divider()
#-------------------------------------------------------------------

# Aplicando Filtros da barra lateral

df1 = df1.loc[df1['country'].isin(paises), :]

#========================================================================

st.title('🏙️ Visão Cidades')
st.divider()

with st.container():
    df_aux = df1.loc[:, ['restaurant_id', 'city', 'country']].groupby(['city','country']).count().sort_values('restaurant_id', ascending=False).reset_index()
    fig = px.bar(df_aux.iloc[0:10], 
                 x='city', 
                 y='restaurant_id', 
                 text='restaurant_id', 
                 labels={'city':'Cidade', 
                         'restaurant_id':'Quantidade de Restaurantes', 
                         'country': 'País'}, 
                 color='country')
    
    fig.update_layout(title={'text': 'Top 10 Cidades com mais Restaurantes registrados', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    st.plotly_chart(fig)


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        df_aux = df1.loc[df1['aggregate_rating'] >= 4 , ['restaurant_id', 'city', 'country']].groupby(['city', 'country']).count().sort_values('restaurant_id', ascending=False).reset_index()
        fig = px.bar(df_aux.iloc[0:7], 
                     x='city', 
                     y='restaurant_id', 
                     text='restaurant_id', 
                     labels={'city': 'Cidade', 
                             'restaurant_id':'Quantidade de Restaurantes', 
                             'country':'País'}, 
                     color='country')
        
        fig.update_layout(title={'text': 'Top 7 Cidades com Restaurantes com Média de Avaliação acima de 4', 
                                 'y':0.95, 
                                 'x': 0.5 , 
                                 'xanchor': 'center', 
                                 'yanchor': 'top'})
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_aux = df1.loc[df1['aggregate_rating'] <= 2.5, ['restaurant_id', 'city', 'country']].groupby(['city', 'country']).count().sort_values('restaurant_id', ascending=False).reset_index()
        fig = px.bar(df_aux.iloc[0:7], 
                     x='city', 
                     y='restaurant_id', 
                     text='restaurant_id', 
                     labels={'city':'Cidade', 
                             'restaurant_id':'Quantidade de Restaurantes', 
                             'country':'País'}, 
                     color='country')
        
        fig.update_layout(title={'text': 'Top 7 Cidades com Restaurantes com Média de Avaliação abaixo de 2.5', 
                                 'y':0.95, 
                                 'x': 0.5 , 
                                 'xanchor': 'center', 
                                 'yanchor': 'top'})
        
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    df_aux = df1.loc[:, ['cuisines', 'city', 'country']].groupby(['city', 'country']).nunique().sort_values('cuisines', ascending=False).reset_index()
    fig = px.bar(df_aux.iloc[0:10], 
                 x='city', 
                 y='cuisines', 
                 text='cuisines', 
                 labels={'city':'Cidades', 
                         'cuisines':'Quantidade de Tipos Culinários Únicos', 
                         'country':'País'}, 
                 color='country')
    
    fig.update_layout(title={'text': 'Top 10 Cidades com mais Restaurantes com tipos de Cullinárias diferentes', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    st.plotly_chart(fig)