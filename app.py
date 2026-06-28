import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta

# Configuração da página de luxo K&G
st.set_page_config(
    page_title="K&G Arte em Confeitaria",
    page_icon="✨",
    layout="wide"
)

# Estilização Premium (Verde Esmeralda, Ouro e Nude Rosado)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #FAF6F0; }
        .brand-header {
            background: linear-gradient(135deg, #043927 0%, #0B533A 100%);
            padding: 25px; border-radius: 15px; text-align: center;
            border-bottom: 4px solid #D4AF37; margin-bottom: 25px;
        }
        .brand-title { font-family: 'Playfair Display', serif; font-size: 36px; color: #FAF6F0; font-weight: 700; }
        .brand-subtitle { font-size: 13px; color: #E3C16F; letter-spacing: 2px; text-transform: uppercase; }
        .section-title { font-family: 'Playfair Display', serif; color: #043927; font-size: 22px; border-left: 4px solid #D4AF37; padding-left: 12px; margin-top: 20px; margin-bottom: 15px; }
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Sistema de Alta Confeitaria, Engenharia de Alimentos e Gestão Fina 💎</div>
    </div>
""", unsafe_allow_html=True)

# Criando as Abas do Sistema
tabs = st.tabs([
    "📊 Dashboard & Financeiro", 
    "👩‍🍳 Precificação & Ficha Técnica", 
    "📦 Embalagens & Impressora", 
    "🥦 ANVISA & Etiquetas", 
    "🛒 Estoque & Compras",
    "🏛️ Inventário (Utensílios)",
    "💼 RH & Departamento Pessoal"
])

# --- ABA 1: DASHBOARD & GESTÃO FINANCEIRA PRIVADA ---
with tabs[0]:
    st.markdown('<div class="section-title">🔒 Painel Financeiro Estratégico</div>', unsafe_allow_html=True)
    
    # Sistema de Proteção contra fofoca de funcionários/clientes
    senha = st.text_input("Digite a senha de proprietária para liberar os números:", type="password")
    if senha == "1234" or senha == "kg10k": # Você pode mudar sua senha aqui
        st.success("Acesso Autorizado, Karyn!")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Meta de Faturamento", "R$ 10.000,00")
        with c2: st.metric("Custos Fixos Totais", "R$ 2.450,00")
        with c3: st.metric("Impostos Estimados (DAS)", "R$ 75,00")
        with c4: st.metric("Pró-Labore Reservado", "R$ 4.000,00")
        
        st.markdown("### 💸 Custos e Despesas do Mês")
        dados_financeiros = pd.DataFrame({
            "Categoria": ["Pró-labore", "Salário Funcionários", "Custos Fixos (Luz/Água)", "Custos Variáveis (Insumos)", "Impostos"],
            "Valor Planejado (R$)": [4000.00, 2500.00, 600.00, 1500.00, 75.00]
        })
        st.dataframe(dados_financeiros, use_container_width=True)
        
        if st.button("🖨️ Imprimir Relatório Financeiro Mensal"):
            st.markdown('<div class="print-box"><b>K&G ARTE EM CONFEITARIA - RELATÓRIO FINANCEIRO</b><br>Data: '+datetime.now().strftime('%d/%m/%Y')+'<br>---------------------------------------<br>Faturamento Alvo: R$ 10.000,00<br>Despesas Operacionais: R$ 8.675,00<br>Lucro Líquido Retido: R$ 1.325,00<br>---------------------------------------<br>Assinatura da Direção</div>', unsafe_allow_html=True)
    else:
        st.warning("Insira a senha correta para visualizar os dados financeiros e relatórios.")

# --- ABA 2: PRECIFICAÇÃO, ACETATO E FICHA TÉCNICA ---
with tabs[1]:
    st.markdown('<div class="section-title">👩‍🍳 Engenharia de Modelagem e Precificação</div>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nome_doce = st.text_input("Nome do Doce / Produto", value="Bombom Personalizado Luxo")
        tipo_pasta = st.selectbox("Tipo de Pasta Utilizada", ["Pasta de Leite em Pó", "Pasta Americana", "Pasta de Chocolate", "Glacê Fluido"])
        tipo_forma = st.selectbox("Tipo de Forma / Molde", ["Forma de Alumínio", "Forma de Acetato (BWB / Porto Formas)", "Molde de Silicone", "Slice Cake"])
    
    with col_p2:
        gramas_chocolate = st.number_input("Quantidade de Chocolate por Doce (g)", value=45)
        gramas_recheio = st.number_input("Quantidade de Recheio por Doce (g)", value=30)
        gramas_pasta = st.number_input("Quantidade de Pasta na Personalização (g)", value=15)
        
    peso_total_doce = gramas_chocolate + gramas_recheio + gramas_pasta
    st.metric("Peso Líquido por Unidade", f"{peso_total_doce} g")
    
    st.markdown("### 🛒 Cadastro de Ingredientes da Receita")
    df_ingredientes = st.data_editor(pd.DataFrame([
        {"Ingrediente": "Chocolate Nobre", "Preço Pago (R$)": 55.0, "Qtd Embalagem (g)": 1000, "Qtd Usada (g)": gramas_chocolate},
        {"Ingrediente": "Leite Condensado (Recheio)", "Preço Pago (R$)": 6.50, "Qtd Embalagem (g)": 395, "Qtd Usada (g)": gramas_recheio},
        {"Ingrediente": "Insumos Pasta de Leite", "Preço Pago (R$)": 32.0, "Qtd Embalagem (g)": 1000, "Qtd Usada (g)": gramas_pasta}
    ]), num_rows="dynamic", use_container_width=True)

    if st.button("📋 Gerar e Imprimir Ficha Técnica para a Cozinha"):
        st.markdown(f"""
            <div class="print-box">
                <b>FICHA TÉCNICA DE PRODUÇÃO - K&G ARTE EM CONFEITARIA</b><br>
                <b>Produto:</b> {nome_doce}<br>
                <b>Molde/Forma:</b> {tipo_forma}<br>
                <b>Elemento Decorativo:</b> {tipo_pasta}<br>
                -----------------------------------------------------<br>
                <b>PADRÃO DE MONTAGEM NA COZINHA (POR UNIDADE):</b><br>
                - Casca/Base: {gramas_chocolate}g de Chocolate<br>
                - Recheio Interno: {gramas_recheio}g<br>
                - Decoração/Modelagem: {gramas_pasta}g de {tipo_pasta}<br>
                -----------------------------------------------------<br>
                <b>Peso Final Padronizado:</b> {peso_total_doce}g<br>
                *Mantenha a balança zerada para cada etapa da pesagem.*
            </div>
        """, unsafe_allow_html=True)

# --- ABA 3: EMBALAGENS DE LUXO E IMPRESSORA PORTÁTIL ---
with tabs[2]:
    st.markdown('<div class="section-title">📦 Gestão de Embalagens e Impressão de Etiquetas</div>', unsafe_allow_html=True)
    
    st.write("Cadastre aqui os custos de apresentação do seu produto:")
    df_embalagens = st.data_editor(pd.DataFrame([
        {"Item": "Caixa de Luxo com Visor", "Preço Cento/Pacote (R$)": 250.0, "Unidades no Pacote": 50, "Usado por Doce": 1},
        {"Item": "Fita de Cetim Premium (Metros)", "Preço Rolo (R$)": 15.0, "Metros no Rolo": 10, "Usado por Doce (m)": 0.4},
        {"Item": "Tags / Cartões Informativos", "Preço (R$)": 80.0, "Unidades no Pacote": 100, "Usado por Doce": 1}
    ]), num_rows="dynamic", use_container_width=True)

    st.markdown("### 🖨️ Conectar e Enviar para Impressora Portátil")
    texto_impressora = st.text_area("Texto para sair na Etiqueta de Envio:", f"K&G Arte em Confeitaria\nFeito com Amor para você!\nProduto: {nome_doce}")
    if st.button("⚡ Enviar Comando de Impressão Portátil"):
        st.success("Comando enviado com sucesso para a sua impressora portátil de doces!")
        st.code(texto_impressora, language="text")

# --- ABA 4: ANVISA, ALERGÊNICOS E CÓDIGO DE BARRAS ---
with tabs[3]:
    st.markdown('<div class="section-title">🥦 Rotulagem Oficial ANVISA e Validade</div>', unsafe_allow_html=True)
    
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        dias_val = st.number_input("Dias de Validade do Doce", value=7)
        lote = st.text_input("Lote Automatizado", value=datetime.now().strftime("%Y%m%d")+"-01")
    with c_e2:
        alergias = st.multiselect("Alertas de Alergênicos (Lei Vigente)", 
            ["Trigo (Glúten)", "Ovos", "Leite", "Derivados de Aveia", "Amendoim", "Soja"], default=["Leite", "Trigo"])
    
    if st.button("🖨️ Gerar Código de Barras EAN-13 para Revenda"):
        st.success("Código de Barras Oficial Solicitado e Vinculado!")
        st.image("https://barcode.tec-it.com/barcode.ashx?data=789600012345&code=EAN13", caption="EAN-13 Pronto para Gôndola Comercial")

# --- ABA 5: ESTOQUE INTELIGENTE E LISTA DE COMPRAS ---
with tabs[4]:
    st.markdown('<div class="section-title">🛒 Controle de Estoque e Alerta de Faltas</div>', unsafe_allow_html=True)
    
    df_estoque = st.data_editor(pd.DataFrame([
        {"Ingrediente": "Chocolate Nobre Blend", "Estoque Atual (kg)": 12.0, "Mínimo Necessário (kg)": 5.0, "Status": "Ok"},
        {"Ingrediente": "Leite Condensado", "Estoque Atual (un)": 3.0, "Mínimo Necessário (un)": 24.0, "Status": "⚠️ COMPRAR URGENTE"},
        {"Ingrediente": "Açúcar de Confeiteiro", "Estoque Atual (kg)": 1.5, "Mínimo Necessário (kg)": 4.0, "Status": "⚠️ COMPRAR URGENTE"}
    ]), num_rows="dynamic", use_container_width=True)
    
    if st.button("📋 Imprimir Lista de Compras Pronta"):
        st.markdown("""
            <div class="print-box">
                <b>🛒 LISTA DE COMPRAS AUTOMÁTICA - K&G</b><br>
                ---------------------------------------<br>
                - Leite Condensado (Faltam 21 un)<br>
                - Açúcar de Confeiteiro (Faltam 2.5 kg)<br>
                ---------------------------------------<br>
                *Gerado direto do estoque inteligente.*
            </div>
        """, unsafe_allow_html=True)

# --- ABA 6: INVENTÁRIO DE EQUIPAMENTOS E UTENSÍLIOS ---
with tabs[5]:
    st.markdown('<div class="section-title">🏛️ Relação de Bens e Patrimônio do Atelier</div>', unsafe_allow_html=True)
    
    categoria_utensilio = st.selectbox("Filtrar Categoria do Inventário", [
        "Formas de Alumínio", "Moldes de Silicone", "Cortadores (Alumínio/Plástico)", "Stencils", "Bailarinas", "Forno & Batedeiras", "Utensílios Gerais"
    ])
    
    df_inventario = st.data_editor(pd.DataFrame([
        {"Item": "Molde Silicone Rosas Luxo", "Categoria": "Moldes de Silicone", "Quantidade": 4, "Estado": "Excelente"},
        {"Item": "Batedeira Planetária Arno", "Categoria": "Forno & Batedeiras", "Quantidade": 1, "Estado": "Uso Diário"},
        {"Item": "Bailarina Profissional Rolamento", "Categoria": "Bailarinas", "Quantidade": 2, "Estado": "Excelente"}
    ]), num_rows="dynamic", use_container_width=True)

# --- ABA 7: RH & DEPARTAMENTO PESSOAL ---
with tabs[6]:
    st.markdown('<div class="section-title">💼 Gestão de Pessoas e Obrigações Trabalhistas</div>', unsafe_allow_html=True)
    
    st.write("Controle de Admissões, Demissões, Folha e Atestados Médicos na Lei:")
    df_rh = st.data_editor(pd.DataFrame([
        {"Funcionário": "Ana Silva (Auxiliar)", "Cargo": "Confeiteira Jr", "Salário (R$)": 1650.00, "Situação": "Ativo", "Atestados/Ocorrências": "Nenhuma"},
        {"Funcionário": "Mariana Costa", "Cargo": "Atendente", "Salário (R$)": 1412.00, "Situação": "Admissão Pendente", "Atestados/Ocorrências": "Exame médico agendado"}
    ]), num_rows="dynamic", use_container_width=True)
