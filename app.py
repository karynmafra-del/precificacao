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
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght=300;400;600&display=swap');
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
        
        /* Caixas de Exibição e Alertas */
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; line-height: 1.4; }
        .lupa-box { border: 3px solid black; background: white; color: black; padding: 10px; font-weight: bold; text-align: center; font-size: 14px; margin-bottom: 10px; font-family: Arial, sans-serif; }
        .preco-box { background: #043927; color: #FAF6F0; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #D4AF37; }
        .alerta-aniv { background: #FAF0F2; border-left: 5px solid #D4AF37; padding: 12px; border-radius: 4px; margin-bottom: 15px; }
        
        /* Estilização das Abas em Rosé Nude */
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
        <div class="brand-subtitle">💎 Sistema de Gestão Industrial ERP & CRM de Elite 💎</div>
    </div>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE SEGURANÇA CONTRA ERROS DE DIGITAÇÃO NAS TABELAS ---
def calcular_custo_tabela_seguro(df, col_preco, col_embalagem, col_usado):
    if df is None or df.empty:
        return 0.0
    try:
        df_temp = df.copy()
        # Converte para numérico e substitui erros/vazios por valores seguros
        df_temp[col_preco] = pd.to_numeric(df_temp[col_preco], errors='coerce').fillna(0.0)
        df_temp[col_embalagem] = pd.to_numeric(df_temp[col_embalagem], errors='coerce').fillna(1.0)
        df_temp[col_usado] = pd.to_numeric(df_temp[col_usado], errors='coerce').fillna(0.0)
        
        # Impede divisão por zero
        df_temp[col_embalagem] = df_temp[col_embalagem].replace(0, 1.0)
        
        custos = (df_temp[col_preco] / df_temp[col_embalagem]) * df_temp[col_usado]
        return float(custos.sum())
    except Exception:
        return 0.0

# 🔒 CHAVE DE ACESSO GLOBAL
chave_usuario = st.text_input("Insira a sua Chave de Acesso para liberar o sistema:", type="password")

if chave_usuario == "kg10k":
    st.success("Acesso Homologado! Seja bem-vinda ao seu centro administrativo, Karyn.")

    # Inicialização dos Bancos de Dados de Receita na memória
    if 'massa_ing' not in st.session_state:
        st.session_state['massa_ing'] = pd.DataFrame([
            {"Ingrediente": "Farinha de Trigo Premium", "Preço Embalagem (R$)": 8.50, "Gramos Embalagem (g)": 1000.0, "Gramos Usados na Receita": 300.0},
            {"Ingrediente": "Chocolate em Pó 50%", "Preço Embalagem (R$)": 22.00, "Gramos Embalagem (g)": 500.0, "Gramos Usados na Receita": 100.0},
            {"Ingrediente": "Ovos Frescos", "Preço Embalagem (R$)": 12.00, "Gramos Embalagem (g)": 600.0, "Gramos Usados na Receita": 240.0},
            {"Ingrediente": "Manteiga Extra", "Preço Embalagem (R$)": 14.00, "Gramos Embalagem (g)": 200.0, "Gramos Usados na Receita": 150.0}
        ])
    if 'recheio_ing' not in st.session_state:
        st.session_state['recheio_ing'] = pd.DataFrame([
            {"Ingrediente": "Leite Condensado Itambé", "Preço Embalagem (R$)": 6.80, "Gramos Embalagem (g)": 395.0, "Gramos Usados na Receita": 395.0},
            {"Ingrediente": "Creme de Leite", "Preço Embalagem (R$)": 4.20, "Gramos Embalagem (g)": 200.0, "Gramos Usados na Receita": 200.0},
            {"Ingrediente": "Leite em Pó Ninho", "Preço Embalagem (R$)": 18.50, "Gramos Embalagem (g)": 400.0, "Gramos Usados na Receita": 100.0}
        ])
    if 'calda_ing' not in st.session_state:
        st.session_state['calda_ing'] = pd.DataFrame([
            {"Ingrediente": "Açúcar Refinado", "Preço Embalagem (R$)": 4.50, "Gramos Embalagem (g)": 1000.0, "Gramos Usados na Receita": 200.0},
            {"Ingrediente": "Água Filtrada", "Preço Embalagem (R$)": 0.00, "Gramos Embalagem (g)": 1000.0, "Gramos Usados na Receita": 500.0}
        ])
    if 'cobertura_ing' not in st.session_state:
        st.session_state['cobertura_ing'] = pd.DataFrame([
            {"Ingrediente": "Chocolate Nobre ao Leite", "Preço Embalagem (R$)": 55.00, "Gramos Embalagem (g)": 1000.0, "Gramos Usados na Receita": 500.0},
            {"Ingrediente": "Creme de Leite (Ganache)", "Preço Embalagem (R$)": 4.20, "Gramos Embalagem (g)": 200.0, "Gramos Usados na Receita": 150.0}
        ])

    # Abas Principais Unificadas
    tabs = st.tabs([
        "💰 CENTRAL FINANCEIRA",
        "📝 1. ORÇAMENTOS & FRETE",
        "👥 2. CRM & ALERTAS",
        "🥣 3. FÁBRICA DE BASES",
        "🍫 4. DOCES PERSONALIZADOS",
        "🎂 5. PRODUTOS COMPLETOS",
        "📦 6. EMBALAGENS & IMPRESSÃO",
        "🥦 7. ANVISA & ROTULAGEM",
        "🛒 8. ESTOQUE INTELIGENTE",
        "🏢 9. FORNECEDORES (CWB)",
        "🏛️ 10. INVENTÁRIO PATRIMONIAL"
    ])

    # ==========================================
    # ABA 0: CENTRAL FINANCEIRA & DRE
    # ==========================================
    with tabs[0]:
        st.markdown('<div class="section-title">📊 Saúde Financeira e Demonstrativo de Resultados (DRE)</div>', unsafe_allow_html=True)
        sub_fin1, sub_fin2, sub_fin3, sub_dp_aba = st.tabs(["📈 Dashboard de Resultados", "💸 Lançamentos Diários", "📉 Estrutura DRE", "👥 Departamento Pessoal (DP)"])
        with sub_fin1:
            st.metric("Meta Faturamento Mês", "R$ 10.000,00")
            st.progress(6420 / 10000, text="64.2% da Meta de R$ 10k Atingida")
            
            # Gráfico de Lucro Realizado
            chart_data = pd.DataFrame({
                "Dias": ["Semana 1", "Semana 2", "Semana 3", "Semana 4"],
                "Receitas": [2100, 1800, 2520, 0],
                "Despesas": [1200, 950, 1100, 0]
            })
            st.bar_chart(chart_data, x="Dias", y=["Receitas", "Despesas"])

        with sub_fin2:
            st.data_editor(pd.DataFrame([{"Data": "28/06/2026", "Tipo": "Receita", "Descrição": "Encomenda Casamento", "Valor (R$)": 1450.00}]), num_rows="dynamic", use_container_width=True, key="fluxo_caixa_key")
        with sub_fin3:
            col_dr1, col_dr2 = st.columns(2)
            with col_dr1:
                st.markdown("##### Custos Fixos")
                st.data_editor(pd.DataFrame([{"Descrição": "Aluguel", "Valor (R$)": 1500.00}]), num_rows="dynamic", use_container_width=True, key="c_fixos_key")
            with col_dr2:
                st.markdown("##### Custos Variáveis")
                st.data_editor(pd.DataFrame([{"Descrição": "Matérias-Primas", "Valor (R$)": 1500.00}]), num_rows="dynamic", use_container_width=True, key="c_var_key")
        with sub_dp_aba:
            st.metric("Pró-Labore da Karyn", "R$ 4.000,00")
            st.data_editor(pd.DataFrame([{"Funcionária": "Ana Silva", "Cargo": "Auxiliar", "Salário (R$)": 1650.00, "Ocorrências": "Nenhuma"}], columns=["Funcionária", "Cargo", "Salário (R$)", "Ocorrências"]), num_rows="dynamic", use_container_width=True, key="dp_key")

    # ==========================================
    # ABA 1: ORÇAMENTOS & FRETE LOGÍSTICO
    # ==========================================
    with tabs[1]:
        st.markdown('<div class="section-title">📝 Emissão de Orçamentos e Logística Rígida de Entregas</div>', unsafe_allow_html=True)
        st.link_button("🗺️ Abrir Rota no Google Maps", "https://www.google.com/maps", type="primary")
        
        col_or1, col_or2 = st.columns(2)
        with col_or1:
            c_nome = st.text_input("Nome do Cliente", value="Fernanda Albuquerque")
            c_whats = st.text_input("WhatsApp", value="(41) 99222-3344")
            c_email = st.text_input("E-mail", value="fernanda@gmail.com")
            c_doce = st.text_input("Produto/Doce Solicitado", value="Bolo de Morango Especial 5kg")
            c_valor_produtos = st.number_input("Valor total dos Produtos (R$)", value=650.00)
            c_obs_criticas = st.text_area("Restrições e Alertas do Cliente", value="Não gosta de passas, tem alergia a canela!")
        
        with col_or2:
            c_endereco = st.text_input("Endereço Completo", value="Rua das Palmeiras, 450 - Campo Largo")
            c_referencia = st.text_input("Ponto de Referência", value="Próximo à Igreja Matriz")
            c_horario = st.time_input("Horário Marcado de Entrega", datetime.now().time())
            c_data_festa = st.date_input("Data de Entrega", datetime.now() + timedelta(days=5))
            
            km_total = st.number_input("Distância Total Ida e Volta (KM)", min_value=0.0, value=25.0)
            quem_entrega = st.radio("Entregador", ["Empresária (Karyn)", "Terceirizado"])
            is_rural = st.checkbox("Rota inclui estrada de terra / área rural?", value=True)
            
            custo_km = km_total * 1.80
            taxa_parada = 25.00 if quem_entrega == "Empresária (Karyn)" else 0.00
            taxa_rural = 35.00 if is_rural else 0.00
            valor_frete_final = custo_km + taxa_parada + taxa_rural
            st.metric("Custo Logístico de Entrega", f"R$ {valor_frete_final:.2f}")

        valor_total_pedido = c_valor_produtos + valor_frete_final
        st.markdown(f"### Valor Final da Proposta: **R$ {valor_total_pedido:.2f}**")

        # Geração de Mensagem para WhatsApp
        msg_whatsapp = f"Olá {c_nome}! Segue o espelho do seu orçamento para o dia {c_data_festa.strftime('%d/%m/%Y')} às {c_horario.strftime('%H:%M')}.\n\n* Itens: {c_doce} - R$ {c_valor_produtos:.2f}\n* Entrega ({c_endereco}): R$ {valor_frete_final:.2f}\n\n*Total:* R$ {valor_total_pedido:.2f}\n\n*Restrições de Cozinha:* {c_obs_criticas}"
        
        if st.button("🖨️ Gerar Espelho de Pedido e Orçamento"):
            st.markdown(f"""
                <div class="print-box">
                    <b>💎 PROPOSTA COMERCIAL EXCLUSIVA - K&G ARTE EM CONFEITARIA 💎</b><br>
                    <b>Código do Pedido:</b> KG-2026-{random.randint(1000, 9999)}<br>
                    -------------------------------------------------------------------------<br>
                    <b>DADOS DO CLIENTE:</b> {c_nome} | WhatsApp: {c_whats} | E-mail: {c_email}<br>
                    <b>ENTREGA:</b> {c_data_festa.strftime('%d/%m/%Y')} às {c_horario.strftime('%H:%M')}<br>
                    <b>ENDEREÇO:</b> {c_endereco} (Ref: {c_referencia})<br>
                    -------------------------------------------------------------------------<br>
                    <b>⚠️ OBSERVAÇÕES CRÍTICAS DE COZINHA:</b> {c_obs_criticas.upper()}<br>
                    -------------------------------------------------------------------------<br>
                    <b>INVESTIMENTO TOTAL: R$ {valor_total_pedido:.2f}</b> (Produtos: R$ {c_valor_produtos:.2f} + Frete: R$ {valor_frete_final:.2f})
                </div>
            """, unsafe_allow_html=True)
            st.text_area("Copiar mensagem pronta para envio:", value=msg_whatsapp, height=150)

    # ==========================================
    # ABA 2: CRM & HISTÓRICO DE PEDIDOS
    # ==========================================
    with tabs[2]:
        st.markdown('<div class="section-title">👥 CRM: Central de Relacionamento e Busca Ativa de Clientes VIP</div>', unsafe_allow_html=True)
        mes_atual = datetime.now().strftime("%m")
        st.markdown(f"<div class='alerta-aniv'>🎉 <b>ALERTA DE MARKETING K&G:</b> Juliana Mendes faz aniversário este mês (12/{mes_atual})! Mande uma mensagem especial.</div>", unsafe_allow_html=True)
        
        df_crm = pd.DataFrame([
            {"Cliente": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "Aniv. Cliente": f"12/{mes_atual}", "Whats Marido": "(41) 99321-7654", "Aniv. Marido": "18/10", "Aniv. Filhos": "Gabriel (04/02)", "Data Casamento": "22/11", "Restrições": "NÃO PODE CONTER AMENDOIM!", "Último Pedido": "KG-2026-1042"},
            {"Cliente": "Carlos Henrique Rocha", "WhatsApp": "(41) 98877-6655", "Aniv. Cliente": "29/08", "Whats Marido": "-", "Aniv. Marido": "-", "Aniv. Filhos": "Sofia (15/05)", "Data Casamento": "-", "Restrições": "Não gosta de suspiro de jeito nenhum.", "Último Pedido": "KG-2026-8841"}
        ])
        
        # Filtro de Busca Ativa
        busca = st.text_input("🔍 Busca Ativa por Nome, Telefone ou Restrições Críticas:")
        if busca:
            df_filtrado = df_crm[df_crm.apply(lambda r: r.astype(str).str.contains(busca, case=False).any(), axis=1)]
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.dataframe(df_crm, use_container_width=True)

    # ==========================================
    # ABA 3: FÁBRICA DE BASES (ITEM A ITEM À PROVA DE FALHAS)
    # ==========================================
    with tabs[3]:
        st.markdown('<div class="section-title">🥣 Fábrica de Bases: Fichas Técnicas de Massas, Recheios e Caldas</div>', unsafe_allow_html=True)
        sub_b1, sub_b2, sub_b3, sub_b4 = st.tabs(["🍞 Massa de Bolo", "🍓 Recheios Estruturados", "💧 Caldas para Regar", "✨ Coberturas e Blindagens"])
        
        with sub_b1:
            st.markdown("##### 📝 Ficha Técnica - Massa de Bolo")
            peso_obtido_massa = st.number_input("Peso Final Obtido na Receita de Massa (g)", value=1000.0, key="p_massa")
            massa_edit = st.data_editor(st.session_state['massa_ing'], num_rows="dynamic", use_container_width=True, key="m_ing_key")
            st.session_state['massa_ing'] = massa_edit
            
            # Cálculo seguro
            custo_massa_total = calcular_custo_tabela_seguro(massa_edit, "Preço Embalagem (R$)", "Gromos Embalagem (g)", "Gramos Usados na Receita")
            if peso_obtido_massa > 0:
                custo_massa_kg = (custo_massa_total / peso_obtido_massa) * 1000
            else:
                custo_massa_kg = 0.0
            st.metric("Custo Total da Massa Elaborada", f"R$ {custo_massa_total:.2f}")
            st.metric("Custo Proporcional por Kilograma (kg)", f"R$ {custo_massa_kg:.2f}")
            
        with sub_b2:
            st.markdown("##### 📝 Ficha Técnica - Recheios")
            peso_obtido_recheio = st.number_input("Peso Final Obtido na Receita de Recheio (g)", value=800.0, key="p_recheio")
            recheio_edit = st.data_editor(st.session_state['recheio_ing'], num_rows="dynamic", use_container_width=True, key="r_ing_key")
            st.session_state['recheio_ing'] = recheio_edit
            
            custo_recheio_total = calcular_custo_tabela_seguro(recheio_edit, "Preço Embalagem (R$)", "Gramos Embalagem (g)", "Gramos Usados na Receita")
            if peso_obtido_recheio > 0:
                custo_recheio_kg = (custo_recheio_total / peso_obtido_recheio) * 1000
            else:
                custo_recheio_kg = 0.0
            st.metric("Custo Total do Recheio", f"R$ {custo_recheio_total:.2f}")
            st.metric("Custo Proporcional por Kilograma (kg)", f"R$ {custo_recheio_kg:.2f}")

        with sub_b3:
            st.markdown("##### 📝 Ficha Técnica - Calda")
            peso_obtido_calda = st.number_input("Peso Final Obtido na Receita de Calda (g)", value=500.0, key="p_calda")
            calda_edit = st.data_editor(st.session_state['calda_ing'], num_rows="dynamic", use_container_width=True, key="c_ing_key")
            st.session_state['calda_ing'] = calda_edit
            
            custo_calda_total = calcular_custo_tabela_seguro(calda_edit, "Preço Embalagem (R$)", "Gramos Embalagem (g)", "Gramos Usados na Receita")
            if peso_obtido_calda > 0:
                custo_calda_kg = (custo_calda_total / peso_obtido_calda) * 1000
            else:
                custo_calda_kg = 0.0
            st.metric("Custo Total da Calda", f"R$ {custo_calda_total:.2f}")
            st.metric("Custo Proporcional por Kilograma (kg)", f"R$ {custo_calda_kg:.2f}")

        with sub_b4:
            st.markdown("##### 📝 Ficha Técnica - Coberturas e Blindagens")
            peso_obtido_cob = st.number_input("Peso Final Obtido na Receita (g)", value=1000.0, key="p_cob")
            cobertura_edit = st.data_editor(st.session_state['cobertura_ing'], num_rows="dynamic", use_container_width=True, key="cob_ing_key")
            st.session_state['cobertura_ing'] = cobertura_edit
            
            custo_cob_total = calcular_custo_tabela_seguro(cobertura_edit, "Preço Embalagem (R$)", "Gramos Embalagem (g)", "Gramos Usados na Receita")
            if peso_obtido_cob > 0:
                custo_cob_kg = (custo_cob_total / peso_obtido_cob) * 1000
            else:
                custo_cob_kg = 0.0
            st.metric("Custo Total da Cobertura", f"R$ {custo_cob_total:.2f}")
            st.metric("Custo Proporcional por Kilograma (kg)", f"R$ {custo_cob_kg:.2f}")

    # ==========================================
    # ABA 4: DOCES PERSONALIZADOS
    # ==========================================
    with tabs[4]:
        st.markdown('<div class="section-title">🍫 Doces Personalizados e Formas Especiais</div>', unsafe_allow_html=True)
        col_doc1, col_doc2 = st.columns(2)
        with col_doc1:
            nome_projeto_doce = st.text_input("Nome/Tema do Doce Personalizado", value="Personagens 3D Safari")
            forma_bwb_id = st.text_input("Forma BWB Utilizada (Número/Modelo)", value="BWB 41")
            peso_choco_forma = st.number_input("Chocolate por Unidade (g)", value=35.0)
        with col_doc2:
            pasta_tipo = st.selectbox("Pasta Utilizada", ["Pasta de Leite Ninho", "Pasta Americana", "Pasta de Chocolate"])
            peso_pasta_bwb = st.number_input("Peso da Pasta na Modelagem (g)", value=20.0)

    # ==========================================
    # ABA 5: PRODUTOS COMPLETOS & CÁLCULO DE PROPORÇÃO
    # ==========================================
    with tabs[5]:
        st.markdown('<div class="section-title">📐 Engenharia de Estrutura de Bolos & Precificação de Venda</div>', unsafe_allow_html=True)
        col_pd1, col_pd2 = st.columns(2)
        with col_pd1:
            nome_bolo_final = st.text_input("Bolo Completo", value="Bolo de Morango com Suspiros e Chantiganache")
            peso_alvo = st.number_input("Peso Alvo Solicitado pelo Cliente (kg)", min_value=1.0, value=5.0)
            tipo_forma_final = st.selectbox("Geometria da Forma", ["Redonda", "Retangular"])
            margem_comercial = st.slider("Selecione a Margem Comercial de Segurança (%)", min_value=40, max_value=50, value=45)
            
        with col_prop2:
            # Lógica de pesos proporcionais da confeitaria estruturada
            peso_alvo_g = peso_alvo * 1000
            calc_massa_final = peso_alvo_g * 0.35
            calc_recheio_final = peso_alvo_g * 0.40
            calc_calda_final = peso_alvo_g * 0.10
            calc_cobertura_final = peso_alvo_g * 0.15
            
            # Cálculo de Forma sugerida
            if tipo_forma_final == "Redonda":
                diametro_sugerido = math.ceil(2 * math.sqrt(peso_alvo_g / (3.14 * 10 * 0.6)))
                st.metric("Forma Redonda Recomendada", f"{diametro_sugerido} cm de diâmetro (Altura de 10cm)")
            else:
                st.metric("Forma Retangular Recomendada", "35x25 cm")

        # CUSTO REAL DINÂMICO INTERLIGADO COM A ABA 3
        custo_massa_composto = (custo_massa_kg / 1000) * calc_massa_final
        custo_recheio_composto = (custo_recheio_kg / 1000) * calc_recheio_final
        custo_calda_composto = (custo_calda_kg / 1000) * calc_calda_final
        custo_cob_composto = (custo_cob_kg / 1000) * calc_cobertura_final
        custo_insumos_total = custo_massa_composto + custo_recheio_composto + custo_calda_composto + custo_cob_composto + 12.00 # Caixa/Embalagem inclusa
        
        st.markdown("##### 📝 Balanço e Distribuição para Produção de Cozinha:")
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        with c_p1: st.metric("Massa Base", f"{int(calc_massa_final)} g", f"Custo: R$ {custo_massa_composto:.2f}")
        with c_p2: st.metric("Recheio + Frutas", f"{int(calc_recheio_final)} g", f"Custo: R$ {custo_recheio_composto:.2f}")
        with c_p3: st.metric("Calda de Regar", f"{int(calc_calda_final)} g", f"Custo: R$ {custo_calda_composto:.2f}")
        with c_p4: st.metric("Blindagem / Cobertura", f"{int(calc_cobertura_final)} g", f"Custo: R$ {custo_cob_composto:.2f}")

        # PRECIFICAÇÃO DETALHADA COM TAXAS DE CARTÃO E IFOOD
        st.markdown("### 💰 Estrutura de Preço de Venda Comercial")
        divisor_margem = (100 - margem_comercial) / 100
        preco_venda_base = custo_insumos_total / divisor_margem
        
        # Taxas de cartões
        v_debito = preco_venda_base / (1 - 0.0199) # Taxa simulação de débito 1.99%
        v_credito = preco_venda_base / (1 - 0.0499) # Taxa simulação de crédito 4.99%
        v_ifood = preco_venda_base / 0.73 # iFood taxa média de 27% para reter margem cheia

        cv1, cv2, cv3, cv4 = st.columns(4)
        with cv1: st.markdown(f"<div class='preco-box'><b>🛍️ DINHEIRO/PIX</b><br><span style='font-size:20px; font-weight:bold;'>R$ {preco_venda_base:.2f}</span><br>Lucro Protegido</div>", unsafe_allow_html=True)
        with cv2: st.markdown(f"<div class='preco-box' style='background:#0B533A;'><b>💳 DÉBITO MAQ.</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_debito:.2f}</span><br>Taxa 1.99% Reassumida</div>", unsafe_allow_html=True)
        with cv3: st.markdown(f"<div class='preco-box' style='background:#0B533A;'><b>💳 CRÉDITO MAQ.</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_credito:.2f}</span><br>Taxa 4.99% Reassumida</div>", unsafe_allow_html=True)
        with cv4: st.markdown(f"<div class='preco-box' style='background:#901414;'><b>🛵 CARDÁPIO IFOOD</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_ifood:.2f}</span><br>Taxa da Plataforma Coberta</div>", unsafe_allow_html=True)

        foto_bolo = st.file_uploader("📸 Enviar Foto do Produto Finalizado", type=["jpg", "png", "jpeg"])

    # ==========================================
    # ABA 6: EMBALAGENS & IMPRESSÃO
    # ==========================================
    with tabs[6]:
        st.markdown('<div class="section-title">📦 Gestão de Embalagens, Laços, Fitas e Envio para Portátil</div>', unsafe_allow_html=True)
        df_emb = st.data_editor(pd.DataFrame([
            {"Embalagem": "Caixa Branca com Visor", "Preço Embalagem (R$)": 12.00, "Unidades no Cento/Pacote": 1, "Usada no Produto": 1},
            {"Embalagem": "Fita Cetim Ouro (metros)", "Preço Embalagem (R$)": 15.00, "Unidades no Cento/Pacote": 10, "Usada no Produto": 1}
        ]), num_rows="dynamic", use_container_width=True, key="emb_key")
        
        texto_impressora = st.text_area("Texto para sair na Impressora Portátil Bluetooth:", f"K&G Arte em Confeitaria\n{nome_bolo_final}\nConsuma com Prazer!")

    # ==========================================
    # ABA 7: ANVISA & ROTULAGEM NUTRICIONAL (RDC 429)
    # ==========================================
    with tabs[7]:
        st.markdown('<div class="section-title">🥦 Rotulagem Frontal e Lupa Legal de Advertência da ANVISA</div>', unsafe_allow_html=True)
        
        lupa_acucar = st.checkbox("Este bolo ultrapassa 15g de Açúcares por 100g de produto?", value=True)
        lupa_gordura = st.checkbox("Este bolo ultrapassa 6g de Gorduras por 100g de produto?", value=False)
        
        if lupa_acucar or lupa_gordura:
            texto_lupa = "<div class='lupa-box'>🔍 <b>ROTULAGEM FRONTAL OBRIGATÓRIA (RDC 429):</b><br>"
            if lupa_acucar: texto_lupa += "⚠️ ALTO EM AÇÚCAR ADICIONADO<br>"
            if lupa_gordura: texto_lupa += "⚠️ ALTO EM GORDURA SATURADA<br>"
            texto_lupa += "</div>"
            st.markdown(texto_lupa, unsafe_allow_html=True)
            
        st.markdown("""
            <table style="border: 2px solid black; width:100%; border-collapse: collapse; background: white; color: black; font-size:12px;">
                <tr><th colspan="3" style="text-align:center; padding: 5px; font-size:14px; border-bottom: 2px solid black;">INFORMAÇÃO NUTRICIONAL</th></tr>
                <tr><td colspan="3" style="padding:5px;">Porção de 100g | Peso Final: """+str(peso_alvo)+"""kg</td></tr>
                <tr style="font-weight:bold; border-bottom: 1px solid black;">
                    <td style="padding:5px;">Componente</td><td style="padding:5px;">Quantidade por 100g</td><td style="padding:5px;">%VD*</td>
                </tr>
                <tr><td style="padding:5px;">Valor Energético</td><td style="padding:5px;">295 kcal</td><td style="padding:5px;">15%</td></tr>
                <tr><td style="padding:5px;">Açúcares Adicionados</td><td style="padding:5px;">"""+("16,2g" if lupa_acucar else "8,5g")+"""</td><td style="padding:5px;">"""+("32%" if lupa_acucar else "17%")+"""</td></tr>
                <tr><td style="padding:5px;">Gorduras Saturadas</td><td style="padding:5px;">"""+("6,4g" if lupa_gordura else "3,2g")+"""</td><td style="padding:5px;">"""+("29%" if lupa_gordura else "15%")+"""</td></tr>
            </table>
        """, unsafe_allow_html=True)
        
        st.image("https://barcode.tec-it.com/barcode.ashx?data=789643120054&code=EAN13", caption="Código de Barras EAN-13 Homologado pela ANVISA")

    # ==========================================
    # ABA 8: ESTOQUE CRÍTICO INTELIGENTE
    # ==========================================
    with tabs[8]:
        st.markdown('<div class="section-title">🛒 Estoque Crítico de Matérias-Primas e Alertas</div>', unsafe_allow_html=True)
        
        estoque_base = pd.DataFrame([
            {"Item de Estoque": "Leite Condensado Itambé", "Quantidade em Estoque (Un)": 5, "Estoque Mínimo de Segurança (Un)": 24},
            {"Item de Estoque": "Creme de Leite", "Quantidade em Estoque (Un)": 15, "Estoque Mínimo de Segurança (Un)": 24},
            {"Item de Estoque": "Chocolate Nobre ao Leite", "Quantidade em Estoque (Un)": 12, "Estoque Mínimo de Segurança (Un)": 5}
        ])
        
        df_est_edit = st.data_editor(estoque_base, num_rows="dynamic", use_container_width=True, key="estoque_crit_key")
        
        # Lógica de Alertas de Falta
        st.markdown("##### 🚨 Alerta Vermelho de Compras:")
        for idx, row in df_est_edit.iterrows():
            try:
                atual = float(row["Quantidade em Estoque (Un)"])
                minimo = float(row["Estoque Mínimo de Segurança (Un)"])
                if atual < minimo:
                    st.error(f"⚠️ {row['Item de Estoque']} está abaixo do estoque de segurança! Adquirir mais {int(minimo - atual)} unidades.")
            except Exception:
                pass

    # ==========================================
    # ABA 9: FORNECEDORES HOMOLOGADOS DE CURITIBA
    # ==========================================
    with tabs[9]:
        st.markdown('<div class="section-title">🏢 Fornecedores e Distribuidores de Curitiba e Região Metropolitana</div>', unsafe_allow_html=True)
        
        fornecedores_cwb = pd.DataFrame([
            {"Fornecedor": "Central do Chocolate CWB", "Telefone": "(41) 3222-1200", "Localização": "Centro, Curitiba - PR", "Insumos": "Chocolate Nobre Callebaut, Sicao"},
            {"Fornecedor": "Nova Íris Embalagens", "Telefone": "(41) 3324-4500", "Localização": "Centro, Curitiba - PR", "Insumos": "Caixas de Papelão e Visores"},
            {"Fornecedor": "BWB Embalagens", "Telefone": "(19) 3812-9900", "Localização": "Distribuição Geral CWB", "Insumos": "Formas de Acetato e Placas"},
            {"Fornecedor": "Plassete Distribuidora", "Telefone": "(41) 3642-1800", "Localização": "Campo Largo - PR", "Insumos": "Bases de Isopor, descartáveis, sacolas"},
            {"Fornecedor": "Parma Alimentos", "Telefone": "(41) 3245-7700", "Localização": "Curitiba - PR", "Insumos": "Leite Condensado e Creme de Leite Atacado"},
            {"Fornecedor": "Mundo do Confeiteiro", "Telefone": "(41) 3012-3400", "Localização": "Água Verde, Curitiba - PR", "Insumos": "Utensílios e corantes finos"},
            {"Fornecedor": "Casa do Confeiteiro", "Telefone": "(41) 3333-8888", "Localização": "Pinheirinho, Curitiba - PR", "Insumos": "Açúcares especiais, suspiros, granulados"},
            {"Fornecedor": "Distribuidora de Frutas Curitiba", "Telefone": "(41) 99999-5555", "Localização": "CEASA Curitiba", "Insumos": "Morangos in natura e frutas vermelhas"},
            {"Fornecedor": "Embalagens Centro", "Telefone": "(41) 3223-1111", "Localização": "Centro, Curitiba - PR", "Insumos": "Laços, tags, fitas de cetim"},
            {"Fornecedor": "Atacado Doce CWB", "Telefone": "(41) 3555-4444", "Localização": "Pinhais - PR", "Insumos": "Insumos secos em grande quantidade"}
        ])
        
        st.data_editor(fornecedores_cwb, num_rows="dynamic", use_container_width=True, key="forn_key")

    # ==========================================
    # ABA 10: INVENTÁRIO PATRIMONIAL DE UTENSÍLIOS
    # ==========================================
    with tabs[10]:
        st.markdown('<div class="section-title">🏛️ Inventário Patrimonial do Atelier K&G</div>', unsafe_allow_html=True)
        st.write("Mantenha a relação de todos os bens físicos do seu atelier para controle patrimonial:")
        
        inventario_base = pd.DataFrame([
            {"Categoria": "Moldes de Silicone", "Equipamento/Utensílio": "Molde Rosas Luxo Grande", "Quantidade": 4, "Valor Unitário (R$)": 45.00},
            {"Categoria": "Forno & Batedeiras", "Equipamento/Utensílio": "Batedeira Planetária Arno", "Quantidade": 1, "Valor Unitário (R$)": 650.00},
            {"Categoria": "Bailarinas", "Equipamento/Utensílio": "Bailarina Profissional com Rolamento", "Quantidade": 2, "Valor Unitário (R$)": 180.00},
            {"Categoria": "Formas de Alumínio", "Equipamento/Utensílio": "Forma Redonda 20cm", "Quantidade": 10, "Valor Unitário (R$)": 22.00}
        ])
        
        df_inv_edit = st.data_editor(inventario_base, num_rows="dynamic", use_container_width=True, key="inv_pat_key")
        
        # Cálculo de patrimônio
        custo_unit = pd.to_numeric(df_inv_edit["Valor Unitário (R$)"], errors='coerce').fillna(0.0)
        quantidades = pd.to_numeric(df_inv_edit["Quantidade"], errors='coerce').fillna(0.0)
        patrimonio_total = (custo_unit * quantidades).sum()
        
        st.metric("Patrimônio Físico Total Acumulado no Atelier", f"R$ {patrimonio_total:.2f}")
        st.file_uploader("📸 Registrar foto de patrimônio (moldes, cortadores, stencils)", type=["png","jpg"])

elif chave_usuario != "":
    st.error("Chave de Acesso Incorreta! Por favor, digite a senha autorizada da K&G.")
else:
    st.warning("Insira a chave de acesso empresarial para visualizar o ecossistema estratégico.")
