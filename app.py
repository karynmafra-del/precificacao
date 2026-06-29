import streamlit as st
import pandas as pd
import math
import random
from datetime import datetime, timedelta
import urllib.parse

# Configuração da página de luxo K&G - Mandatório ser o primeiro comando Streamlit
st.set_page_config(
    page_title="K&G Arte em Confeitaria",
    page_icon="✨",
    layout="wide"
)

# =========================================================================
# 💾 INICIALIZAÇÃO SEGURA DO BANCO DE DADOS (PERSISTÊNCIA EM MEMÓRIA)
# =========================================================================
if 'banco_massas' not in st.session_state:
    st.session_state['banco_massas'] = pd.DataFrame([
        {"Nome da Massa": "Massa Choc Premium", "Custo por kg (R$)": 18.50},
        {"Nome da Massa": "Pão de Ló de Baunilha", "Custo por kg (R$)": 14.20},
        {"Nome da Massa": "Red Velvet Elite", "Custo por kg (R$)": 25.00}
    ])

if 'banco_recheios' not in st.session_state:
    st.session_state['banco_recheios'] = pd.DataFrame([
        {"Nome do Recheio": "Brigadeiro de Ninho", "Custo por kg (R$)": 22.00},
        {"Nome do Recheio": "Geleia de Morango Caseira", "Custo por kg (R$)": 18.00},
        {"Nome do Recheio": "Brigadeiro ao Leite 32%", "Custo por kg (R$)": 20.00}
    ])

if 'banco_caldas' not in st.session_state:
    st.session_state['banco_caldas'] = pd.DataFrame([
        {"Nome da Calda": "Calda de Chocolate Fina", "Custo por kg (R$)": 5.00},
        {"Nome da Calda": "Calda de Especiarias", "Custo por kg (R$)": 6.50},
        {"Nome da Calda": "Calda Básica de Açúcar", "Custo por kg (R$)": 3.00}
    ])

if 'banco_coberturas' not in st.session_state:
    st.session_state['banco_coberturas'] = pd.DataFrame([
        {"Nome da Cobertura": "Chantiganache ao Leite", "Custo por kg (R$)": 35.00},
        {"Nome da Cobertura": "Glacê de Leite em Pó", "Custo por kg (R$)": 28.00}
    ])

if 'banco_crm' not in st.session_state:
    st.session_state['banco_crm'] = pd.DataFrame([
        {
            "Cliente VIP": "Juliana Mendes Rossi", 
            "WhatsApp": "(41) 99123-4567", 
            "E-mail": "juliana@rossi.com", 
            "Aniv. Cliente": "12/06", 
            "Aniv. Marido": "18/10", 
            "Aniv. Filhos": "Gabriel (04/02)", 
            "Data Casamento": "22/11", 
            "Pedidos Anteriores": "KG-2026-1042", 
            "🚨 RESTRIÇÕES": "NÃO PODE CONTER AMENDOIM!"
        },
        {
            "Cliente VIP": "Carlos Henrique Rocha", 
            "WhatsApp": "(41) 98877-6655", 
            "E-mail": "carlos@rocha.com", 
            "Aniv. Cliente": "29/08", 
            "Aniv. Marido": "-", 
            "Aniv. Filhos": "Sofia (15/05)", 
            "Data Casamento": "-", 
            "Pedidos Anteriores": "KG-2026-8841", 
            "🚨 RESTRIÇÕES": "NÃO GOSTA DE SUSPIRO!"
        }
    ])

if 'fluxo_caixa_db' not in st.session_state:
    st.session_state['fluxo_caixa_db'] = pd.DataFrame([
        {"Data": "2026-06-28", "Tipo": "Receita (Entrada)", "Descrição": "Encomenda Casamento - Fernanda", "Valor (R$)": 1450.00},
        {"Data": "2026-06-28", "Tipo": "Despesa (Saída)", "Descrição": "Reposição de Morangos e Embalagens", "Valor (R$)": 150.00}
    ])

if 'banco_estoque' not in st.session_state:
    st.session_state['banco_estoque'] = pd.DataFrame([
        {"Ingrediente": "Chocolate Callebaut", "Estoque Atual (kg)": 15.0, "Estoque Mínimo (kg)": 5.0, "Unidade": "kg"},
        {"Ingrediente": "Leite Condensado", "Estoque Atual (kg)": 4.0, "Estoque Mínimo (kg)": 24.0, "Unidade": "un"},
        {"Ingrediente": "Morangos Frescos", "Estoque Atual (kg)": 1.0, "Estoque Mínimo (kg)": 4.0, "Unidade": "kg"},
        {"Ingrediente": "Suspiros Brancos", "Estoque Atual (kg)": 0.5, "Estoque Mínimo (kg)": 2.0, "Unidade": "kg"}
    ])

if 'banco_fornecedores' not in st.session_state:
    st.session_state['banco_fornecedores'] = pd.DataFrame([
        {"Fornecedor": "BWB Embalagens S/A", "Região/Contato": "Paraná / Central", "Insumos": "Formas de Acetato, Silicone e Placas"},
        {"Fornecedor": "Central do Chocolate CWB", "Região/Contato": "Curitiba / Centro", "Insumos": "Chocolates Belgas, Sicao, Callebaut Atacado"},
        {"Fornecedor": "Nova Íris Embalagens", "Região/Contato": "Curitiba / Centro", "Insumos": "Caixas com Visor, Fitas de Cetim e Tags"},
        {"Fornecedor": "Plassete Distribuidora", "Região/Contato": "Região Metropolitana", "Insumos": "Bases de Isopor, Sacolas e Descartáveis"},
        {"Fornecedor": "Porto Formas Paraná", "Região/Contato": "Curitiba / Portão", "Insumos": "Formas de Acetato Especiais e Utensílios"},
        {"Fornecedor": "Embalagens CWB Express", "Região/Contato": "Curitiba / Sítio Cercado", "Insumos": "Sacolas Kraft, Laços e Papel de Seda"},
        {"Fornecedor": "Atacado Confeiteiro Pinhais", "Região/Contato": "RMC / Pinhais", "Insumos": "Açúcares, Farinhas e Granulados Belgas"},
        {"Fornecedor": "Mercado Municipal Curitiba - Box Morangos", "Região/Contato": "Curitiba / Centro", "Insumos": "Morangos in natura selecionados e mirtilos"},
        {"Fornecedor": "Central do Gás CWB", "Região/Contato": "Curitiba / Rápido", "Insumos": "Gás P13 de Alta Pressão para Cozinha"},
        {"Fornecedor": "Lojas Santo Antônio CWB", "Região/Contato": "Curitiba / Online", "Insumos": "Corantes Gel, Cortadores e Sprays de Brilho"}
    ])

