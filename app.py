import streamlit as st
import pandas as pd
import math
import random
import json
import os
from datetime import datetime, timedelta

# Configuração da página do Streamlit
st.set_page_config(
    page_title="K&G Arte em Confeitaria",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght=400;700&family=Poppins:wght=300;400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #FAF6F0; }
        
        /* Cabeçalho de Alta Confeitaria */
        .brand-header {
            background: linear-gradient(135deg, #043927 0%, #0B533A 100%);
            padding: 25px; border-radius: 15px; text-align: center;
            border-bottom: 4px solid #D4AF37; margin-bottom: 25px;
        }
        .brand-title { font-family: 'Playfair Display', serif; font-size: 36px; color: #FAF6F0; font-weight: 700; }
        .brand-subtitle { font-size: 13px; color: #E3C16F; letter-spacing: 2px; text-transform: uppercase; }
        
        /* Estilo dos Títulos de Seções */
        .section-title { font-family: 'Playfair Display', serif; color: #043927; font-size: 22px; border-left: 4px solid #D4AF37; padding-left: 12px; margin-top: 20px; margin-bottom: 15px; }
        
        /* Caixas de Estilo Visual */
        .print-box { background: white; border: 1px solid #ced4da; padding: 20px; border-radius: 10px; font-family: monospace; color: black; line-height: 1.4; }
        .lupa-box { border: 3px solid black; background: white; color: black; padding: 10px; font-weight: bold; text-align: center; font-size: 14px; margin-bottom: 10px; font-family: Arial, sans-serif; }
        .preco-box { background: #043927; color: #FAF6F0; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #D4AF37; }
        .alerta-aniv { background: #FAF0F2; border-left: 5px solid #D4AF37; padding: 12px; border-radius: 4px; margin-bottom: 15px; }
        
        .safety-alert-box {
            background-color: #FFF5F5;
            border-left: 6px solid #E53E3E;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            color: #C53030;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div class="brand-title">K&G Arte em Confeitaria</div>
        <div class="brand-subtitle">💎 Sistema ERP & CRM Integrado de Alta Confeitaria & Salgados 💎</div>
    </div>
""", unsafe_allow_html=True)

def limpar_e_converter_coluna(df, coluna, padrao=0.0):
    if df is None or df.empty or coluna not in df.columns:
        return pd.Series([padrao] * (len(df) if df is not None else 1))
    try:
        serie_str = df[coluna].astype(str).str.replace(',', '.', regex=False).str.strip()
        return pd.to_numeric(serie_str, errors='coerce').fillna(padrao)
    except Exception:
        return pd.Series([padrao] * len(df))

def corrigir_colunas_df(df):
    if df is None:
        return pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"])
    
    mapeamento = {
        "Gramos Usados na Receita": "Qtd Usada",
        "Gramos Embalagem (g)": "Qtd na Embalagem",
        "Qtd Usada na Receita": "Qtd Usada",
        "Quantidade Usada": "Qtd Usada",
        "Qtd na Embalagem (g/ml/un)": "Qtd na Embalagem",
        "Preço Embalagem (R$)": "Preço Embalagem (R$)"
    }
    df_corrigido = df.rename(columns=mapeamento)
    
    colunas_obrigatorias = ["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]
    for col in colunas_obrigatorias:
        if col not in df_corrigido.columns:
            if col == "Ingrediente":
                df_corrigido[col] = "Novo Insumo"
            elif col == "Unidade":
                df_corrigido[col] = "g"
            elif col == "Qtd na Embalagem":
                df_corrigido[col] = 1000.0
            else:
                df_corrigido[col] = 0.0
                
    df_corrigido["Ingrediente"] = df_corrigido["Ingrediente"].fillna("Novo Insumo")
    df_corrigido["Qtd Usada"] = pd.to_numeric(df_corrigido["Qtd Usada"], errors='coerce').fillna(0.0)
    df_corrigido["Unidade"] = df_corrigido["Unidade"].fillna("g")
    df_corrigido["Qtd na Embalagem"] = pd.to_numeric(df_corrigido["Qtd na Embalagem"], errors='coerce').fillna(1000.0)
    df_corrigido["Preço Embalagem (R$)"] = pd.to_numeric(df_corrigido["Preço Embalagem (R$)"], errors='coerce').fillna(0.0)
                
    return df_corrigido[colunas_obrigatorias]

config_colunas_ingredientes = {}
if hasattr(st, "column_config"):
    try:
        config_colunas_ingredientes = {
            "Ingrediente": st.column_config.TextColumn(
                "🧁 Ingrediente / Insumo",
                placeholder="Ex: Farinha Venturelli",
                required=True,
                width="medium"
            ),
            "Qtd Usada": st.column_config.NumberColumn(
                "⚖️ Qtd Usada",
                placeholder="0.0",
                min_value=0.0,
                step=0.1,
                required=True,
                format="%.1f"
            ),
            "Unidade": st.column_config.SelectboxColumn(
                "📏 Unidade",
                options=["g", "ml", "un"],
                required=True,
                default="g"
            ),
            "Qtd na Embalagem": st.column_config.NumberColumn(
                "📦 Qtd Embalagem",
                placeholder="1000",
                min_value=0.1,
                step=1.0,
                required=True,
                format="%.1f"
            ),
            "Preço Embalagem (R$)": st.column_config.NumberColumn(
                "💰 Preço Embalagem",
                placeholder="0.00",
                min_value=0.0,
                step=0.01,
                required=True,
                format="R$ %.2f"
            )
        }
    except Exception:
        config_colunas_ingredientes = {}

def calcular_peso_bruto_ingredientes(df):
    if df is None or df.empty:
        return 0.0
    try:
        df_temp = corrigir_colunas_df(df)
        df_temp = df_temp.dropna(subset=["Ingrediente"])
        df_temp = df_temp[df_temp["Ingrediente"].astype(str).str.strip() != ""]
        
        if df_temp.empty:
            return 0.0
            
        usados = limpar_e_converter_coluna(df_temp, "Qtd Usada", 0.0)
        total_g = 0.0
        
        for idx, row in df_temp.iterrows():
            qtd = float(usados.iloc[idx])
            unidade = str(row.get("Unidade", "g")).strip().lower()
            ingrediente = str(row.get("Ingrediente", "")).lower()
            
            if unidade == 'un':
                if "ovo" in ingrediente:
                    total_g += qtd * 50.0  
                elif "leite condensado" in ingrediente:
                    total_g += qtd * 395.0 
                elif "creme de leite" in ingrediente:
                    total_g += qtd * 200.0 
                else:
                    total_g += qtd * 1.0    
            else:
                total_g += qtd
        return total_g
    except Exception:
        return 0.0

def calcular_custo_tabela_seguro(df, col_preco, col_embalagem, col_usado):
    if df is None or df.empty:
        return 0.0
    try:
        df_temp = corrigir_colunas_df(df)
        df_temp = df_temp.dropna(subset=["Ingrediente"])
        df_temp = df_temp[df_temp["Ingrediente"].astype(str).str.strip() != ""]
            
        if df_temp.empty:
            return 0.0
            
        precos = limpar_e_converter_coluna(df_temp, col_preco, 0.0)
        embalagens = limpar_e_converter_coluna(df_temp, col_embalagem, 1.0)
        usados = limpar_e_converter_coluna(df_temp, col_usado, 0.0)
        
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

def salvar_dados_disco():
    try:
        if 'banco_massas_rec' in st.session_state:
            backup_dict = {
                "massas": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"], "perda_coccao": v.get("perda_coccao", 10.0)} for k, v in st.session_state['banco_massas_rec'].items()},
                "recheios": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"], "perda_coccao": v.get("perda_coccao", 15.0)} for k, v in st.session_state['banco_recheios_rec'].items()},
                "caldas": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"]} for k, v in st.session_state['banco_caldas_rec'].items()},
                "coberturas": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"]} for k, v in st.session_state['banco_coberturas_rec'].items()},
                "crm": st.session_state['banco_crm'].to_dict(orient="records") if 'banco_crm' in st.session_state else [],
                "fixos": st.session_state['df_fixos'].to_dict(orient="records") if 'df_fixos' in st.session_state else [],
                "var": st.session_state['df_var'].to_dict(orient="records") if 'df_var' in st.session_state else [],
                "decoracao": st.session_state.get('decoracao_bolo_completo', '')
            }
            with open("banco_confeitaria_local.json", "w", encoding="utf-8") as f:
                json.dump(backup_dict, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

def carregar_dados_disco():
    if os.path.exists("banco_confeitaria_local.json"):
        try:
            with open("banco_confeitaria_local.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not data.get("massas"):
                return False

            st.session_state['banco_massas_rec'] = {
                k: {
                    "ingredientes": pd.DataFrame(v["ingredientes"]),
                    "peso_obtido": v["peso_obtido"],
                    "preparo": v["preparo"],
                    "perda_coccao": v.get("perda_coccao", 10.0)
                } for k, v in data["massas"].items()
            }
            st.session_state['banco_recheios_rec'] = {
                k: {
                    "ingredientes": pd.DataFrame(v["ingredientes"]),
                    "peso_obtido": v["peso_obtido"],
                    "preparo": v["preparo"],
                    "perda_coccao": v.get("perda_coccao", 15.0)
                } for k, v in data["recheios"].items()
            }
            st.session_state['banco_caldas_rec'] = {
                k: {
                    "ingredientes": pd.DataFrame(v["ingredientes"]),
                    "peso_obtido": v["peso_obtido"],
                    "preparo": v["preparo"]
                } for k, v in data["caldas"].items()
            }
            st.session_state['banco_coberturas_rec'] = {
                k: {
                    "ingredientes": pd.DataFrame(v["ingredientes"]),
                    "peso_obtido": v["peso_obtido"],
                    "preparo": v["preparo"]
                } for k, v in data["coberturas"].items()
            }
            st.session_state['banco_crm'] = pd.DataFrame(data["crm"])
            st.session_state['df_fixos'] = pd.DataFrame(data["fixos"])
            st.session_state['df_var'] = pd.DataFrame(data["var"])
            st.session_state['decoracao_bolo_completo'] = data["decoracao"]
            return True
        except Exception:
            pass
    return False

def exportar_backup_json():
    try:
        backup_dict = {
            "massas": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"], "perda_coccao": v.get("perda_coccao", 10.0)} for k, v in st.session_state['banco_massas_rec'].items()},
            "recheios": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"], "perda_coccao": v.get("perda_coccao", 15.0)} for k, v in st.session_state['banco_recheios_rec'].items()},
            "caldas": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"]} for k, v in st.session_state['banco_caldas_rec'].items()},
            "coberturas": {k: {"ingredientes": v["ingredientes"].to_dict(orient="records"), "peso_obtido": v["peso_obtido"], "preparo": v["preparo"]} for k, v in st.session_state['banco_coberturas_rec'].items()},
            "crm": st.session_state['banco_crm'].to_dict(orient="records") if 'banco_crm' in st.session_state else [],
            "fixos": st.session_state['df_fixos'].to_dict(orient="records") if 'df_fixos' in st.session_state else [],
            "var": st.session_state['df_var'].to_dict(orient="records") if 'df_var' in st.session_state else [],
            "decoracao": st.session_state.get('decoracao_bolo_completo', '')
        }
        return json.dumps(backup_dict, ensure_ascii=False, indent=4)
    except Exception:
        return ""

def importar_backup_json(json_str):
    try:
        data = json.loads(json_str)
        st.session_state['banco_massas_rec'] = {
            k: {
                "ingredientes": pd.DataFrame(v["ingredientes"]),
                "peso_obtido": v["peso_obtido"],
                "preparo": v["preparo"],
                "perda_coccao": v.get("perda_coccao", 10.0)
            } for k, v in data["massas"].items()
        }
        st.session_state['banco_recheios_rec'] = {
            k: {
                "ingredientes": pd.DataFrame(v["ingredientes"]),
                "peso_obtido": v["peso_obtido"],
                "preparo": v["preparo"],
                "perda_coccao": v.get("perda_coccao", 15.0)
            } for k, v in data["recheios"].items()
        }
        st.session_state['banco_caldas_rec'] = {
            k: {
                "ingredientes": pd.DataFrame(v["ingredientes"]),
                "peso_obtido": v["peso_obtido"],
                "preparo": v["preparo"]
            } for k, v in data["caldas"].items()
        }
        st.session_state['banco_coberturas_rec'] = {
            k: {
                "ingredientes": pd.DataFrame(v["ingredientes"]),
                "peso_obtido": v["peso_obtido"],
                "preparo": v["preparo"]
            } for k, v in data["coberturas"].items()
        }
        st.session_state['banco_crm'] = pd.DataFrame(data["crm"])
        st.session_state['df_fixos'] = pd.DataFrame(data["fixos"])
        st.session_state['df_var'] = pd.DataFrame(data["var"])
        st.session_state['decoracao_bolo_completo'] = data["decoracao"]
        salvar_dados_disco()
        return True
    except Exception:
        return False

def renderizar_tabela_segura(df_dados, col_config_dict, chave_unica):
    df_dados_corrigido = corrigir_colunas_df(df_dados)
    if hasattr(st, "data_editor"):
        if col_config_dict and len(col_config_dict) > 0:
            return st.data_editor(
                df_dados_corrigido,
                num_rows="dynamic",
                use_container_width=True,
                column_config=col_config_dict,
                key=chave_unica
            )
        else:
            return st.data_editor(
                df_dados_corrigido,
                num_rows="dynamic",
                use_container_width=True,
                key=chave_unica
            )
    else:
        return st.data_editor(df_dados_corrigido, num_rows="dynamic", use_container_width=True, key=chave_unica)

chave_usuario = st.text_input("Insira a sua Chave de Acesso para liberar o sistema:", type="password")

if chave_usuario == "kg10k":
    st.success("Acesso Autorizado! Seja bem-vinda de volta, Karyn.")
    
    st.markdown("""
        <div class="safety-alert-box">
            <b>⚠️ MEDIDA DE SEGURANÇA SUPREMA K&G:</b><br>
            Sempre que finalizar um novo cadastro de receita ou cliente, clique no botão <b>'💾 Baixar Backup de Segurança'</b> na barra lateral para salvar sua planilha física no seu celular ou computador!
        </div>
    """, unsafe_allow_html=True)

    dados_carregados = carregar_dados_disco()

    if not dados_carregados or 'banco_massas_rec' not in st.session_state or len(st.session_state.get('banco_massas_rec', {})) == 0:
        st.session_state['banco_massas_rec'] = {
            "Massa Branca MBL (Camila Ayana)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 4.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Óleo de Soja Liza", "Qtd Usada": 150.0, "Unidade": "g", "Qtd na Embalagem": 900.0, "Preço Embalagem (R$)": 7.50},
                    {"Ingrediente": "Leite Integral", "Qtd Usada": 150.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20},
                    {"Ingrediente": "Iogurte Natural Batavo", "Qtd Usada": 170.0, "Unidade": "g", "Qtd na Embalagem": 170.0, "Preço Embalagem (R$)": 3.20},
                    {"Ingrediente": "Leite Ninho Pó", "Qtd Usada": 30.0, "Unidade": "g", "Qtd na Embalagem": 380.0, "Preço Embalagem (R$)": 16.50},
                    {"Ingrediente": "Açúcar Refinado União", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Farinha de Trigo Venturelli", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Fermento Químico", "Qtd Usada": 18.0, "Unidade": "g", "Qtd na Embalagem": 100.0, "Preço Embalagem (R$)": 6.00}
                ]),
                "peso_obtido": 950.0,
                "preparo": "No liquidificador, adicione os ovos, o óleo de soja, o leite integral, o iogurte natural, o leite Ninho em pó e o açúcar refinado. Bata em velocidade média-alta por um período de 2 a 5 minutos até obter uma emulsão perfeitamente lisa, esbranquiçada e sem grânulos de açúcar. Transfira a mistura líquida para um bowl de inox. Peneire a farinha de trigo Venturelli diretamente sobre os líquidos em três etapas, misturando delicadamente com o fouet de dentro para fora para evitar o desenvolvimento excessivo de glúten. Adicione o fermento químico por último, incorporando-o de forma homogênea com movimentos suaves. Distribua em formas untadas ou com papel manteiga no fundo e asse em forno turbo pré-aquecido a 180°C por aproximadamente 35 a 40 minutos.",
                "perda_coccao": 10.0
            },
            "Massa de Chocolate MBL (Camila Ayana)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 4.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Óleo de Soja Liza", "Qtd Usada": 150.0, "Unidade": "g", "Qtd na Embalagem": 900.0, "Preço Embalagem (R$)": 7.50},
                    {"Ingrediente": "Leite Integral", "Qtd Usada": 220.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20},
                    {"Ingrediente": "Creme de Leite Itambé", "Qtd Usada": 200.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.80},
                    {"Ingrediente": "Chocolate 50% Melken", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 1050.0, "Preço Embalagem (R$)": 42.00},
                    {"Ingrediente": "Açúcar Refinado União", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Farinha de Trigo Venturelli", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Fermento Químico", "Qtd Usada": 18.0, "Unidade": "g", "Qtd na Embalagem": 100.0, "Preço Embalagem (R$)": 6.00}
                ]),
                "peso_obtido": 1100.0,
                "preparo": "Adicione os ovos, o óleo, o leite integral, o creme de leite Itambé, o chocolate em pó 50% Melken e o açúcar no liquidificador. Processe por 3 minutos na velocidade máxima até dissolver completamente o chocolate em pó e homogeneizar as gorduras. Verta o creme em um bowl grande. Peneire a farinha Venturelli sobre a mistura, mexendo com o fouet apenas até homogeneizar. Adicione o fermento e incorpore-o com cuidado. Asse a 180°C em forno convencional ou 160°C em forno de convecção por 38 minutos.",
                "perda_coccao": 10.0
            },
            "Massa Cacau Black MBL": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 4.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Óleo de Soja Liza", "Qtd Usada": 150.0, "Unidade": "g", "Qtd na Embalagem": 900.0, "Preço Embalagem (R$)": 7.50},
                    {"Ingrediente": "Leite Integral", "Qtd Usada": 220.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20},
                    {"Ingrediente": "Creme de Leite", "Qtd Usada": 200.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.80},
                    {"Ingrediente": "Cacau em Pó Black", "Qtd Usada": 70.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 52.00},
                    {"Ingrediente": "Açúcar Refinado União", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Farinha de Trigo Venturelli", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Fermento Químico", "Qtd Usada": 18.0, "Unidade": "g", "Qtd na Embalagem": 100.0, "Preço Embalagem (R$)": 6.00}
                ]),
                "peso_obtido": 1050.0,
                "preparo": "Misture no liquidificador todos os líquidos, o cacau em pó black e o açúcar. Processe por 3 minutos. Incorpore a farinha de trigo peneirada no bowl delicadamente usando o fouet para evitar que a massa fique pesada e perca o ponto aerado. Finalize com o fermento químico em pó. Transfira para formas de fundo falso e asse a 170°C para preservar a umidade natural do cacau alcalino black.",
                "perda_coccao": 10.0
            },
            "Massa Red Velvet MBL (Camila Ayana)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 4.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Óleo de Soja Liza", "Qtd Usada": 150.0, "Unidade": "g", "Qtd na Embalagem": 900.0, "Preço Embalagem (R$)": 7.50},
                    {"Ingrediente": "Leite Integral (buttermilk)", "Qtd Usada": 150.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20},
                    {"Ingrediente": "Suco de Limão", "Qtd Usada": 20.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 6.00},
                    {"Ingrediente": "Iogurte Natural Batavo", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 170.0, "Preço Embalagem (R$)": 3.20},
                    {"Ingrediente": "Chocolate em Pó 50%", "Qtd Usada": 30.0, "Unidade": "g", "Qtd na Embalagem": 1050.0, "Preço Embalagem (R$)": 42.00},
                    {"Ingrediente": "Corante Vermelho Morango", "Qtd Usada": 5.0, "Unidade": "g", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 9.50},
                    {"Ingrediente": "Pasta Saborizante Frutas", "Qtd Usada": 15.0, "Unidade": "g", "Qtd na Embalagem": 250.0, "Preço Embalagem (R$)": 68.00},
                    {"Ingrediente": "Açúcar Refinado União", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Farinha de Trigo Venturelli", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Fermento Químico", "Qtd Usada": 18.0, "Unidade": "g", "Qtd na Embalagem": 100.0, "Preço Embalagem (R$)": 6.00}
                ]),
                "peso_obtido": 1000.0,
                "preparo": "Preparo do Buttermilk: Adicione os 20 g de suco de limão ao leite integral morno. Deixe descansar por 10 minutos até talhar completamente. No liquidificador, bata os ovos, o óleo de soja, o buttermilk preparado, o iogurte natural, o chocolate em pó, o corante gel vermelho morango, a pasta de frutas silvestres e o açúcar por 4 minutos até obter uma cor homogênea e brilhante. Transfira a emulsão para um bowl e incorpore a farinha peneirada, misturando de baixo para cima com cuidado. Adicione o fermento químico. Asse a 170°C em assadeiras baixas para obter discos planos perfeitos.",
                "perda_coccao": 10.0
            },
            "Massa Cookie Base": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Margarina Primor Pro", "Qtd Usada": 225.0, "Unidade": "g", "Qtd na Embalagem": 3000.0, "Preço Embalagem (R$)": 42.00},
                    {"Ingrediente": "Açúcar Mascavo", "Qtd Usada": 180.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 14.50},
                    {"Ingrediente": "Açúcar Refinado", "Qtd Usada": 180.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 3.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Leite Ninho Pó", "Qtd Usada": 75.0, "Unidade": "g", "Qtd na Embalagem": 380.0, "Preço Embalagem (R$)": 16.50},
                    {"Ingrediente": "Farinha de Trigo Premium", "Qtd Usada": 420.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Fermento Químico", "Qtd Usada": 12.0, "Unidade": "g", "Qtd na Embalagem": 100.0, "Preço Embalagem (R$)": 6.00},
                    {"Ingrediente": "Gotas de Chocolate Sicao", "Qtd Usada": 450.0, "Unidade": "g", "Qtd na Embalagem": 1010.0, "Preço Embalagem (R$)": 49.00}
                ]),
                "peso_obtido": 1500.0,
                "preparo": "Na batedeira equipada com a espátula tipo leque/raquete, bata a margarina Primor Pro (em ponto de pomada, por volta de 20°C) com o açúcar mascavo e o açúcar refinado até formar um creme fofo e claro. Adicione os ovos um a um, batendo bem após cada adição para emulsionar a massa. Desligue a batedeira e peneire a farinha de trigo, o leite Ninho e o fermento por cima do creme amanteigado. Misture em velocidade mínima por apenas 30 segundos ou até a farinha sumir (não bata para não desenvolver glúten). Despeje as gotas de chocolate Sicao e misture com uma espátula de silicone dura. Leve a massa à geladeira por pelo menos 2 horas antes de porcionar e assar. Asse a 180°C por 12 a 15 minutos (o centro deve continuar macio).",
                "perda_coccao": 10.0
            },
            "Massa de Brownie (Nescau)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Margarina Primor Pro", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 3000.0, "Preço Embalagem (R$)": 42.00},
                    {"Ingrediente": "Açúcar Refinado União", "Qtd Usada": 500.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 6.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Água Filtrada", "Qtd Usada": 150.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00},
                    {"Ingrediente": "Achocolatado Nescau", "Qtd Usada": 670.0, "Unidade": "g", "Qtd na Embalagem": 1500.0, "Preço Embalagem (R$)": 21.00},
                    {"Ingrediente": "Farinha de Trigo Premium", "Qtd Usada": 450.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50}
                ]),
                "peso_obtido": 2000.0,
                "preparo": "Na batedeira equipada com o batedor globo, bata os ovos inteiros e o açúcar refinado em velocidade máxima por cerca de 5 minutos até dobrar de volume e formar uma espuma firme e clara. Derreta a margarina Primor Pro junto com os 150 ml de água e adicione-os morno-frios na batedeira sob velocidade mínima. Desligue a batedeira e troque para o batedor de raquete. Adicione o achocolatado Nescau e a farinha de trigo peneirada. Bata apenas até incorporar. Espalhe a massa pesada em assadeira forrada com papel manteiga. Asse a 180°C por 25 minutos. O topo deve estar com uma casquinha craquelada brilhante e o centro ligeiramente úmido.",
                "perda_coccao": 15.0
            },
            "Massa Salgados de Forno (Batata)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Farinha de Trigo Premium", "Qtd Usada": 900.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Batata Asterix Cozida", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 7.50},
                    {"Ingrediente": "Açúcar Refinado", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Margarina Qualy", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 3.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Sal Refinado", "Qtd Usada": 15.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 3.00},
                    {"Ingrediente": "Lecitina de Soja Líquida", "Qtd Usada": 10.0, "Unidade": "g", "Qtd na Embalagem": 250.0, "Preço Embalagem (R$)": 18.50},
                    {"Ingrediente": "Melhorador Platinum", "Qtd Usada": 10.0, "Unidade": "g", "Qtd na Embalagem": 300.0, "Preço Embalagem (R$)": 14.50},
                    {"Ingrediente": "Açúcar Invertido", "Qtd Usada": 25.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 12.00},
                    {"Ingrediente": "Fermento Biológico Seco", "Qtd Usada": 20.0, "Unidade": "g", "Qtd na Embalagem": 100.0, "Preço Embalagem (R$)": 9.50},
                    {"Ingrediente": "Água Morna", "Qtd Usada": 250.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00}
                ]),
                "peso_obtido": 1850.0,
                "preparo": "Descasque e cozinhe as batatas Asterix até estarem muito macias. Esprema-as ainda quentes e espere esfriar completamente. Em um bowl, dilua o fermento biológico seco e o açúcar refinado na água morna (temperatura controlada a máximo 35°C). Deixe descansar por 5 minutos para ativar. Adicione a batata espremida, a margarina Qualy, os ovos, o açúcar invertido, a lecitina de soja líquida e o melhorador de farinha Platinum. Misture tudo. Adicione a farinha de trigo Premium peneirada em três partes. No meio do processo, adicione o sal refinado (nunca adicione o sal diretamente sobre o fermento ativo). Sove a massa vigorosamente em bancada de mármore por cerca de 12 minutos até desenvolver a rede de glúten (ponto de véu fino). Boleie a massa, cubra com filme plástico e deixe fermentar até dobrar de volume (aproximadamente 45 minutos em temperatura ambiente).",
                "perda_coccao": 5.0
            },
            "Massa Quiche e Empadão (Patê Brisée)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Farinha de Trigo Premium", "Qtd Usada": 1000.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Margarina Qualy (Ponto Pomada)", "Qtd Usada": 600.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 16.00},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 2.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Sal Refinado", "Qtd Usada": 10.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 3.00}
                ]),
                "peso_obtido": 1600.0,
                "preparo": "Em um bowl higienizado, coloque a farinha de trigo peneirada, o sal refinado e a margarina Qualy em consistência de pomada. Com as pontas dos dedos, faça um processo de 'sablage' (esfregar a margarina na farinha) até obter uma textura que se assemelha a uma areia grossa e úmida. Não sove! Adicione os ovos ligeiramente batidos e misture a massa apertando-a contra as paredes do bowl apenas até que ela se aglutine e forme uma bola homogênea. Envolva em filme plástico e refrigere por no mínimo 1 hora antes de abrir nas formas.",
                "perda_coccao": 3.0
            }
        }

    if not dados_carregados or 'banco_recheios_rec' not in st.session_state or len(st.session_state.get('banco_recheios_rec', {})) == 0:
        st.session_state['banco_recheios_rec'] = {
            "Base Branca Coringa": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Leite Condensado Piracanjuba", "Qtd Usada": 395.0, "Unidade": "g", "Qtd na Embalagem": 395.0, "Preço Embalagem (R$)": 6.50},
                    {"Ingrediente": "Creme de Leite Piracanjuba", "Qtd Usada": 600.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.80},
                    {"Ingrediente": "Chocolate Branco (LeCacau)", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 1010.0, "Preço Embalagem (R$)": 45.00},
                    {"Ingrediente": "Leite Integral", "Qtd Usada": 100.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20}
                ]),
                "peso_obtido": 1015.0,
                "preparo": "Em uma panela de fundo triplo de aço inox, adicione o leite condensado Piracanjuba e o chocolate branco picado. Misture bem até diluir um pouco o chocolate. Adicione o creme de leite e o leite integral. Mexa tudo a frio até homogeneizar. Leve ao fogo médio-baixo, mexendo constantemente em movimentos de '8' com um batedor de silicone. Cozinhe até o ponto desejado: Ponto de Copo/Fatia Macia (temperatura interna de 98°C) ou Ponto de Recheio Firme (100,5°C a 101°C). Desligue o fogo e bata vigorosamente o recheio com o fouet de inox por 1 minuto para emulsificar a gordura e garantir brilho. Cubra com filme plástico em contato direto.",
                "perda_coccao": 15.0
            },
            "Base Preta Coringa": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Leite Condensado Piracanjuba", "Qtd Usada": 395.0, "Unidade": "g", "Qtd na Embalagem": 395.0, "Preço Embalagem (R$)": 6.50},
                    {"Ingrediente": "Creme de Leite Piracanjuba", "Qtd Usada": 600.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.80},
                    {"Ingrediente": "Chocolate Meio Amargo (LeCacau)", "Qtd Usada": 100.0, "Unidade": "g", "Qtd na Embalagem": 1010.0, "Preço Embalagem (R$)": 46.00},
                    {"Ingrediente": "Chocolate 50% Melken", "Qtd Usada": 50.0, "Unidade": "g", "Qtd na Embalagem": 1050.0, "Preço Embalagem (R$)": 42.00},
                    {"Ingrediente": "Leite Integral", "Qtd Usada": 150.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20}
                ]),
                "peso_obtido": 1058.0,
                "preparo": "Misture o leite condensado com o chocolate em pó 50% Melken até dissolver os grânulos secos na panela fria. Adicione o creme de leite, o chocolate meio amargo LeCacau picado e o leite integral. Cozinhe em fogo médio-alto no início, reduzindo para fogo médio quando começar a ferver. Retire ao atingir o ponto de blocos firmes (100,5°C). Bata com fouet após apagar o fogo. Cubra com filme plástico em contato e reserve.",
                "perda_coccao": 15.0
            },
            "Geleia de Morango (Especial)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Morangos Congelados CEASA", "Qtd Usada": 1000.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 24.00},
                    {"Ingrediente": "Açúcar Cristal União", "Qtd Usada": 400.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 4.90},
                    {"Ingrediente": "Pasta Saborizante Frutas", "Qtd Usada": 30.0, "Unidade": "g", "Qtd na Embalagem": 250.0, "Preço Embalagem (R$)": 68.00},
                    {"Ingrediente": "Suco de Limão Espremido", "Qtd Usada": 100.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 6.00},
                    {"Ingrediente": "Água Filtrada", "Qtd Usada": 500.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00}
                ]),
                "peso_obtido": 1421.0,
                "preparo": "Em uma panela de aço inox média, coloque os morangos congelados inteiros, o açúcar cristal e a água filtrada. Leve ao fogo médio e deixe os morangos cozinharem. Quando começar a reduzir, adicione o suco de limão filtrado para ativar a pectina natural. Deixe cozinhar em fogo baixo por cerca de 30 minutos ou até que o líquido atinja consistência de xarope espesso. Adicione a pasta saborizante de frutas silvestres e misture bem. Passe o mixer de mão rapidamente para quebrar os pedaços grandes, mantendo uma textura pedaçuda de geleia rústica. Esfrie e refrigere.",
                "perda_coccao": 30.0
            },
            "Gelatto de Ninho": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Manteiga sem Sal Itambé", "Qtd Usada": 200.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 12.50},
                    {"Ingrediente": "Leite Ninho Pó", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 380.0, "Preço Embalagem (R$)": 16.50},
                    {"Ingrediente": "Creme de Leite Gelado", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.80},
                    {"Ingrediente": "Leite Condensado Gelado", "Qtd Usada": 395.0, "Unidade": "g", "Qtd na Embalagem": 395.0, "Preço Embalagem (R$)": 6.50},
                    {"Ingrediente": "Emulsificante de Sorvete", "Qtd Usada": 8.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 11.00}
                ]),
                "peso_obtido": 1100.0,
                "preparo": "O creme de leite e o leite condensado devem estar sob refrigeração a 4°C por no mínimo 12 horas. A manteiga deve estar em temperatura ambiente macia (22°C). Na batedeira equipada com o batedor globo, adicione a manteiga sem sal e o leite condensado gelado. Bata em velocidade média-alta por 5 minutos até virar um creme esbranquiçado. Adicione o leite Ninho em pó peneirado em duas etapas, batendo em velocidade baixa apenas para incorporar. Adicione o creme de leite gelado e o emulsificante para sorvete. Aumente para a velocidade máxima e bata por exatos 4 minutos. O creme vai expandir e virar um mousse brilhante, leve e ultra aveludado.",
                "perda_coccao": 0.0
            },
            "Recheio Frango Cremoso (Coxinha)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Peito de Frango (Sassami)", "Qtd Usada": 715.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 18.00},
                    {"Ingrediente": "Margarina Qualy", "Qtd Usada": 75.0, "Unidade": "g", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Azeite de Oliva", "Qtd Usada": 7.0, "Unidade": "ml", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 28.00},
                    {"Ingrediente": "Molho de Tomate", "Qtd Usada": 120.0, "Unidade": "g", "Qtd na Embalagem": 340.0, "Preço Embalagem (R$)": 4.50},
                    {"Ingrediente": "Requeijão Crioulo", "Qtd Usada": 75.0, "Unidade": "g", "Qtd na Embalagem": 400.0, "Preço Embalagem (R$)": 12.00},
                    {"Ingrediente": "Água de Cozimento", "Qtd Usada": 250.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00}
                ]),
                "peso_obtido": 1068.0,
                "preparo": "Na panela de pressão, cozinhe o peito de frango Sassami com água e sal por 15 minutos. Escorra a água, reservando 250 ml para temperar, e balance a panela fechada com força para desfiar. Em uma panela de fundo triplo, derreta a margarina Qualy com o azeite de oliva. Refogue cebola e alho picados muito finos. Adicione o frango desfiado e frite até dourar. Junte o molho de tomate e os 250 ml de água de cozimento. Deixe reduzir até secar. Desligue o fogo e misture o requeijão Crioulo para dar cremosidade (deve ficar úmido, porém firme). Esfrie completamente antes de usar.",
                "perda_coccao": 10.0
            },
            "Recheio Costela Cremosa": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Costela Desfiada", "Qtd Usada": 940.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 26.00},
                    {"Ingrediente": "Água da Costela", "Qtd Usada": 250.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00},
                    {"Ingrediente": "Molho Madeira Predilecta", "Qtd Usada": 300.0, "Unidade": "g", "Qtd na Embalagem": 340.0, "Preço Embalagem (R$)": 9.50},
                    {"Ingrediente": "Requeijão Catupiry Original", "Qtd Usada": 80.0, "Unidade": "g", "Qtd na Embalagem": 1500.0, "Preço Embalagem (R$)": 59.90},
                    {"Ingrediente": "Molho Barbecue", "Qtd Usada": 30.0, "Unidade": "g", "Qtd na Embalagem": 400.0, "Preço Embalagem (R$)": 11.50},
                    {"Ingrediente": "Farinha de Trigo", "Qtd Usada": 50.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 8.50},
                    {"Ingrediente": "Água Pura", "Qtd Usada": 400.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00}
                ]),
                "peso_obtido": 1900.0,
                "preparo": "O peito de costela bovina deve ser previamente cozido na pressão por 45 minutos e desfiado completamente, limpando toda e qualquer gordura excessiva. Em uma panela, coloque a costela bovina desfiada, os 250 ml de água de cozimento, o molho madeira e o barbecue. Dissolva os 50 g de farinha de trigo nos 400 ml de água fria pura. Adicione à panela sob fogo médio-baixo, mexendo constantemente até cozinhar o amido e virar um creme encorpado. Adicione o Catupiry original por último e misture. Deixe ferver por mais 3 minutos.",
                "perda_coccao": 5.0
            },
            "Creme Base das Quiches (Royal)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Leite Integral", "Qtd Usada": 300.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.20},
                    {"Ingrediente": "Ricota Fresca", "Qtd Usada": 250.0, "Unidade": "g", "Qtd na Embalagem": 250.0, "Preço Embalagem (R$)": 8.90},
                    {"Ingrediente": "Creme de Leite Itambé", "Qtd Usada": 400.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 3.80},
                    {"Ingrediente": "Ovos Frescos", "Qtd Usada": 4.0, "Unidade": "un", "Qtd na Embalagem": 30.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Sal Refinado", "Qtd Usada": 8.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 3.00}
                ]),
                "peso_obtido": 1158.0,
                "preparo": "No liquidificador, quebre os ovos um a um. Adicione a ricota fresca esfarelada, o creme de leite Itambé, o leite integral e o sal refinado. Processe em velocidade máxima por exatos 2 minutos até dissolver completamente todos os pedacinhos da ricota e emulsificar os ovos nos laticínios. Verta diretamente sobre a base de quiche já montada com a massa Brisée e o recheio de sua preferência. Asse a 180°C até coagular.",
                "perda_coccao": 0.0
            }
        }

    if not dados_carregados or 'banco_caldas_rec' not in st.session_state or len(st.session_state.get('banco_caldas_rec', {})) == 0:
        st.session_state['banco_caldas_rec'] = {
            "Calda Glaciada Exclusiva": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Glaçúcar União", "Qtd Usada": 500.0, "Unidade": "g", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 6.50},
                    {"Ingrediente": "Água Fervente", "Qtd Usada": 750.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00}
                ]),
                "peso_obtido": 1200.0,
                "preparo": "Em um recipiente de plástico com bico dosador ou jarra graduada resistente ao calor, coloque os 500 g de açúcar de confeiteiro Glaçúcar União peneirado. Ferva os 750 ml de água filtrada a 100°C. Verta a água fervente imediatamente sobre o Glaçúcar e mexa vigorosamente com o fouet até que todos os cristais estejam completamente diluídos. Espere esfriar e utilize."
            },
            "Calda de Leite de Coco MBL": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Leite Condensado", "Qtd Usada": 395.0, "Unidade": "g", "Qtd na Embalagem": 395.0, "Preço Embalagem (R$)": 6.50},
                    {"Ingrediente": "Leite de Coco Sococo", "Qtd Usada": 500.0, "Unidade": "ml", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 11.00},
                    {"Ingrediente": "Água Filtrada", "Qtd Usada": 1000.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 0.00}
                ]),
                "peso_obtido": 1857.0,
                "preparo": "Em uma panela pequena, coloque o leite de coco Sococo e a água filtrada. Leve ao fogo médio e espere ferver por exatos 3 minutos (esse processo de fervura do leite de coco prolonga consideravelmente a validade do bolo montado). Retire do fogo e misture imediatamente o leite condensado, misturando bem até homogeneizar por completo. Mantenha sob refrigeração."
            }
        }

    if not dados_carregados or 'banco_coberturas_rec' not in st.session_state or len(st.session_state.get('banco_coberturas_rec', {})) == 0:
        st.session_state['banco_coberturas_rec'] = {
            "Chantininho Estruturado": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Chantilly Supreme Amélia", "Qtd Usada": 1000.0, "Unidade": "ml", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 18.50},
                    {"Ingrediente": "Leite Ninho Pó", "Qtd Usada": 200.0, "Unidade": "g", "Qtd na Embalagem": 380.0, "Preço Embalagem (R$)": 16.50},
                    {"Ingrediente": "Emulsificante de Sorvete", "Qtd Usada": 15.0, "Unidade": "g", "Qtd na Embalagem": 200.0, "Preço Embalagem (R$)": 11.00},
                    {"Ingrediente": "Merengue Powder", "Qtd Usada": 20.0, "Unidade": "g", "Qtd na Embalagem": 150.0, "Preço Embalagem (R$)": 19.90}
                ]),
                "peso_obtido": 1235.0,
                "preparo": "O Chantilly Supreme Amélia deve estar extremamente gelado (4°C por 24 horas e no freezer por 15 minutos antes). Na batedeira equipada com o batedor globo, adicione o chantilly gelado, o leite Ninho em pó peneirado e o Merengue Powder. Misture levemente a seco com a batedeira desligada. Adicione o emulsificante de sorvete. Inicie o batimento em velocidade baixa por 1 minuto e aumente gradualmente para a velocidade média-alta. Bata até que o creme forme um buraco no meio da batedeira (ponto duro). Transfira para um bowl de plástico selado e deixe estabilizar na geladeira por 12 horas antes de hidratar e decorar."
            },
            "Merengue Suíço (Maçarico)": {
                "ingredientes": pd.DataFrame([
                    {"Ingrediente": "Clara de Ovos", "Qtd Usada": 90.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 22.00},
                    {"Ingrediente": "Açúcar Refinado União", "Qtd Usada": 140.0, "Unidade": "g", "Qtd na Embalagem": 1000.0, "Preço Embalagem (R$)": 5.40},
                    {"Ingrediente": "Açúcar Glaçúcar União", "Qtd Usada": 60.0, "Unidade": "g", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 6.50},
                    {"Ingrediente": "Amido de Milho Maizena", "Qtd Usada": 10.0, "Unidade": "g", "Qtd na Embalagem": 500.0, "Preço Embalagem (R$)": 7.50}
                ]),
                "peso_obtido": 300.0,
                "preparo": "Em um recipiente metálico ou de vidro limpo e isento de gorduras, misture as claras e o açúcar refinado União. Leve em banho-maria em fogo baixo, mexendo sem parar. A mistura deve atingir exatos 55°C a 60°C para pasteurizar as claras sem coagular a albumina. Se ao esfregar com os dedos não sentir grãos de açúcar, retire imediatamente. Coloque na batedeira com o batedor globo e bata em velocidade máxima por 10 minutos até o bowl esfriar e formar picos firmes. Peneire o Glaçúcar e o amido de milho Maizena diretamente sobre o merengue batido. Incorpore delicadamente com uma espátula de silicone em movimentos envolventes de baixo para cima."
            }
        }

    for r_nome in st.session_state['banco_massas_rec']:
        st.session_state['banco_massas_rec'][r_nome]["ingredientes"] = corrigir_colunas_df(st.session_state['banco_massas_rec'][r_nome]["ingredientes"])
    for r_nome in st.session_state['banco_recheios_rec']:
        st.session_state['banco_recheios_rec'][r_nome]["ingredientes"] = corrigir_colunas_df(st.session_state['banco_recheios_rec'][r_nome]["ingredientes"])
    for r_nome in st.session_state['banco_caldas_rec']:
        st.session_state['banco_caldas_rec'][r_nome]["ingredientes"] = corrigir_colunas_df(st.session_state['banco_caldas_rec'][r_nome]["ingredientes"])
    for r_nome in st.session_state['banco_coberturas_rec']:
        st.session_state['banco_coberturas_rec'][r_nome]["ingredientes"] = corrigir_colunas_df(st.session_state['banco_coberturas_rec'][r_nome]["ingredientes"])

    if 'banco_crm' not in st.session_state or st.session_state['banco_crm'] is None or st.session_state['banco_crm'].empty:
        st.session_state['banco_crm'] = pd.DataFrame([
            {"Cliente VIP": "Juliana Mendes Rossi", "WhatsApp": "(41) 99123-4567", "E-mail": "juliana@rossi.com", "Aniv. Cliente": "12/06", "Aniv. Marido": "18/10", "Aniv. Filhos": "Gabriel (04/02)", "Data Casamento": "22/11", "Restrições": "ALERGIA GRAVE A AMENDOIM!", "Últimos Pedidos": "KG-2026-1042"},
            {"Cliente VIP": "Carlos Henrique Rocha", "WhatsApp": "(41) 98877-6655", "E-mail": "carlos@rocha.com", "Aniv. Cliente": "29/08", "Aniv. Marido": "-", "Aniv. Filhos": "Sofia (15/05)", "Data Casamento": "-", "Restrições": "Sem cebola ou alho cru", "Últimos Pedidos": "KG-2026-8841"}
        ])

    if 'df_fixos' not in st.session_state or st.session_state['df_fixos'] is None or st.session_state['df_fixos'].empty:
        st.session_state['df_fixos'] = pd.DataFrame([
            {"Descrição do Custo Fixo": "Aluguel / Atelier", "Valor Mensal (R$)": 1500.00},
            {"Descrição do Custo Fixo": "Água e Energia Elétrica", "Valor Mensal (R$)": 650.00},
            {"Descrição do Custo Fixo": "Imposto MEI / DAS Nacional", "Valor Mensal (R$)": 75.00},
            {"Descrição do Custo Fixo": "Internet e Plataformas", "Valor Mensal (R$)": 150.00}
        ])

    if 'df_var' not in st.session_state or st.session_state['df_var'] is None or st.session_state['df_var'].empty:
        st.session_state['df_var'] = pd.DataFrame([
            {"Descrição do Custo Variável": "Matérias-Primas e Embalagens", "Valor Estimado (R$)": 1500.00},
            {"Descrição do Custo Variável": "Gás de Cozinha Recarga", "Valor Estimado (R$)": 135.00},
            {"Descrição do Custo Variável": "Taxas de Entrega / Apps", "Valor Estimado (R$)": 220.00}
        ])

    with st.sidebar:
        st.markdown("### 🔒 CENTRAL DE SEGURANÇA K&G")
        st.write("Baixe uma cópia das suas receitas para o celular/computador e fique 100% segura contra perdas!")
        
        backup_json = exportar_backup_json()
        
        st.download_button(
            label="💾 Baixar Backup de Segurança",
            data=backup_json,
            file_name=f"backup_confeitaria_kg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("---")
        st.write("🔄 **Restaurar Receitas Perdidas:**")
        arquivo_upload_backup = st.file_uploader("Envie seu arquivo de backup (.json) para restaurar:", type=["json"])
        if arquivo_upload_backup is not None:
            conteudo = arquivo_upload_backup.read().decode("utf-8")
            if st.button("🚀 Confirmar e Restaurar Tudo Agora", use_container_width=True):
                if importar_backup_json(conteudo):
                    st.success("✔️ Todos os dados e receitas foram restaurados com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao ler o arquivo de backup. Verifique se é um arquivo de backup K&G válido.")

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
    # ABA 1: ORÇAMENTOS & FRETE LOGÍSTICO
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
            is_rural = st.checkbox("Rota includes estrada de terra / área rural? (Adiciona taxa de risco)", value=True)
            
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
                salvar_dados_disco()

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
        st.markdown(f"<div class='alerta-aniv'>🎉 <b>ALERTA DE MARKETING K&G:</b> Juliana Mendes Rossi faz aniversário este mês! Dispare uma mensagem especial de fidelização.</div>", unsafe_allow_html=True)
        
        busca = st.text_input("🔍 Busca Ativa por Nome, Telefone, Códigos de Pedidos ou Alergias:")
        df_mostrar_crm = st.session_state['banco_crm']
        if busca:
            df_mostrar_crm = df_mostrar_crm[
                df_mostrar_crm["Cliente VIP"].astype(str).str.contains(busca, case=False, na=False) |
                df_mostrar_crm["WhatsApp"].astype(str).str.contains(busca, na=False) |
                df_mostrar_crm["Restrições"].astype(str).str.contains(busca, case=False, na=False) |
                df_mostrar_crm["Últimos Pedidos"].astype(str).str.contains(busca, na=False)
            ]
        
        df_crm_ed = st.data_editor(df_mostrar_crm, num_rows="dynamic", use_container_width=True, key="crm_base_key")
        
        if st.button("💾 Salvar Alterações no CRM"):
            st.session_state['banco_crm'] = df_crm_ed
            st.success("CRM Atualizado com sucesso!")
            salvar_dados_disco()

    # ==========================================
    # ABA 3: FÁBRICA DE BASES
    # ==========================================
    with tabs[3]:
        st.markdown('<div class="section-title">🥣 Fábrica de Bases: Gestão de Receitas e Custos</div>', unsafe_allow_html=True)
        sub_b1, sub_b2, sub_b3, sub_b4 = st.tabs(["🍞 Massas", "🍓 Recheios, Cremes & Geleias", "💧 Caldas para Regar", "✨ Coberturas & Molhos"])
        
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
                            "perda_coccao": 10.0
                        }
                        st.success(f"Massa '{novo_m_nome}' cadastrada!")
                        salvar_dados_disco()
                        st.rerun()

            st.write("---")
            sel_massa = st.selectbox("Selecione a Massa para Visualizar/Alimentar:", list(st.session_state['banco_massas_rec'].keys()))
            
            if sel_massa:
                rec_m = st.session_state['banco_massas_rec'][sel_massa]
                st.markdown("##### 📋 Ingredientes Cadastrados")
                
                m_edit = renderizar_tabela_segura(
                    rec_m["ingredientes"],
                    config_colunas_ingredientes,
                    f"m_edit_{sel_massa}"
                )
                st.session_state['banco_massas_rec'][sel_massa]["ingredientes"] = m_edit
                salvar_dados_disco()
                
                peso_bruto_m = calcular_peso_bruto_ingredientes(m_edit)
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown("##### ⚙️ Rendimento Inteligente")
                    perda_massa_pct = st.slider("Fator de Perda no Forno (%)", min_value=0.0, max_value=30.0, value=float(rec_m.get("perda_coccao", 10.0)), step=0.5, key=f"perda_m_{sel_massa}")
                    st.session_state['banco_massas_rec'][sel_massa]["perda_coccao"] = perda_massa_pct
                    
                    peso_obt_m = peso_bruto_m * (1 - perda_massa_pct / 100.0) if perda_massa_pct > 0 else peso_bruto_m
                    st.session_state['banco_massas_rec'][sel_massa]["peso_obtido"] = peso_obt_m if peso_obt_m > 0 else 1000.0
                    
                    st.info(f"⚖️ **Peso Bruto:** {peso_bruto_m:.1f} g  |  📉 **Peso Líquido:** {peso_obt_m:.1f} g")
                    
                    custo_massa_total = calcular_custo_tabela_seguro(m_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_m_kg = (custo_massa_total / peso_obt_m * 1000) if peso_obt_m > 0 else 0.0
                    st.metric("Custo Total da Receita", f"R$ {custo_massa_total:.2f}")
                    st.metric("Custo por kg de Massa", f"R$ {custo_m_kg:.2f}")
                with col_m2:
                    prep_m = st.text_area("🥣 Modo de Preparo", value=rec_m.get("preparo", ""), key=f"prep_m_{sel_massa}")
                    st.session_state['banco_massas_rec'][sel_massa]["preparo"] = prep_m
                    
                    st.write("---")
                    st.markdown("##### 🗑️ Excluir Receita")
                    conf_del_m = st.checkbox("Desejo excluir esta receita permanentemente.", key=f"conf_del_m_{sel_massa}")
                    if st.button("🗑️ Excluir Permanentemente", key=f"btn_del_m_{sel_massa}", type="primary", disabled=not conf_del_m):
                        del st.session_state['banco_massas_rec'][sel_massa]
                        st.success("Receita excluída com sucesso!")
                        salvar_dados_disco()
                        st.rerun()

        # --- SUB-ABA 2: RECHEIOS ---
        with sub_b2:
            st.markdown("##### ➕ Cadastrar Novo Recheio ou Creme")
            with st.form("novo_recheio_form"):
                novo_r_nome = st.text_input("Nome do Novo Recheio")
                submit_r = st.form_submit_button("➕ Cadastrar Recheio")
                if submit_r and novo_r_nome:
                    if novo_r_nome not in st.session_state['banco_recheios_rec']:
                        st.session_state['banco_recheios_rec'][novo_r_nome] = {
                            "ingredientes": pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                            "peso_obtido": 1000.0,
                            "preparo": "Descreva aqui o modo de preparo passo a passo.",
                            "perda_coccao": 15.0
                        }
                        st.success(f"Recheio '{novo_r_nome}' cadastrado!")
                        salvar_dados_disco()
                        st.rerun()

            st.write("---")
            sel_recheio = st.selectbox("Selecione o Recheio para Visualizar/Alimentar:", list(st.session_state['banco_recheios_rec'].keys()))
            
            if sel_recheio:
                rec_r = st.session_state['banco_recheios_rec'][sel_recheio]
                st.markdown("##### 📋 Ingredientes Cadastrados")
                
                r_edit = renderizar_tabela_segura(
                    rec_r["ingredientes"],
                    config_colunas_ingredientes,
                    f"r_edit_{sel_recheio}"
                )
                st.session_state['banco_recheios_rec'][sel_recheio]["ingredientes"] = r_edit
                salvar_dados_disco()
                
                peso_bruto_r = calcular_peso_bruto_ingredientes(r_edit)
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.markdown("##### ⚙️ Rendimento Inteligente")
                    perda_recheio_pct = st.slider("Fator de Perda na Panela (%)", min_value=0.0, max_value=40.0, value=float(rec_r.get("perda_coccao", 15.0)), step=0.5, key=f"perda_r_{sel_recheio}")
                    st.session_state['banco_recheios_rec'][sel_recheio]["perda_coccao"] = perda_recheio_pct
                    
                    peso_obt_r = peso_bruto_r * (1 - perda_recheio_pct / 100.0) if perda_recheio_pct > 0 else peso_bruto_r
                    st.session_state['banco_recheios_rec'][sel_recheio]["peso_obtido"] = peso_obt_r if peso_obt_r > 0 else 1000.0
                    
                    st.info(f"⚖️ **Peso Bruto:** {peso_bruto_r:.1f} g  |  📉 **Peso Líquido:** {peso_obt_r:.1f} g")
                    
                    custo_recheio_total = calcular_custo_tabela_seguro(r_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_r_kg = (custo_recheio_total / peso_obt_r * 1000) if peso_obt_r > 0 else 0.0
                    st.metric("Custo Total do Recheio", f"R$ {custo_recheio_total:.2f}")
                    st.metric("Custo por kg de Recheio", f"R$ {custo_r_kg:.2f}")
                with col_r2:
                    prep_r = st.text_area("🥣 Modo de Preparo", value=rec_r.get("preparo", ""), key=f"prep_r_{sel_recheio}")
                    st.session_state['banco_recheios_rec'][sel_recheio]["preparo"] = prep_r
                    
                    st.write("---")
                    st.markdown("##### 🗑️ Excluir Receita")
                    conf_del_r = st.checkbox("Desejo excluir esta receita permanentemente.", key=f"conf_del_r_{sel_recheio}")
                    if st.button("🗑️ Excluir Permanentemente", key=f"btn_del_r_{sel_recheio}", type="primary", disabled=not conf_del_r):
                        del st.session_state['banco_recheios_rec'][sel_recheio]
                        st.success("Receita excluída com sucesso!")
                        salvar_dados_disco()
                        st.rerun()

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
                            "preparo": "Misturar e aplicar."
                        }
                        st.success(f"Calda '{novo_c_nome}' cadastrada!")
                        salvar_dados_disco()
                        st.rerun()

            st.write("---")
            sel_calda = st.selectbox("Selecione a Calda para Editar:", list(st.session_state['banco_caldas_rec'].keys()))
            if sel_calda:
                rec_c = st.session_state['banco_caldas_rec'][sel_calda]
                st.markdown("##### 📋 Angredientes Cadastrados")
                
                c_edit = renderizar_tabela_segura(
                    rec_c["ingredientes"],
                    config_colunas_ingredientes,
                    f"c_edit_{sel_calda}"
                )
                st.session_state['banco_caldas_rec'][sel_calda]["ingredientes"] = c_edit
                salvar_dados_disco()
                
                peso_obt_c = calcular_peso_bruto_ingredientes(c_edit)
                st.session_state['banco_caldas_rec'][sel_calda]["peso_obtido"] = peso_obt_c if peso_obt_c > 0 else 1000.0
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.info(f"⚖️ **Rendimento Final (Líquido):** {peso_obt_c:.1f} g/ml")
                    custo_calda_total = calcular_custo_tabela_seguro(c_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_c_kg = (custo_calda_total / peso_obt_c * 1000) if peso_obt_c > 0 else 0.0
                    st.metric("Custo Total da Calda", f"R$ {custo_calda_total:.2f}")
                    st.metric("Custo por kg", f"R$ {custo_c_kg:.2f}")
                with col_c2:
                    prep_c = st.text_area("🥣 Instruções de Preparo", value=rec_c.get("preparo", ""), key=f"prep_c_{sel_calda}")
                    st.session_state['banco_caldas_rec'][sel_calda]["preparo"] = prep_c

        # --- SUB-ABA 4: COBERTURAS & ADICIONAIS ---
        with sub_b4:
            st.markdown("##### ➕ Cadastrar Nova Cobertura / Adicional")
            with st.form("nova_cob_form"):
                novo_cob_nome = st.text_input("Nome do Adicional")
                submit_cob = st.form_submit_button("➕ Cadastrar")
                if submit_cob and novo_cob_nome:
                    if novo_cob_nome not in st.session_state['banco_coberturas_rec']:
                        st.session_state['banco_coberturas_rec'][novo_cob_nome] = {
                            "ingredientes": pd.DataFrame(columns=["Ingrediente", "Qtd Usada", "Unidade", "Qtd na Embalagem", "Preço Embalagem (R$)"]),
                            "peso_obtido": 1000.0,
                            "preparo": "Bater e aplicar."
                        }
                        st.success(f"Elemento '{novo_cob_nome}' cadastrado!")
                        salvar_dados_disco()
                        st.rerun()

            st.write("---")
            sel_cob = st.selectbox("Selecione a Cobertura/Molho para Editar:", list(st.session_state['banco_coberturas_rec'].keys()))
            if sel_cob:
                rec_cob = st.session_state['banco_coberturas_rec'][sel_cob]
                st.markdown("##### 📋 Ingredientes Cadastrados")
                
                cob_edit = renderizar_tabela_segura(
                    rec_cob["ingredientes"],
                    config_colunas_ingredientes,
                    f"cob_edit_{sel_cob}"
                )
                st.session_state['banco_coberturas_rec'][sel_cob]["ingredientes"] = cob_edit
                salvar_dados_disco()
                
                peso_obt_cob = calcular_peso_bruto_ingredientes(cob_edit)
                st.session_state['banco_coberturas_rec'][sel_cob]["peso_obtido"] = peso_obt_cob if peso_obt_cob > 0 else 1000.0
                
                col_cob1, col_cob2 = st.columns(2)
                with col_cob1:
                    st.info(f"⚖️ **Rendimento Final:** {peso_obt_cob:.1f} g")
                    custo_cob_total = calcular_custo_tabela_seguro(cob_edit, "Preço Embalagem (R$)", "Qtd na Embalagem", "Qtd Usada")
                    custo_cob_kg = (custo_cob_total / peso_obt_cob * 1000) if peso_obt_cob > 0 else 0.0
                    st.metric("Custo Total", f"R$ {custo_cob_total:.2f}")
                    st.metric("Custo por kg/unidade", f"R$ {custo_cob_kg:.2f}")
                with col_cob2:
                    prep_cob = st.text_area("🥣 Modo de Preparo", value=rec_cob.get("preparo", ""), key=f"prep_cob_{sel_cob}")
                    st.session_state['banco_coberturas_rec'][sel_cob]["preparo"] = prep_cob

    # ==========================================
    # ABA 4: DOCES & SALGADOS PERSONALIZADOS
    # ==========================================
    with tabs[4]:
        st.markdown('<div class="section-title">🍫 Doces Personalizados e Formas Especiais</div>', unsafe_allow_html=True)
        col_doc1, col_doc2 = st.columns(2)
        with col_doc1:
            nome_projeto_doce = st.text_input("Nome/Tema do Doce Personalizado", value="Docinhos Finos Casamento")
            forma_bwb_id = st.text_input("Forma BWB Utilizada (Número/Modelo)", value="BWB 90")
            peso_choco_forma = st.number_input("Chocolate por Unidade (g)", value=25.0)
        with col_doc2:
            pasta_tipo = st.selectbox("Pasta Utilizada", ["Pasta de Leite Ninho", "Pasta Americana", "Modelagem de Chocolate"])
            peso_pasta_bwb = st.number_input("Peso da Pasta na Modelagem (g)", value=15.0)

    # ==========================================
    # ABA 5: PRODUTOS COMPLETOS & FICHA TÉCNICA
    # ==========================================
    with tabs[5]:
        st.markdown('<div class="section-title">📐 Engenharia Estrutural e Precificação Dinâmica de Vendas</div>', unsafe_allow_html=True)
        
        col_pd1, col_pd2 = st.columns(2)
        with col_pd1:
            nome_bolo_final = st.text_input("Nome do Produto Comercial Completo", value="Bolo Ninho Supremo Especial")
            tipo_produto_completo = st.selectbox("Tipo de Produto Comercial", ["Bolo Completo", "Quiche / Empadão", "Salgados de Forno / Coxinhas"])
            peso_alvo = st.number_input("Peso Alvo Solicitado pelo Cliente (kg)", min_value=0.1, value=1.0)
            tipo_forma_final = st.selectbox("Geometria da Forma de Assar", ["Redonda", "Marmita Retangular", "Unidade Individual / Sem Forma"])
            margem_comercial = st.slider("Selecione a Margem Comercial de Segurança (%)", min_value=30, max_value=80, value=45)
            
            sel_massa_composta = st.selectbox("Selecione a Massa Base:", list(st.session_state['banco_massas_rec'].keys()))
            sel_recheio_composto = st.selectbox("Selecione o Recheio Base:", list(st.session_state['banco_recheios_rec'].keys()))
            
            if tipo_produto_completo == "Bolo Completo":
                sel_calda_composta = st.selectbox("Selecione a Calda de Regar:", list(st.session_state['banco_caldas_rec'].keys()))
                sel_cobertura_composto = st.selectbox("Selecione a Cobertura/Blindagem:", list(st.session_state['banco_coberturas_rec'].keys()))
            else:
                st.write("*(Caldas e coberturas de bolo ocultadas para produtos salgados)*")
                sel_calda_composta = None
                sel_cobertura_composto = None
            
        with col_pd2:
            peso_alvo_g = peso_alvo * 1000
            
            if tipo_produto_completo == "Bolo Completo":
                calc_massa_final = peso_alvo_g * 0.35
                calc_recheio_final = peso_alvo_g * 0.40
                calc_calda_final = peso_alvo_g * 0.10
                calc_cobertura_final = peso_alvo_g * 0.15
            elif tipo_produto_completo == "Quiche / Empadão":
                calc_massa_final = peso_alvo_g * 0.45
                calc_recheio_final = peso_alvo_g * 0.55
                calc_calda_final = 0.0
                calc_cobertura_final = 0.0
            else:
                calc_massa_final = peso_alvo_g * 0.55
                calc_recheio_final = peso_alvo_g * 0.45
                calc_calda_final = 0.0
                calc_cobertura_final = 0.0
            
            if tipo_forma_final == "Redonda":
                diametro_sugerido = math.ceil(2 * math.sqrt(peso_alvo_g / (3.14 * 10 * 0.6)))
                forma_recomenda_txt = f"Forma Redonda de {diametro_sugerido} cm (Altura padrão de 10cm)"
                st.metric("Forma Redonda Recomendada", f"{diametro_sugerido} cm de diâmetro")
            elif tipo_forma_final == "Marmita Retangular":
                forma_recomenda_txt = "Marmita Alumínio de 220ml com tampa"
                st.metric("Embalagem Recomendada", "Marmita Alumínio")
            else:
                forma_recomenda_txt = "Assadeira Individual padrão"
                st.metric("Assadeira Recomendada", "Assadeira Fundo Falso")

            st.markdown("##### 🎨 Acabamento, Decoração e Apresentação")
            decor_final_input = st.text_area(
                "Descreva a finalização estética e técnicas aplicadas:",
                value=st.session_state.get('decoracao_bolo_completo', "Decoração com morangos frescos higienizados, placas decorativas de chocolate e finalização com açúcar de confeiteiro."),
                height=110,
                key="decoracao_final_area"
            )
            st.session_state['decoracao_bolo_completo'] = decor_final_input

        custo_m_kg = get_recipe_cost_kg(st.session_state['banco_massas_rec'], sel_massa_composta)
        custo_r_kg = get_recipe_cost_kg(st.session_state['banco_recheios_rec'], sel_recheio_composto)
        custo_c_kg = get_recipe_cost_kg(st.session_state['banco_caldas_rec'], sel_calda_composta) if sel_calda_composta else 0.0
        custo_cob_kg = get_recipe_cost_kg(st.session_state['banco_coberturas_rec'], sel_cobertura_composto) if sel_cobertura_composto else 0.0

        custo_massa_composto = (custo_m_kg / 1000) * calc_massa_final
        custo_recheio_composto = (custo_r_kg / 1000) * calc_recheio_final
        custo_calda_composto = (custo_c_kg / 1000) * calc_calda_final if sel_calda_composta else 0.0
        custo_cob_composto = (custo_cob_kg / 1000) * calc_cobertura_final if sel_cobertura_composto else 0.0
        custo_insumos_total = custo_massa_composto + custo_recheio_composto + custo_calda_composto + custo_cob_composto + 4.50 
        
        st.markdown("##### 📝 Balanço Estrutural para Bancada de Produção:")
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        with c_p1: st.metric(f"Massa ({sel_massa_composta})", f"{int(calc_massa_final)} g", f"Custo: R$ {custo_massa_composto:.2f}")
        with c_p2: st.metric(f"Recheio ({sel_recheio_composto})", f"{int(calc_recheio_final)} g", f"Custo: R$ {custo_recheio_composto:.2f}")
        with c_p3: 
            if calc_calda_final > 0:
                st.metric(f"Calda ({sel_calda_composta})", f"{int(calc_calda_final)} g", f"Custo: R$ {custo_calda_composto:.2f}")
            else:
                st.metric("Calda", "Isento")
        with c_p4:
            if calc_cobertura_final > 0:
                st.metric(f"Cobertura ({sel_cobertura_composto})", f"{int(calc_cobertura_final)} g", f"Custo: R$ {custo_cob_composto:.2f}")
            else:
                st.metric("Cobertura", "Isento")

        st.markdown("### 💰 Tabela de Preço de Venda Comercial")
        divisor_margem = (100 - margem_comercial) / 100
        preco_venda_base = custo_insumos_total / divisor_margem
        
        v_debito = preco_venda_base / (1 - 0.0199)
        v_credito = preco_venda_base / (1 - 0.0499)
        v_ifood = preco_venda_base / 0.73

        cv1, cv2, cv3, cv4 = st.columns(4)
        with cv1: st.markdown(f"<div class='preco-box'><b>🛍| PIX / DINHEIRO</b><br><span style='font-size:20px; font-weight:bold;'>R$ {preco_venda_base:.2f}</span><br>Lucro de {margem_comercial}%</div>", unsafe_allow_html=True)
        with cv2: st.markdown(f"<div class='preco-box' style='background:#0B533A;'><b>💳 DÉBITO MAQ.</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_debito:.2f}</span><br>Taxa 1.99% inclusa</div>", unsafe_allow_html=True)
        with cv3: st.markdown(f"<div class='preco-box' style='background:#0B533A;'><b>💳 CRÉDITO MAQ.</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_credito:.2f}</span><br>Taxa 4.99% inclusa</div>", unsafe_allow_html=True)
        with cv4: st.markdown(f"<div class='preco-box' style='background:#901414;'><b>🛵 CARDÁPIO IFOOD</b><br><span style='font-size:20px; font-weight:bold;'>R$ {v_ifood:.2f}</span><br>Taxas iFood Inclusas</div>", unsafe_allow_html=True)

        st.write("---")
        if st.button("🖨️ Emitir Ficha Técnica de Produção"):
            st.markdown(f"""
                <div class="print-box">
                    <div style="text-align: center; border-bottom: 2px solid #043927; padding-bottom: 10px;">
                        <span style="font-size: 20px; font-weight: bold; color: #043927;">💎 FICHA DE PRODUÇÃO UNIFICADA - K&G ARTE EM CONFEITARIA 💎</span><br>
                        <span style="font-size: 12px; letter-spacing: 1px;">PADRONIZAÇÃO E ENGENHARIA DE PRODUTO</span>
                    </div>
                    <br>
                    <b>🍰 PRODUTO:</b> {nome_bolo_final.upper()}<br>
                    <b>⚖️ PESO ALVO DE ENCOMENDA:</b> {peso_alvo:.2f} kg ({peso_alvo_g:.0f}g)<br>
                    <b>📐 EMBALAGEM / FORMA:</b> {forma_recomenda_txt}<br>
                    -------------------------------------------------------------------------<br>
                    <b>🧁 COMPOSIÇÃO DE MONTAGEM DE BANCADA:</b><br>
                    * Massa ({sel_massa_composta}): <b>{int(calc_massa_final)} g</b><br>
                    * Recheio ({sel_recheio_composto}): <b>{int(calc_recheio_final)} g</b><br>
                    {"* Calda (" + str(sel_calda_composta) + "): <b>" + str(int(calc_calda_final)) + " g</b><br>" if calc_calda_final > 0 else ""}
                    {"* Cobertura (" + str(sel_cobertura_composto) + "): <b>" + str(int(calc_cobertura_final)) + " g</b><br>" if calc_cobertura_final > 0 else ""}
                    -------------------------------------------------------------------------<br>
                    <b>🎨 FINALIZAÇÃO ESTÉTICA E TÉCNICAS:</b><br>
                    <i>{st.session_state['decoracao_bolo_completo']}</i><br>
                    -------------------------------------------------------------------------<br>
                    <b>💸 PREÇO DE VENDA PIX/DINHEIRO: R$ {preco_venda_base:.2f}</b>
                </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # ABA 6: EMBALAGENS & IMPRESSÃO PORTÁTIL
    # ==========================================
    with tabs[6]:
        st.markdown('<div class="section-title">📦 Gestão de Embalagens, Laços, Fitas e Envio para Portátil</div>', unsafe_allow_html=True)
        df_emb = st.data_editor(pd.DataFrame([
            {"Embalagem": "Marmita Wyda 220ml com tampa", "Preço Embalagem (R$)": 1.20, "Unidades no Pacote": 100, "Usada no Produto": 1},
            {"Embalagem": "Pote Galvanotek G742m 250ml", "Preço Embalagem (R$)": 1.50, "Unidades no Pacote": 50, "Usada no Produto": 1},
            {"Embalagem": "Plástico Celofane Folha 15x15", "Preço Embalagem (R$)": 0.05, "Unidades no Pacote": 100, "Usada no Produto": 1}
        ]), num_rows="dynamic", use_container_width=True, key="emb_key")
        
        texto_impressora = st.text_area("Texto para sair na Impressora Portátil Bluetooth:", f"K&G Arte em Confeitaria\n{nome_bolo_final}\nConsuma com Prazer!")

    # ==========================================
    # ABA 7: ANVISA & ROTULAGEM NUTRICIONAL (RDC 429)
    # ==========================================
    with tabs[7]:
        st.markdown('<div class="section-title">🥦 Rotulagem Frontal e Lupa Legal de Advertência da ANVISA</div>', unsafe_allow_html=True)
        
        lupa_acucar = st.checkbox("Este produto ultrapassa 15g de Açúcares por 100g?", value=True)
        lupa_gordura = st.checkbox("Este produto ultrapassa 6g de Gorduras Saturadas por 100g?", value=False)
        
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
        
        st.image("https://barcode.tec-it.com/barcode.ashx?data=789643120054&code=EAN13", caption="Exemplo de Código de Barras EAN-13")

    # ==========================================
    # ABA 8: ESTOQUE CRÍTICO INTELIGENTE
    # ==========================================
    with tabs[8]:
        st.markdown('<div class="section-title">🛒 Estoque Crítico de Matérias-Primas e Alertas</div>', unsafe_allow_html=True)
        
        estoque_base = pd.DataFrame([
            {"Item de Estoque": "Farinha Venturelli (kg)", "Quantidade em Estoque (Un)": 15.0, "Estoque Mínimo (Un)": 10.0},
            {"Item de Estoque": "Margarina Qualy (500g)", "Quantidade em Estoque (Un)": 3.0, "Estoque Mínimo (Un)": 8.0},
            {"Item de Estoque": "Leite Condensado (Moça)", "Quantidade em Estoque (Un)": 24.0, "Estoque Mínimo (Un)": 36.0},
            {"Item de Estoque": "Morangos in natura (Bandeja)", "Quantidade em Estoque (Un)": 2.0, "Estoque Mínimo (Un)": 10.0}
        ])
        
        df_est_edit = st.data_editor(estoque_base, num_rows="dynamic", use_container_width=True, key="estoque_crit_key")
        
        st.markdown("##### 🚨 Alertas de Compras Urgentes:")
        for idx, row in df_est_edit.iterrows():
            try:
                atual = float(limpar_e_converter_coluna(pd.DataFrame([row]), "Quantidade em Estoque (Un)", 0.0)[0])
                minimo = float(limpar_e_converter_coluna(pd.DataFrame([row]), "Estoque Mínimo (Un)", 0.0)[0])
                if atual < minimo:
                    st.error(f"⚠️ **{row['Item de Estoque']}** está abaixo do mínimo! Adquirir mais {int(minimo - atual)} unidades.")
            except Exception:
                pass

    # ==========================================
    # ABA 9: FORNECEDORES HOMOLOGADOS DE CURITIBA
    # ==========================================
    with tabs[9]:
        st.markdown('<div class="section-title">🏢 Fornecedores e Distribuidores de Curitiba e RMC</div>', unsafe_allow_html=True)
        
        fornecedores_cwb = pd.DataFrame([
            {"Fornecedor": "Central do Chocolate CWB", "Telefone": "(41) 3222-1200", "Localização": "Centro, Curitiba - PR", "Insumos": "Chocolates Nobres Callebaut, Sicao, LeCacau"},
            {"Fornecedor": "Nova Íris Embalagens", "Telefone": "(41) 3324-4500", "Localização": "Centro, Curitiba - PR", "Insumos": "Caixas de Papelão, Marmitas, Potes e Pratos"},
            {"Fornecedor": "CEASA Curitiba (Distribuidor)", "Telefone": "(41) 99999-5555", "Localização": "CEASA PR", "Insumos": "Morangos, Laranja, Maracujá e frutas frescas"},
            {"Fornecedor": "Dijos Doce Embalagens", "Telefone": "(41) 3014-9988", "Localização": "Portão, Curitiba - PR", "Insumos": "Formas Leila, Desmoldante Carlex e Adicionais"}
        ])
        st.data_editor(fornecedores_cwb, num_rows="dynamic", use_container_width=True, key="forn_key")

    # ==========================================
    # ABA 10: INVENTÁRIO PATRIMONIAL DO ATELIER
    # ==========================================
    with tabs[10]:
        st.markdown('<div class="section-title">🏛️ Inventário Patrimonial do Atelier K&G</div>', unsafe_allow_html=True)
        
        inventario_base = pd.DataFrame([
            {"Categoria": "Equipamentos Elétricos", "Equipamento/Utensílio": "Forno de Convecção Prática MiniConv", "Quantidade": 1, "Valor Unitário (R$)": 4500.00},
            {"Categoria": "Utensílios", "Equipamento/Utensílio": "Rolo de Massa Profissional 48cm", "Quantidade": 1, "Valor Unitário (R$)": 85.00},
            {"Categoria": "Equipamentos Elétricos", "Equipamento/Utensílio": "Seladora a Vácuo de Alimentos Cetro", "Quantidade": 1, "Valor Unitário (R$)": 380.00},
            {"Categoria": "Equipamentos Elétricos", "Equipamento/Utensílio": "Batedeira Planetária Arno", "Quantidade": 1, "Valor Unitário (R$)": 650.00}
        ])
        
        df_inv_edit = st.data_editor(inventario_base, num_rows="dynamic", use_container_width=True, key="inv_pat_key")
        
        custo_unit = limpar_e_converter_coluna(df_inv_edit, "Valor Unitário (R$)", 0.0)
        quantidades = limpar_e_converter_coluna(df_inv_edit, "Quantidade", 0.0)
        patrimonio_total = (custo_unit * quantidades).sum()
        
        st.metric("Patrimônio Físico Atelier", f"R$ {patrimonio_total:.2f}")

    # Salva automaticamente em cada atualização
    salvar_dados_disco()

elif chave_usuario != "":
    st.error("Chave de Acesso Incorreta! Por favor, digite a senha autorizada da K&G.")
else:
    st.warning("Insira a chave de acesso empresarial para visualizar o ecossistema estratégico.")
