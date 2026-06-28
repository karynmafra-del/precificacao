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
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; }
        .lupa-box { border: 3px solid black; background: white; color: black; padding: 10px; font-weight: bold; text-align: center; font-size: 14px; margin-bottom: 10px; font-family: Arial, sans-serif; }
        .preco-box { background: #043927; color: #FAF6F0; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Painel de Gestão ERP, CRM e Engenharia de Custos 💎</div>
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

# Abas Principais do Sistema
tabs = st.tabs([
    "💰 CENTRAL FINANCEIRA & DRE",
    "👥 DEPARTAMENTO PESSOAL (DP)",
    "👥 CRM & HISTÓRICO DE PEDIDOS",
    "🥣 1. FÁBRICA DE BASES",
    "🍫 2. DOCES PERSONALIZADOS",
    "🎂 3. PRODUTOS COMPLETOS",
    "📦 EMBALAGENS & IMPRESSÃO",
    "🥦 ANVISA & ADVERTÊNCIAS",
    "🛒 ESTOQUE INTELIGENTE",
    "🏢 FORNECEDORES (CWB)",
    "🏛️ INVENTÁRIO DE BENS"
])

# ==========================================
# ABA 0: CENTRAL FINANCEIRA & DRE
# ==========================================
with tabs[0]:
    st.markdown('<div class="section-title">📊 Gestão de Fluxo, DRE e Demonstrativos de Lucro</div>', unsafe_allow_html=True)
    sub_fin1, sub_fin2, sub_fin3 = st.tabs(["📈 Dashboard de Resultados", "💸 Lançamentos Diários", "📉 Estrutura DRE (Fixos e Variáveis)"])
    
    with sub_fin1:
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1: st.metric("Meta Faturamento Mês", "R$ 10.000,00")
        with col_d2: st.metric("Faturamento Atual Real", "R$ 6.420,00")
        with col_d3: st.metric("Ponto de Equilíbrio Operacional", "R$ 5.800,00")
        with col_d4: st.metric("Margem de Lucro Média", "32.5 %")
        st.progress(6420 / 10000, text="64.2% da Meta do Mês Alcançada")
        
    with sub_fin2:
        st.write("📝 Registro de Entradas e Saídas do Caixa:")
        st.data_editor(pd.DataFrame([
            {"Data": "28/06/2026", "Tipo": "Receita (Entrada)", "Descrição": "Encomenda Casamento - Bolo 5kg + Doces", "Valor (R$)": 1450.00},
            {"Data": "28/06/2026", "Tipo": "Despesa (Saída)", "Descrição": "Compra de Morangos e Suspiros - Mercado Central", "Valor (R$)": 120.00}
        ]), num_rows="dynamic", use_container_width=True, key="fluxo_caixa_key")
        
    with sub_fin3:
        st.write("Registre e acompanhe as despesas estruturais da sua confeitaria:")
        col_dre1, col_dre2 = st.columns(2)
        with col_dre1:
            st.markdown("##### 📌 Custos Fixos (Independem das Vendas)")
            st.data_editor(pd.DataFrame([
                {"Descrição do Custo Fixo": "Aluguel / Espaço Comercial", "Valor Mensal (R$)": 1500.00},
                {"Descrição do Custo Fixo": "Água e Energia Elétrica", "Valor Mensal (R$)": 650.00},
                {"Descrição do Custo Fixo": "Imposto MEI / DAS Nacional", "Valor Mensal (R$)": 75.00},
                {"Descrição do Custo Fixo": "Internet e Plataformas de Software", "Valor Mensal (R$)": 150.00}
            ]), num_rows="dynamic", use_container_width=True, key="custos_fixos_key")
        with col_dre2:
            st.markdown("##### 📌 Custos Variáveis (Sobem conforme a Produção)")
            st.data_editor(pd.DataFrame([
                {"Descrição do Custo Variável": "Matérias-Primas e Insumos de Reposição", "Valor Estimado (R$)": 1500.00},
                {"Descrição do Custo Variável": "Gás de Cozinha Recarga", "Valor Estimado (R$)": 135.00},
                {"Descrição do Custo Variável": "Taxas de Entrega / Logística", "Valor Estimado (R$)": 220.00}
            ]), num_rows="dynamic", use_container_width=True, key="custos_variaveis_key")
            
        if st.button("🖨️ Imprimir DRE Gerencial"):
            st.markdown('<div class="print-box"><b>K&G ARTE EM CONFEITARIA - DEMONSTRATIVO DE RESULTADOS (DRE)</b><br>Data: '+datetime.now().strftime('%d/%m/%Y')+'<br>---------------------------------------<br>Faturamento Bruto: R$ 6.420,00<br>(-) Custos Fixos Totais: R$ 2.375,00<br>(-) Custos Variáveis Totais: R$ 1.855,00<br>---------------------------------------<br>(=) Lucro Líquido Operacional: R$ 2.190,00<br>---------------------------------------<br>Homologado pela Diretoria Executiva</div>', unsafe_allow_html=True)

# ==========================================
# ABA 1: DEPARTAMENTO PESSOAL (CLT, PRÓ-LABORE & RH)
# ==========================================
with tabs[1]:
    st.markdown('<div class="section-title">👥 Gestão de Departamento Pessoal, Remunerações e Ocorrências</div>', unsafe_allow_html=True)
    sub_dp1, sub_dp2 = st.tabs(["💰 Retiradas & Folha de Pagamento", "📋 Registro de Atestados & Contratos"])
    
    with sub_dp1:
        st.write("Controle financeiro de remunerações da equipe e da proprietária:")
        col_rem1, col_rem2 = st.columns(2)
        with col_rem1:
            st.markdown("##### 👑 Pró-Labore da Empresária")
            st.metric("Retirada Mensal Fixada (Karyn)", "R$ 4.000,00")
        with col_rem2:
            st.markdown("##### 👥 Folha de Salários (Equipe)")
            st.data_editor(pd.DataFrame([
                {"Funcionário contratado": "Ana Silva", "Cargo": "Auxiliar de Confeitaria", "Salário Base (R$)": 1650.00},
                {"Funcionário contratado": "Mariana Costa", "Cargo": "Atendente de Balcão", "Salário Base (R$)": 1412.00}
            ]), num_rows="dynamic", use_container_width=True, key="salarios_equipe_key")
            
    with sub_dp2:
        st.write("Controle administrativo de ocorrências trabalhistas e status de contratação na lei:")
        st.data_editor(pd.DataFrame([
            {"Funcionário": "Ana Silva", "Status do Contrato": "CLT Ativo", "Atestados Apresentados": "Nenhum registrado", "Histórico de Férias": "Período aquisitivo em andamento"},
            {"Funcionário": "Mariana Costa", "Status do Contrato": "CLT Ativo", "Atestados Apresentados": "1 dia (Anexado ao prontuário)", "Histórico de Férias": "Regular"},
            {"Funcionário": "Candidata em Seleção", "Status do Contrato": "Admissão Pendente", "Atestados Apresentados": "Exame admissional agendado", "Histórico de Férias": "-"}
        ]), num_rows="dynamic", use_container_width=True, key="rh_ocorrencias_key")

# ==========================================
# ABA 2: CRM & HISTÓRICO DE PEDIDOS
# ==========================================
with tabs[2]:
    st.markdown('<div class="section-title">👥 Gestão de Relacionamento (CRM) e Fichas de Atendimento</div>', unsafe_allow_html=True)
    sub_crm1, sub_crm2 = st.tabs(["📇 Cadastro de Clientes & Restrições", "📋 Histórico de Encomendas & Pedidos"])
    
    with sub_crm1:
        st.data_editor(pd.DataFrame([
            {"Cliente VIP": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "Aniversário": "12/04", "🚨 OBSERVAÇÕES / RESTRIÇÕES CRÍTICAS": "NÃO PODE CONTER AMENDOIM (Alergia Severa)!"},
            {"Cliente VIP": "Carlos Henrique Rocha", "WhatsApp": "(41) 98877-6655", "Aniversário": "29/08", "🚨 OBSERVAÇÕES / RESTRIÇÕES CRÍTICAS": "Não gosta de suspiro. Prefere geleia ácida."}
        ]), num_rows="dynamic", use_container_width=True, key="crm_clientes_key")
    with sub_crm2:
        st.data_editor(pd.DataFrame([
            {"ID": "KG-2026-01", "Cliente": "Juliana Mendes Rossi", "Produto Encomendado": "Bolo Supremo de Nozes 3kg", "Data de Entrega": "04/07/2026", "Valor Total (R$)": 450.00, "Status": "Agendado"}
        ]), num_rows="dynamic", use_container_width=True, key="crm_pedidos_key")

# ==========================================
# ABA 3: FÁBRICA DE BASES
# ==========================================
with tabs[3]:
    st.markdown('<div class="section-title">🥣 Central de Produção de Sub-Bases Cadastradas</div>', unsafe_allow_html=True)
    sub_b1, sub_b2, sub_b3, sub_b4 = st.tabs(["🍞 Massas de Bolo", "🍓 Recheios Estruturados", "💧 Caldas para Molhar", "✨ Coberturas & Blindagens"])
    with sub_b1:
        m_edit = st.data_editor(pd.DataFrame(list(st.session_state['banco_massas'].items()), columns=["Nome da Massa", "Custo por kg (R$)"]), num_rows="dynamic", use_container_width=True, key="m_edit_key")
        st.session_state['banco_massas'] = dict(m_edit.values)
    with sub_b2:
        r_edit = st.data_editor(pd.DataFrame(list(st.session_state['banco_recheios'].items()), columns=["Nome do Recheio", "Custo por kg (R$)"]), num_rows="dynamic", use_container_width=True, key="r_edit_key")
        st.session_state['banco_recheios'] = dict(r_edit.values)
    with sub_b3:
        c_edit = st.data_editor(pd.DataFrame(list(st.session_state['banco_caldas'].items()), columns=["Nome da Calda", "Custo por kg (R$)"]), num_rows="dynamic", use_container_width=True, key="c_edit_key")
        st.session_state['banco_caldas'] = dict(c_edit.values)
    with sub_b4:
        cob_edit = st.data_editor(pd.DataFrame(list(st.session_state['banco_coberturas'].items()), columns=["Nome da Cobertura", "Custo por kg (R$)"]), num_rows="dynamic", use_container_width=True, key="cob_edit_key")
        st.session_state['banco_coberturas'] = dict(cob_edit.values)

# ==========================================
# ABA 4: DOCES PERSONALIZADOS
# ==========================================
with tabs[4]:
    st.markdown('<div class="section-title">🍫 Engenharia de Doces Personalizados (Formas BWB)</div>', unsafe_allow_html=True)
    col_bwb1, col_bwb2 = st.columns(2)
    with col_bwb1:
        forma_bwb_id = st.text_input("Código/Número da Forma BWB Usada", value="BWB 9431")
        peso_choco_forma = st.number_input("Gramas de Chocolate por Casquinha (g)", value=25)
    with col_bwb2:
        tipo_pasta_bwb = st.selectbox("Pasta Escolhida para Modelagem", ["Pasta de Leite em Pó", "Pasta Americana"])
        peso_pasta_bwb = st.number_input("Gramas de Pasta por Unidade (g)", value=10)

# ==========================================
# ABA 5: PRODUTOS COMPLETOS & CALCULADORA IFOOD
# ==========================================
with tabs[5]:
    st.markdown('<div class="section-title">📐 Engenharia Estrutural de Pesos e Precificação Balcão vs iFood</div>', unsafe_allow_html=True)
    col_prop1, col_prop2 = st.columns(2)
    with col_prop1:
        nome_bolo_final = st.text_input("Nome do Produto Final Homologado", value="Bolo de Morango Especial com Suspiros")
        peso_alvo = st.number_input("Defina o Peso Alvo Solicitado pelo Cliente (kg)", min_value=1.0, value=5.0)
        formato_forma = st.selectbox("Formato Geométrico da Forma", ["Redonda", "Quadrada", "Retangular"])
        margem_desejada = st.slider("Defina a sua Margem de Segurança (%) contra alta de insumos", min_value=40, max_value=50, value=45)
    
    with col_prop2:
        peso_alvo_g = peso_alvo * 1000
        calc_massa = peso_alvo_g * 0.35
        calc_recheio = peso_alvo_g * 0.40
        calc_cobertura = peso_alvo_g * 0.15
        calc_calda = peso_alvo_g * 0.10
        custo_insumos_base = (peso_alvo * 25.0)
        
        if formato_forma == "Redonda":
            diametro_sugerido = math.ceil(2 * math.sqrt(peso_alvo_g / (3.14 * 10 * 0.6)))
            st.metric("📐 Diâmetro Recomendado da Forma", f"{diametro_sugerido} cm")
        else:
            st.metric("📐 Medida Recomendada da Forma", "35x25 cm")
        st.metric("💵 Custo Real Estimado de Produção", f"R$ {custo_insumos_base:.2f}")

    st.markdown("### 💰 Tabela Inteligente de Venda Comercial")
    fator_margem = (100 - margem_desejada) / 100
    preco_balcao = custo_insumos_base / fator_margem
    preco_ifood = preco_balcao / 0.75
    
    c_v1, c_v2, c_v3 = st.columns(3)
    with c_v1:
        st.markdown(f"<div class='preco-box'><b>🛍️ PREÇO RECOMENDADO BALCÃO</b><br><span style='font-size:24px; font-weight:bold;'>R$ {preco_balcao:.2f}</span><br>Lucro Protegido de {margem_desejada}%</div>", unsafe_allow_html=True)
    with c_v2:
        st.markdown(f"<div class='preco-box' style='background:#901414;'><b>🛵 PREÇO RECOMENDADO IFOOD</b><br><span style='font-size:24px; font-weight:bold;'>R$ {preco_ifood:.2f}</span><br>Taxas de App Cobertas</div>", unsafe_allow_html=True)
    with c_v3:
        st.metric("🛡️ Margem de Flutuação Segurada", f"R$ {(preco_balcao - custo_insumos_base):.2f}", "Margem para suportar altas")

    foto_composto = st.file_uploader("📸 Anexar Foto do Padrão Visual Finalizado", type=["png","jpg","jpeg"], key="foto_final")

# --- DEMAIS ABAS COMPLEMENTARES MANTIDAS ---
with tabs[6]: st.write("Módulo de Cubagem e Impressora Portátil Ativo.")
with tabs[7]:
    st.markdown('<div class="section-title">🥦 Parâmetros de Vigilância ANVISA</div>', unsafe_allow_html=True)
    st.markdown("<div class='lupa-box'>🔍 <b>ROTULAGEM AMBIENTAL/FRONTAL MANDATÓRIA:</b><br>⚠️ ALTO EM AÇÚCAR ADICIONADO</div>", unsafe_allow_html=True)
with tabs[8]: st.write("Estoque Inteligente Ativo.")
with tabs[9]:
    st.write("Fornecedores Principais de Curitiba (BWB, Central do Chocolate CWB, Nova Íris, Plassete).")
with tabs[10]: st.write("Inventário de Bens Ativo.")
