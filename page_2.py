#------------------------------------------------------------
# bibliotecas
import pandas as pd
import plotly.express as px
import streamlit as st

from utils import data_process, graf_preco, remove_outlier
from filtros import filtro_paises, filtro_notas

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

st.sidebar.markdown('## Notas')
notas = filtro_notas('Este filtro altera todas as visualizações desta página')

st.sidebar.divider()
#-------------------------------------------------------------------

# Aplicando Filtros da barra lateral

df1 = df1.loc[df1['country'].isin(paises), :]
df1 = df1.loc[df1['aggregate_rating'].between(notas[0], notas[1]), :]

#========================================================================

st.title('🌎 Visão Países')
st.divider()

with st.container():
    df_aux = df1.loc[:, ['restaurant_id', 'country']].groupby('country').nunique().sort_values('restaurant_id', ascending=False).reset_index()
    fig = px.bar(df_aux, 
                 x='country', 
                 y='restaurant_id', 
                 text='restaurant_id', 
                 labels={'country':'País', 
                         'restaurant_id':'Quantidade de Restaurantes'})
    
    fig.update_layout(title={'text': 'Quantidade de Restaurantes registrados por País',
                              'y':0.95, 
                              'x': 0.5 , 
                              'xanchor': 'center', 
                              'yanchor': 'top'})
    
    st.plotly_chart(fig)


with st.container():
    df_aux = df1.loc[:, ['city', 'country']].groupby('country').nunique().sort_values('city', ascending=False).reset_index()
    fig = px.bar(df_aux, 
                 x='country', 
                 y='city', 
                 text='city', 
                 labels={'country':'País', 
                         'city':'Quantidade de Cidades'})
    
    fig.update_layout(title={'text': 'Quantidade de Cidades registradas por País', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    st.plotly_chart(fig)


with st.container():
    col1, col2 = st.columns(2, gap='large', vertical_alignment='bottom')

    with col1:
        st.markdown(' ')

    with col2:
        conv = st.toggle('Ative a conversão das moedas para Real (R$)',
                         help= 'Este Filtro altera apenas a visualização do preço médio do prato para duas pessoas')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        
        df_aux = df1.loc[:, ['votes', 'country']].groupby('country').mean().sort_values('votes', ascending=False).reset_index().round(2)
        fig = px.bar(df_aux, 
                     x='country', 
                     y='votes', 
                     text='votes', 
                     labels={'country':'País', 
                             'votes':'Quantidade de Avaliações'})
        
        fig.update_layout(title={'text': 'Média de Avaliações feitas por País', 
                                 'y':0.95, 
                                 'x': 0.5 , 
                                 'xanchor': 'center', 
                                 'yanchor': 'top'})
        
        st.plotly_chart(fig)



    with col2:
        if 'Australia' in paises:
            df2 = remove_outlier(df1)

            if conv:
                fig = graf_preco(df2, 'average_cost_for_two_brl')
                st.plotly_chart(fig) # gráfico com preços convertidos
            else:
                fig = graf_preco(df2, 'average_cost_for_two')
                st.plotly_chart(fig) # gráfico com preços não convertidos
                
        else:
            if conv:
                fig = graf_preco(df1, 'average_cost_for_two_brl')
                st.plotly_chart(fig) # gráfico com preços convertidos
            else:
                fig = graf_preco(df1, 'average_cost_for_two')
                st.plotly_chart(fig) # gráfico com preços não convertidos     