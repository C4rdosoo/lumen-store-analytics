# 📊 Case de BI - Lumen Store (Processo Seletivo Equal)

Este repositório contém a solução técnica desenvolvida para o desafio de Estágio em Business Intelligence. O projeto simula um cenário real da varejista **Lumen Store**, focando na transformação de dados brutos em insights estratégicos.

## 🧠 O Desafio
O objetivo foi analisar o desempenho comercial da empresa e responder a perguntas de negócio utilizando dados de vendas, produtos e vendedores.

**Principais Perguntas Respondidas:**
1. Qual a evolução do Faturamento Bruto vs. Líquido?
2. Qual a performance individual das filiais e vendedores?
3. Quais produtos e famílias geram maior margem de lucro?
4. **(Análise Avançada)** Quais produtos apresentam afinidade de compra (Market Basket Analysis)?

## 🛠️ Tecnologias Utilizadas
* **Python (Pandas):**
    * Limpeza e tratamento de dados (ETL).
    * Criação do modelo estrela (união de Fato e Dimensões).
    * Algoritmo de associação para identificar padrões de compra cruzada (Cross-sell).
* **Power BI:**
    * Dashboard interativo para visualização de KPIs.
    * Cálculos DAX para margem e ticket médio.

## 📂 Estrutura do Projeto
* `/dados`: Arquivos originais (csv/xlsx).
* `/scripts`: Código Python (`analise_lumen.py`) utilizado para processar os dados.
* `/output`: Base de dados tratada e tabelas auxiliares geradas pelo script.
* `/dashboard`: Arquivo `.pbix` do Power BI.

