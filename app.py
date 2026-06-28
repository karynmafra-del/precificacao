import streamlit as st
import pandas as pd

# Configuração da página para se ajustar a celulares e notebooks
st.set_page_config(page_title="Dani Personalizados - Precificação", layout="centered")

st.title("🎂 Dani Personalizados - Sistema de Precificação")
st.write("Gerencie seus custos, receitas e preços de venda na palma da mão ou no computador.")

# --- Banco de Dados em Memória (Simulando a Planilha) ---
if 'ingredientes' not in st.session_state:
    st.session_state.ingredientes = pd.DataFrame([
        {"Ingrediente": "Ovos", "Quantidade Embalagem": 30, "Unidade": "Un", "Preço Pago (R$)": 22.00},
        {"Ingrediente": "Chocolate ao Leite", "Quantidade Embalagem": 2100, "Unidade": "g", "Preço Pago (R$)": 62.00},
        {"Ingrediente": "Chocolate em pó", "Quantidade Embalagem": 200, "Unidade": "g", "Preço Pago (R$)": 16.00},
        {"Ingrediente": "Farinha de Trigo", "Quantidade Embalagem": 1000, "Unidade": "g", "Preço Pago (R$)": 6.00},
        {"Ingrediente": "Manteiga", "Quantidade Embalagem": 200, "Unidade": "g", "Preço Pago (R$)": 12.00},
        {"Ingrediente": "Leite Condensado", "Quantidade Embalagem": 395, "Unidade": "g", "Preço Pago (R$)": 7.00},
        {"Ingrediente": "Creme de Leite", "Quantidade Embalagem": 200, "Unidade": "g", "Preço Pago (R$)": 3.50},
        {"Ingrediente": "Açúcar Impalpável", "Quantidade Embalagem": 1000, "Unidade": "g", "Preço Pago (R$)": 11.79},
        {"Ingrediente": "Leite em pó", "Quantidade Embalagem": 380, "Unidade": "g", "Preço Pago (R$)": 18.00},
    ])

if 'despesas' not in st.session_state:
    st.session_state.despesas = {"Fixas": 150.00, "Salario_Desejado": 2000.00, "Horas_Mes": 160}

# --- Menu de Navegação Superior (Perfeito para Celular) ---
aba = st.selectbox("Selecione a Tela:", ["📊 Precificar Produto", "🛒 Cadastro de Ingredientes", "💰 Custos e Mão de Obra"])

# --- TELA 1: CUSTOS E MÃO DE OBRA ---
if aba == "💰 Custos e Mão de Obra":
    st.header("⚙️ Configurações de Custos")
    
    despesas_fixas = st.number_input("Despesas Fixas Mensais (R$)", value=st.session_state.despesas["Fixas"])
    salario = st.number_input("Salário Pretendido (R$)", value=st.session_state.despesas["Salario_Desejado"])
    horas = st.number_input("Horas de Trabalho por Mês", value=st.session_state.despesas["Horas_Mes"])
    
    custo_hora = (despesas_fixas + salario) / horas if horas > 0 else 0
    st.metric("Seu Custo por Hora de Trabalho:", f"R$ {custo_hora:.2f}")
    
    if st.button("Salvar Custos"):
        st.session_state.despesas = {"Fixas": despesas_fixas, "Salario_Desejado": salario, "Horas_Mes": horas}
        st.success("Custos atualizados com sucesso!")

# --- TELA 2: CADASTRO DE INGREDIENTES ---
elif aba == "🛒 Cadastro de Ingredientes":
    st.header("🌾 Estoque e Preços de Insumos")
    
    st.subheader("Adicionar ou Atualizar Ingrediente")
    with st.form("form_ingrediente"):
        nome = st.text_input("Nome do Ingrediente")
        qtd = st.number_input("Quantidade da Embalagem", min_value=1.0, value=1000.0)
        unidade = st.selectbox("Unidade de Medida", ["g", "Un", "ml"])
        preco = st.number_input("Preço Pago (R$)", min_value=0.0, value=10.0)
        
        enviar = st.form_submit_button("Salvar Insumo")
        if enviar and nome:
            novo_ing = pd.DataFrame([{"Ingrediente": nome, "Quantidade Embalagem": qtd, "Unidade": unidade, "Preço Pago (R$)": preco}])
            st.session_state.ingredientes = pd.concat([st.session_state.ingredientes[st.session_state.ingredientes['Ingrediente'] != nome], novo_ing], ignore_index=True)
            st.success(f"{nome} atualizado!")

    st.subheader("Lista de Ingredientes Cadastrados")
    st.dataframe(st.session_state.ingredientes, use_container_width=True)

# --- TELA 3: PRECIFICAÇÃO DE RECEITAS ---
elif aba == "📊 Precificar Produto":
    st.header("⚖️ Nova Precificação / Ficha Técnica")
    
    # Calcular custo por grama/unidade de cada ingrediente
    df_ing = st.session_state.ingredientes.copy()
    df_ing['Custo Unitário'] = df_ing['Preço Pago (R$)'] / df_ing['Quantidade Embalagem']
    
    lista_nomes = df_ing['Ingrediente'].tolist()
    
    st.subheader("Selecione os Ingredientes Usados:")
    num_itens = st.number_input("Quantos ingredientes essa receita leva?", min_value=1, max_value=20, value=3)
    
    custo_ingredientes_total = 0.0
    
    for i in range(int(num_itens)):
        col1, col2 = st.columns([2, 1])
        with col1:
            ing_selecionado = st.selectbox(f"Ingrediente {i+1}", lista_nomes, key=f"ing_{i}")
        with col2:
            qtd_usada = st.number_input(f"Qtd Usada ({df_ing[df_ing['Ingrediente']==ing_selecionado]['Unidade'].values[0]})", min_value=0.0, key=f"qtd_{i}")
            
        custo_un = df_ing[df_ing['Ingrediente'] == ing_selecionado]['Custo Unitário'].values[0]
        custo_item = qtd_usada * custo_un
        custo_ingredientes_total += custo_item

    st.markdown("---")
    st.subheader("⏱️ Tempo de Produção e Margem")
    tempo_producao = st.number_input("Tempo gasto para fazer/decorar (em minutos)", min_value=0, value=30)
    margem_lucro = st.slider("Margem de Lucro Desejada (%)", min_value=0, max_value=300, value=100)
    
    # Cálculos Finais
    custo_hora_atual = (st.session_state.despesas["Fixas"] + st.session_state.despesas["Salario_Desejado"]) / st.session_state.despesas["Horas_Mes"]
    custo_mao_obra = (tempo_producao / 60) * custo_hora_atual
    
    custo_total_produto = custo_ingredientes_total + custo_mao_obra
    preco_venda_sugerido = custo_total_produto * (1 + (margem_lucro / 100))
    
    st.markdown("### 📋 Resumo Financeiro do Produto")
    c1, c2 = st.columns(2)
    c1.metric("Custo dos Insumos", f"R$ {custo_ingredientes_total:.2f}")
    c2.metric("Custo da Mão de Obra", f"R$ {custo_mao_obra:.2f}")
    
    st.metric("🔥 CUSTO TOTAL DE PRODUÇÃO", f"R$ {custo_total_produto:.2f}")
    st.success(f"💰 PREÇO DE VENDA SUGERIDO: R$ {preco_venda_sugerido:.2f}")
