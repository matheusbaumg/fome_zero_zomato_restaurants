# bibliotecas

import inflection
import pandas as pd
import plotly.express as px
# -------------------- Funções --------------------

countries = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America" }

colors = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred" }


def country_name(country_id):
    ''' Esta função traduz os códigos da coluna country_code, troca os códigos dos países por seus nomes'''
    return countries[country_id]


def create_price_type(price_range):
    ''' Esta função cria a coluna price_type, que atribui uma categoria de preço ao restaurante de acordo com o número da coluna price_range'''
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    

def color_name(color_code):
    ''' Esta função troca os códigos pelos nomes das cores na coluna rating_color'''
    return colors[color_code]


def rename_columns(dataframe):
    ''' Esta função altera a formatação dos títulos das colunas do dataframe
        - coloca tudo em letras minúsculas
        - substitui os espaços por underline (_)'''
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


def transform_data (df):
    ''' Esta função aplica as funções para transformação da formatação do dataframe
        
        Função aplicadas:
        - rename_columns - renomeia as colunas
        - country_name - traduz os códigos para os nomes dos paises
        - create_price_type - cria uma coluna com categorias de preços
        - color_name - traduz os códigos para os nomes das cores
        '''
    df = rename_columns(df)
    df['country_code'] = df['country_code'].apply(lambda x: country_name(x))
    df['price_type'] = df['price_range'].apply(lambda x: create_price_type(x))
    df['rating_color'] = df['rating_color'].apply(lambda x: color_name(x))

    return df


def clean_data(df):
    ''' Esta função faz a limpeza dos dados do data frame
        
        Ações realizadas:
        - remoção de linhas duplicadas
        - remoção de linhas com elementos faltantes
        - remove a coluna 'switch_to_order_menu' que contem o mesmo dado para todas as linhas
        - remove a coluna 'locality_verbose' que contem informações repetidas de outras colunas
        - altera a coluna 'cuisines' pra ficar apenas com o primeiro tipo listado para cada restaurante
        - renomeia a coluna 'country_code' para 'country'
        - remove restaurantes que são os únicos do seu tipo de cuinária e não tem avaliação
        - reseta o index do dataframe
    '''
    df = df.drop_duplicates()
    df = df.dropna()
    df = df.drop('switch_to_order_menu', axis=1)
    df = df.drop('locality_verbose', axis=1)
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])
    df = df.rename(columns={'country_code': 'country'})
    df = df.drop(df.loc[df['cuisines']=='Drinks Only'].index)
    df = df.drop(df.loc[df['cuisines'] == 'Mineira'].index)
    df = df.reset_index(drop=True)

    return df


def conv_moedas(df):
    ''' Esta função faz o câmbio das moedas locais de cada país para valores em Reais (BRL)
    '''
    cambio = {'currency': ['Botswana Pula(P)', 
                           'Brazilian Real(R$)', 
                           'Dollar($)', 
                           'Emirati Diram(AED)', 
                           'Indian Rupees(Rs.)', 
                           'Indonesian Rupiah(IDR)', 
                           'NewZealand($)', 
                           'Pounds(£)',
                           'Qatari Rial(QR)', 
                           'Rand(R)', 
                           'Sri Lankan Rupee(LKR)',
                           'Turkish Lira(TL)'], 
                'taxa_cambio':[0.3995, 1, 5.4283, 1.4777, 0.06504, 0.0003314, 3.3167, 6.8793, 1.4886, 0.2977, 0.01778, 0.1648]}
    cambio = pd.DataFrame(cambio)
    df_conv = df.merge(cambio, on='currency')
    df_conv['average_cost_for_two_brl'] = df_conv['average_cost_for_two']*df_conv['taxa_cambio']
    
    return df_conv


def data_process(df):
    ''' Esta função recebe o dataframe original, processa e devolve pronto para as análises
        
        Operações realizadas:
        - aplica a função transform_data que altera a formatação do dataframe
        - aplica a função clean_data que realiza a limpeza do dataframe
        - aplica a função conv_moedas que cria duas novas colunas no dataframe
            - cambio - com as taxas de câmbio das moedas locais para Reais (BRL)
            - average_cost_for_two_brl - com os valores convertidos para Reais
    '''
    df = transform_data(df)
    df = clean_data(df)
    df = conv_moedas(df)

    return df


