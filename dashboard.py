import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import datetime

dataframe = pd.read_csv('./dataset_merge/ACOES.csv', index_col='Date', parse_dates=True)
data_melt = pd.melt(dataframe.reset_index(), id_vars='Date', var_name='acoes', value_name='precos')

# Lista de Ações
list_acoes = ['AAPL', 'SNAP', 'TWTR', 'AMD', 'NVDA', 'MSFT', 'UBER', 'FB', 'NFLX', 'ABEV']


# Criando colunas para posicionar as metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label='AAPL', value=str(dataframe.loc[dataframe.last_valid_index(), 'AAPL']),
              delta=str(round(dataframe.pct_change().loc[dataframe.last_valid_index(), 'AAPL'], 4)))

with col2:
    st.metric(label='NFLX', value=str(dataframe.loc[dataframe.last_valid_index(), 'NFLX']),
              delta=str(round(dataframe.pct_change().loc[dataframe.last_valid_index(), 'NFLX'], 4)))

with col3:
    st.metric(label='ABEV', value=str(dataframe.loc[dataframe.last_valid_index(), 'ABEV']),
              delta=str(round(dataframe.pct_change().loc[dataframe.last_valid_index(), 'ABEV'], 4)))

with col4:
    st.metric(label='UBER', value=str(dataframe.loc[dataframe.last_valid_index(), 'UBER']),
              delta=str(round(dataframe.pct_change().loc[dataframe.last_valid_index(), 'UBER'], 4)))

with col5:
    st.metric(label='TWTR', value=str(dataframe.loc[dataframe.last_valid_index(), 'TWTR']),
              delta=str(round(dataframe.pct_change().loc[dataframe.last_valid_index(), 'TWTR'], 4)))

# Criando a Sidebar
with st.sidebar:
    st.title('Cotações')
    checkbox1 = st.checkbox('Tabela')
    if checkbox1:
        options = st.multiselect('Selecione as ações que deseja ver:', list_acoes, default='AAPL')
        date = st.date_input('data de inicio', value=dataframe.last_valid_index(),
                             min_value=dataframe.first_valid_index(), max_value=dataframe.last_valid_index())
        date2 = st.date_input('data de fim', value=dataframe.last_valid_index(),
                              min_value=dataframe.first_valid_index(), max_value=dataframe.last_valid_index())
        if date > date2:
            st.write('Data de incio não pode ser maior que a data de fim')

        radio = st.radio('Alterar modo da tabela', ('Valores', 'Variação percentual'), index=0)
        st.write(radio)

        checkbox2 = st.checkbox('Descrições')
        checkbox3 = st.checkbox('Visualzar Gráfico')

# criando o Container
with st.container():
    if checkbox1:
        if radio == 'Valores':
            st.dataframe(
                dataframe.loc[str(date):str(date2), options]
            )
        elif radio == 'Variação percentual':
            st.dataframe(
                dataframe.pct_change().loc[str(date):str(date2), options]
            )

        if checkbox2:
            st.markdown('**Estatísticas Descritivas**')

            st.write(dataframe.loc[str(date):str(date2), options].describe().T)

        if checkbox3:
            fig = px.line(data_melt[data_melt['acoes'].isin(options)],
                          x='Date', y='precos', color='acoes')
            st.plotly_chart(fig, use_container_width=True)
