import streamlit as st 
import pandas as pd     
import plotly.express as px 

st.set_page_config(page_title="Lumen Dashboard" , layout="wide")
st.title("Lumen Store - Painel de Gerencia ")

#para otmização do sistema
@st.cache_data
def carregar_dados () : 
    try:
        return pd.read_excel("Lumen_Analitico_Final.xlsx")
    except FileNotFoundError: 
        return None
    
df = carregar_dados ()

if df is None:
    st.error ( "O arquivo 'Lumen_Analitico_Final.xlsx' ainda não foi gerado ")
    st.stop()
    
#Filtros 

st.sidebar.header('Filtros')
meses = st.sidebar.multiselect("mês",
                               options=sorted(df['Mes_Ano'].unique()),
                               default=sorted(df['Mes_Ano'].unique()) 
                               )
df_filtrado = df[df['Mes_Ano'].isin(meses)]    


#Criando Tabelas 

aba1 ,aba2 , aba3 , aba4 = st.tabs(["Finaças" , "Vendedores" , "Produtos" , "Cliente" ])


with aba1: 
    st.header( "Finanças ")
    col1,col2,col3  = st.columns(3)
    
    col1.metric("Faturamento Bruto", f"R${df_filtrado['Receita Liquida'].sum():,.2f}")
    col2.metric("Total Desconto", f"R${df_filtrado['Desconto'].sum():,.2f}")
    col3.metric("Faturamento Liquido", f"R${df_filtrado['Receita Bruta'].sum():,.2f}")
    
    temp = df_filtrado.groupby('Mes_Ano')[['Receita Bruta', 'Receita Liquida']].sum().reset_index()
    
    
    st.plotly_chart(px.bar(temp,
                           x='Mes_Ano',
                           y=['Receita Bruta', 'Receita Liquida'], 
                           title= "Total de descontos em ", 
                           barmode='group'),
                    use_container_width=True)
    
    
    