def remove_outlier(df):
    ''' Esta função remoce o autlier de preço de um restaurante da Austrália

        Ações realizadas:
        - Encontra o restaurante com o autlier de preço
        - Remove este restaurante do dataframe

        Input:
            - df - dataframe

        Output:
            - df1 - dataframe sem o outlier
    '''
    # encontra o restaurante com o outlier
    outl = df.loc[df['country'] == 'Australia',['restaurant_id', 'country' ,'average_cost_for_two']].sort_values('average_cost_for_two', ascending=False).index[0]
    # remove o outlier
    df1 = df.drop(outl)
    df1 = df1.reset_index(drop=True)
    
    return df1


def graf_preco(df, arg):
    ''' Esta função desenha o gráfico com as médias dos preços do prato para duas pessoas em cada país
        
        Ações realizadas:
        - Faz o cálculo das médias e monta o dataframe auxiliar para a construção do gráfico
        - Faz a configuração do gráfico
        - Faz a configuração do título do gráfico

        Input:
            - df - dataframe
            - arg - especifica se o gráfico é com os valores em moedas locais ou em Reais
                - 'average_cost_for_two' - para valores em moedas locais
                - 'average_cost_for_two_brl' - para valores em Reais
        
        Output:
            - fig - figura do gráfico para ser exibido
    '''
    # calcula média
    df_aux = df.loc[:, [arg, 'country']].groupby('country').mean().sort_values(arg, ascending=False).reset_index().round(2)
    # config gráfico
    fig = px.bar(df_aux, 
                    x='country', 
                    y= arg, 
                    text= arg, 
                    labels={'country':'País', 
                            arg:'Preço de prato para duas pessoas'})
    
    # config título do gráfico
    if arg == 'average_cost_for_two_brl':
        text = '(em R$)'
    else:
        text = '(moedas locais)'

    fig.update_layout(title={'text': f'Média de preço de um prato para duas pessoas por País {text}', 
                                'y':0.95, 
                                'x': 0.5 , 
                                'xanchor': 'center', 
                                'yanchor': 'top'})
    return fig



def cozinhas(df, pais_cozinha):
    ''' Esta função traz os dados do restaurante com maior média de avaliação da culinária especificada
        
        Caso haja mais de um restaurante com a maior média de avaliação o selecionado será aquele com menor ID

        Input:
            - df - dataframe contendo os dados necessários
            - pais_cozinha - especifica qual o tipo de culinária do restaurante

        Output:
            - dados do restaurante com maior média de avaliação
                - nome
                - nota de avaliação
                - país
                - cidade
                - prato_pra_dois - custo do prato para duas pessoas
                - moeda - moeda local
    '''
    df_coz = (df.loc[df['cuisines'] == pais_cozinha, ['restaurant_id', 'restaurant_name', 'aggregate_rating', 'country', 'city', 'average_cost_for_two', 'currency']].
                  sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).
                  reset_index(drop=True))
    nome = df_coz.loc[0, 'restaurant_name']
    nota = df_coz.loc[0, 'aggregate_rating']
    pais = df_coz.loc[0, 'country']
    cidade = df_coz.loc[0, 'city']
    prato_para_dois = df_coz.loc[0, 'average_cost_for_two']
    moeda = df_coz.loc[0, 'currency']
    
    dados = [nome, nota, pais, cidade, prato_para_dois, moeda]
    
    return dados


def rank_culinarias(df, asc):
    ''' Esta função desenha o gráfico das 10 culinárias com maiores e menores notas médias de avaliação
        
        Ações realizadas:
            - Faz o cálculo das médias e monta o dataframe auxiliar para a construção do gráfico
            - Faz a configuração do gráfico
            - Faz a configuração do título do gráfico
        
        Input:
            - df - dataframe
            - asc - especifica se o gráfico é para as culinárias com maiores ou com menores notas
                - True - para o gráfico com a culinárias com menores notas
                - False - para o gráfico com a culinárias com maiores notas
        
        Output:
            - fig - figura do gráfico para ser exibido           
    
    '''
    df_aux = df.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=asc).reset_index().round(2)

    fig = px.bar(df_aux.iloc[0:10], 
                 x='cuisines', 
                 y='aggregate_rating', 
                 text='aggregate_rating', 
                 labels={'cuisines':'Tipo de Culinária', 
                         'aggregate_rating':'Média da Avaliação Média'})

    if asc == True:
        text = 'Menores'
    else:
        text = 'Maiores'
    
    fig.update_layout(title={'text': f'Top 10 Culinárias com {text} médias de avaliação', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    return fig