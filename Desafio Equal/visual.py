import streamlit as st 
import pandas as pd     
import plotly.express as px 

st.set_page_config(page_title="Lumen Dashboard" , layout="wide")

col_logo, col_titulo = st.columns([2, 20]) 

with col_logo:
    
    st.image("Lumen.png", width=200) 

with col_titulo:
    st.title("Lumen Store - Painel de Gerencia")



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
    
    col1.metric("Receita Bruta", f"R${df_filtrado['Receita Liquida'].sum():,.2f}")
    col2.metric("Total Desconto", f"R${df_filtrado['Desconto'].sum():,.2f}")
    col3.metric("Faturamento Liquido", f"R${df_filtrado['Receita Bruta'].sum():,.2f}")
    
    temp = df_filtrado.groupby('Mes_Ano')[['Receita Liquida', 'Receita Bruta']].sum().reset_index()
    
    
    fig = px.bar(temp,
                           x='Mes_Ano',
                           y=['Receita Liquida', 'Receita Bruta'], 
                           title= "Total de descontos em ", 
                           barmode='group')
 
    fig.update_yaxes(range=[1000000 , 3200000])
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig,use_container_width=True)
    
with aba2:

 if 'filial_venda' in df_filtrado.columns:
    st.subheader("Performance de filiais")
    evolucao = df_filtrado.groupby(['Mes_Ano','filial_venda'])['Receita Liquida'].sum().reset_index()
    fig_ev = px.line(evolucao , x= 'Mes_Ano' , y= 'Receita Liquida' ,  color= 'filial_venda', markers= True)
    st.plotly_chart(fig_ev ,use_container_width= True)

 else:
    st.warning = ('Coluna não encontrada ')

with aba3:
    st.header ("Analise de Produtos")
    
    coluna_familia = 'descricaofamilia'
    
    st.divider()
    
    #Part 1 : familia 

    if coluna_familia in df_filtrado.columns:
    
        df_familia = df_filtrado.groupby(coluna_familia)[['Receita Liquida']].sum().reset_index()
    
        df_familia = df_familia.sort_values('Receita Liquida', ascending= False)
    
        total_receitas = df_familia['Receita Liquida'].sum()
        df_familia['Participacao (%)'] = (df_familia['Receita Liquida'] / total_receitas) * 100
    
        top_5_famila = df_familia.head(5)
    
        if not df_familia.empty:
            top_1_nome = df_familia.iloc[0][coluna_familia]
            top_1_perc = df_familia.iloc[0]['Participacao (%)']
            
            st.info(f'A familia **{top_1_nome}** é o lider de vendas, '
                f'representando **{top_1_perc:.1f}%** do faturamento selecionado ')
 
        else :
            st.warning("Não há dados para os filtos selecionados")
            
        st.divider()
        
        fig_top5 = px.bar(top_5_famila,
                  x='Receita Liquida',
                  y= coluna_familia,
                  orientation = 'h',
                  text_auto= True , 
                  title = "Top 5 familias mais Relevantes" ,
                  color = 'Receita Liquida' ,
                  color_continuous_scale = 'Blues' )

        fig_top5.update_layout(yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig_top5, use_container_width = True)

    else: 
        st.error(f"Error A coluna '{coluna_familia}' não existe do DataFrame.   ")
        
        
        
    st.divider()    
    
    
    #Produtos 
    
    st.subheader ( "Detalhe: Top 5 Produtos por Familia")
    
    cols_necessarias = [ 'quantidade',
                        'preco_venda_unitario', 
                        'custo_produto_unitario', 
                        'descricaoproduto',
                        'descricaofamilia'] 
    
    if all( col in df_filtrado.columns for col in cols_necessarias): 
        
        
        df_filtrado['Lucro_Calculado'] = df_filtrado['quantidade'] * (df_filtrado ['preco_venda_unitario'] - df_filtrado['custo_produto_unitario'] )
        
        # escolhendo a familia 
        lista_familia = sorted(df_filtrado['descricaofamilia'].unique())
        familia_selecionada = st.selectbox("Selecione a Familia para Detalhar:" , options= lista_familia)
        
        
        #filtagem de dados 
        df_produto_familia = df_filtrado[df_filtrado['descricaofamilia']== familia_selecionada]
        
        
        #agrupamento de produtos  + soma da receita 
        df_top_produtos = df_produto_familia.groupby('descricaoproduto')[['Receita Liquida', 'Lucro_Calculado']].sum().reset_index()
        
        df_top_produtos = df_top_produtos.sort_values('Receita Liquida', ascending = False).head(5)

        if not df_top_produtos.empty:
            prod_lider = df_top_produtos.iloc[0]['descricaoproduto']
            receita_lider = df_top_produtos.iloc[0]['Receita Liquida']
            total_da_familia = df_produto_familia['Receita Liquida'].sum()
            
            
            perc_dependencia = (receita_lider / total_da_familia) * 100 
            
            # regra de alerta para  > 40 % , é uma dependecia alta 
            tipo_alerta = "warning" if perc_dependencia > 40 else "info"
            
            if tipo_alerta == 'warning':
                st.warning(f" O produto **{prod_lider}** concentra **{perc_dependencia:.1f}%** "
                               f"de toda a receita da família {familia_selecionada}.")
            else:
                st.info(f"O produto **{prod_lider}** é o líder, representando **{perc_dependencia:.1f}%** "
                            f"das vendas desta família.")
                
        fig_prod = px.bar(df_top_produtos,
                          x='Receita Liquida', 
                              y='descricaoproduto',
                              orientation='h',
                              text_auto=True,
                              title=f"Top 5 Produtos - {familia_selecionada}",
                              color='Lucro_Calculado', 
                              color_continuous_scale='Greens', 
                              labels={'descricaoproduto': 'Produto', 'Lucro_Calculado': 'Lucro Total', 'Receita Liquida': 'Vendas'})
        
        fig_prod.update_layout(yaxis=dict(autorange="reversed")) # Maior no topo
        st.plotly_chart(fig_prod, use_container_width=True)
            
    else:
        st.error("As colunas necessárias para o cálculo de lucro não foram encontradas no Excel.")
                         
                
        
        