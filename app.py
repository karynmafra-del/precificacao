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

# Estilização de Elite K&G (Verde Esmeralda, Ouro e Customização das Abas em Rosé Nude)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght=400;700&family=Poppins:wght=300;400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #FAF6F0; }
        
        /* Cabeçalho da Marca */
        .brand-header {
            background: linear-gradient(135deg, #043927 0%, #0B533A 100%);
            padding: 25px; border-radius: 15px; text-align: center;
            border-bottom: 4px solid #D4AF37; margin-bottom: 25px;
        }
        .brand-title { font-family: 'Playfair Display', serif; font-size: 36px; color: #FAF6F0; font-weight: 700; }
        .brand-subtitle { font-size: 13px; color: #E3C16F; letter-spacing: 2px; text-transform: uppercase; }
        
        /* Títulos de Seção */
        .section-title { font-family: 'Playfair Display', serif; color: #043927; font-size: 22px; border-left: 4px solid #D4AF37; padding-left: 12px; margin-top: 20px; margin-bottom: 15px; }
        
        /* Caixas de Texto e Exibição */
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; line-height: 1.4; }
        .lupa-box { border: 3px solid black; background: white; color: black; padding: 10px; font-weight: bold; text-align: center; font-size: 14px; margin-bottom: 10px; font-family: Arial, sans-serif; }
        .preco-box { background: #043927; color: #FAF6F0; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #D4AF37; }
        .alerta-aniv { background: #FAF0F2; border-left: 5px solid #D4AF37; padding: 12px; border-radius: 4px; margin-bottom: 15px; }
        
        /* PINTOU AS ABAS EM ROSÉ NUDE */
        button[data-baseweb="tab"] {
            color: #555555 !important;
            font-weight: 400 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #043927 !important;
            font-weight: 600 !important;
        }
        div[role="tablist"] div[style*="left"] {
            background-color: #E6C5BA !important; 
            height: 4px !important;
            border-radius: 2px;
        }
        .stTabs [data-baseweb="tab-highlight-id"] {
            background-color: #E6C5BA !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Ecossistema ERP & CRM Unificado de Alta Confeitaria 💎</div>
    </div>
""", unsafe_allow_html=True)

# Inicialização dos Bancos de Dados na memória para reaproveitamento entre as abas
if 'banco_massas' not in st.session_state:
    st.session_state['banco_massas'] = {"Massa Choc Premium": 18.50, "Pão de Ló de Baunilha": 14.20, "Red Velvet Elite": 25.00}
if 'banco_recheios' not in st.session_state:
    st.session_state['banco_recheios'] = {"Brigadeiro de Ninho": 22.00, "Geleia de Morango Caseira": 18.00, "Brigadeiro ao Leite 32%": 20.00}
if 'banco_caldas' not in st.session_state:
    st.session_state['banco_caldas'] = {"Calda de Chocolate Fina": 5.00, "Calda de Especiarias": 6.50, "Calda Básica de Açúcar": 3.00}
if 'banco_coberturas' not in st.session_state:
    st.session_state['banco_coberturas'] = {"Chantiganache ao Leite": 35.00, "Glacê de Leite em Pó": 28.00}

# Abas do Menu Principal Completas e Unificadas
tabs = st.tabs([
    "💰 CENTRAL FINANCEIRA & DRE",
    "📝 1. ORÇAMENTOS & LOGÍSTICA",
    "👥 2. CRM & ALERTAS",
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
# ABA 0: CENTRAL FINANCEIRA & DRE & DP
# ==========================================
with tabs[0]:
    st.markdown('<div class="section-title">📊 Gestão de Fluxo, DRE e Demonstrativos de Lucro</div>', unsafe_allow_html=True)
    sub_fin1, sub_fin2, sub_fin3, sub_dp_aba = st.tabs(["📈 Dashboard de Resultados", "💸 Lançamentos Diários", "📉 Estrutura DRE (Fixos/Variáveis)", "👥 Departamento Pessoal (DP)"])
    with sub_fin1:
        st.metric("Meta Faturamento Mês", "R$ 10.000,00")
        st.progress(6420 / 10000, text="64.2% da Meta Batida")
    with sub_fin2:
        st.data_editor(pd.DataFrame([{"Data": "28/06/2026", "Tipo": "Receita (Entrada)", "Descrição": "Encomenda Casamento", "Valor (R$)": 1450.00}]), num_rows="dynamic", use_container_width=True, key="fluxo_caixa_key")
    with sub_fin3:
        col_dr1, col_dr2 = st.columns(2)
        with col_dr1:
            st.markdown("##### 📌 Custos Fixos")
            st.data_editor(pd.DataFrame([
                {"Descrição do Custo Fixo": "Aluguel / Atelier", "Valor Mensal (R$)": 1500.00},
                {"Descrição do Custo Fixo": "Água e Energia Elétrica", "Valor Mensal (R$)": 650.00},
                {"Descrição do Custo Fixo": "Imposto MEI / DAS Nacional", "Valor Mensal (R$)": 75.00},
                {"Descrição do Custo Fixo": "Internet e Plataformas de Software", "Valor Mensal (R$)": 150.00}
            ]), num_rows="dynamic", use_container_width=True, key="c_fixos_key")
        with col_dr2:
            st.markdown("##### 📌 Custos Variáveis")
            st.data_editor(pd.DataFrame([
                {"Descrição do Custo Variável": "Matérias-Primas e Embalagens", "Valor Estimado (R$)": 1500.00},
                {"Descrição do Custo Variável": "Gás de Cozinha Recarga", "Valor Estimado (R$)": 135.00},
                {"Descrição do Custo Variável": "Taxas de Entrega / Apps", "Valor Estimado (R$)": 220.00}
            ]), num_rows="dynamic", use_container_width=True, key="c_var_key")
            
        if st.button("🖨️ Imprimir DRE Gerencial"):
            st.markdown('<div class="print-box"><b>K&G ARTE EM CONFEITARIA - DEMONSTRATIVO DE RESULTADOS (DRE)</b><br>Data: '+datetime.now().strftime('%d/%m/%Y')+'<br>---------------------------------------<br>Faturamento Bruto: R$ 6.420,00<br>(-) Custos Fixos Totais: R$ 2.375,00<br>(-) Custos Variáveis Totais: R$ 1.855,00<br>---------------------------------------<br>(=) Lucro Líquido Operacional: R$ 2.190,00</div>', unsafe_allow_html=True)
            
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
# ABA 1: ORÇAMENTOS & ENGENHARIA LOGÍSTICA (COMPLETA)
# ==========================================
with tabs[1]:
    st.markdown('<div class="section-title">📝 Emissão de Orçamentos e Engenharia Logística de Frete</div>', unsafe_allow_html=True)
    st.link_button("🗺️ Abrir Google Maps em Nova Aba para Consultar Rota", "https://www.google.com/maps", type="primary")
    
    col_or1, col_or2 = st.columns(2)
    with col_or1:
        c_nome = st.text_input("Nome Completo do Cliente", value="Fernanda Albuquerque")
        c_whats = st.text_input("WhatsApp de Contato", value="(41) 99222-3344")
        c_email = st.text_input("E-mail do Cliente", value="fernanda.albuquerque@gmail.com")
        c_doce = st.text_input("Item Solicitado (Bolo/Doces)", value="Bolo de Morango Especial 5kg")
        c_valor_produtos = st.number_input("Valor total dos Produtos (R$)", value=650.00)
        c_obs_criticas = st.text_area("🚨 Restrições Alimentares / Observações do Pedido (Ex: Alergias, intolerâncias)", value="Não gosta de uva passa. Alergia severa a canela!")
    
    with col_or2:
        c_endereco = st.text_input("Endereço Completo de Entrega", value="Rua das Chácaras, 1200 - Campo Largo")
        c_referencia = st.text_input("Ponto de Referência para Entrega", value="Chácara Recanto das Flores - Próximo à igrejinha")
        c_horario = st.time_input("Horário Marcado para a Entrega", datetime.now().time())
        c_data_festa = st.date_input("Data de Entrega", datetime.now() + timedelta(days=7))
        
        st.markdown("##### 🚗 Cálculo de Deslocamento e Risco Logístico")
        km_total = st.number_input("Distância Total Ida e Volta (KM)", min_value=0.0, value=20.0)
        quem_entrega = st.radio("Quem realizará a entrega?", ["A própria empresária (Para a produção)", "Terceirizado (Motoboy/Uber)"])
        is_rural = st.checkbox("A entrega será em área rural / estrada de terra? (Adiciona taxa de desgaste veicular e risco)", value=True)
        
        custo_km = km_total * 1.80
        taxa_parada = 25.00 if quem_entrega == "A própria empresária (Para a produção)" else 0.00
        taxa_rural = 35.00 if is_rural else 0.00
        valor_frete_final = custo_km + taxa_parada + taxa_rural
        st.metric("Custo Final do Frete", f"R$ {valor_frete_final:.2f}", f"Estrada de terra/risco: +R$ {taxa_rural:.2f}")

    valor_total_pedido = c_valor_produtos + valor_frete_final
    st.markdown(f"### 💵 Valor Total do Contrato: **R$ {valor_total_pedido:.2f}**")

    if 'id_pedido_atual' not in st.session_state:
        st.session_state['id_pedido_atual'] = f"KG-2026-{random.randint(1000, 9999)}"

    if st.button("🖨️ Gerar Espelho da Proposta Comercial"):
        st.markdown(f"""
            <div class="print-box">
                <b>💎 PROPOSTA COMERCIAL EXCLUSIVA - K&G ARTE EM CONFEITARIA 💎</b><br>
                <b>Código do Pedido:</b> {st.session_state['id_pedido_atual']}<br>
                <b>Data de Emissão:</b> {datetime.now().strftime('%d/%m/%Y')} | <b>Entrega:</b> {c_data_festa.strftime('%d/%m/%Y')} às {c_horario.strftime('%H:%M')}<br>
                -------------------------------------------------------------------------<br>
                <b>DADOS DO CLIENTE:</b><br>
                - Nome: {c_nome} | WhatsApp: {c_whats} | E-mail: {c_email}<br>
                -------------------------------------------------------------------------<br>
                <b>🚨 DIRETRIZES DA COZINHA (RESTRIÇÕES CRÍTICAS):</b><br>
                {c_obs_criticas.upper()}<br>
                -------------------------------------------------------------------------<br>
                <b>LOGÍSTICA DE ENTREGA DE LUXO:</b><br>
                - Endereço: {c_endereco}<br>
                - Ponto de Referência: {c_referencia}<br>
                - Classificação de Rota: {"⚠️ ÁREA RURAL / ESTRADA DE TERRA" if is_rural else "Rota Urbana Padrão"}<br>
                -------------------------------------------------------------------------<br>
                <b>ESPECIFICAÇÃO DE VALORES:</b><br>
                - {c_doce}: R$ {c_valor_produtos:.2f}<br>
                - Frete e Deslocamento Técnico Garantido: R$ {valor_frete_final:.2f}<br>
                -------------------------------------------------------------------------<br>
                <b>VALOR TOTAL DO INVESTIMENTO: R$ {valor_total_pedido:.2f}</b><br>
                -------------------------------------------------------------------------<br>
                *Garantia de pontualidade, estrutura estável e sabor inigualáveis K&G.*
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# ABA 2: CRM & ALERTAS DE ANIVERSÁRIOS DO MÊS
# ==========================================
with tabs[2]:
    st.markdown('<div class="section-title">👥 CRM: Histórico Completo de Datas da Família e Pedidos</div>', unsafe_allow_html=True)
    mes_atual = datetime.now().strftime("%m")
    st.markdown(f"<div class='alerta-aniv'>🎉 <b>CENTRAL DE RELACIONAMENTO K&G:</b> Aniversariante do Mês detectado: <b>Juliana Mendes Rossi (12/{mes_atual})</b>. Dispare um carinho em forma de cupom!</div>", unsafe_allow_html=True)
    st.data_editor(pd.DataFrame([
        {"Cliente VIP": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "E-mail": "juliana@rossi.com", "Aniv. Cliente": f"12/{mes_atual}", "Aniv. Marido": "18/10", "Aniv. Filhos": "Gabriel (04/02)", "Data Casamento": "22/11", "Pedidos Anteriores": "KG-2026-1042", "🚨 RESTRIÇÕES": "NÃO PODE CONTER AMENDOIM!"},
        {"Cliente VIP": "Carlos Henrique Rocha", "WhatsApp": "(41) 98877-6655", "E-mail": "carlos@rocha.com", "Aniv. Cliente": "29/08", "Aniv. Marido": "-", "Aniv. Filhos": "Sofia (15/05)", "Data Casamento": "-", "Pedidos Anteriores": "KG-2026-8841", "🚨 RESTRIÇÕES": "Não gosta de suspiro de jeito nenhum."}
    ]), num_rows="dynamic", use_container_width=True, key="crm_clientes_v3_key")

# ==========================================
# ABA 3: FÁBRICA DE BASES (4 SUB-ABAS DE ENGENHARIA)
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
# ABA 4: DOCES PERSONALIZADOS (BWB + PROJETO)
# ==========================================
with tabs[4]:
    st.markdown('<div class="section-title">🍫 Engenharia de Projetos por Forma de Acetato</div>', unsafe_allow_html=True)
    st.write("Mapeie o tipo específico de doce produzido em cada numeração de forma:")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        nome_projeto_doce = st.text_input("Nome/Tipo do Doce Produzido", value="Bombom Decorado Personagem 3D Safari")
        forma_bwb_id = st.text_input("Código/Número da Forma BWB Usada", value="Forma BWB 41")
        peso_choco_forma = st.number_input("Gramas de Chocolate Usados na Casca (g)", value=30)
    with col_b2:
        recheio_selecionado = st.selectbox("Selecione o Recheio Interno", list(st.session_state['banco_recheios'].keys()))
        tipo_pasta_bwb = st.selectbox("Pasta Escolhida para a Modelagem Fina", ["Pasta de Leite em Pó", "Pasta Americana", "Pasta de Chocolate"])
        peso_pasta_bwb = st.number_input("Gramas de Pasta Utilizados na Escultura (g)", value=20)
    st.success(f"Projeto ativo mapeado com sucesso: '{nome_projeto_doce}' na {forma_bwb_id}.")

# ==========================================
# ABA 5: PRODUTOS COMPLETOS, PESOS, BALCÃO E IFOOD (40% A 50%)
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
            st.metric("📐 Diâmetro Recomendado da Forma de Alumínio", f"{diametro_sugerido} cm", "Para Altura de 10cm")
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
        st.markdown(f"<div class='preco-box' style='background:#901414;'><b>🛵 PREÇO RECOMENDADO IFOOD</b><br><span style='font-size:24px; font-weight:bold;'>R$ {preco_ifood:.2f}</span><br>Taxas do App Cobertas</div>", unsafe_allow_html=True)
    with c_v3:
        st.metric("🛡️ Margem de Flutuação Segurada", f"R$ {(preco_balcao - custo_insumos_base):.2f}", "Blindagem de Insumos")

    st.markdown("##### ⚖️ Pesagem Obrigatória de Distribuição de Carga para a Cozinha:")
    c_g1, c_g2, c_g3, c_g4 = st.columns(4)
    with c_g1: st.metric("Massa Base Total", f"{int(calc_massa)} g")
    with c_g2: st.metric("Recheio, Frutas e Suspiro", f"{int(calc_recheio)} g")
    with c_g3: st.metric("Cobertura / Chantiganache", f"{int(calc_cobertura)} g")
    with c_g4: st.metric("Calda de Regar", f"{int(calc_calda)} g")

    foto_composto = st.file_uploader("📸 Anexar Foto do Padrão Visual Finalizado", type=["png","jpg","jpeg"], key="foto_final")

# --- DEMAIS ABAS COMPLEMENTARES PRESERVADAS ---
with tabs[6]: 
    st.markdown('<div class="section-title">📦 Cubagem de Embalagens e Impressora Portátil</div>', unsafe_allow_html=True)
    st.data_editor(pd.DataFrame([
        {"Item": "Caixa Altura Dupla com Visor", "Preço Pago (R$)": 12.00, "Quantidade": 1},
        {"Item": "Fita de Cetim Larga Ouro", "Preço Proporcional (R$)": 1.20, "Quantidade": 1}
    ]), num_rows="dynamic", use_container_width=True, key="df_embalagens_key")
    texto_portatil = st.text_area("Layout de Saída da Mini Etiqueta Bluetooth:", "K&G Arte em Confeitaria\nFeito com Amor!")

with tabs[7]:
    st.markdown('<div class="section-title">🥦 Parâmetros de Vigilância ANVISA & Validades</div>', unsafe_allow_html=True)
    lupa_acucar = st.checkbox("Alto Teor de Açúcar Adicionado (RDC 429)?", value=True)
    if lupa_acucar:
        st.markdown("<div class='lupa-box'>🔍 <b>ROTULAGEM AMBIENTAL/FRONTAL MANDATÓRIA:</b><br>⚠️ ALTO EM AÇÚCAR ADICIONADO</div>", unsafe_allow_html=True)
    if st.button("🖨️ Emitir Código de Barras EAN-13 para Revenda"):
        st.image("https://barcode.tec-it.com/barcode.ashx?data=789943210562&code=EAN13", caption="Código EAN-13 Atribuído!")

with tabs[8]: 
    st.markdown('<div class="section-title">🛒 Estoque Crítico de Matérias-Primas</div>', unsafe_allow_html=True)
    st.data_editor(pd.DataFrame([{"Ingrediente": "Chocolate Nobre", "Estoque (kg)": 12.0, "Status": "Ok"}]), key="estoque_key")

with tabs[9]: 
    st.markdown('<div class="section-title">🏢 Fornecedores Homologados de Curitiba e Região</div>', unsafe_allow_html=True)
    df_cwb = pd.DataFrame([
        {"Fornecedor": "BWB Embalagens S/A", "Região": "Paraná / Central", "Insumo Líder": "Formas de Acetato e Placas"},
        {"Fornecedor": "Central do Chocolate CWB", "Região": "Curitiba / Centro", "Insumo Líder": "Chocolates Nobres Atacado"},
        {"Fornecedor": "Nova Íris Embalagens", "Região": "Curitiba / Centro", "Insumo Líder": "Caixas de Luxo e Fitas Cetim"}
    ])
    st.dataframe(df_cwb, use_container_width=True)

with tabs[10]: 
    st.markdown('<div class="section-title">🏛️ Relação Patrimonial de Ferramentas (Inventário)</div>', unsafe_allow_html=True)
    st.data_editor(pd.DataFrame([{"Item": "Molde Silicone Rosas Luxo", "Categoria": "Moldes de Silicone", "Quantidade": 4}]), key="inventario_key")
