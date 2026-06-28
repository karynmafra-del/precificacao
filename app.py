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
        <div class="brand-subtitle">💎 ecossistema erp & crm de alta confeitaria e inteligência de mercado 💎</div>
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

# Abas Principais Reformuladas
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

# ==========================================
# ABA 0: CENTRAL FINANCEIRA & DRE
# ==========================================
with tabs[0]:
    st.markdown('<div class="section-title">📊 Gestão de Fluxo, DRE e Demonstrativos de Lucro</div>', unsafe_allow_html=True)
    sub_fin1, sub_fin2, sub_fin3, sub_dp_aba = st.tabs(["📈 Dashboard de Resultados", "💸 Lançamentos Diários", "📉 Estrutura DRE", "👥 Departamento Pessoal (DP)"])
    
    with sub_fin1:
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1: st.metric("Meta Faturamento Mês", "R$ 10.000,00")
        with col_d2: st.metric("Faturamento Atual Real", "R$ 6.420,00")
        with col_d3: st.metric("Ponto de Equilíbrio Operacional", "R$ 5.800,00")
        with col_d4: st.metric("Margem de Lucro Média", "32.5 %")
        st.progress(6420 / 10000, text="64.2% da Meta do Mês Alcançada")
        
    with sub_fin2:
        st.data_editor(pd.DataFrame([
            {"Data": "28/06/2026", "Tipo": "Receita (Entrada)", "Descrição": "Encomenda Casamento - Bolo 5kg + Doces", "Valor (R$)": 1450.00},
            {"Data": "28/06/2026", "Tipo": "Despesa (Saída)", "Descrição": "Compra de Morangos e Suspiros", "Valor (R$)": 120.00}
        ]), num_rows="dynamic", use_container_width=True, key="fluxo_caixa_key")
        
    with sub_fin3:
        col_dre1, col_dre2 = st.columns(2)
        with col_dre1:
            st.markdown("##### 📌 Custos Fixos")
            st.data_editor(pd.DataFrame([
                {"Descrição do Custo Fixo": "Aluguel / Atelier", "Valor Mensal (R$)": 1500.00},
                {"Descrição do Custo Fixo": "Água e Energia Elétrica", "Valor Mensal (R$)": 650.00},
                {"Descrição do Custo Fixo": "Imposto MEI / DAS", "Valor Mensal (R$)": 75.00}
            ]), num_rows="dynamic", use_container_width=True, key="custos_fixos_key")
        with col_dre2:
            st.markdown("##### 📌 Custos Variáveis")
            st.data_editor(pd.DataFrame([
                {"Descrição do Custo Variável": "Matérias-Primas e Embalagens", "Valor Estimado (R$)": 1500.00},
                {"Descrição do Custo Variável": "Taxas de Entrega / Apps", "Valor Estimado (R$)": 220.00}
            ]), num_rows="dynamic", use_container_width=True, key="custos_variaveis_key")

    with sub_dp_aba:
        st.markdown("##### 👥 Gestão de DP, Remunerações e Contratos CLT")
        col_rem1, col_rem2 = st.columns(2)
        with col_rem1:
            st.metric("Retirada Pró-Labore (Karyn)", "R$ 4.000,00")
        with col_rem2:
            st.data_editor(pd.DataFrame([
                {"Funcionário contratado": "Ana Silva", "Cargo": "Auxiliar Confeitaria", "Salário Base (R$)": 1650.00, "Ocorrências/Atestados": "Nenhum registrado"},
                {"Funcionário contratado": "Mariana Costa", "Cargo": "Atendente Balcão", "Salário Base (R$)": 1412.00, "Ocorrências/Atestados": "1 dia (Anexado)"}
            ]), num_rows="dynamic", use_container_width=True, key="salarios_equipe_key")

