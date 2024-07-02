import streamlit as st

st.set_page_config(page_title='Painel', page_icon=':material/monitoring:', layout='wide')

st.logo('logo5.png')

pagina1 = st.Page('page_1.py', title='Home', icon='📊')
pagina2 = st.Page('page_2.py', title='Países', icon='🌎')
pagina3 = st.Page('page_3.py', title='Cidades', icon='🏙️')
pagina4 = st.Page('page_4.py', title='Culinárias', icon='🍽️')

pg = st.navigation([ pagina1, pagina2, pagina3, pagina4])

pg.run()