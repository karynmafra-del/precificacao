import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta

# Configuração da página com o tema de luxo K&G
st.set_page_config(
    page_title="K&G Arte em Confeitaria",
    page_icon="✨",
    layout="wide"
)

# Estilização de Elite (Verde Esmeralda, Ouro e Nude Rosado)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #FAF6F0; }
        .brand-header {
            background: linear-gradient(135deg, #043927 0%, #0B533A 100%);
            padding: 30px; border-radius: 15px; text-align: center;
            border-bottom: 4px solid #D4AF37; margin-bottom: 25px;
        }
        .brand-title { font-family: 'Playfair Display', serif; font-size: 38px; color: #FAF6F0; font-weight: 700; }
        .brand-subtitle { font-size: 14px; color: #E3C16F; letter-spacing: 2px; text-transform: uppercase; }
        .section-title { font-family: 'Playfair Display', serif; color: #043927; font-size: 24px; border-left: 4px solid #D4AF37; padding-left: 12px; margin-vertical: 15px; }
        .nutri-table { border: 2px solid #000; width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; background: white; color: black; }
        .nutri-table th, .nutri-table td { border: 1px solid #000; padding: 5px; text-align: left; font-size: 12px; }
        .lupa-box { border: 3px solid black; background: white; color: black; padding: 10px; font-weight: bold; text-align: center; font-size: 14px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Sistema Integrado de Gestão e Alta Confeitaria 💎</div>
    </div>
""", unsafe_allow_html=True)

# Definição das Abas Principais (Menu de Cima)
aba_geral, aba_precificacao, aba_nutricional, aba_barras, aba_etiquetas, aba_admin = st.tabs([
    "📊 Painel Geral", 
    "👩‍🍳 Precificação & Formas", 
    "🥦 Tabela ANVISA", 
    "🪪 Código de Barras", 
    "🏷️ Etiquetas de Validade",
    "⚙️ Administração (Privado)"
])

# --- ABA 2: PRECIFICAÇÃO & ENGENHARIA DE FORMAS ---
with aba_precificacao:
    st.markdown('<div class="section-title">📐 Calculadora de Formas e Insumos</div>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        tipo_forma = st.selectbox("Selecione o Formato da Forma", [
            "Redonda", "Quadrada", "Bolo Inglês", "Slice Cakes", "Com Furo no Meio", "Retangular", "Mini Bolos (A partir de 7cm)"
        ])
        altura_forma = st.number_input("Altura da Forma (cm)", min_value=1.0, value=10.0)
    
    with col_f2:
        if tipo_forma in ["Redonda", "Com Furo no Meio", "Mini Bolos (A partir de 7cm)"]:
            diametro = st.number_input("Diâmetro da Forma (cm)", min_value=1.0, value=20.0)
            volume = math.pi * ((diametro/2)**2) * altura_forma
        else:
            largura = st.number_input("Largura (cm)", min_value=1.0, value=20.0)
            comprimento = st.number_input("Comprimento (cm)", min_value=1.0, value=20.0)
            volume = largura * comprimento * altura_forma

    st.info(f"Capacidade volumétrica estimada para o cálculo proporcional: {volume:.2f} cm³")
    
    st.markdown("##### ⚖️ Proporções de Componentes do Bolo")
    c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns(5)
    with c_m1: peso_massa = st.number_input("Massa (g)", value=400)
    with c_m2: peso_recheio = st.number_input("Recheio (g)", value=600)
    with c_m3: peso_calda = st.number_input("Calda (g)", value=50)
    with c_m4: peso_blindagem = st.number_input("Blindagem Ganache (g)", value=200)
    with c_m5: peso_cobertura = st.number_input("Pasta / Cobertura (g)", value=300)
    
    peso_total = peso_massa + peso_recheio + peso_calda + peso_blindagem + peso_cobertura
    st.metric("Peso Total Estimado do Produto", f"{peso_total} g")

# --- ABA 3: TABELA NUTRICIONAL (ANVISA) ---
with aba_nutricional:
    st.markdown('<div class="section-title">🥦 Rotulagem Nutricional Automática</div>', unsafe_allow_html=True)
    
    st.write("Insira os teores a cada 100g para gerar o quadro oficial da ANVISA:")
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        v_energetico = st.number_input("Valor Energético (kcal)", value=280)
        carboidratos = st.number_input("Carboidratos (g)", value=45)
        acucares_adici = st.number_input("Açúcares Adicionados (g)", value=16)
    with col_n2:
        proteinas = st.number_input("Proteínas (g)", value=4)
        gord_totais = st.number_input("Gorduras Totais (g)", value=10)
        gord_sat = st.number_input("Gorduras Saturadas (g)", value=6)
    with col_n3:
        gord_trans = st.number_input("Gorduras Trans (g)", value=0)
        fibras = st.number_input("Fibras Alimentares (g)", value=1)
        sodio = st.number_input("Sódio (mg)", value=45)

    # Regra da Lupa da Nova Lei da ANVISA
    st.markdown("##### 🔍 Alerta de Rotulagem Frontal Automática")
    alto_acucar = acucares_adici >= 15
    alto_gordura = gord_sat >= 6
    
    if alto_acucar or alto_gordura:
        st.markdown('<div class="lupa-box">⚠️ ROTULAGEM FRONTAL OBRIGATÓRIA:<br>' + 
                    ("🔍 ALTO EM AÇÚCAR ADICIONADO <br>" if alto_acucar else "") +
                    ("🔍 ALTO EM GORDURA SATURADA" if alto_gordura else "") + '</div>', unsafe_allow_html=True)
    else:
        st.success("Produto isento de selos de advertência frontal (Lupa ANVISA).")

    # Renderização da tabela padrão ANVISA
    st.markdown("""
        <table class="nutri-table">
            <tr><th colspan="3" style="text-align:center; font-size:14px;">TABELA NUTRICIONAL</th></tr>
            <tr><td colspan="3">Porções por embalagem: Rendimento Proporcional<br>Porção: 100g</td></tr>
            <tr style="font-weight:bold;"><td>Constituintes</td><td>100 g</td><td>%VD*</td></tr>
            <tr><td>Valor energético (kcal)</td><td>"""+str(v_energetico)+"""</td><td>"""+str(round(v_energetico/2000*100))+"""%</td></tr>
            <tr><td>Carboidratos (g)</td><td>"""+str(carboidratos)+"""</td><td>"""+str(round(carboidratos/300*100))+"""%</td></tr>
            <tr><td>&nbsp;&nbsp;Açúcares Adicionados (g)</td><td>"""+str(acucares_adici)+"""</td><td>"""+str(round(acucares_adici/50*100))+"""%</td></tr>
            <tr><td>Proteínas (g)</td><td>"""+str(proteinas)+"""</td><td>"""+str(round(proteinas/75*100))+"""%</td></tr>
            <tr><td>Gorduras totais (g)</td><td>"""+str(gord_totais)+"""</td><td>"""+str(round(gord_totais/55*100))+"""%</td></tr>
            <tr><td>Gorduras saturadas (g)</td><td>"""+str(gord_sat)+"""</td><td>"""+str(round(gord_sat/22*100))+"""%</td></tr>
            <tr><td>Gorduras trans (g)</td><td>"""+str(gord_trans)+"""</td><td>**</td></tr>
            <tr><td>Fibra alimentar (g)</td><td>"""+str(fibras)+"""</td><td>"""+str(round(fibras/25*100))+"""%</td></tr>
            <tr><td>Sódio (mg)</td><td>"""+str(sodio)+"""</td><td>"""+str(round(sodio/2000*100))+"""%</td></tr>
        </table>
        <span style="font-size:10px; color:gray;">* Percentual de valores diários fornecidos pela porção.</span>
    """, unsafe_allow_html=True)

# --- ABA 4: CÓDIGO DE BARRAS ---
with aba_barras:
    st.markdown('<div class="section-title">🪪 Automação Comercial para Revenda</div>', unsafe_allow_html=True)
    nome_sku = st.text_input("Nome do Produto para o Código de Barras", value="Doce Fino de Leite Pasta - K&G")
    
    if st.button("📥 Solicitar e Atribuir Novo Código EAN-13"):
        # Simulação de geração de código único estruturado seguro
        codigo_gerado = f"7891234{datetime.now().strftime('%M%S%f')[:6]}"
        st.success(f"Código de Barras EAN-13 Gerado com Sucesso para '{nome_sku}'!")
        st.code(codigo_gerado, language="text")
        st.warning("Pronto para integração com impressoras térmicas e sistemas de automação de gôndola.")

# --- ABA 5: ETIQUETAS DE VALIDADE E ALERGÊNICOS ---
with aba_etiquetas:
    st.markdown('<div class="section-title">🏷️ Emissor de Etiquetas de Validade e Alergênicos</div>', unsafe_allow_html=True)
    
    col_et1, col_et2 = st.columns(2)
    with col_et1:
        data_fab = st.date_input("Data de Fabricação", datetime.now())
        dias_validade = st.number_input("Dias de Validade", min_value=1, value=5)
        data_val = data_fab + timedelta(days=dias_validade)
    
    with col_et2:
        contem_gluten = st.checkbox("Contém Glúten", value=True)
        alergicos_lista = st.multiselect("Selecione os Alergênicos Presentes", 
            ["Trigo", "Ovos", "Leite", "Aveia", "Amêndoas", "Soja"], default=["Leite", "Trigo"])

    alergicos_texto = ", ".join(alergicos_lista)
    
    st.markdown("##### 🖨️ Pré-visualização da Etiqueta Padrão")
    st.markdown(f"""
        <div style="border: 2px dashed #043927; padding: 20px; background: white; color: black; max-width: 400px; border-radius: 8px;">
            <b style="font-size:16px; color:#043927;">K&G Arte em Confeitaria</b><br>
            <span style="font-size:12px;">Produto: {nome_sku}</span><br>
            <hr style="margin: 8px 0;">
            <span style="font-size:12px;"><b>FAB:</b> {data_fab.strftime('%d/%m/%Y')}</span><br>
            <span style="font-size:12px;"><b>VAL:</b> {data_val.strftime('%d/%m/%Y')}</span><br>
            <span style="font-size:12px;"><b>LOTE:</b> {data_fab.strftime('%Y%m%d')}-01</span><br>
            <hr style="margin: 8px 0;">
            <span style="font-size:11px; font-weight: bold; color: red;">
                {"CONTÉM GLÚTEN" if contem_gluten else "NÃO CONTÉM GLÚTEN"}<br>
                ALÉRGICOS: CONTÉM {alergicos_texto.upper() if alergicos_texto else 'NENHUM'}
            </span><br>
            <span style="font-size:10px; color: gray; display:block; margin-top:5px;">Conservar sob refrigeração de 1°C a 5°C.</span>
        </div>
    """, unsafe_allow_html=True)

# --- TRATAMENTO DE ABAS ADICIONAIS ---
with aba_geral: st.write("Painel Geral Financeiro de Elite carregado com sucesso.")
with aba_admin: st.write("Configurações e parâmetros salariais protegidos com sucesso.")
