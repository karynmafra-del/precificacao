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

# Inicialização de variáveis globais compartilhadas (Evita qualquer erro de variável indefinida)
custo_massa_kg = 0.0
custo_recheio_kg = 0.0
custo_calda_kg = 0.0
custo_cob_kg = 0.0
peso_alvo = 5.0
nome_bolo_final = "Bolo de Morango Especial"

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
        
        /* Customização das Abas em Rosé Nude */
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
        <div class="brand-subtitle">💎 Sistema ERP & CRM Integrado de Alta Confeitaria 💎</div>
    </div>
""", unsafe_allow_html=True)

# --- FUNÇÃO EXECUTIVA DE LIMPEZA E TRATAMENTO DE VÍRGULAS EM NÚMEROS ---
def limpar_e_converter_coluna(df, coluna, padrao=0.0):
    if df is None or df.empty or coluna not in df.columns:
        return pd.Series([padrao] * (len(df) if df is not None else 1))
    try:
        # Força a conversão para texto, substitui vírgula por ponto e remove espaços
        serie_str = df[coluna].astype(str).str.replace(',', '.', regex=False).str.strip()
        # Retorna convertido em float numérico seguro
        return pd.to_numeric(serie_str, errors='coerce').fillna(padrao)
    except Exception:
        return pd.Series([padrao] * len(df))

# --- CALCULO MATEMÁTICO INTEGRADO DE FICHAS TÉCNICAS (BLINDADO CONTRA LINHAS EM BRANCO) ---
def calcular_custo_tabela_seguro(df, col_preco, col_embalagem, col_usado):
    if df is None or df.empty:
        return 0.0
    try:
        df_temp = df.copy()
        
        # Super Filtro de Segurança: Remove qualquer linha que tenha sido criada vazia ou com None
        if "Ingrediente" in df_temp.columns:
            df_temp = df_temp.dropna(subset=["Ingrediente"])
            df_temp = df_temp[df_temp["Ingrediente"].astype(str).str.strip() != "None"]
            df_temp = df_temp[df_temp["Ingrediente"].astype(str).str.strip() != ""]
            
        if df_temp.empty:
            return 0.0
            
        precos = limpar_e_converter_coluna(df_temp, col_preco, 0.0)
        embalagens = limpar_e_converter_coluna(df_temp, col_embalagem, 1.0)
        usados = limpar_e_converter_coluna(df_temp, col_usado, 0.0)
        
        # Evita qualquer divisão por zero
        embalagens = embalagens.replace(0, 1.0)
        
        custos = (precos / embalagens) * usados
        return float(custos.sum())
    except Exception:
        return 0.0

def get_recipe_cost_kg(banco, name):
    if not name or name not in banco:
        return 0.0
    try:
        recipe = banco[name]
        df = recipe["ingredientes"]
        peso_obtido = recipe.get("peso_obtido", 1000.0)
        if peso_obtido <= 0:
            peso_obtido = 1.0
        custo_total = calcular_custo_tabela_seguro(df, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
        return (custo_total / peso_obtido) * 1000.0
    except Exception:
        return 0.0

# --- FUNÇÃO AUXILIAR PARA ADICIONAR INGREDIENTE SEM COMPLICAÇÃO ---
def adicionar_ingrediente_banco(banco_key, receita_nome, ingrediente, unidade, preco, qtd_emb, qtd_usada):
    try:
        preco_val = float(str(preco).replace(',', '.').strip()) if preco else 0.0
    except:
        preco_val = 0.0
    try:
        qtd_emb_val = float(str(qtd_emb).replace(',', '.').strip()) if qtd_emb else 1.0
    except:
        qtd_emb_val = 1.0
    try:
        qtd_usada_val = float(str(qtd_usada).replace(',', '.').strip()) if qtd_usada else 0.0
    except:
        qtd_usada_val = 0.0
        
    new_row = {
        "Ingrediente": ingrediente,
        "Qtd Usada": qtd_usada_val,
        "Unidade": unidade,
        "Qtd na Embalagem": qtd_emb_val,
        "Preço Embalagem (R$)": preco_val
    }
    
    df = st.session_state[banco_key][receita_nome]["ingredientes"]
    st.session_state[banco_key][receita_nome]["ingredientes"] = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# 🔒 CHAVE DE ACESSO GLOBAL DO SISTEMA
chave_usuario = st.text_input("Insira a sua Chave de Acesso para liberar o sistema:", type="password")

if chave_usuario == "kg10k":
    st.success("Acesso Autorizado! Seja bem-vinda ao seu sistema, Karyn.")

    # Inicialização dos Bancos de Dados na memória para persistência entre as abas (Sem "Manteiga Extra" na massa padrão!)
    if 'banco_massas_rec' not in st.session_state:
        st.session_state['banco_massas_rec'] = {
            "Massa Choc Premium": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Farinha de Trigo Premium", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 25.00},
                    {"Ingrediente": "Chocolate em Pó 50%", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 70.00},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 4.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 25.00},
                    {"Ingrediente": "Creme de leite", "Qtd Usada": 200.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.50}
                ], columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                "peso_obtido": 1000.0,
                "preparo": "Bater claras em neve, juntar secos aos poucos na velocidade baixa da planetária.",
                "decoracao": "Dourado uniforme com aroma intenso de cacau nobre."
            },
            "Pão de Ló de Baunilha": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Farinha de Trigo Premium", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Açúcar Refinado", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 4.50},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 5.0, "Unidade": "un", "Qtd na Embalagem": 12.0, "Preço Embalagem (R$)": 12.00}
                ], columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                "peso_obtido": 1000.0,
                "preparo": "Emulsionar ovos e açúcar, peneirar farinha levemente e assar a 180°C.",
                "decoracao": "Espessura simétrica, ideal para camadas com frutas frescas."
            }
        }

    if 'banco_recheios_rec' not in st.session_state:
        st.session_state['banco_recheios_rec'] = {
            "Brigadeiro de Ninho": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Leite Condensado Itambé", "Qtd Usada": 1.0, "Unidade": "un", "Qtd na Embalagem": 1.0, "Preço Embalagem (R$)": 6.80},
                    {"Ingrediente": "Creme de Leite", "Qtd Usada": 1.0, "Unidade": "un", "Qtd na Embalagem": 1.0, "Preço Embalagem (R$)": 4.20},
                    {"Ingrediente": "Leite Ninho", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 400.0, "Preço Embalagem (R$)": 18.50}
                ], columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                "peso_obtido": 695.0,
                "preparo": "Levar ao fogo mexendo sem parar até atingir ponto de bloco firme para estruturação de bolos.",
                "decoracao": "Cor marfim lisa, sem grumos e textura ultra aveludada."
            }
        }

    if 'banco_caldas_rec' not in st.session_state:
        st.session_state['banco_caldas_rec'] = {
            "Calda Básica de Açúcar": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Açúcar Refinado", "Qtd Usada": 150.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 4.50},
                    {"Ingrediente": "Água Filtrada", "Qtd Usada": 500.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.0}
                ], columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                "peso_obtido": 650.0,
                "preparo": "Ferver água e açúcar até reduzir ligeiramente e homogeneizar. Deixar esfriar.",
                "decoracao": "Fluidez perfeita para absorção uniforme na massa."
            }
        }

    if 'banco_coberturas_rec' not in st.session_state:
        st.session_state['banco_coberturas_rec'] = {
            "Chantiganache ao Leite": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Chocolate Nobre ao Leite", "Qtd Usada": 500.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 55.00},
                    {"Ingrediente": "Creme de Leite", "Qtd Usada": 200.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 4.20}
                ], columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                "peso_obtido": 700.0,
                "preparo": "Derreter o chocolate nobre e emulsionar com creme de leite. Bater levemente para obter textura fosca.",
                "decoracao": "Firmeza total para blindagem de quinas perfeitas."
            }
        }

    # Inicialização do CRM, DRE e outros dados do ERP
    if 'banco_crm' not in st.session_state:
        st.session_state['banco_crm'] = pd.DataFrame([
            {"Cliente VIP": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "E-mail": "juliana@rossi.com", "Aniv. Cliente": "12/06", "Aniv. Marido": "18/10", "Aniv. Filhos": "Gabriel (04/02)", "Data Casamento": "22/11", "Restrições": "NÃO PODE CONTER AMENDOIM!", "Últimos Pedidos": "KG-2026-1042"},
            {"Cliente VIP": "Carlos Henrique Rocha", "WhatsApp": "(41) 98877-6655", "E-mail": "carlos@rocha.com", "Aniv. Cliente": "29/08", "Aniv. Marido": "-", "Aniv. Filhos": "Sofia (15/05)", "Data Casamento": "-", "Restrições": "Não gosta de suspiro de jeito nenhum.", "Últimos Pedidos": "KG-2026-8841"}
        ])

    if 'df_fixos' not in st.session_state:
        st.session_state['df_fixos'] = pd.DataFrame([
            {"Descrição do Custo Fixo": "Aluguel / Atelier", "Valor Mensal (R$)": 1500.00},
            {"Descrição do Custo Fixo": "Água e Energia Elétrica", "Valor Mensal (R$)": 650.00},
            {"Descrição do Custo Fixo": "Imposto MEI / DAS Nacional", "Valor Mensal (R$)": 75.00},
            {"Descrição do Custo Fixo": "Internet e Plataformas", "Valor Mensal (R$)": 150.00}
        ])

    if 'df_var' not in st.session_state:
        st.session_state['df_var'] = pd.DataFrame([
            {"Descrição do Custo Variável": "Matérias-Primas e Embalagens", "Valor Estimado (R$)": 1500.00},
            {"Descrição do Custo Variável": "Gás de Cozinha Recarga", "Valor Estimado (R$)": 135.00},
            {"Descrição do Custo Variável": "Taxas de Entrega / Apps", "Valor Estimado (R$)": 220.00}
        ])

    # Criação das Abas Principais
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
            
            chart_data = pd.DataFrame({
                "Período": ["Semana 1", "Semana 2", "Semana 3", "Semana 4"],
                "Receitas": [2100, 1800, 2520, 0],
                "Despesas": [1200, 950, 1100, 0]
            })
            st.bar_chart(chart_data, x="Período", y=["Receitas", "Despesas"])

        with sub_fin2:
            st.data_editor(pd.DataFrame([{"Data": "28/06/2026", "Tipo": "Receita", "Descrição": "Encomenda Casamento", "Valor (R$)": 1450.00}]), num_rows="dynamic", use_container_width=True, key="fluxo_caixa_key")
        with sub_fin3:
            col_dr1, col_dr2 = st.columns(2)
            with col_dr1:
                st.markdown("##### Custos Fixos")
                df_fixos_ed = st.data_editor(st.session_state['df_fixos'], num_rows="dynamic", use_container_width=True, key="c_fixos_key")
                st.session_state['df_fixos'] = df_fixos_ed
                total_fixos = limpar_e_converter_coluna(df_fixos_ed, "Valor Mensal (R$)", 0.0).sum()
                st.metric("Total de Custos Fixos", f"R$ {total_fixos:.2f}")
            with col_dr2:
                st.markdown("##### Custos Variáveis")
                df_var_ed = st.data_editor(st.session_state['df_var'], num_rows="dynamic", use_container_width=True, key="c_var_key")
                st.session_state['df_var'] = df_var_ed
                total_var = limpar_e_converter_coluna(df_var_ed, "Valor Estimado (R$)", 0.0).sum()
                st.metric("Total de Custos Variáveis", f"R$ {total_var:.2f}")
        with sub_dp_aba:
            st.metric("Pró-Labore da Karyn", "R$ 4.000,00")
            st.data_editor(pd.DataFrame([{"Funcionária": "Ana Silva", "Cargo": "Auxiliar", "Salário (R$)": 1650.00, "Ocorrências": "Nenhuma"}], columns=["Funcionária", "Cargo", "Salário (R$)", "Ocorrências"]), num_rows="dynamic", use_container_width=True, key="dp_key")

    # ==========================================
    # ABA 1: ORÇAMENTOS, FRETE LOGÍSTICO & CRM
    # ==========================================
    with tabs[1]:
        st.markdown('<div class="section-title">📝 Emissão de Orçamentos e Logística Rígida de Entregas</div>', unsafe_allow_html=True)
        st.link_button("🗺️ Abrir Rota no Google Maps para traçar KM", "https://www.google.com/maps", type="primary")
        
        col_or1, col_or2 = st.columns(2)
        with col_or1:
            c_nome = st.text_input("Nome do Cliente", value="Fernanda Albuquerque")
            c_whats = st.text_input("WhatsApp", value="(41) 99222-3344")
            c_email = st.text_input("E-mail", value="fernanda@gmail.com")
            c_doce = st.text_input("Produto/Doce Solicitado", value="Bolo de Morango Especial 5kg")
            c_valor_produtos = st.number_input("Valor total dos Produtos (R$)", value=650.00)
            c_obs_criticas = st.text_area("Restrições, Alergias e Alertas do Cliente", value="Não gosta de passas, tem alergia a canela!")
        
        with col_or2:
            c_endereco = st.text_input("Endereço Completo de Entrega", value="Rua das Palmeiras, 450 - Campo Largo")
            c_referencia = st.text_input("Ponto de Referência para Entrega", value="Próximo à Igreja Matriz")
            c_horario = st.time_input("Horário Marcado de Entrega", datetime.now().time())
            c_data_festa = st.date_input("Data de Entrega", datetime.now() + timedelta(days=5))
            
            km_total = st.number_input("Distância Total Ida e Volta (KM)", min_value=0.0, value=25.0)
            quem_entrega = st.radio("Entregador responsável", ["A própria empresária (Para a produção)", "Terceirizado (Motoboy/Uber)"])
            is_rural = st.checkbox("Rota inclui estrada de terra / área rural? (Adiciona taxa de risco e desgaste do carro)", value=True)
            
            custo_km = km_total * 1.80
            taxa_parada = 25.00 if quem_entrega == "A própria empresária (Para a produção)" else 0.00
            taxa_rural = 35.00 if is_rural else 0.00
            valor_frete_final = custo_km + taxa_parada + taxa_rural
            st.metric("Custo Logístico de Entrega", f"R$ {valor_frete_final:.2f}")

        valor_total_pedido = c_valor_produtos + valor_frete_final
        st.markdown(f"### Valor Final da Proposta: **R$ {valor_total_pedido:.2f}**")

        if 'id_pedido_atual' not in st.session_state:
            st.session_state['id_pedido_atual'] = f"KG-2026-{random.randint(1000, 9999)}"

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("📥 Fechar Pedido e Enviar para o CRM"):
                novo_vip = {
                    "Cliente VIP": c_nome,
                    "WhatsApp": c_whats,
                    "E-mail": c_email,
                    "Aniv. Cliente": "01/01",
                    "Aniv. Marido": "-",
                    "Aniv. Filhos": "-",
                    "Data Casamento": "-",
                    "Restrições": c_obs_criticas,
                    "Últimos Pedidos": st.session_state['id_pedido_atual']
                }
                st.session_state['banco_crm'] = pd.concat([st.session_state['banco_crm'], pd.DataFrame([novo_vip])], ignore_index=True)
                st.success(f"Pedido {st.session_state['id_pedido_atual']} enviado para a ficha de {c_nome} no CRM!")
                st.session_state['id_pedido_atual'] = f"KG-2026-{random.randint(1000, 9999)}"
        with col_b2:
            st.write("")

        msg_whatsapp = f"Olá {c_nome}! Segue o espelho do seu orçamento para o dia {c_data_festa.strftime('%d/%m/%Y')} às {c_horario.strftime('%H:%M')}.\n\n* Itens: {c_doce} - R$ {c_valor_produtos:.2f}\n* Entrega ({c_endereco}): R$ {valor_frete_final:.2f}\n\n*Total:* R$ {valor_total_pedido:.2f}\n\n*Restrições de Cozinha:* {c_obs_criticas}"
        
        if st.button("🖨️ Emitir Espelho do Orçamento Completo"):
            st.markdown(f"""
                <div class="print-box">
                    <b>💎 PROPOSTA COMERCIAL EXCLUSIVA - K&G ARTE EM CONFEITARIA 💎</b><br>
                    <b>Código do Pedido:</b> {st.session_state['id_pedido_atual']}<br>
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
            st.text_area("Copiar mensagem pronta para WhatsApp:", value=msg_whatsapp, height=150)

    # ==========================================
    # ABA 2: CRM & HISTÓRICO DE PEDIDOS
    # ==========================================
    with tabs[2]:
        st.markdown('<div class="section-title">👥 CRM: Central de Relacionamento e Busca Ativa de Clientes VIP</div>', unsafe_allow_html=True)
        mes_atual = datetime.now().strftime("%m")
        st.markdown(f"<div class='alerta-aniv'>🎉 <b>ALERTA DE MARKETING K&G:</b> Juliana Mendes faz aniversário este mês (12/{mes_atual})! Dispare uma mensagem especial e carinhosa.</div>", unsafe_allow_html=True)
        
        busca = st.text_input("🔍 Busca Ativa por Nome, Telefone, Códigos de Pedidos ou Alergias:")
        
        df_crm_ed = st.data_editor(st.session_state['banco_crm'], num_rows="dynamic", use_container_width=True, key="crm_base_key")
        st.session_state['banco_crm'] = df_crm_ed

    # ==========================================
    # ABA 3: FÁBRICA DE BASES
    # ==========================================
    with tabs[3]:
        st.markdown('<div class="section-title">🥣 Fábrica de Bases: Gestão Ilimitada de Receitas e Custos</div>', unsafe_allow_html=True)
        sub_b1, sub_b2, sub_b3, sub_b4 = st.tabs(["🍞 Massas de Bolo", "🍓 Recheios Estruturados", "💧 Caldas para Regar", "✨ Coberturas e Blindagens"])
        
        # --- SUB-ABA 1: MASSAS ---
        with sub_b1:
            st.markdown("##### ➕ Cadastrar Nova Receita de Massa")
            with st.form("nova_massa_form"):
                novo_m_nome = st.text_input("Nome da Nova Massa")
                submit_m = st.form_submit_button("➕ Cadastrar Massa")
                if submit_m and novo_m_nome:
                    if novo_m_nome not in st.session_state['banco_massas_rec']:
                        st.session_state['banco_massas_rec'][novo_m_nome] = {
                            "ingredientes": pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                            "peso_obtido": 1000.0,
                            "preparo": "Descreva aqui o modo de preparo passo a passo.",
                            "decoracao": "Padrão estético aceito para a produção."
                        }
                        st.success(f"Massa '{novo_m_nome}' cadastrada! Selecione-a abaixo para alimentar os ingredientes.")
                    else:
                        st.warning("Massa já cadastrada!")

            st.write("---")
            sel_massa = st.selectbox("Selecione a Massa para Visualizar/Alimentar:", list(st.session_state['banco_massas_rec'].keys()))
            
            if sel_massa:
                rec_m = st.session_state['banco_massas_rec'][sel_massa]
                
                # 📥 FORMULÁRIO COM FLUXO DE DIGITAÇÃO REFORMULADO
                st.markdown(f"##### 📥 Adicionar Novo Insumo: *{sel_massa}*")
                with st.form(key=f"form_add_ing_massa_{sel_massa}", clear_on_submit=True):
                    col_ing1, col_ing2, col_ing3, col_ing4, col_ing5 = st.columns(5)
                    with col_ing1:
                        f_ing = st.text_input("Ingrediente", placeholder="Ex: Chocolate 50%", key=f"f_m_ing_{sel_massa}")
                    with col_ing2:
                        f_usd = st.text_input("Quantidade Usada na Receita", value="0", key=f"f_m_usd_{sel_massa}")
                    with col_ing3:
                        f_uni = st.selectbox("Unidade", ["g", "ml", "un"], key=f"f_m_uni_{sel_massa}")
                    with col_ing4:
                        f_emb = st.text_input("Quantidade na Embalagem", value="1000", key=f"f_m_emb_{sel_massa}")
                    with col_ing5:
                        f_prec = st.text_input("Preço Embalagem (R$)", value="0.00", key=f"f_m_prec_{sel_massa}")
                    
                    submit_ing_m = st.form_submit_button("💾 Salvar Ingrediente na Receita", type="primary")
                    if submit_ing_m and f_ing:
                        adicionar_ingrediente_banco('banco_massas_rec', sel_massa, f_ing, f_uni, f_prec, f_emb, f_usd)
                        st.success(f"✔️ {f_ing} adicionado e salvo com sucesso!")
                        st.rerun()

                st.markdown("##### 📋 Ingredientes Cadastrados")
                m_edit = st.data_editor(
                    rec_m["ingredientes"],
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"m_edit_{sel_massa}"
                )
                st.session_state['banco_massas_rec'][sel_massa]["ingredientes"] = m_edit
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    peso_obt_m = st.number_input("Rendimento Final da Receita (g, ml ou un)", value=float(rec_m.get("peso_obtido", 1000.0)), key=f"peso_m_{sel_massa}")
                    st.session_state['banco_massas_rec'][sel_massa]["peso_obtido"] = peso_obt_m
                    custo_massa_total = calcular_custo_tabela_seguro(m_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_m_kg = (custo_massa_total / peso_obt_m * 1000) if peso_obt_m > 0 else 0.0
                    st.metric("Custo Total da Receita", f"R$ {custo_massa_total:.2f}")
                    st.metric("Custo por kg de Massa", f"R$ {custo_m_kg:.2f}")
                with col_m2:
                    prep_m = st.text_area("Modo de Preparo", value=rec_m.get("preparo", ""), key=f"prep_m_{sel_massa}")
                    dec_m = st.text_area("Decoração & Padronização Estética", value=rec_m.get("decoracao", ""), key=f"dec_m_{sel_massa}")
                    st.session_state['banco_massas_rec'][sel_massa]["preparo"] = prep_m
                    st.session_state['banco_massas_rec'][sel_massa]["decoracao"] = dec_m

        # --- SUB-ABA 2: RECHEIOS ---
        with sub_b2:
            st.markdown("##### ➕ Cadastrar Novo Recheio Estruturado")
            with st.form("novo_recheio_form"):
                novo_r_nome = st.text_input("Nome do Novo Recheio")
                submit_r = st.form_submit_button("➕ Cadastrar Recheio")
                if submit_r and novo_r_nome:
                    if novo_r_nome not in st.session_state['banco_recheios_rec']:
                        st.session_state['banco_recheios_rec'][novo_r_nome] = {
                            "ingredientes": pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                            "peso_obtido": 1000.0,
                            "preparo": "Descreva aqui o modo de preparo passo a passo.",
                            "decoracao": "Padrão estético aceito para a produção."
                        }
                        st.success(f"Recheio '{novo_r_nome}' cadastrado! Selecione-o abaixo para alimentar.")
                    else:
                        st.warning("Recheio já cadastrado!")

            st.write("---")
            sel_recheio = st.selectbox("Selecione o Recheio para Visualizar/Alimentar:", list(st.session_state['banco_recheios_rec'].keys()))
            
            if sel_recheio:
                rec_r = st.session_state['banco_recheios_rec'][sel_recheio]
                
                # 📥 FORMULÁRIO COM FLUXO DE DIGITAÇÃO REFORMULADO
                st.markdown(f"##### 📥 Adicionar Novo Ingrediente ao Recheio: *{sel_recheio}*")
                with st.form(key=f"form_add_ing_recheio_{sel_recheio}", clear_on_submit=True):
                    col_ing1, col_ing2, col_ing3, col_ing4, col_ing5 = st.columns(5)
                    with col_ing1:
                        f_ing = st.text_input("Ingrediente", placeholder="Ex: Leite Moça", key=f"f_r_ing_{sel_recheio}")
                    with col_ing2:
                        f_usd = st.text_input("Quantidade Usada na Receita", value="0", key=f"f_r_usd_{sel_recheio}")
                    with col_ing3:
                        f_uni = st.selectbox("Unidade", ["g", "ml", "un"], key=f"f_r_uni_{sel_recheio}")
                    with col_ing4:
                        f_emb = st.text_input("Quantidade na Embalagem", value="395", key=f"f_r_emb_{sel_recheio}")
                    with col_ing5:
                        f_prec = st.text_input("Preço Embalagem (R$)", value="0.00", key=f"f_r_prec_{sel_recheio}")
                    
                    submit_ing_r = st.form_submit_button("💾 Salvar Ingrediente na Receita", type="primary")
                    if submit_ing_r and f_ing:
                        adicionar_ingrediente_banco('banco_recheios_rec', sel_recheio, f_ing, f_uni, f_prec, f_emb, f_usd)
                        st.success(f"✔️ {f_ing} adicionado e salvo com sucesso!")
                        st.rerun()

                st.markdown("##### 📋 Ingredientes Cadastrados")
                r_edit = st.data_editor(
                    rec_r["ingredientes"],
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"r_edit_{sel_recheio}"
                )
                st.session_state['banco_recheios_rec'][sel_recheio]["ingredientes"] = r_edit
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    peso_obt_r = st.number_input("Rendimento Final da Receita (g, ml ou un)", value=float(rec_r.get("peso_obtido", 1000.0)), key=f"peso_r_{sel_recheio}")
                    st.session_state['banco_recheios_rec'][sel_recheio]["peso_obtido"] = peso_obt_r
                    custo_recheio_total = calcular_custo_tabela_seguro(r_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_r_kg = (custo_recheio_total / peso_obt_r * 1000) if peso_obt_r > 0 else 0.0
                    st.metric("Custo Total do Recheio", f"R$ {custo_recheio_total:.2f}")
                    st.metric("Custo por kg de Recheio", f"R$ {custo_r_kg:.2f}")
                with col_r2:
                    prep_r = st.text_area("Modo de Preparo", value=rec_r.get("preparo", ""), key=f"prep_r_{sel_recheio}")
                    dec_r = st.text_area("Decoração & Padronização", value=rec_r.get("decoracao", ""), key=f"dec_r_{sel_recheio}")
                    st.session_state['banco_recheios_rec'][sel_recheio]["preparo"] = prep_r
                    st.session_state['banco_recheios_rec'][sel_recheio]["decoracao"] = dec_r

        # --- SUB-ABA 3: CALDAS ---
        with sub_b3:
            st.markdown("##### ➕ Cadastrar Nova Calda")
            with st.form("nova_calda_form"):
                novo_c_nome = st.text_input("Nome da Nova Calda")
                submit_c = st.form_submit_button("➕ Cadastrar Calda")
                if submit_c and novo_c_nome:
                    if novo_c_nome not in st.session_state['banco_caldas_rec']:
                        st.session_state['banco_caldas_rec'][novo_c_nome] = {
                            "ingredientes": pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                            "peso_obtido": 1000.0,
                            "preparo": "Misturar e ferver.",
                            "decoracao": "Calda fluida."
                        }
                        st.success(f"Calda '{novo_c_nome}' cadastrada! Selecione-a abaixo para alimentar.")
                    else:
                        st.warning("Calda já cadastrada!")

            st.write("---")
            sel_calda = st.selectbox("Selecione a Calda para Editar:", list(st.session_state['banco_caldas_rec'].keys()))
            if sel_calda:
                rec_c = st.session_state['banco_caldas_rec'][sel_calda]
                
                # 📥 FORMULÁRIO COM FLUXO DE DIGITAÇÃO REFORMULADO
                st.markdown(f"##### 📥 Adicionar Novo Ingrediente à Calda: *{sel_calda}*")
                with st.form(key=f"form_add_ing_calda_{sel_calda}", clear_on_submit=True):
                    col_ing1, col_ing2, col_ing3, col_ing4, col_ing5 = st.columns(5)
                    with col_ing1:
                        f_ing = st.text_input("Ingrediente", placeholder="Ex: Açúcar Cristal", key=f"f_c_ing_{sel_calda}")
                    with col_ing2:
                        f_usd = st.text_input("Quantidade Usada na Receita", value="0", key=f"f_c_usd_{sel_calda}")
                    with col_ing3:
                        f_uni = st.selectbox("Unidade", ["g", "ml", "un"], key=f"f_c_uni_{sel_calda}")
                    with col_ing4:
                        f_emb = st.text_input("Quantidade na Embalagem", value="1000", key=f"f_c_emb_{sel_calda}")
                    with col_ing5:
                        f_prec = st.text_input("Preço Embalagem (R$)", value="0.00", key=f"f_c_prec_{sel_calda}")
                    
                    submit_ing_c = st.form_submit_button("💾 Salvar Ingrediente na Receita", type="primary")
                    if submit_ing_c and f_ing:
                        adicionar_ingrediente_banco('banco_caldas_rec', sel_calda, f_ing, f_uni, f_prec, f_emb, f_usd)
                        st.success(f"✔️ {f_ing} adicionado e salvo com sucesso!")
                        st.rerun()

                st.markdown("##### 📋 Ingredientes Cadastrados")
                c_edit = st.data_editor(
                    rec_c["ingredientes"],
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"c_edit_{sel_calda}"
                )
                st.session_state['banco_caldas_rec'][sel_calda]["ingredientes"] = c_edit
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    peso_obt_c = st.number_input("Rendimento Final (g, ml ou un)", value=float(rec_c.get("peso_obtido", 1000.0)), key=f"peso_c_{sel_calda}")
                    st.session_state['banco_caldas_rec'][sel_calda]["peso_obtido"] = peso_obt_c
                    custo_calda_total = calcular_custo_tabela_seguro(c_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_c_kg = (custo_calda_total / peso_obt_c * 1000) if peso_obt_c > 0 else 0.0
                    st.metric("Custo Total da Calda", f"R$ {custo_calda_total:.2f}")
                    st.metric("Custo por kg", f"R$ {custo_c_kg:.2f}")
                with col_c2:
                    prep_c = st.text_area("Modo de Preparo", value=rec_c.get("preparo", ""), key=f"prep_c_{sel_calda}")
                    dec_c = st.text_area("Padronização", value=rec_c.get("decoracao", ""), key=f"dec_c_{sel_calda}")
                    st.session_state['banco_caldas_rec'][sel_calda]["preparo"] = prep_c
                    st.session_state['banco_caldas_rec'][sel_calda]["decoracao"] = dec_c

        # --- SUB-ABA 4: COBERTURAS ---
        with sub_b4:
            st.markdown("##### ➕ Cadastrar Nova Cobertura / Blindagem")
            with st.form("nova_cob_form"):
                novo_cob_nome = st.text_input("Nome da Nova Cobertura")
                submit_cob = st.form_submit_button("➕ Cadastrar Cobertura")
                if submit_cob and novo_cob_nome:
                    if novo_cob_nome not in st.session_state['banco_coberturas_rec']:
                        st.session_state['banco_coberturas_rec'][novo_cob_nome] = {
                            "ingredientes": pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                            "peso_obtido": 1000.0,
                            "preparo": "Modo de preparo.",
                            "decoracao": "Instruções."
                        }
                        st.success(f"Cobertura '{novo_cob_nome}' cadastrada! Selecione-a abaixo para alimentar.")
                    else:
                        st.warning("Cobertura já cadastrada!")

            st.write("---")
            sel_cob = st.selectbox("Selecione a Cobertura para Editar:", list(st.session_state['banco_coberturas_rec'].keys()))
            if sel_cob:
                rec_cob = st.session_state['banco_coberturas_rec'][sel_cob]
                
                # 📥 FORMULÁRIO COM FLUXO DE DIGITAÇÃO REFORMULADO
                st.markdown(f"##### 📥 Adicionar Novo Ingrediente ao Banho/Blindagem: *{sel_cob}*")
                with st.form(key=f"form_add_ing_cob_{sel_cob}", clear_on_submit=True):
                    col_ing1, col_ing2, col_ing3, col_ing4, col_ing5 = st.columns(5)
                    with col_ing1:
                        f_ing = st.text_input("Ingrediente", placeholder="Ex: Chocolate Sicao", key=f"f_cob_ing_{sel_cob}")
                    with col_ing2:
                        f_usd = st.text_input("Quantidade Usada na Receita", value="0", key=f"f_cob_usd_{sel_cob}")
                    with col_ing3:
                        f_uni = st.selectbox("Unidade", ["g", "ml", "un"], key=f"f_cob_uni_{sel_cob}")
                    with col_ing4:
                        f_emb = st.text_input("Quantidade na Embalagem", value="1000", key=f"f_cob_emb_{sel_cob}")
                    with col_ing5:
                        f_prec = st.text_input("Preço Embalagem (R$)", value="0.00", key=f"f_cob_prec_{sel_cob}")
                    
                    submit_ing_cob = st.form_submit_button("💾 Salvar Ingrediente na Receita", type="primary")
                    if submit_ing_cob and f_ing:
                        adicionar_ingrediente_banco('banco_coberturas_rec', sel_cob, f_ing, f_uni, f_prec, f_emb, f_usd)
                        st.success(f"✔️ {f_ing} adicionado e salvo com sucesso!")
                        st.rerun()

                st.markdown("##### 📋 Ingredientes Cadastrados")
                cob_edit = st.data_editor(
                    rec_cob["ingredientes"],
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"cob_edit_{sel_cob}"
                )
                st.session_state['banco_coberturas_rec'][sel_cob]["ingredientes"] = cob_edit
                
                col_cob1, col_cob2 = st.columns(2)
                with col_cob1:
                    peso_obt_cob = st.number_input("Rendimento Final (g, ml ou un)", value=float(rec_cob.get("peso_obtido", 1000.0)), key=f"peso_cob_{sel_cob}")
                    st.session_state['banco_coberturas_rec'][sel_cob]["peso_obtido"] = peso_obt_cob
                    custo_cob_total = calcular_custo_tabela_seguro(cob_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_cob_kg = (custo_cob_total / peso_obt_cob * 1000) if peso_obt_cob > 0 else 0.0
                    st.metric("Custo Total da Cobertura", f"R$ {custo_cob_total:.2f}")
                    st.metric("Custo por kg/unidade", f"R$ {custo_cob_kg:.2f}")
                with col_cob2:
                    prep_cob = st.text_area("Modo de Preparo", value=rec_cob.get("preparo", ""), key=f"prep_cob_{sel_cob}")
                    dec_cob = st.text_area("Padronização", value=rec_cob.get("decoracao", ""), key=f"dec_cob_{sel_cob}")
                    st.session_state['banco_coberturas_rec'][sel_cob]["preparo"] = prep_cob
                    st.session_state['banco_coberturas_rec'][sel_cob]["decoracao"] = dec_cob

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
    # ABA 5: PRODUTOS COMPLETOS & CÁLCULO DE PROPORÇÃO (CONECTADA ÀS BASES DA ABA 3)
    # ==========================================
    with tabs[5]:
        st.markdown('<div class="section-title">📐 Engenharia de Estrutura de Bolos & Precificação Dinâmica de Venda</div>', unsafe_allow_html=True)
        
        col_pd1, col_pd2 = st.columns(2)
        with col_pd1:
            nome_bolo_final = st.text_input("Bolo Completo", value="Bolo de Morango com Suspiros e Chantiganache")
            peso_alvo = st.number_input("Peso Alvo Solicitado pelo Cliente (kg)", min_value=1.0, value=5.0)
            tipo_forma_final = st.selectbox("Geometria da Forma", ["Redonda", "Retangular"], key="geom_forma_v5")
            margem_comercial = st.slider("Selecione a Margem Comercial de Segurança (%)", min_value=40, max_value=50, value=45, key="margem_v5")
            
            # Dropdowns Dinâmicos conectados com as chaves inseridas na Aba 3
            sel_massa_composta = st.selectbox("Selecione a Massa Base:", list(st.session_state['banco_massas_rec'].keys()))
            sel_recheio_composto = st.selectbox("Selecione o Recheio Estruturado:", list(st.session_state['banco_recheios_rec'].keys()))
            sel_calda_composta = st.selectbox("Selecione a Calda de Regar:", list(st.session_state['banco_caldas_rec'].keys()))
            sel_cobertura_composta = st.selectbox("Selecione a Cobertura/Blindagem:", list(st.session_state['banco_coberturas_rec'].keys()))
            
        with col_pd2:
            peso_alvo_g = peso_alvo * 1000
            calc_massa_final = peso_alvo_g * 0.35
            calc_recheio_final = peso_alvo_g * 0.40
            calc_calda_final = peso_alvo_g * 0.10
            calc_cobertura_final = peso_alvo_g * 0.15
            
            if tipo_forma_final == "Redonda":
                diametro_sugerido = math.ceil(2 * math.sqrt(peso_alvo_g / (3.14 * 10 * 0.6)))
                st.metric("Forma Redonda Recomendada", f"{diametro_sugerido} cm de diâmetro (Altura de 10cm)")
            else:
                st.metric("Forma Retangular Recomendada", "35x25 cm")

        # Busca dinâmica do custo real por kg de cada base calculada na Aba 3
        custo_m_kg = get_recipe_cost_kg(st.session_state['banco_massas_rec'], sel_massa_composta)
        custo_r_kg = get_recipe_cost_kg(st.session_state['banco_recheios_rec'], sel_recheio_composto)
        custo_c_kg = get_recipe_cost_kg(st.session_state['banco_caldas_rec'], sel_calda_composta)
        custo_cob_kg = get_recipe_cost_kg(st.session_state['banco_coberturas_rec'], sel_cobertura_composta)

        # Cálculo do custo proporcional das camadas
        custo_massa_composto = (custo_m_kg / 1000) * calc_massa_final
        custo_recheio_composto = (custo_r_kg / 1000) * calc_recheio_final
        custo_calda_composto = (custo_c_kg / 1000) * calc_calda_final
        custo_cob_composto = (custo_cob_kg / 1000) * calc_cobertura_final
        custo_insumos_total = custo_massa_composto + custo_recheio_composto + custo_calda_composto + custo_cob_composto + 12.00
        
        st.markdown("##### 📝 Balanço Estrutural para Produção de Cozinha:")
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        with c_p1: st.metric(f"Massa ({sel_massa_composta})", f"{int(calc_massa_final)} g", f"Custo: R$ {custo_massa_composto:.2f}")
        with c_p2: st.metric(f"Recheio ({sel_recheio_composto})", f"{int(calc_recheio_final)} g", f"Custo: R$ {custo_recheio_composto:.2f}")
        with c_p3: st.metric(f"Calda ({sel_calda_composta})", f"{int(calc_calda_final)} g", f"Custo: R$ {custo_calda_composto:.2f}")
        with c_p4: st.metric(f"Cobertura ({sel_cobertura_composta})", f"{int(calc_cobertura_final)} g", f"Custo: R$ {custo_cob_composto:.2f}")

        # PRECIFICAÇÃO DE VENDAS COM COBERTURA DE TAXAS
        st.markdown("### 💰 Tabela de Preço de Venda Comercial")
        divisor_margem = (100 - margem_comercial) / 100
        preco_venda_base = custo_insumos_total / divisor_margem
        
        v_debito = preco_venda_base / (1 - 0.0199)
        v_credito = preco_venda_base / (1 - 0.0499)
        v_ifood = preco_venda_base / 0.73

        cv1, cv2, cv3, cv4 = st.columns(4)
        with cv1: st.markdown(f"<div class='preco-box'><b>🛍️ PIX / DINHEIRO</b><br><span style='font-size:20px; font-weight:bold;'>R$ {preco_venda_base:.2f}</span><br>Lucro Limpo de {margem_comercial}%</div>", unsafe_allow_html=True)
        with cv2: st.markdown(f"<div class='preco-box' style='background:#0B533A;'><b>💳 DÉBITO MAQ.</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_debito:.2f}</span><br>Taxa 1.99% inclusa</div>", unsafe_allow_html=True)
        with cv3: st.markdown(f"<div class='preco-box' style='background:#0B533A;'><b>💳 CRÉDITO MAQ.</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_credito:.2f}</span><br>Taxa 4.99% inclusa</div>", unsafe_allow_html=True)
        with cv4: st.markdown(f"<div class='preco-box' style='background:#901414;'><b>🛵 CARDÁPIO IFOOD</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_ifood:.2f}</span><br>Taxas de Delivery Cobertas</div>", unsafe_allow_html=True)

        foto_bolo = st.file_uploader("📸 Enviar Foto do Produto Finalizado", type=["jpg", "png", "jpeg"], key="uploader_v5")

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
        
        st.markdown("##### 🚨 Alerta Vermelho de Compras:")
        for idx, row in df_est_edit.iterrows():
            try:
                atual = float(limpar_e_converter_coluna(pd.DataFrame([row]), "Quantidade em Estoque (Un)", 0.0)[0])
                minimo = float(limpar_e_converter_coluna(pd.DataFrame([row]), "Estoque Mínimo de Segurança (Un)", 0.0)[0])
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
        
        custo_unit = limpar_e_converter_coluna(df_inv_edit, "Valor Unitário (R$)", 0.0)
        quantidades = limpar_e_converter_coluna(df_inv_edit, "Quantidade", 0.0)
        patrimonio_total = (custo_unit * quantidades).sum()
        
        st.metric("Patrimônio Físico Total Acumulado no Atelier", f"R$ {patrimonio_total:.2f}")
        st.file_uploader("📸 Registrar foto de patrimônio (moldes, cortadores, stencils)", type=["png","jpg"])

elif chave_usuario != "":
    st.error("Chave de Acesso Incorreta! Por favor, digite a senha autorizada da K&G.")
else:
    st.warning("Insira a chave de acesso empresarial para visualizar o ecossistema estratégico.")
