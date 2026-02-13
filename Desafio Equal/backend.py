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
df_completo = df_completo.sort_values(df_completo['data_venda'])
df_completo['Mes_Ano'] = df_completo['data_venda'].dt.strftime('%Y-%m')




df_completo['Custo Total'] = df_completo['quantidade']*df_completo['custo_produto_unitario']
df_completo['Receita Bruta'] = df_completo["valor_monetario_total"]


#grantia de desconto (caso não tenha na coluna cria zerada 

if'valor_desconto' in df_completo.columns:
    df_completo['Desconto'] = df_completo['valor_desconto']
else:
    df_completo ['Desconto']= 0 


#resposta 1 
df_completo['Receita Liquida'] = df_completo['Receita Bruta'] + df_completo ['Desconto']


#resp 5 
df_completo['Lucro'] = df_completo['Receita Bruta'] - df_completo ['Custo Total']


pasta_atual = os.path.dirname(os.path.abspath(__file__))

caminho_arquivo = os.path.join(pasta_atual , "Lumen_Analitico_Final.xlsx")


df_completo.to_excel(caminho_arquivo, index=False)
print(" Base pronta: 'Lumen_Analitico_Final.xlsx'")