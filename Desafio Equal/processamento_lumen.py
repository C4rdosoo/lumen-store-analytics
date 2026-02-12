import pandas as pd 
import os 



#lendo os arquivos 

try: 
    df_vendas = pd.read_excel('fato_vendas.xlsx')
    df_produtos = pd.read_excel('dim_produtos.xlsx ')
    df_familia = pd.read_excel('dim_familia_produtos.xlsx ')
    df_vendedor = pd.read_excel('dim_vendedor.xlsx ')
    print("inportado com sucesso")
except FloatingPointError:
    print("Erro: Nenhum arquivo encontrado, Verifique se estão na pasta")

exit () 

# Fazendo que os numeros sejam lidos como string 


df_vendas ['codigo_produto'] = df_vendas ['codigo_produto'].astype(str)
df_vendas ['codigo_vendedor'] = df_vendas['codigo_vendedor'].astype(str)
df_produtos ['codigo_produto'] = df_produtos['codigo_produto'].astype(str)
df_produtos ['codigo_familia'] = df_produtos['codigo_familia'].astype(str)
df_familia['codigo_familia'] = df_familia ['codigo_familia'].astype(str)
df_vendedor['codigo_vendedor'] = df_vendedor['codigo_familia'].astype(str)

