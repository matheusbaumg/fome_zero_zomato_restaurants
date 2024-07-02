#------------------------------------------------------------
# bibliotecas
import pandas as pd
import streamlit as st

from utils import data_process, cozinhas, rank_culinarias
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
paises = filtro_paises(df1, 'Este filtro altera a visualização da tabela e dos gráficos')

# qunatidade de restaurantes mostrados na tabela
st.sidebar.markdown('## Restaurantes')
qnt_rest = st.sidebar.slider(
    'Selecionea quantidade de Restaurantes que deseja visualizar na tabela',
    min_value=1, 
    max_value=20, 
    value=10, 
    step=1)

# seleção dos tipos de culinárias
st.sidebar.markdown('## Culinárias')
culinarias_ord = df1['cuisines'].unique()
culinarias_ord.sort()

culinarias = st.sidebar.multiselect('Selecione os Tupos de Culinárias',
                                   options=culinarias_ord,
                                   default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian'],
                                   help='Este filtro altera a visualização da tabela')

# seleção notas dos restaurantes
st.sidebar.markdown('## Notas')
notas = filtro_notas('Este filtro altera a visualização da tabela')

st.sidebar.divider()
#-------------------------------------------------------------------

# Aplicando Filtros da barra lateral

df2 = df1.loc[df1['country'].isin(paises), :] # altera tabela e gráficos

df3 = df2.loc[df1['aggregate_rating'].between(notas[0], notas[1]), :] # altera tabela
df3 = df3.loc[df1['cuisines'].isin(culinarias), :] # altera tabela

#========================================================================


st.title('🍽️ Visão Tipos de Culinárias')
st.divider()

with st.container():
    st.markdown('## Melhores Restaurantes das Principais Culinárias')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
            dados = cozinhas(df1, 'Brazilian')
                    
            st.metric(f'Brazilian: {dados[0]}', 
                    value=f'{dados[1]}/5.0', 
                    help=f'''
                                País: {dados[2]} \n
                                Cidade: {dados[3]} \n
                                Prato para dois: {dados[4]} {dados[5]}
                            ''')

    with col2:
        dados = cozinhas(df1, 'Italian')
                
        st.metric(f'Italian: {dados[0]}', 
                  value=f'{dados[1]}/5.0', 
                  help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                        ''')
 
    with col3:
        dados = cozinhas(df1, 'American')
                
        st.metric(f'American: {dados[0]}', 
                  value=f'{dados[1]}/5.0', 
                  help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                        ''')

    with col4:
        dados = cozinhas(df1, 'Japanese')
                
        st.metric(f'Japanese: {dados[0]}', 
                  value=f'{dados[1]}/5.0', 
                  help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                        ''')

    with col5:
        dados = cozinhas(df1, 'Arabian')
                
        st.metric(f'Arabian: {dados[0]}', 
                  value=f'{dados[1]}/5.0', 
                  help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                        ''')
st.divider()

with st.container():

    st.markdown(f'## Top {qnt_rest} Restaurantes')
    
    st.dataframe(df3.loc[:, ['restaurant_id','restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'average_cost_for_two_brl', 'aggregate_rating', 'votes']].
                 sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])[0:qnt_rest], 
                 use_container_width=True, 
                 hide_index=True, 
                 column_config={'restaurant_id':None,
                                 'restaurant_name': st.column_config.TextColumn('Nome do Restaurante'), 
                                 'country': 'País', 
                                 'city': 'Cidade' , 
                                 'cuisines':'Culinária', 
                                 'average_cost_for_two':st.column_config.NumberColumn('Prato para dois', 
                                                                                      width='small', 
                                                                                      help='Preço médio do prato para duas pessoas na moedas locais dos países'), 
                                 'average_cost_for_two_brl':st.column_config.NumberColumn('Prato para dois (BRL)', 
                                                                                          format='%.2f', 
                                                                                          help='Preço médio do prato para duas pessoas em Reais (R$)'), 
                                 'aggregate_rating': 'Nota Média', 
                                 'votes': 'Avaliações'})


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = rank_culinarias(df2, False)
        st.plotly_chart(fig)

    with col2:
        fig = rank_culinarias(df2, True)
        st.plotly_chart(fig)