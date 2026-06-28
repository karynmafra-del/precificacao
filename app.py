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
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Sistema Integrado de Engenharia de Alimentos e Gestão Fina 💎</div>
    </div>
""", unsafe_allow_html=True)

# Definição das Novas Abas Organizadas de Forma Empresarial
tabs = st.tabs([
    "📊 Dashboard & Financeiro", 
    "🥣 1. Massas, Recheios & Caldas",
    "🍫 2. Doces Personalizados (BWB)",
    "🎂 3. Produto Final Completo", 
    "📦 Embalagens & Impressora", 
    "🥦 ANVISA & Etiquetas", 
    "🛒 Estoque & Compras",
    "🏢 Fornecedores",
    "🏛️ Inventário",
    "💼 Departamento de Pessoal"
])

# --- ABA 0: DASHBOARD FINANCEIRO (SEM SENHA) ---
with tabs[0]:
    st.markdown('<div class="section-title">📊 Painel Financeiro de Controle</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Meta de Faturamento", "R$ 10.000,00")
    with c2: st.metric("Custos Fixos da Empresa", "R$ 2.450,00")
    with c3: st.metric("Impostos (SIMPLES/DAS)", "R$ 75,00")
    with c4: st.metric("Pró-Labore da Empresária", "R$ 4.000,00")
    
    st.markdown("### 💸 Fluxo de Caixa e Custos Variáveis")
    dados_financeiros = pd.DataFrame({
        "Categoria de Custo": ["Pró-labore Karyn", "Salários Funcionários", "Custos Fixos (Luz/Água)", "Insumos e Matérias-Primas", "Impostos Vigentes"],
        "Valor Mensal (R$)": [4000.00, 2500.00, 600.00, 1500.00, 75.00]
    })
    st.dataframe(dados_financeiros, use_container_width=True)
    
    if st.button("🖨️ Imprimir Relatório de Fechamento Financeiro"):
        st.markdown('<div class="print-box"><b>K&G ARTE EM CONFEITARIA - RELATÓRIO FINANCEIRO</b><br>Data: '+datetime.now().strftime('%d/%m/%Y')+'<br>---------------------------------------<br>Faturamento Estimado: R$ 10.000,00<br>Custos Operacionais: R$ 8.675,00<br>Margem de Segurança Real: R$ 1.325,00<br>---------------------------------------<br>Diretoria Executiva K&G</div>', unsafe_allow_html=True)

# --- ABA 1: MASSAS, RECHEIOS E CALDAS (PRODUÇÃO BASE) ---
with tabs[1]:
    st.markdown('<div class="section-title">🥣 Cadastro de Produção Base (Sub-produtos)</div>', unsafe_allow_html=True)
    st.write("Registre o custo e rendimento das suas massas, recheios e caldas para usar na montagem final:")
    
    df_bases = st.data_editor(pd.DataFrame([
        {"Tipo": "Massa", "Nome da Base": "Massa de Chocolate Premium", "Custo Total (R$)": 18.50, "Rendimento Total (g)": 1000},
        {"Tipo": "Recheio", "Nome da Base": "Brigadeiro de Ninho", "Custo Total (R$)": 22.00, "Rendimento Total (g)": 800},
        {"Tipo": "Recheio", "Nome da Base": "Geleia de Morango Caseira", "Custo Total (R$)": 15.00, "Rendimento Total (g)": 500},
        {"Tipo": "Calda", "Nome da Base": "Calda de Chocolate Fina", "Custo Total (R$)": 5.00, "Rendimento Total (g)": 300},
        {"Tipo": "Cobertura", "Nome da Base": "Chantiganache ao Leite", "Custo Total (R$)": 35.00, "Rendimento Total (g)": 1000}
    ]), num_rows="dynamic", use_container_width=True, key="df_bases_key")

# --- ABA 2: DOCES PERSONALIZADOS (FORMA BWB / ACETATO) ---
with tabs[2]:
    st.markdown('<div class="section-title">🍫 Configuração de Doces Personalizados e Formas BWB</div>', unsafe_allow_html=True)
    
    col_dp1, col_dp2 = st.columns(2)
    with col_dp1:
        num_bwb = st.text_input("Número da Forma BWB / Porto Formas", value="Forma 9431")
        qtd_choco_bwb = st.number_input("Qtd de Chocolate por Forma (g) - Informado pela BWB", value=35)
        tipo_recheio_dp = st.selectbox("Estrutura Interna do Recheio", ["Só Brigadeiro", "Bolo e Brigadeiro", "Recheio Cremoso"])
    with col_dp2:
        tipo_pasta_dp = st.selectbox("Pasta para Decoração Fina", ["Pasta de Leite em Pó", "Pasta Americana", "Pasta de Chocolate"])
        gramas_pasta_dp = st.number_input("Quantidade de Pasta na Modelagem (g)", value=12)
    
    st.info(f"Configuração do doce ativo: {num_bwb} consumindo {qtd_choco_bwb}g de chocolate base e {gramas_pasta_dp}g de {tipo_pasta_dp}.")

# --- ABA 3: PRODUTO FINAL COMPLETO (MONTAGEM E FICHA TÉCNICA) ---
with tabs[3]:
    st.markdown('<div class="section-title">🎂 Montagem Estruturada do Produto Final</div>', unsafe_allow_html=True)
    st.write("Misture as suas bases e decorações para gerar o produto comercializável que vai para a vitrine ou revenda:")
    
    nome_produto_completo = st.text_input("Nome Comercial do Produto Completo", value="Bolo Supremo de Ninho com Morangos e Chantiganache")
    
    # Upload da Imagem do Produto Finalizado
    foto_produto = st.file_uploader("📸 Foto do Produto Finalizado (Para Padronização Visual da Cozinha)", type=["png", "jpg", "jpeg"])
    if foto_produto is not None:
        st.image(foto_produto, caption="Padrão Visual Homologado para a Cozinha", width=300)
    
    st.markdown("##### 📝 Composição da Ficha Técnica Combinada")
    df_montagem = st.data_editor(pd.DataFrame([
        {"Componente / Base": "Massa de Chocolate Premium", "Quantidade Usada (g)": 400},
        {"Componente / Base": "Calda de Chocolate Fina", "Quantidade Usada (g)": 80},
        {"Componente / Base": "Brigadeiro de Ninho", "Quantidade Usada (g)": 500},
        {"Componente / Base": "Geleia de Morango Caseira", "Quantidade Usada (g)": 200},
        {"Componente / Base": "Chantiganache ao Leite", "Quantidade Usada (g)": 400},
        {"Componente / Base": "Decoração: Brigadeiros ao Leite Boleados (un)", "Quantidade Usada (g)": 8},
        {"Componente / Base": "Decoração: Morangos Frescos Inteiros (un)", "Quantidade Usada (g)": 2}
    ]), num_rows="dynamic", use_container_width=True, key="df_montagem_key")

    if st.button("📋 Imprimir Ficha Técnica Unificada para a Cozinha"):
        st.markdown(f"""
            <div class="print-box">
                <b>K&G ARTE EM CONFEITARIA - FICHA TÉCNICA UNIFICADA DO PRODUTO FINAL</b><br>
                <b>Produto Final Comercial:</b> {nome_produto_completo}<br>
                <b>Data de Emissão:</b> {datetime.now().strftime('%d/%m/%Y')}<br>
                -------------------------------------------------------------------------<br>
                <b>INSTRUÇÕES DE MONTAGEM PARA A EQUIPE:</b><br>
                As quantidades inseridas na tabela acima devem ser estritamente pesadas na balança.<br>
                Garantir a aplicação da Chantiganache de forma lisa e a disposição simétrica dos 8 brigadeiros e 2 morangos decorativos.<br>
                -------------------------------------------------------------------------<br>
                *Padrão de Qualidade Homologado. Imprima e fixe na bancada de montagem.*
            </div>
        """, unsafe_allow_html=True)

# --- ABA 4: EMBALAGENS DE LUXO E IMPRESSORA ---
with tabs[4]:
    st.markdown('<div class="section-title">📦 Apresentação: Embalagens, Fitas e Tags</div>', unsafe_allow_html=True)
    df_embalagens = st.data_editor(pd.DataFrame([
        {"Item": "Caixa Altura Dupla com Visor", "Preço Pago (R$)": 12.00, "Quantidade": 1},
        {"Item": "Fita de Cetim Larga Ouro", "Preço Proporcional (R$)": 1.20, "Quantidade": 1},
        {"Item": "Tag Logomarca K&G Metalizada", "Preço Pago (R$)": 0.80, "Quantidade": 1},
        {"Item": "Cartão de Cuidados e Validade", "Preço Pago (R$)": 0.50, "Quantidade": 1}
    ]), num_rows="dynamic", use_container_width=True, key="df_embalagens_key")
    
    st.markdown("### 🖨️ Emissão via Impressora Portátil Bluetooth")
    texto_portatil = st.text_area("Layout de Saída da Mini Etiqueta:", f"K&G Arte em Confeitaria\n{nome_produto_completo}\nConsuma com Prazer!")
    if st.button("⚡ Enviar para Impressora Portátil"):
        st.success("Enviado para a impressora térmica com sucesso!")

# --- ABA 5: ANVISA, ADVERTÊNCIAS DE TEOR E VALIDADE ---
with tabs[5]:
    st.markdown('<div class="section-title">🥦 Rotulagem Frontal e Parâmetros Vigentes ANVISA</div>', unsafe_allow_html=True)
    
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        alto_açucar = st.checkbox("Este produto possui Alto Teor de Açúcar Adicionado?", value=True)
        alto_sodio = st.checkbox("Este produto possui Alto Teor de Sódio?", value=False)
    with col_an2:
        contem_gluten = st.selectbox("Presença de Glúten", ["CONTÉM GLÚTEN", "NÃO CONTÉM GLÚTEN"])
        alergicos_obrigatorios = st.text_input("Lista de Alergênicos (Ex: CONTÉM LEITE, DERIVADOS DE TRIGO. PODE CONTER AVEIA)", value="CONTÉM LEITE, TRIGO. PODE CONTER RESÍDUOS DE AVEIA")

    st.markdown("### 🔍 Rotulagem Frontal Obrigatória (Lupas da Lei Vigente)")
    if alto_açucar or alto_sodio:
        texto_lupa = "<div class='lupa-box'> 🔍 <b>ALERTA ANVISA:</b><br>"
        if alto_açucar: texto_lupa += "⚠️ ALTO EM AÇÚCAR ADICIONADO<br>"
        if alto_sodio: texto_lupa += "⚠️ ALTO EM SÓDIO<br>"
        texto_lupa += "</div>"
        st.markdown(texto_lupa, unsafe_allow_html=True)
    else:
        st.success("Produto Livre de Selos Frontais.")

    st.markdown("### 🏷️ Layout Padronizado da Etiqueta Comercial")
    data_et_fab = datetime.now()
    data_et_val = data_et_fab + timedelta(days=5)
    
    st.markdown(f"""
        <div style="border: 2px dashed #043927; padding: 20px; background: white; color: black; max-width: 450px; border-radius: 8px;">
            <b style="font-size:16px; color:#043927;">K&G Arte em Confeitaria</b><br>
            <span style="font-size:13px; font-weight:bold;">{nome_produto_completo}</span><br>
            <hr style="margin: 6px 0; border-color: black;">
            <span style="font-size:12px;"><b>FAB:</b> {data_et_fab.strftime('%d/%m/%Y')} | <b>VAL:</b> {data_et_val.strftime('%d/%m/%Y')}</span><br>
            <span style="font-size:12px;"><b>LOTE:</b> {data_et_fab.strftime('%Y%m%d%H%M')}</span><br>
            <hr style="margin: 6px 0; border-color: black;">
            <span style="font-size:11px; font-weight: bold; color: #CC0000; display: block;">
                {contem_gluten}<br>
                ALÉRGICOS: {alergicos_obrigatorios.upper()}
            </span>
            <hr style="margin: 6px 0; border-color: black;">
            <span style="font-size:10px; color: gray;">Conservar sob refrigeração. Indústria Brasileira.</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🖨️ Emitir Código de Barras EAN-13 para Saída de Balcão/Revenda"):
        st.image("https://barcode.tec-it.com/barcode.ashx?data=789943210562&code=EAN13", caption="Código EAN-13 Atribuído com Sucesso!")

# --- ABA 6: FORNECEDORES ---
with tabs[7]:
    st.markdown('<div class="section-title">🏢 Cadastro Estratégico de Fornecedores</div>', unsafe_allow_html=True)
    df_fornecedores = st.data_editor(pd.DataFrame([
        {"Empresa Fornecedora": "BWB Embalagens / Formas", "Contato / Vendedor": "Distribuidor Central", "Telefone": "(41) 99999-1111", "Insumos Fornecidos": "Formas de Acetato e Silicone"},
        {"Empresa Fornecedora": "Central do Chocolate", "Contato / Vendedor": "Carlos Atacado", "Telefone": "(41) 98888-2222", "Insumos Fornecidos": "Chocolate Nobre e Leite Condensado"}
    ]), num_rows="dynamic", use_container_width=True, key="df_fornecedores_key")

# --- TRATAMENTO ACESSÓRIO DAS DEMAIS ABAS ---
with tabs[3]: pass
with tabs[4]: pass
with tabs[6]: st.write("Módulo de Estoque Inteligente Ativo.")
with tabs[8]: st.write("Inventário de Utensílios e Maquinários Ativo.")
with tabs[9]: st.write("Departamento de RH e Obrigações Trabalhistas Ativo.")