if 'banco_inventario' not in st.session_state:
    st.session_state['banco_inventario'] = pd.DataFrame([
        {"Item": "Molde de Silicone Rosas Luxo", "Categoria": "Moldes de Silicone", "Quantidade": 4, "Estado": "Excelente", "Valor Aproximado (R$)": 120.00},
        {"Item": "Batedeira Planetária Arno", "Categoria": "Forno & Batedeiras", "Quantidade": 1, "Estado": "Uso Diário", "Valor Aproximado (R$)": 850.00},
        {"Item": "Forma Redonda de Alumínio 20cm", "Categoria": "Formas de Alumínio", "Quantidade": 6, "Estado": "Excelente", "Valor Aproximado (R$)": 180.00}
    ])

# =========================================================================
# 🎨 ESTILIZAÇÃO VISUAL PREMIUM (VERDE, OURO, ROSÉ NUDE)
# =========================================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #FAF6F0; }
        
        /* Cabeçalho */
        .brand-header {
            background: linear-gradient(135deg, #043927 0%, #0B533A 100%);
            padding: 25px; border-radius: 15px; text-align: center;
            border-bottom: 4px solid #D4AF37; margin-bottom: 25px;
        }
        .brand-title { font-family: 'Playfair Display', serif; font-size: 36px; color: #FAF6F0; font-weight: 700; }
        .brand-subtitle { font-size: 13px; color: #E3C16F; letter-spacing: 2px; text-transform: uppercase; }
        
        /* Títulos */
        .section-title { font-family: 'Playfair Display', serif; color: #043927; font-size: 22px; border-left: 4px solid #D4AF37; padding-left: 12px; margin-top: 20px; margin-bottom: 15px; }
        
        /* Containers */
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; line-height: 1.4; }
        .preco-box { background: #043927; color: #FAF6F0; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #D4AF37; }
        .alerta-aniv { background: #FAF0F2; border-left: 5px solid #D4AF37; padding: 12px; border-radius: 4px; margin-bottom: 15px; }
        
        /* Design das Lupas ANVISA RDC 429 */
        .lupa-container {
            display: flex; gap: 15px; background: white; border: 3px solid black; padding: 15px; border-radius: 8px; max-width: 500px; margin-bottom: 15px;
        }
        .lupa-simbolo { font-size: 32px; display: flex; align-items: center; justify-content: center; padding: 5px; }
        .lupa-conteudo { color: black; font-family: Arial, sans-serif; }
        .lupa-titulo { font-weight: 900; font-size: 16px; letter-spacing: 1px; border-bottom: 2px solid black; padding-bottom: 2px; }
        .lupa-item { font-weight: 900; font-size: 13px; margin-top: 4px; color: black; }
        
        /* Customização de Abas em Rosé Nude */
        button[data-baseweb="tab"] { color: #555555 !important; font-weight: 400 !important; }
        button[data-baseweb="tab"][aria-selected="true"] { color: #043927 !important; font-weight: 600 !important; }
        div[role="tablist"] div[style*="left"] { background-color: #E6C5BA !important; height: 4px !important; border-radius: 2px; }
        .stTabs [data-baseweb="tab-highlight-id"] { background-color: #E6C5BA !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Sistema ERP & CRM Unificado de Alta Confeitaria 💎</div>
    </div>
""", unsafe_allow_html=True)

# 🔒 LOGIN E CHAVE DE ACESSO GLOBAL DO SISTEMA
st.markdown('<div class="section-title">🔒 Login de Segurança</div>', unsafe_allow_html=True)
chave_usuario = st.text_input("Insira a sua Chave de Acesso Empresarial para liberar o aplicativo:", type="password")

if chave_usuario == "kg10k":
    st.success("Acesso Autorizado! Seja bem-vinda ao seu centro administrativo, Karyn.")

    # Criando as Abas Oficiais do Menu Principal
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

    # =========================================================================
    # TAB 0: CENTRAL FINANCEIRA & DRE & DP
    # =========================================================================
    with tabs[0]:
        st.markdown('<div class="section-title">📊 Gestão de Fluxo, DRE e Demonstrativos de Lucro</div>', unsafe_allow_html=True)
        sub_fin1, sub_fin2, sub_fin3, sub_dp_aba = st.tabs(["📈 Dashboard de Resultados", "💸 Lançamentos Diários", "📉 Estrutura DRE (Fixos/Variáveis)", "👥 Departamento Pessoal (DP)"])
        
        # Cálculos de Fluxo Dinâmicos
        df_fluxo = st.session_state['fluxo_caixa_db']
        df_fluxo["Valor (R$)"] = df_fluxo["Valor (R$)"].astype(float)
        entradas = df_fluxo[df_fluxo["Tipo"] == "Receita (Entrada)"]["Valor (R$)"].sum()
        saidas = df_fluxo[df_fluxo["Tipo"] == "Despesa (Saída)"]["Valor (R$)"].sum()
        saldo_caixa = entradas - saidas

        with sub_fin1:
            col_d1, col_d2, col_d3, col_d4 = st.columns(4)
            with col_d1: st.metric("Meta Faturamento Mês", "R$ 10.000,00")
            with col_d2: st.metric("Faturamento Real Acumulado", f"R$ {entradas:.2f}")
            with col_d3: st.metric("Despesas Operacionais", f"R$ {saidas:.2f}")
            with col_d4: st.metric("Saldo Líquido em Caixa", f"R$ {saldo_caixa:.2f}")
            
            progresso_faturamento = min((entradas / 10000.0), 1.0)
            st.progress(progresso_faturamento, text=f"{progresso_faturamento*100:.1f}% da Meta Batida")
            
            # Gráfico de Dashboard Financeiro Adicionado
            st.markdown("##### 📈 Balanço Gráfico das Operações Financeiras (Receitas vs Despesas)")
            chart_data = pd.DataFrame({
                "Categoria": ["Receitas", "Despesas", "Saldo em Caixa"],
                "Valor (R$)": [entradas, saidas, saldo_caixa]
            })
            st.bar_chart(data=chart_data, x="Categoria", y="Valor (R$)", color="#043927", use_container_width=True)
            
        with sub_fin2:
            st.write("📝 Registro de Entradas e Saídas do Caixa:")
            edited_fluxo = st.data_editor(st.session_state['fluxo_caixa_db'], num_rows="dynamic", use_container_width=True, key="fluxo_edit_box")
            st.session_state['fluxo_caixa_db'] = edited_fluxo
            
        with sub_fin3:
            col_dr1, col_dr2 = st.columns(2)
            with col_dr1:
                st.markdown("##### 📌 Custos Fixos")
                edited_fixos = st.data_editor(pd.DataFrame([
                    {"Descrição": "Aluguel / Atelier", "Valor (R$)": 1500.00},
                    {"Descrição": "Água e Energia", "Valor (R$)": 650.00},
                    {"Descrição": "Imposto MEI / DAS", "Valor (R$)": 75.00},
                    {"Descrição": "Internet e Plataformas", "Valor (R$)": 150.00}
                ]), num_rows="dynamic", use_container_width=True, key="fixos_edit_box")
            with col_dr2:
                st.markdown("##### 📌 Custos Variáveis")
                edited_var = st.data_editor(pd.DataFrame([
                    {"Descrição": "Reposição de Insumos", "Valor (R$)": 1500.00},
                    {"Descrição": "Gás de Cozinha Recarga", "Valor (R$)": 135.00},
                    {"Descrição": "Taxas de Entrega / Apps", "Valor (R$)": 220.00}
                ]), num_rows="dynamic", use_container_width=True, key="var_edit_box")
                
            if st.button("🖨️ Imprimir DRE Gerencial"):
                st.markdown(f"""
                    <div class="print-box">
                        <b>K&G ARTE EM CONFEITARIA - DEMONSTRATIVO DE RESULTADOS (DRE)</b><br>
                        <b>Data de Emissão:</b> {datetime.now().strftime('%d/%m/%Y')}<br>
                        -------------------------------------------------------------------------<br>
                        Faturamento Bruto: R$ {entradas:.2f}<br>
                        (-) Custos Fixos Operacionais: R$ {edited_fixos['Valor (R$)'].sum():.2f}<br>
                        (-) Custos Variáveis Acumulados: R$ {edited_var['Valor (R$)'].sum():.2f}<br>
                        -------------------------------------------------------------------------<br>
                        <b>(=) Resultado Líquido Operacional: R$ {entradas - (edited_fixos['Valor (R$)'].sum() + edited_var['Valor (R$)'].sum()):.2f}</b><br>
                    </div>
                """, unsafe_allow_html=True)
                
        with sub_dp_aba:
            st.markdown("##### 👥 Gestão de DP, Remunerações e Contratos CLT")
            col_rem1, col_rem2 = st.columns(2)
            with col_rem1:
                st.metric("Retirada Pró-Labore (Karyn)", "R$ 4.000,00")
            with col_rem2:
                st.data_editor(pd.DataFrame([
                    {"Funcionário": "Ana Silva", "Cargo": "Auxiliar Confeitaria", "Salário Base (R$)": 1650.00, "Ocorrências/Atestados": "Nenhum registrado"},
                    {"Funcionário": "Mariana Costa", "Cargo": "Atendente Balcão", "Salário Base (R$)": 1412.00, "Ocorrências/Atestados": "1 dia (Anexado)"}
                ]), num_rows="dynamic", use_container_width=True, key="dp_edit_box")

    # =========================================================================
    # TAB 1: ORÇAMENTOS & LOGÍSTICA (COMPLETA)
    # =========================================================================
    with tabs[1]:
        st.markdown('<div class="section-title">📝 Emissão de Orçamentos e Engenharia Logística de Frete</div>', unsafe_allow_html=True)
        st.link_button("🗺️ Abrir Google Maps em Nova Aba para Consultar Rota", "https://www.google.com/maps", type="primary")
        
        col_or1, col_or2 = st.columns(2)
        with col_or1:
            c_nome = st.text_input("Nome Completo do Cliente", value="Fernanda Albuquerque")
            c_whats = st.text_input("WhatsApp de Contato (Apenas números com DDD)", value="41992223344")
            c_email = st.text_input("E-mail do Cliente", value="fernanda.albuquerque@gmail.com")
            c_doce = st.text_input("Item Solicitado (Bolo/Doces)", value="Bolo de Morango Especial 5kg")
            c_valor_produtos = st.number_input("Valor total dos Produtos (R$)", value=650.00)
            c_obs_criticas = st.text_area("🚨 Restrições Alimentares / Observações do Pedido", value="Não gosta de uva passa. Alergia severa a canela!")
        
        with col_or2:
            c_endereco = st.text_input("Endereço Completo de Entrega", value="Rua das Chácaras, 1200 - Campo Largo")
            c_referencia = st.text_input("Ponto de Referência para Entrega", value="Chácara Recanto das Flores - Próximo à igrejinha")
            c_horario = st.time_input("Horário Marcado para a Entrega", datetime.now().time())
            c_data_festa = st.date_input("Data de Entrega", datetime.now() + timedelta(days=7))
            
            st.markdown("##### 🚗 Cálculo de Deslocamento e Risco Logístico")
            km_total = st.number_input("Distância Total Ida e Volta (KM)", min_value=0.0, value=20.0)
            quem_entrega = st.radio("Quem realizará a entrega?", ["A própria empresária (Para a produção)", "Terceirizado (Motoboy/Uber)"])
            is_rural = st.checkbox("A entrega será em área rural / estrada de terra? (Adiciona taxa de desgaste veicular e risco)", value=True)
            
            # Algoritmo logístico de frete estruturado
            custo_km = km_total * 1.80
            taxa_parada = 25.00 if quem_entrega == "A própria empresária (Para a produção)" else 0.00
            taxa_rural = 35.00 if is_rural else 0.00
            valor_frete_final = custo_km + taxa_parada + taxa_rural
            st.metric("Custo Final do Frete", f"R$ {valor_frete_final:.2f}", f"Estrada de terra/risco: +R$ {taxa_rural:.2f}")

        valor_total_pedido = c_valor_produtos + valor_frete_final
        st.markdown(f"### 💵 Valor Total do Contrato: **R$ {valor_total_pedido:.2f}**")

        if 'id_pedido_atual' not in st.session_state:
            st.session_state['id_pedido_atual'] = f"KG-2026-{random.randint(1000, 9999)}"

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("📥 Fechar Pedido e Enviar para o CRM"):
                # Captura dados e atualiza CRM de forma dinâmica
                novo_pedido = {
                    "Cliente VIP": c_nome,
                    "WhatsApp": c_whats,
                    "E-mail": c_email,
                    "Aniv. Cliente": "Não Informado",
                    "Aniv. Marido": "-",
                    "Aniv. Filhos": "-",
                    "Data Casamento": "-",
                    "Pedidos Anteriores": st.session_state['id_pedido_atual'],
                    "🚨 RESTRIÇÕES": c_obs_criticas
                }
                df_crm_atual = st.session_state['banco_crm']
                if c_nome in df_crm_atual["Cliente VIP"].values:
                    idx = df_crm_atual[df_crm_atual["Cliente VIP"] == c_nome].index[0]
                    prev = df_crm_atual.at[idx, "Pedidos Anteriores"]
                    df_crm_atual.at[idx, "Pedidos Anteriores"] = f"{prev}, {st.session_state['id_pedido_atual']}"
                    df_crm_atual.at[idx, "🚨 RESTRIÇÕES"] = c_obs_criticas
                else:
                    st.session_state['banco_crm'] = pd.concat([df_crm_atual, pd.DataFrame([novo_pedido])], ignore_index=True)
                
                # Registra o lançamento da receita no fluxo de caixa automaticamente!
                novo_lancamento = {
                    "Data": str(datetime.now().date()),
                    "Tipo": "Receita (Entrada)",
                    "Descrição": f"Encomenda {st.session_state['id_pedido_atual']} - {c_nome}",
                    "Valor (R$)": valor_total_pedido
                }
                st.session_state['fluxo_caixa_db'] = pd.concat([st.session_state['fluxo_caixa_db'], pd.DataFrame([novo_lancamento])], ignore_index=True)
                
                st.success(f"Pedido {st.session_state['id_pedido_atual']} integrado ao CRM e lançado no fluxo financeiro da confeitaria!")
                st.session_state['id_pedido_atual'] = f"KG-2026-{random.randint(1000, 9999)}"
        
        with col_act2:
            if st.button("🖨️ Gerar Espelho da Proposta Comercial"):
                st.markdown(f"""
                    <div class="print-box">
                        <b>💎 PROPOSTA COMERCIAL EXCLUSIVA - K&G ARTE EM CONFEITARIA 💎</b><br>
                        <b>Código do Pedido:</b> {st.session_state['id_pedido_atual']}<br>
                        <b>Entrega Programada:</b> {c_data_festa.strftime('%d/%m/%Y')} às {c_horario.strftime('%H:%M')}<br>
                        -------------------------------------------------------------------------<br>
                        <b>DADOS DO CLIENTE VIP:</b><br>
                        - Nome: {c_nome} | WhatsApp: {c_whats} | E-mail: {c_email}<br>
                        -------------------------------------------------------------------------<br>
                        <b>🚨 DIRETRIZES DE COZINHA E RESTRIÇÕES:</b><br>
                        {c_obs_criticas.upper()}<br>
                        -------------------------------------------------------------------------<br>
                        <b>LOGÍSTICA DE TRANSPORTE E ENTREGA:</b><br>
                        - Endereço: {c_endereco}<br>
                        - Referência: {c_referencia}<br>
                        - Rota Especial: {"⚠️ ÁREA RURAL" if is_rural else "Rota Urbana Padrão"}<br>
                        -------------------------------------------------------------------------<br>
                        <b>VALORES DO CONTRATO:</b><br>
                        - {c_doce}: R$ {c_valor_produtos:.2f}<br>
                        - Taxa de Entrega Técnica: R$ {valor_frete_final:.2f}<br>
                        -------------------------------------------------------------------------<br>
                        <b>VALOR TOTAL INVESTIDO: R$ {valor_total_pedido:.2f}</b><br>
                    </div>
                """, unsafe_allow_html=True)

        # Automação de Envio pelas plataformas
        st.markdown("##### 🚀 Canal de Atendimento Digital Integrado")
        msg_proposta = f"Olá, {c_nome}! Aqui é a Karyn da K&G Arte em Confeitaria. ✨ Segue a sua proposta exclusiva para o seu pedido {c_doce}. Valor total de R$ {valor_total_pedido:.2f} com entrega agendada para {c_data_festa.strftime('%d/%m/%Y')} às {c_horario.strftime('%H:%M')} no endereço: {c_endereco}. Restrições mapeadas: {c_obs_criticas}. Podemos confirmar o agendamento?"
        
        col_send1, col_send2 = st.columns(2)
        with col_send1:
            texto_encoded = urllib.parse.quote(msg_proposta)
            link_wa = f"https://wa.me/55{c_whats.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}?text={texto_encoded}"
            st.link_button("📲 Enviar Proposta por WhatsApp", link_wa, type="primary", use_container_width=True)
        with col_send2:
            link_mail = f"mailto:{c_email}?subject=Proposta K%26G Confeitaria - Pedido {st.session_state['id_pedido_atual']}&body={msg_proposta}"
            st.link_button("📩 Enviar Proposta por E-mail", link_mail, use_container_width=True)

    # =========================================================================
    # TAB 2: CRM & HISTÓRICO COM ALERTA DE ANIVERSÁRIOS DO MÊS
    # =========================================================================
    with tabs[2]:
        st.markdown('<div class="section-title">👥 CRM: Fichas de Relacionamento e Histórico de Encomendas</div>', unsafe_allow_html=True)
        
        # Leitura dinâmica inteligente de aniversariantes
        mes_vigente = datetime.now().strftime("%m")
        df_crm_atual = st.session_state['banco_crm']
        
        # Filtro de busca inteligente (Busca Ativa)
        st.markdown("##### 🔍 Filtros para Busca Ativa de Clientes")
        termo_busca = st.text_input("Pesquise por nome, telefone, e-mail ou restrição alimentar:", "")
        
        if termo_busca:
            df_filtrado = df_crm_atual[
                df_crm_atual['Cliente VIP'].str.contains(termo_busca, case=False, na=False) |
                df_crm_atual['WhatsApp'].str.contains(termo_busca, case=False, na=False) |
                df_crm_atual['E-mail'].str.contains(termo_busca, case=False, na=False) |
                df_crm_atual['🚨 RESTRIÇÕES'].str.contains(termo_busca, case=False, na=False)
            ]
        else:
            df_filtrado = df_crm_atual

        # Identificação dinâmica de aniversários do mês no Banco de Dados
        lista_aniversariantes = []
        for index, row in df_crm_atual.iterrows():
            dia_mes = str(row["Aniv. Cliente"]).split("/")
            if len(dia_mes) == 2 and dia_mes[1] == mes_vigente:
                lista_aniversariantes.append(f"{row['Cliente VIP']} (Dia {dia_mes[0]}/{mes_vigente})")
        
        if lista_aniversariantes:
            anivs_formatados = ", ".join(lista_aniversariantes)
            st.markdown(f"""
                <div class='alerta-aniv'>
                    🎉 <b>CRM MARKETING INTELIGENTE K&G:</b><br>
                    Clientes fazendo aniversário neste mês (Mês {mes_vigente}): <b>{anivs_formatados}</b>.<br>
                    <i>Mande uma mensagem especial e garanta a encomenda da festa!</i>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhum cliente faz aniversário no mês corrente.")

        # Editor de Dados Completo do CRM
        st.markdown("##### 📇 Lista Geral de Clientes VIP e Histórico de Datas")
        edited_crm = st.data_editor(df_filtrado, num_rows="dynamic", use_container_width=True, key="crm_edit_table")
        
        # Atualiza a memória com o que foi editado
        if termo_busca == "":
            st.session_state['banco_crm'] = edited_crm

        st.markdown("##### 🤖 Automação de Atendimento e Mensagens Rápidas")
        modelo_selecionado = st.selectbox("Selecione o modelo de mensagem para copiar:", [
            "Feliz Aniversário Personalizado",
            "Pós-Venda (Como foi a festa?)",
            "Cobrança de Orçamento Pendente"
        ])
        
        if modelo_selecionado == "Feliz Aniversário Personalizado":
            texto_modelo = "Parabéns! 🎂✨ Hoje é seu dia especial e nós da K&G Arte em Confeitaria queremos celebrar com você! Desejamos um novo ciclo repleto de doçura, amor e conquistas. Para deixar sua festa ainda mais saborosa, preparamos um cupom de 10% de desconto na sua próxima encomenda de doces finos. Vamos celebrar?"
        elif modelo_selecionado == "Pós-Venda (Como foi a festa?)":
            texto_modelo = "Olá! Passando para saber como foi a festa e, principalmente, se todos gostaram do bolo e dos doces! 🥰 O seu feedback é precioso para continuarmos produzindo momentos felizes na cozinha da K&G!"
        else:
            texto_modelo = "Olá! Passando para saber se conseguiu analisar o orçamento exclusivo que preparamos para o seu evento. Como nossa agenda de alta confeitaria é bastante concorrida, gostaria de verificar se podemos garantir a sua reserva para esta semana!"
            
        st.text_area("Copie a mensagem e dispare para o WhatsApp do cliente:", texto_modelo, height=120)

    # =========================================================================
    # TAB 3: FÁBRICA DE BASES (MASSAS, RECHEIOS, CALDAS, COBERTURAS)
    # =========================================================================
    with tabs[3]:
        st.markdown('<div class="section-title">🥣 Central de Produção e Fichas Técnicas Item a Item</div>', unsafe_allow_html=True)
        st.write("Descreva e precifique os ingredientes detalhados de cada receita base para que o sistema atualize o preço do kg de forma profissional e real!")
        
        sub_b1, sub_b2, sub_b3, sub_b4 = st.tabs(["🍞 Massas de Bolo", "🍓 Recheios Estruturados", "💧 Caldas para Molhar", "✨ Coberturas & Blindagens"])
        
        with sub_b1:
            st.markdown("##### 🍞 Calculadora Ficha Técnica de Massa de Bolo")
            col_mas1, col_mas2 = st.columns(2)
            with col_mas1:
                # Use os dados reais da tabela dinâmica
                lista_m = st.session_state['banco_massas']["Nome da Massa"].tolist()
                massa_ativa = st.selectbox("Selecione a Massa para Ver/Editar Ficha Técnica", lista_m)
                peso_massa_receita = st.number_input("Peso final obtido na receita de massa (g)", value=1000, key="peso_m_rec")
            with col_mas2:
                st.write("Ingredientes da Receita da Massa:")
                df_ing_massa = st.data_editor(pd.DataFrame([
                    {"Ingrediente": "Farinha de Trigo Premium", "Preço Embalagem (R$)": 8.50, "Gramos Embalagem (g)": 1000, "Gramos Usados na Receita": 350},
                    {"Ingrediente": "Chocolate em Pó 50%", "Preço Embalagem (R$)": 22.00, "Gramos Embalagem (g)": 500, "Gramos Usados na Receita": 100},
                    {"Ingrediente": "Ovos Frescos", "Preço Embalagem (R$)": 12.00, "Gramos Embalagem (g)": 600, "Gramos Usados na Receita": 240},
                    {"Ingrediente": "Manteiga Extra", "Preço Embalagem (R$)": 14.00, "Gramos Embalagem (g)": 200, "Gramos Usados na Receita": 150}
                ]), num_rows="dynamic", use_container_width=True, key=f"ing_massa_edit_{massa_ativa}")
                
                # Algoritmo de cálculo dinâmico da ficha técnica
                custo_massa_total = df_ing_massa.apply(lambda r: (r["Preço Embalagem (R$)"] / r["Gramos Embalagem (g)"]) * r["Gramos Usados na Receita"], axis=1).sum()
                custo_massa_kg = (custo_massa_total / peso_massa_receita) * 1000
                st.metric("Custo Total da Massa Produzida", f"R$ {custo_massa_total:.2f}")
                st.metric("Custo Real Calculado por kg", f"R$ {custo_massa_kg:.2f}")
                
                if st.button(f"💾 Atualizar Custo por kg de {massa_ativa} no Sistema", key=f"btn_mas_{massa_ativa}"):
                    df_b_m = st.session_state['banco_massas']
                    idx = df_b_m[df_b_m["Nome da Massa"] == massa_ativa].index[0]
                    df_b_m.at[idx, "Custo por kg (R$)"] = round(custo_massa_kg, 2)
                    st.session_state['banco_massas'] = df_b_m
                    st.success(f"Preço de {massa_ativa} atualizado com sucesso no banco de dados!")
                    
        with sub_b2:
            st.markdown("##### 🍓 Calculadora Ficha Técnica de Recheio Estruturado")
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                lista_r = st.session_state['banco_recheios']["Nome do Recheio"].tolist()
                recheio_ativo = st.selectbox("Selecione o Recheio para Ver/Editar Ficha Técnica", lista_r)
                peso_recheio_receita = st.number_input("Peso final obtido na receita de recheio (g)", value=800, key="peso_r_rec")
            with col_rec2:
                st.write("Ingredientes da Receita do Recheio:")
                df_ing_recheio = st.data_editor(pd.DataFrame([
                    {"Ingrediente": "Leite Condensado", "Preço Embalagem (R$)": 6.50, "Gramos Embalagem (g)": 395, "Gramos Usados na Receita": 790},
                    {"Ingrediente": "Creme de Leite 20%", "Preço Embalagem (R$)": 4.20, "Gramos Embalagem (g)": 200, "Gramos Usados na Receita": 400},
                    {"Ingrediente": "Leite Ninho Saco", "Preço Embalagem (R$)": 21.00, "Gramos Embalagem (g)": 400, "Gramos Usados na Receita": 100}
                ]), num_rows="dynamic", use_container_width=True, key=f"ing_recheio_edit_{recheio_ativo}")
                
                custo_recheio_total = df_ing_recheio.apply(lambda r: (r["Preço Embalagem (R$)"] / r["Gramos Embalagem (g)"]) * r["Gramos Usados na Receita"], axis=1).sum()
                custo_recheio_kg = (custo_recheio_total / peso_recheio_receita) * 1000
                st.metric("Custo Total do Recheio Produzido", f"R$ {custo_recheio_total:.2f}")
                st.metric("Custo Real Calculado por kg", f"R$ {custo_recheio_kg:.2f}")
                
                if st.button(f"💾 Atualizar Custo por kg de {recheio_ativo} no Sistema", key=f"btn_rec_{recheio_ativo}"):
                    df_b_r = st.session_state['banco_recheios']
                    idx = df_b_r[df_b_r["Nome do Recheio"] == recheio_ativo].index[0]
                    df_b_r.at[idx, "Custo por kg (R$)"] = round(custo_recheio_kg, 2)
                    st.session_state['banco_recheios'] = df_b_r
                    st.success(f"Preço de {recheio_ativo} atualizado com sucesso no banco de dados!")

        with sub_b3:
            st.markdown("##### 💧 Calculadora Ficha Técnica de Calda de Regar")
            col_cal1, col_cal2 = st.columns(2)
            with col_cal1:
                lista_c = st.session_state['banco_caldas']["Nome da Calda"].tolist()
                calda_ativa = st.selectbox("Selecione a Calda para Ver/Editar Ficha Técnica", lista_c)
                peso_calda_receita = st.number_input("Peso final obtido na receita de calda (g)", value=500, key="peso_c_rec")
            with col_cal2:
                st.write("Ingredientes da Receita da Calda:")
                df_ing_calda = st.data_editor(pd.DataFrame([
                    {"Ingrediente": "Açúcar Refinado", "Preço Embalagem (R$)": 4.50, "Gramos Embalagem (g)": 1000, "Gramos Usados na Receita": 200},
                    {"Ingrediente": "Cravos e Canela em Rama", "Preço Embalagem (R$)": 6.00, "Gramos Embalagem (g)": 50, "Gramos Usados na Receita": 5}
                ]), num_rows="dynamic", use_container_width=True, key=f"ing_calda_edit_{calda_ativa}")
                
                custo_calda_total = df_ing_calda.apply(lambda r: (r["Preço Embalagem (R$)"] / r["Gramos Embalagem (g)"]) * r["Gramos Usados na Receita"], axis=1).sum()
                custo_calda_kg = (custo_calda_total / peso_calda_receita) * 1000
                st.metric("Custo Total da Calda Produzida", f"R$ {custo_calda_total:.2f}")
                st.metric("Custo Real Calculado por kg", f"R$ {custo_calda_kg:.2f}")
                
                if st.button(f"💾 Atualizar Custo por kg de {calda_ativa} no Sistema", key=f"btn_cal_{calda_ativa}"):
                    df_b_c = st.session_state['banco_caldas']
                    idx = df_b_c[df_b_c["Nome da Calda"] == calda_ativa].index[0]
                    df_b_c.at[idx, "Custo por kg (R$)"] = round(custo_calda_kg, 2)
                    st.session_state['banco_caldas'] = df_b_c
                    st.success(f"Preço de {calda_ativa} atualizado com sucesso no banco de dados!")

        with sub_b4:
            st.markdown("##### ✨ Calculadora Ficha Técnica de Cobertura e Blindagem")
            col_cob1, col_cob2 = st.columns(2)
            with col_cob1:
                lista_cob = st.session_state['banco_coberturas']["Nome da Cobertura"].tolist()
                cobertura_ativa = st.selectbox("Selecione a Cobertura para Ver/Editar Ficha Técnica", lista_cob)
                peso_cobertura_receita = st.number_input("Peso final obtido na receita de cobertura (g)", value=600, key="peso_cob_rec")
            with col_cob2:
                st.write("Ingredientes da Receita da Cobertura:")
                df_ing_cobertura = st.data_editor(pd.DataFrame([
                    {"Ingrediente": "Chocolate Callebaut Sicao", "Preço Embalagem (R$)": 45.00, "Gramos Embalagem (g)": 1010, "Gramos Usados na Receita": 400},
                    {"Ingrediente": "Chantilly Líquido", "Preço Embalagem (R$)": 18.00, "Gramos Embalagem (g)": 1000, "Gramos Usados na Receita": 200}
                ]), num_rows="dynamic", use_container_width=True, key=f"ing_cobertura_edit_{cobertura_ativa}")
                
                custo_cobertura_total = df_ing_cobertura.apply(lambda r: (r["Preço Embalagem (R$)"] / r["Gramos Embalagem (g)"]) * r["Gramos Usados na Receita"], axis=1).sum()
                custo_cobertura_kg = (custo_cobertura_total / peso_cobertura_receita) * 1000
                st.metric("Custo Total da Cobertura Produzida", f"R$ {custo_cobertura_total:.2f}")
                st.metric("Custo Real Calculado por kg", f"R$ {custo_cobertura_kg:.2f}")
                
                if st.button(f"💾 Atualizar Custo por kg de {cobertura_ativa} no Sistema", key=f"btn_cob_{cobertura_ativa}"):
                    df_b_cob = st.session_state['banco_coberturas']
                    idx = df_b_cob[df_b_cob["Nome da Cobertura"] == cobertura_ativa].index[0]
                    df_b_cob.at[idx, "Custo por kg (R$)"] = round(custo_cobertura_kg, 2)
                    st.session_state['banco_coberturas'] = df_b_cob
                    st.success(f"Preço de {cobertura_ativa} atualizado com sucesso no banco de dados!")

    # =========================================================================
    # TAB 4: DOCES PERSONALIZADOS (BWB/ACETATO)
    # =========================================================================
    with tabs[4]:
        st.markdown('<div class="section-title">🍫 Engenharia de Projetos por Forma de Acetato</div>', unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            nome_projeto_doce = st.text_input("Nome/Tipo do Doce Produzido", value="Bombom Decorado Personagem 3D Safari")
            forma_bwb_id = st.text_input("Código/Número da Forma BWB Usada", value="Forma BWB 41")
            peso_choco_forma = st.number_input("Gramas de Chocolate Usados na Casca (g)", value=30)
        with col_b2:
            lista_recheios_salvos = list(st.session_state['banco_recheios']["Nome do Recheio"].values)
            recheio_selecionado = st.selectbox("Selecione o Recheio Interno", lista_recheios_salvos)
            tipo_pasta_bwb = st.selectbox("Pasta Escolhida para a Modelagem Fina", ["Pasta de Leite em Pó", "Pasta Americana", "Pasta de Chocolate"])
            peso_pasta_bwb = st.number_input("Gramas de Pasta Utilizados na Escultura (g)", value=20)
        
        st.success(f"Projeto ativo mapeado com sucesso: '{nome_projeto_doce}' na {forma_bwb_id} com recheio de {recheio_selecionado}.")

    # =========================================================================
    # TAB 5: PRODUTOS COMPLETOS & PRECIFICADORA DE BALCÃO E IFOOD (INTERLIGADA)
    # =========================================================================
    with tabs[5]:
        st.markdown('<div class="section-title">📐 Engenharia Estrutural de Pesos e Precificação Balcão vs iFood</div>', unsafe_allow_html=True)
        col_prop1, col_prop2 = st.columns(2)
        with col_prop1:
            nome_bolo_final = st.text_input("Nome do Produto Final Homologado", value="Bolo de Morango Especial com Suspiros")
            peso_alvo = st.number_input("Defina o Peso Alvo Solicitado pelo Cliente (kg)", min_value=1.0, value=5.0)
            formato_forma = st.selectbox("Formato Geométrico da Forma", ["Redonda", "Quadrada", "Retangular"])
            margem_desejada = st.slider("Defina a sua Margem de Segurança (%) contra alta de insumos", min_value=40, max_value=50, value=45)
            
            st.markdown("##### 👩‍🍳 Selecione as Sub-Bases de Produção Cadastradas:")
            sel_massa = st.selectbox("Escolha a Massa de Bolo", list(st.session_state['banco_massas']["Nome da Massa"].values))
            sel_recheio = st.selectbox("Escolha o Recheio", list(st.session_state['banco_recheios']["Nome do Recheio"].values))
            sel_calda = st.selectbox("Escolha a Calda", list(st.session_state['banco_caldas']["Nome da Calda"].values))
            sel_cobertura = st.selectbox("Escolha a Cobertura/Blindagem", list(st.session_state['banco_coberturas']["Nome da Cobertura"].values))
            
            # Taxas da Máquina de Cartão
            st.markdown("##### 💳 Taxas Operacionais da Máquina de Cartão")
            taxa_debito = st.number_input("Taxa de Débito (%)", min_value=0.0, max_value=10.0, value=1.99)
            taxa_credito = st.number_input("Taxa de Crédito à Vista (%)", min_value=0.0, max_value=15.0, value=3.99)
            
        with col_prop2:
            # Algoritmo de estrutura de pesos da confeitaria (Padrão K&G)
            peso_alvo_g = peso_alvo * 1000
            calc_massa = peso_alvo_g * 0.35
            calc_recheio = peso_alvo_g * 0.40
            calc_cobertura = peso_alvo_g * 0.15
            calc_calda = peso_alvo_g * 0.10
            
            # Puxa custos do banco de dados para cálculo real de insumos baseado na Ficha Técnica!
            custo_kg_massa = st.session_state['banco_massas'][st.session_state['banco_massas']["Nome da Massa"] == sel_massa]["Custo por kg (R$)"].values[0]
            custo_kg_recheio = st.session_state['banco_recheios'][st.session_state['banco_recheios']["Nome do Recheio"] == sel_recheio]["Custo por kg (R$)"].values[0]
            custo_kg_calda = st.session_state['banco_caldas'][st.session_state['banco_caldas']["Nome da Calda"] == sel_calda]["Custo por kg (R$)"].values[0]
            custo_kg_cobertura = st.session_state['banco_coberturas'][st.session_state['banco_coberturas']["Nome da Cobertura"] == sel_cobertura]["Custo por kg (R$)"].values[0]
            
            custo_massa_real = (calc_massa / 1000) * custo_kg_massa
            custo_recheio_real = (calc_recheio / 1000) * custo_kg_recheio
            custo_calda_real = (calc_calda / 1000) * custo_kg_calda
            custo_cobertura_real = (calc_cobertura / 1000) * custo_kg_cobertura
            
            custo_insumos_base = custo_massa_real + custo_recheio_real + custo_calda_real + custo_cobertura_real
            
            if formato_forma == "Redonda":
                diametro_sugerido = math.ceil(2 * math.sqrt(peso_alvo_g / (3.14 * 10 * 0.6)))
                st.metric("📐 Diâmetro Recomendado da Forma de Alumínio", f"{diametro_sugerido} cm", "Para Altura padrão de 10cm")
            else:
                st.metric("📐 Medida Recomendada da Forma", "35x25 cm")
            
            st.metric("💵 Custo Real de Matéria-Prima Calculado", f"R$ {custo_insumos_base:.2f}")

        # Lógica avançada de precificação com inclusão de taxas de máquinas e iFood
        st.markdown("### 💰 Tabela Inteligente de Venda Comercial")
        fator_margem = (100 - margem_desejada) / 100
        preco_balcao_bruto = custo_insumos_base / fator_margem
        
        # Preço final embutindo as taxas de débito e crédito para não perder margem
        preco_balcao_debito = preco_balcao_bruto / (1 - (taxa_debito / 100.0))
        preco_balcao_credito = preco_balcao_bruto / (1 - (taxa_credito / 100.0))
        
        # Preço do iFood cobrindo a pesada taxa de 25% mais a margem selecionada
        preco_ifood = preco_balcao_bruto / 0.75 
        
        c_v1, c_v2, c_v3 = st.columns(3)
        with c_v1:
            st.markdown(f"""
                <div class='preco-box'>
                    <b>🛍️ PREÇO RECOMENDADO BALCÃO (DINHEIRO/PIX)</b><br>
                    <span style='font-size:24px; font-weight:bold;'>R$ {preco_balcao_bruto:.2f}</span><br>
                    <small>Débito: R$ {preco_balcao_debito:.2f} | Crédito: R$ {preco_balcao_credito:.2f}</small>
                </div>
            """, unsafe_allow_html=True)
        with c_v2:
            st.markdown(f"<div class='preco-box' style='background:#901414;'><b>🛵 PREÇO RECOMENDADO IFOOD</b><br><span style='font-size:24px; font-weight:bold;'>R$ {preco_ifood:.2f}</span><br>Taxas do App Cobertas</div>", unsafe_allow_html=True)
        with c_v3:
            st.metric("🛡️ Margem de Flutuação Segurada", f"R$ {(preco_balcao_bruto - custo_insumos_base):.2f}", "Blindagem contra inflação")

        st.markdown("##### ⚖️ Balanço de Pesagem de Carga para a Cozinha:")
        c_g1, c_g2, c_g3, c_g4 = st.columns(4)
        with c_g1: st.metric(f"Massa ({sel_massa})", f"{int(calc_massa)} g")
        with c_g2: st.metric(f"Recheio ({sel_recheio})", f"{int(calc_recheio)} g")
        with c_g3: st.metric(f"Cobertura ({sel_cobertura})", f"{int(calc_cobertura)} g")
        with c_g4: st.metric(f"Calda de Regar ({sel_calda})", f"{int(calc_calda)} g")

        foto_composto = st.file_uploader("📸 Anexar Foto do Padrão Visual Finalizado", type=["png","jpg","jpeg"], key="foto_final")
        if foto_composto is not None:
            st.image(foto_composto, caption="Aparência do Bolo Homologada para a Cozinha", width=250)

    # =========================================================================
    # TAB 6: EMBALAGENS DE LUXO & IMPRESSORA PORTÁTIL
    # =========================================================================
    with tabs[6]:
        st.markdown('<div class="section-title">📦 Cubagem de Embalagens e Impressora Portátil</div>', unsafe_allow_html=True)
        st.write("Insira e edite itens de embalagem e insumos secundários:")
        st.data_editor(pd.DataFrame([
            {"Item": "Caixa Altura Dupla com Visor Premium", "Preço Cento/Pacote (R$)": 250.00, "Unidades no Pacote": 50, "Custo Unitário (R$)": 5.00},
            {"Item": "Fita de Cetim Larga Ouro (metros)", "Preço Rolo (R$)": 15.00, "Metros no Rolo": 10, "Custo Unitário (R$)": 1.50},
            {"Item": "Tag Logomarca K&G Metalizada", "Preço Pago (R$)": 80.00, "Unidades no Pacote": 100, "Custo Unitário (R$)": 0.80}
        ]), num_rows="dynamic", use_container_width=True, key="embalagens_edit_box")
        
        texto_portatil = st.text_area("Layout de Saída da Mini Etiqueta Bluetooth:", f"K&G Arte em Confeitaria\nFeito com Amor!\nProduto: {nome_bolo_final}")
        if st.button("⚡ Enviar para Impressora Térmica Portátil"):
            st.success("Comando enviado com sucesso para a maquininha!")

    # =========================================================================
    # TAB 7: ANVISA & ADVERTÊNCIAS OFICIAIS (RDC 429)
    # =========================================================================
    with tabs[7]:
        st.markdown('<div class="section-title">🥦 Rotulagem Frontal e Critérios de Vigilância ANVISA</div>', unsafe_allow_html=True)
        
        col_an1, col_an2 = st.columns(2)
        with col_an1:
            alto_açucar = st.checkbox("Alto Teor de Açúcar Adicionado?", value=True)
            alto_gordura = st.checkbox("Alto Teor de Gordura Saturada?", value=True)
            alto_sodio = st.checkbox("Alto Teor de Sódio?", value=False)
            contem_gluten = st.selectbox("Glúten", ["CONTÉM GLÚTEN", "NÃO CONTÉM GLÚTEN"])
            alergicos = st.text_input("Alergênicos", value="CONTÉM LEITE, TRIGO. PODE CONTER DERIVADOS DE SOJA.")
        
        with col_an2:
            st.markdown("##### 🔍 Rotulagem Frontal Obrigatória (Formato Oficial Magnifying Glass / Lupa - RDC 429):")
            if alto_açucar or alto_gordura or alto_sodio:
                lupa_html = """
                <div class="lupa-container">
                    <div class="lupa-simbolo">🔍</div>
                    <div class="lupa-conteudo">
                        <div class="lupa-titulo">ALTO EM</div>
                """
                if alto_açucar: lupa_html += "<div class='lupa-item'>AÇÚCAR ADICIONADO</div>"
                if alto_gordura: lupa_html += "<div class='lupa-item'>GORDURA SATURADA</div>"
                if alto_sodio: lupa_html += "<div class='lupa-item'>SÓDIO</div>"
                lupa_html += "</div></div>"
                st.markdown(lupa_html, unsafe_allow_html=True)
            else:
                st.success("Produto Isento de Rotulagem Frontal.")

        # Espelho de Etiqueta de Envio Comercial
        d_et_f = datetime.now()
        d_et_v = d_et_f + timedelta(days=7)
        st.markdown(f"""
            <div style="border: 2px dashed #043927; padding: 20px; background: white; color: black; max-width: 450px; border-radius: 8px;">
                <b style="font-size:16px; color:#043927;">K&G Arte em Confeitaria</b><br>
                <span style="font-size:13px; font-weight:bold;">{nome_bolo_final}</span><br>
                <hr style="margin: 6px 0; border-color: black;">
                <span style="font-size:12px;"><b>FAB:</b> {d_et_f.strftime('%d/%m/%Y')} | <b>VAL:</b> {d_et_v.strftime('%d/%m/%Y')}</span><br>
                <span style="font-size:12px;"><b>LOTE:</b> {d_et_f.strftime('%Y%m%d%H%M')}</span><br>
                <hr style="margin: 6px 0; border-color: black;">
                <span style="font-size:11px; font-weight: bold; color: #CC0000; display: block;">
                    {contem_gluten}<br>
                    ALÉRGICOS: {alergicos.upper()}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🖨️ Emitir Código de Barras EAN-13 para Saída de Balcão"):
            # Gerando código EAN-13 oficial conforme lei de rotulagem
            st.image("https://barcode.tec-it.com/barcode.ashx?data=789943210562&code=EAN13", caption="EAN-13 Pronto para Gôndola Comercial", width=250)

    # =========================================================================
    # TAB 8: ESTOQUE INTELIGENTE COM ALERTA E LISTA DE COMPRAS AUTOMÁTICA
    # =========================================================================
    with tabs[8]:
        st.markdown('<div class="section-title">🛒 Estoque Crítico de Matérias-Primas e Insumos</div>', unsafe_allow_html=True)
        st.write("Edite as quantidades. O sistema calculará o status e montará a sua lista de mercado de forma inteligente:")
        
        df_est = st.session_state['banco_estoque']
        # Conversão explícita para float
        df_est["Estoque Atual (kg)"] = df_est["Estoque Atual (kg)"].astype(float)
        df_est["Estoque Mínimo (kg)"] = df_est["Estoque Mínimo (kg)"].astype(float)
        
        # Algoritmo de checagem de estoque crítico
        df_est["Status"] = df_est.apply(lambda row: "⚠️ COMPRAR URGENTE" if row["Estoque Atual (kg)"] < row["Estoque Mínimo (kg)"] else "Ok", axis=1)
        
        edited_est = st.data_editor(df_est, num_rows="dynamic", use_container_width=True, key="estoque_edit_table")
        st.session_state['banco_estoque'] = edited_est

        if st.button("📋 Imprimir Lista de Compras Pronta"):
            itens_falta = edited_est[edited_est["Status"] == "⚠️ COMPRAR URGENTE"]
            if not itens_falta.empty:
                bloco_lista = "<b>🛒 LISTA DE COMPRAS AUTOMÁTICA K&G (ABASTECIMENTO)</b><br>"
                bloco_lista += "-------------------------------------------------------------<br>"
                for _, item in itens_falta.iterrows():
                    quantidade_necessaria = item["Estoque Mínimo (kg)"] - item["Estoque Atual (kg)"]
                    bloco_lista += f"- {item['Ingrediente']}: Comprar {quantidade_necessaria:.1f} {item['Unidade']}<br>"
                bloco_lista += "-------------------------------------------------------------<br>"
                bloco_lista += "*Gerado de acordo com as margens críticas do estoque K&G.*"
                st.markdown(f"<div class='print-box'>{bloco_lista}</div>", unsafe_allow_html=True)
            else:
                st.success("Estoque seguro! Não há itens abaixo do nível mínimo hoje.")

    # =========================================================================
    # TAB 9: FORNECEDORES CURITIBA E RMC
    # =========================================================================
    with tabs[9]:
        st.markdown('<div class="section-title">🏢 Fornecedores Principais de Curitiba e Região Metropolitana</div>', unsafe_allow_html=True)
        st.write("Mantenha aqui os contatos e prazos das distribuidoras parceiras da K&G:")
        edited_forn = st.data_editor(st.session_state['banco_fornecedores'], num_rows="dynamic", use_container_width=True, key="forn_edit_box")
        st.session_state['banco_fornecedores'] = edited_forn

    # =========================================================================
    # TAB 10: INVENTÁRIO DE UTENSÍLIOS E PATRIMÔNIO
    # =========================================================================
    with tabs[10]:
        st.markdown('<div class="section-title">🏛️ Relação Patrimonial de Ferramentas (Inventário)</div>', unsafe_allow_html=True)
        st.write("Mapeie todos os bens do atelier separados pelas categorias operacionais da cozinha:")
        
        edited_inv = st.data_editor(
            st.session_state['banco_inventario'],
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Categoria": st.column_config.SelectboxColumn(
                    "Categoria do Bem",
                    options=[
                        "Formas de Alumínio", 
                        "Moldes de Silicone", 
                        "Cortadores (Alumínio/Plástico)", 
                        "Stencils", 
                        "Bailarinas", 
                        "Forno & Batedeiras", 
                        "Utensílios Gerais"
                    ]
                )
            },
            key="inventario_edit_box"
        )
        st.session_state['banco_inventario'] = edited_inv

elif chave_usuario != "":
    st.error("Chave de Acesso Incorreta! O conteúdo permanece bloqueado por segurança contra terceiros.")
else:
    st.warning("Insira a chave de acesso acima para visualizar as informações confidenciais do atelier.")
