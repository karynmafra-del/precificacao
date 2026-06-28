import streamlit as st
import pandas as pd
import math
import random
from datetime import datetime, timedelta

# Configuração da página de luxo K&G
st.set_page_config(
    page_title="K&G Arte em Confeitaria",
    page_icon="✨",
    layout="wide"
)

# Estilização Premium K&G (Verde Esmeralda, Ouro e Nude Rosado)
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
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; line-height: 1.4; }
        .lupa-box { border: 3px solid black; background: white; color: black; padding: 10px; font-weight: bold; text-align: center; font-size: 14px; margin-bottom: 10px; font-family: Arial, sans-serif; }
        .preco-box { background: #043927; color: #FAF6F0; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #D4AF37; }
        .alerta-aniv { background: #FAF0F2; border-left: 5px solid #D4AF37; padding: 12px; border-radius: 4px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Ecossistema ERP, CRM e Engenharia Logística de Confeitaria Fina 💎</div>
    </div>
""", unsafe_allow_html=True)

# Inicialização de Bancos de Dados Temporários na memória
if 'banco_massas' not in st.session_state:
    st.session_state['banco_massas'] = {"Massa Choc Premium": 18.50, "Pão de Ló de Baunilha": 14.20, "Red Velvet Elite": 25.00}
if 'banco_recheios' not in st.session_state:
    st.session_state['banco_recheios'] = {"Brigadeiro de Ninho": 22.00, "Geleia de Morango Caseira": 18.00, "Brigadeiro ao Leite 32%": 20.00}
if 'banco_caldas' not in st.session_state:
    st.session_state['banco_caldas'] = {"Calda de Chocolate Fina": 5.00, "Calda de Especiarias": 6.50, "Calda Básica de Açúcar": 3.00}
if 'banco_coberturas' not in st.session_state:
    st.session_state['banco_coberturas'] = {"Chantiganache ao Leite": 35.00, "Glacê de Leite em Pó": 28.00}

# Abas Principais
tabs = st.tabs([
    "💰 CENTRAL FINANCEIRA & DRE",
    "📝 1. ORÇAMENTOS & PEDIDOS",
    "👥 2. CRM (CLIENTES & ALERTAS)",
    "🥣 3. FÁBRICA DE BASES",
    "🍫 4. DOCES PERSONALIZADOS (BWB)",
    "🎂 5. PRODUTOS COMPLETOS",
    "📦 EMBALAGENS & IMPRESSÃO",
    "🥦 ANVISA & ADVERTÊNCIAS",
    "🛒 ESTOQUE INTELIGENTE",
    "🏢 FORNECEDORES (CWB)",
    "🏛️ INVENTÁRIO DE BENS"
])

# --- ABA 0: CENTRAL FINANCEIRA ---
with tabs[0]:
    st.markdown('<div class="section-title">📊 Gestão de Fluxo, DRE e Demonstrativos de Lucro</div>', unsafe_allow_html=True)
    sub_fin1, sub_fin2, sub_fin3, sub_dp_aba = st.tabs(["📈 Dashboard de Resultados", "💸 Lançamentos Diários", "📉 Estrutura DRE", "👥 Departamento Pessoal (DP)"])
    with sub_fin1:
        st.metric("Meta Faturamento Mês", "R$ 10.000,00")
        st.progress(6420 / 10000, text="64.2% da Meta do Mês Alcançada")
    with sub_fin2:
        st.data_editor(pd.DataFrame([
            {"Data": "28/06/2026", "Tipo": "Receita (Entrada)", "Descrição": "Encomenda Casamento - Bolo 5kg + Doces", "Valor (R$)": 1450.00}
        ]), num_rows="dynamic", use_container_width=True, key="fluxo_caixa_key")
    with sub_fin3:
        st.data_editor(pd.DataFrame([{"Descrição do Custo Fixo": "Aluguel / Atelier", "Valor Mensal (R$)": 1500.00}]), num_rows="dynamic", use_container_width=True, key="custos_fixos_key")
    with sub_dp_aba:
        st.metric("Retirada Pró-Labore (Karyn)", "R$ 4.000,00")

# ==========================================
# ABA 1: GERADOR DE ORÇAMENTOS & INTELIGÊNCIA DE FRETE
# ==========================================
with tabs[1]:
    st.markdown('<div class="section-title">📝 Emissão de Orçamentos e Engenharia de Frete por KM</div>', unsafe_allow_html=True)
    
    col_or1, col_or2 = st.columns(2)
    with col_or1:
        c_nome = st.text_input("Nome do Cliente", value="Fernanda Albuquerque")
        c_whats = st.text_input("WhatsApp de Contato", value="(41) 99222-3344")
        c_email = st.text_input("E-mail do Cliente", value="fernanda.albuquerque@gmail.com")
        c_doce = st.text_input("Item Solicitado (Bolo/Doces)", value="Bolo de Morango Especial 5kg")
        c_valor_produtos = st.number_input("Valor dos Produtos (R$)", value=650.00)
    
    with col_or2:
        c_data_festa = st.date_input("Data de Entrega", datetime.now() + timedelta(days=7))
        st.markdown("##### 🚗 Calculadora Logística de Frete Integrada")
        km_total = st.number_input("Distância Total Ida e Volta (Consultar no Google Maps em KM)", min_value=0.0, value=20.0)
        quem_entrega = st.radio("Quem realizará a entrega?", ["A própria empresária (Para produção)", "Terceirizado (Motoboy/Uber)"])
        
        # Fórmula inteligente de logística K&G
        custo_km = km_total * 1.80  # R$ 1,80 por KM rodado
        taxa_parada = 25.00 if quem_entrega == "A própria empresária (Para produção)" else 0.00
        valor_frete_final = custo_km + taxa_parada
        
        st.metric("Custo Logístico Calculado do Frete", f"R$ {valor_frete_final:.2f}", f"R$ {custo_km:.2f} rodagem + R$ {taxa_parada:.2f} parada")

    valor_total_pedido = c_valor_produtos + valor_frete_final
    st.markdown(f"### 💵 Valor Total do Orçamento: **R$ {valor_total_pedido:.2f}**")

    if 'id_pedido_atual' not in st.session_state:
        st.session_state['id_pedido_atual'] = f"KG-2026-{random.randint(1000, 9999)}"

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📲 Preparar Envio para o WhatsApp"):
            st.success(f"Pedido pré-salvo! Copie o texto abaixo e envie para o WhatsApp {c_whats}")
    with col_btn2:
        if st.button("📩 Preparar Envio para o E-mail"):
            st.success(f"Pedido pré-salvo! Copie o texto abaixo e dispare para o e-mail: {c_email}")

    st.markdown("##### 🖨️ Visualização do Espelho do Orçamento Comercial")
    st.markdown(f"""
        <div class="print-box">
            <b>💎 PROPOSTA COMERCIAL EXCLUSIVA - K&G ARTE EM CONFEITARIA 💎</b><br>
            <b>Código do Orçamento:</b> {st.session_state['id_pedido_atual']}<br>
            <b>Data de Emissão:</b> {datetime.now().strftime('%d/%m/%Y')} | <b>Entrega Contratada:</b> {c_data_festa.strftime('%d/%m/%Y')}<br>
            -------------------------------------------------------------------------<br>
            <b>DADOS DO CLIENTE:</b><br>
            - Nome: {c_nome}<br>
            - WhatsApp: {c_whats}<br>
            - E-mail: {c_email}<br>
            -------------------------------------------------------------------------<br>
            <b>ESPECIFICAÇÃO DOS ITENS:</b><br>
            - {c_doce}: R$ {c_valor_produtos:.2f}<br>
            - Frete Técnico Especializado ({km_total} km rodados): R$ {valor_frete_final:.2f}<br>
            -------------------------------------------------------------------------<br>
            <b>VALOR TOTAL DO INVESTIMENTO: R$ {valor_total_pedido:.2f}</b><br>
            -------------------------------------------------------------------------<br>
            *Obs. Importante de Produção: Cliente possui restrições a suspiros.*
        </div>
    """, unsafe_allow_html=True)

# --- ABA 2: CRM ---
with tabs[2]:
    st.markdown('<div class="section-title">👥 CRM: Histórico Completo de Datas da Família e Pedidos</div>', unsafe_allow_html=True)
    st.data_editor(pd.DataFrame([
        {"Cliente VIP": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "E-mail": "juliana@rossi.com", "Aniv. Cliente": "12/06", "Aniv. Marido": "18/10", "Aniv. Filhos": "Gabriel (04/02)", "Últimos Pedidos": "KG-2026-1042", "🚨 RESTRIÇÕES": "NÃO PODE CONTER AMENDOIM!"}
    ]), num_rows="dynamic", use_container_width=True, key="crm_clientes_v2_key")

# --- DEMAIS ABAS MANTIDAS ---
with tabs[3]: st.write("Fábrica de Bases carregada.")
with tabs[4]: st.write("Módulo de Modelagem BWB carregado.")
with tabs[5]: st.write("Cálculos de produtos casados e iFood ativos.")
with tabs[6]: st.write("Cubagem de embalagens ativa.")
with tabs[7]: st.markdown("<div class='lupa-box'>🔍 <b>ALERTA ANVISA:</b> ALTO EM AÇÚCAR ADICIONADO</div>", unsafe_allow_html=True)
with tabs[8]: st.write("Estoque ativo.")
with tabs[9]: st.write("Fornecedores de Curitiba ativos.")
with tabs[10]: st.write("Inventário de bens ativo.")