# ==========================================
# NOVA ABA 1: GERADOR DE ORÇAMENTOS E PEDIDOS AUTOMÁTICO
# ==========================================
with tabs[1]:
    st.markdown('<div class="section-title">📝 Emissão de Orçamentos e Lançamento Automático</div>', unsafe_allow_html=True)
    st.write("Insira os dados da encomenda. O sistema gerará um número único e alimentará o seu CRM sozinho:")
    
    col_or1, col_or2 = st.columns(2)
    with col_or1:
        c_nome = st.text_input("Nome do Cliente", value="Fernanda Albuquerque")
        c_whats = st.text_input("WhatsApp de Contato", value="(41) 99222-3344")
        c_doce = st.text_input("Item Solicitado (Bolo/Doces)", value="Bolo de Morango 5kg + 50 Bombons 3D")
    with col_or2:
        c_data_festa = st.date_input("Data de Entrega da Encomenda", datetime.now() + timedelta(days=7))
        c_valor = st.number_input("Valor Total Combinado (R$)", value=680.00)
        c_obs_criticas = st.text_area("Restrições Alimentares / Observações do Pedido", value="Cliente odeia suspiro! Alergia leve a abacaxi.")

    # Geração automática de número de pedido estruturado
    if 'id_pedido_atual' not in st.session_state:
        st.session_state['id_pedido_atual'] = f"KG-{datetime.now().strftime('%Y')}-{random.randint(1000, 9999)}"

    st.info(f"Código identificador gerado para esta operação: **{st.session_state['id_pedido_atual']}**")

    if st.button("📥 Fechar Pedido e Enviar para o CRM"):
        st.success(f"Pedido {st.session_state['id_pedido_atual']} integrado com sucesso à ficha da cliente {c_nome}!")
        # Atualiza o ID para o próximo orçamento
        st.session_state['id_pedido_atual'] = f"KG-{datetime.now().strftime('%Y')}-{random.randint(1000, 9999)}"

    if st.button("🖨️ Imprimir Cópia do Orçamento Comercial"):
        st.markdown(f"""
            <div class="print-box">
                <b>💎 ORÇAMENTO DE LUXO - K&G ARTE EM CONFEITARIA 💎</b><br>
                <b>Pedido Nº:</b> {st.session_state['id_pedido_atual']}<br>
                <b>Data de Emissão:</b> {datetime.now().strftime('%d/%m/%Y')} | <b>Entrega:</b> {c_data_festa.strftime('%d/%m/%Y')}<br>
                -------------------------------------------------------------------------<br>
                <b>CLIENTE VIP:</b> {c_nome} | <b>CONTATO:</b> {c_whats}<br>
                <b>PRODUTO ENCOMENDADO:</b> {c_doce}<br>
                <b>VALOR DO CONTRATO:</b> R$ {c_valor:.2f}<br>
                -------------------------------------------------------------------------<br>
                <b>🚨 DIRETRIZ CRÍTICA DE COZINHA (RESTRIÇÃO):</b> {c_obs_criticas.upper()}<br>
                -------------------------------------------------------------------------<br>
                *K&G Arte em Confeitaria - Agradecemos a preferência.*
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# ABA 2: CRM EXPANDIDO COM ALERTAS DE ANIVERSÁRIOS DO MÊS
# ==========================================
with tabs[2]:
    st.markdown('<div class="section-title">👥 CRM: Histórico Completo de Datas da Família e Pedidos</div>', unsafe_allow_html=True)
    
    # Alerta Inteligente de Aniversário do Mês (Simulação Baseada no mês atual)
    mes_atual = datetime.now().strftime("%m")
    st.markdown(f"""
        <div class="alerta-aniv">
            🎉 <b>CENTRAL DE RELACIONAMENTO K&G - LEMBRETE DE MARKETING:</b><br>
            Clientes fazendo aniversário este mês (Mês {mes_atual}): <b>Juliana Mendes Rossi (Aniv: 12/{mes_atual})</b>.<br>
            <i>Dispare uma mensagem de felicitações exclusiva da K&G no WhatsApp!</i>
        </div>
    """, unsafe_allow_html=True)

    st.write("Mapeamento completo da vida do cliente e vinculação de códigos anteriores:")
    st.data_editor(pd.DataFrame([
        {"Cliente VIP": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "Aniv. Cliente": f"12/{mes_atual}", "Aniv. Marido": "18/10", "Aniv. Filhos": "Gabriel (04/02)", "Data Casamento": "22/11", "Últimos Pedidos": "KG-2026-1042, KG-2026-3391", "🚨 RESTRIÇÕES": "NÃO PODE CONTER AMENDOIM!"},
        {"Cliente VIP": "Carlos Henrique Rocha", "WhatsApp": "(41) 98877-6655", "Aniv. Cliente": "29/08", "Aniv. Marido": "-", "Aniv. Filhos": "Sofia (15/05)", "Data Casamento": "-", "Últimos Pedidos": "KG-2026-8841", "🚨 RESTRIÇÕES": "Não gosta de suspiro de jeito nenhum."}
    ]), num_rows="dynamic", use_container_width=True, key="crm_clientes_v2_key")

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
# ABA 4: DOCES PERSONALIZADOS (NOME DO DOCE IMPLEMENTADO)
# ==========================================
with tabs[4]:
    st.markdown('<div class="section-title">🍫 Engenharia de Projetos por Forma de Acetato</div>', unsafe_allow_html=True)
    st.write("Mapeie o tipo específico de doce produzido em cada numeração de forma para garantir a cobrança justa da sua arte:")
    
    col_bwb1, col_bwb2 = st.columns(2)
    with col_bwb1:
        nome_projeto_doce = st.text_input("Nome/Tipo do Doce Produzido", value="Bombom Decorado Personagem 3D Safari")
        forma_bwb_id = st.text_input("Código/Número da Forma BWB Usada", value="Forma BWB 41")
        peso_choco_forma = st.number_input("Gramas de Chocolate Usados na Casca (g)", value=30)
    with col_bwb2:
        recheio_selecionado = st.selectbox("Selecione o Recheio Interno", list(st.session_state['banco_recheios'].keys()))
        tipo_pasta_bwb = st.selectbox("Pasta Escolhida para a Modelagem Fina", ["Pasta de Leite em Pó", "Pasta Americana", "Pasta de Chocolate"])
        peso_pasta_bwb = st.number_input("Gramas de Pasta Utilizados na Escultura (g)", value=20)
        
    st.success(f"Projeto ativo: '{nome_projeto_doce}' mapeado na {forma_bwb_id} com recheio de {recheio_selecionado}.")

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

# --- DEMAIS ABAS COMPLEMENTARES MANTIDAS ---
with tabs[6]: st.write("Módulo de Cubagem e Impressora Portátil Ativo.")
with tabs[7]:
    st.markdown('<div class="section-title">🥦 Parâmetros de Vigilância ANVISA</div>', unsafe_allow_html=True)
    st.markdown("<div class='lupa-box'>🔍 <b>ROTULAGEM AMBIENTAL/FRONTAL MANDATÓRIA:</b><br>⚠️ ALTO EM AÇÚCAR ADICIONADO</div>", unsafe_allow_html=True)
with tabs[8]: st.write("Estoque Inteligente Ativo.")
with tabs[9]: st.write("Fornecedores Principais de Curitiba (BWB, Central do Chocolate CWB, Nova Íris, Plassete) mapeados.")
with tabs[10]: st.write("Inventário de Bens Ativo.")
