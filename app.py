import streamlit as st
import pandas as pd

# Configuração da página com ícone moderno de brilhante/luxo
st.set_page_config(
    page_title="K&G Arte em Confeitaria",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização de Luxo: Verde Esmeralda, Ouro e Nude Rosado
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Poppins:wght@300;400;600&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main {
            background-color: #FAF6F0;
        }
        
        .brand-header {
            background: linear-gradient(135deg, #043927 0%, #0B533A 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(4,57,39,0.15);
            border-bottom: 4px solid #D4AF37;
            margin-bottom: 35px;
        }
        
        .brand-title {
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            color: #FAF6F0;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .brand-subtitle {
            font-size: 16px;
            color: #E3C16F;
            font-weight: 300;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            color: #043927;
            font-size: 26px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #D4AF37;
            padding-left: 12px;
        }
        
        .metric-card {
            background-color: #FFFFFF;
            padding: 22px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #EAE0D5;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: #D4AF37;
        }
        
        .highlight-card {
            background: linear-gradient(135deg, #FAF0E6 0%, #F4E2DE 100%);
            padding: 30px;
            border-radius: 18px;
            text-align: center;
            border: 2px solid #D4AF37;
            box-shadow: 0 8px 20px rgba(212,175,55,0.12);
            margin-top: 25px;
        }
        
        div[data-testid="stSidebar"] {
            background-color: #043927 !important;
        }
        div[data-testid="stSidebar"] * {
            color: #FAF6F0 !important;
        }
        div[data-testid="stSidebar"] input {
            color: #043927 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Topo Elegantissimo
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Sistema Alta Costura em Precificação 💎</div>
    </div>
""", unsafe_allow_html=True)

# --- PAINEL LATERAL PREMIUM ---
st.sidebar.markdown("<h2 style='color: #E3C16F; font-family: Playfair Display; text-align: center;'>Configurações de Elite</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("### 👩‍🍳 Sua Mão de Obra")
salario_desejado = st.sidebar.number_input("Próxima Meta de Faturamento (R$)", min_value=0.0, value=10000.0, step=500.0)
horas_dia = st.sidebar.slider("Horas de Produção por Dia", 1, 16, 8)
dias_semana = st.sidebar.slider("Dias de Trabalho por Semana", 1, 7, 5)

total_horas_mes = horas_dia * dias_semana * 4.33
valor_hora = salario_desejado / total_horas_mes if total_horas_mes > 0 else 0

st.sidebar.markdown(f"""
    <div style='background-color: #0B533A; padding: 15px; border-radius: 10px; border: 1px solid #E3C16F; text-align: center; margin-top: 10px;'>
        <span style='font-size: 13px; color: #FAF6F0;'>VALOR VALIOSO DA SUA HORA</span><br>
        <span style='font-size: 20px; font-weight: bold; color: #E3C16F;'>R$ {valor_hora:.2f}</span>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Margens do Atelier")
custos_fixos_pct = st.sidebar.slider("Custos Indiretos / Fixos (%)", 0, 100, 12)
margem_lucro_pct = st.sidebar.slider("Margem de Lucro Desejada (%)", 0, 300, 40)

# --- CORPO PRINCIPAL ---
st.markdown('<div class="section-title">✨ Criação e Ficha Técnica</div>', unsafe_allow_html=True)

col_prod1, col_prod2 = st.columns(2)
with col_prod1:
    nome_produto = st.text_input("Nome da Obra de Arte", placeholder="Ex: Doce Personalizado em Pasta de Leite")
with col_prod2:
    tempo_gasto = st.number_input("Tempo Dedicado à Produção (em horas)", min_value=0.0, value=1.0, step=0.1)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h5>🛒 Ingredientes e Insumos Utilizados</h5>', unsafe_allow_html=True)

dados_iniciais = pd.DataFrame([
    {"Ingrediente / Material": "Pasta de Leite em Pó", "Preço Pago (R$)": 35.0, "Qtd Comprada": 1000.0, "Unidade": "g", "Qtd Usada": 150.0},
    {"Ingrediente / Material": "Embalagem de Luxo / Tag", "Preço Pago (R$)": 45.0, "Qtd Comprada": 20.0, "Unidade": "un", "Qtd Usada": 1.0}
])

df_materiais = st.data_editor(
    dados_iniciais,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Ingrediente / Material": st.column_config.TextColumn("Item"),
        "Preço Pago (R$)": st.column_config.NumberColumn("Preço Pago", format="R$ %.2f"),
        "Qtd Comprada": st.column_config.NumberColumn("Qtd Comprada"),
        "Unidade": st.column_config.SelectboxColumn("Unidade", options=["g", "kg", "un", "ml", "l", "m"]),
        "Qtd Usada": st.column_config.NumberColumn("Qtd Usada")
    }
)

custo_materiais = 0.0
for _, row in df_materiais.iterrows():
    try:
        p = float(row["Preço Pago (R$)"])
        qc = float(row["Qtd Comprada"])
        qu = float(row["Qtd Usada"])
        if qc > 0: custo_materiais += (p / qc) * qu
    except: continue

custo_mao_de_obra = tempo_gasto * valor_hora
custo_direto_total = custo_materiais + custo_mao_de_obra

porcentagem_restante = 1 - (custos_fixos_pct / 100.0) - (margem_lucro_pct / 100.0)
preco_venda = custo_direto_total / porcentagem_restante if porcentagem_restante > 0 else custo_direto_total * (1 + (custos_fixos_pct + margem_lucro_pct)/100)

valor_custo_fixo = preco_venda * (custos_fixos_pct / 100.0)
valor_lucro_real = preco_venda * (margem_lucro_pct / 100.0)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Demonstrativo de Valores</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><span style="color: #6B7280; font-size: 13px;">🍓 Total Insumos</span><br><b style="font-size: 22px; color: #043927;">R$ {custo_materiais:.2f}</b></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><span style="color: #6B7280; font-size: 13px;">⏳ Mão de Obra</span><br><b style="font-size: 22px; color: #043927;">R$ {custo_mao_de_obra:.2f}</b></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><span style="color: #6B7280; font-size: 13px;">🏛️ Custos Fixos</span><br><b style="font-size: 22px; color: #043927;">R$ {valor_custo_fixo:.2f}</b></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><span style="color: #6B7280; font-size: 13px;">👑 Lucro Líquido K&G</span><br><b style="font-size: 22px; color: #0B533A;">R$ {valor_lucro_real:.2f}</b></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="highlight-card">
        <span style="font-size: 13px; color: #043927; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;">Preço Final Sugerido ao Cliente</span><br>
        <span style="font-size: 46px; font-weight: 800; color: #043927; font-family: 'Playfair Display', serif;">R$ {preco_venda:.2f}</span>
    </div>
""", unsafe_allow_html=True)
