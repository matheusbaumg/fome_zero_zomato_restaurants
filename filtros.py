import streamlit as st


def filtro_paises(df, help_text):
    ''' Esta função cria o filtro de paises para a Barra Lateral do Streamlit

        Ações realizadas:
        - Encontra os paises listado no dataframe
        - Ordena esta lista de paises encontrados em ordem alfabética
        - Constroi o seletor dos países para colocar na barra lateral
        - Define os paises que ficarão selecionados por padrão

        Input:
            - df - dataframe com os dados necessários
            - help_text - texto para ser exibido na opção help (?) do filtro

        Output:
            - paises - lista com os paises selecionado
    '''
    paises_ord = df['country'].unique()
    paises_ord.sort()
    paises = st.sidebar.multiselect('Escolha os países que deseja vizualizar os restaurantes', 
                                    options=paises_ord, 
                                    default=["Brazil", 
                                             "England", 
                                             "Qatar", 
                                             "South Africa", 
                                             "Canada", 
                                             "Australia"], 
                                    help=help_text)
    return paises


def filtro_notas(help_text):
    ''' Esta função constroi o filtro de notas dos restaurantes para a Barra Lateral do Streamlit

        Input:
            - help_text - texto para ser exibido na opção help (?) do filtro

        Output:
            - notas - lista com as notas selecionadas para os restaurantes
    '''
    notas = st.sidebar.slider('Selecione as notas dos restaurantes que deseja visualizar', 
                              min_value=0.0, 
                              max_value=5.0, 
                              value=(0.0 , 5.0), 
                              help=help_text)
    return notas
