import pandas as pd 
import os 



#lendo os arquivos 

try:
    print("importando planilhas")
    df_vendas = pd.read_excel('fato_vendas.xlsx')
    df_produtos = pd.read_excel('dim_produtos.xlsx')
    df_familia = pd.read_excel('dim_familia_produtos.xlsx')
    df_vendedor = pd.read_excel('dim_vendedor.xlsx')
    print("importado com sucesso")
except FileNotFoundError:
    print("Erro: Nenhum arquivo encontrado, Verifique se estão na pasta ❌")
    exit () 

# Fazendo que os numeros sejam lidos como string 


df_vendas ['codigo_produto'] = df_vendas ['codigo_produto'].astype(str)
df_vendas ['codigo_vendedor'] = df_vendas['codigo_vendedor'].astype(str)

df_produtos ['codigo_produto'] = df_produtos['codigo_produto'].astype(str)
df_produtos ['codigo_familia'] = df_produtos['codigo_familia'].astype(str)

df_familia['codigo_familia'] = df_familia ['codigo_familia'].astype(str)

df_vendedor['codigo_vendedor'] = df_vendedor['codigo_vendedor'].astype(str)



df_completo = df_vendas.merge(df_produtos, on = 'codigo_produto', how= 'left')
df_completo = df_completo.merge(df_familia,on='codigo_familia', how='left')
df_completo = df_completo.merge(df_vendedor,on='codigo_vendedor', how='left')


df_completo['data_venda'] = pd.to_datetime(df_completo['data_venda'])


#Calculo 1 - Custo total 

df_completo['Custo Total'] = df_completo['quantidade']*df_completo['custo_produto_unitario']

#Calculo 2 - Lucro 

df_completo['Lucro'] = df_completo['valor_monetario_total'] - df_completo ['Custo Total']


#Produtos comprados juntos 

cesta = df_completo[['codigo_cliente','descricaofamilia']].dropna().drop_duplicates()

afinidade = cesta.merge(cesta, on= 'codigo_cliente')

afinidade = afinidade[afinidade['descricaofamilia_x']!= afinidade['descricaofamilia_y']]

ranking = afinidade.groupby(['descricaofamilia_x', 'descricaofamilia_y']).size().reset_index(name = 'qdt_juntos')
ranking = ranking.sort_values('qdt_juntos' , ascending=False )


print ('salvando no excel ')
df_completo.to_excel("Lumen_Dados_Completos.xlsx", index=False)
ranking.to_excel("Lumen_Afinidade.xlsx", index = False )