import streamlit as st
import pandas as pd
import requests
import json
import re
import os
import google.generativeai as genai

# ==========================================
# CONFIGURACIÓN "MEMORIA PROFUNDA" (V13.0)
# ==========================================
st.set_page_config(page_title="Mentor MinTIC 2026: Elite Edition", layout="wide", page_icon="🏅")

GEMINI_KEY = st.secrets.get("GEMINI_KEY", "AIzaSyA-Aybc_CO_UxqM7f0nd0r2JJjeqJ3YfEU")
genai.configure(api_key=GEMINI_KEY, transport='rest')

WORKSPACE_PATH = r"f:\HMO\SENA_PROYECTOS\MINTIC_2026_DATOS"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 50px; border-radius: 0 0 50px 50px; text-align: center;
        margin-bottom: 40px; border-bottom: 2px solid #38bdf8;
    }
    .pillar-box { 
        background: #1e293b; padding: 25px; border-radius: 15px; 
        border-left: 6px solid #38bdf8; margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2); line-height: 1.7;
    }
    .coach-msg { background: #0ea5e9; color: white; padding: 15px; border-radius: 12px; font-weight: 600; margin-bottom: 20px; border-left: 10px solid #0369a1; }
    .big-data-badge { background: #38bdf8; color: #0f172a; padding: 8px 18px; border-radius: 40px; font-size: 14px; font-weight: 800; }
    .stButton>button { border-radius: 12px; font-weight: 700; transition: all 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(56,189,248,0.4); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <div style="color:#38bdf8; font-weight:800; letter-spacing:4px; margin-bottom:10px;">ESTRATEGIA • RIGOR • IMPACTO</div>
        <div class="main-title" style="font-size:42px; font-weight:800; text-transform:uppercase;">🏅 MENTOR MINTIC 2026: ELITE v13.0</div>
        <div style="opacity:0.8; font-size:18px;">Transformando Datos en Liderazgo Sistémico</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MOTOR DE INTELIGENCIA ESTRATÉGICA
# ==========================================
class EliteMentor:
    def __init__(self):
        self.model_name = 'gemini-1.5-flash'

    def analyze_deep(self, idea, ds_name, rows, columns):
        model = genai.GenerativeModel(self.model_name)
        prompt = f"""
        Actúa como un Mentor de Datos Senior e Inspirador. 
        Analiza el reto '{idea}' con el dataset '{ds_name}'.
        Variables: {columns}. Registros: {rows}.
        
        REGLA DE ORO: Penaliza lo trivial. El análisis debe ser profundo e investigativo.
        JSON (6 líneas por campo):
        - problema: Falla sistémica o asimetría de información.
        - reto: Desafío de modelado y arquitectura de datos.
        - solucion: Estrategia analítica y algoritmos específicos.
        - impacto_social: Cambio real en la vida del ciudadano colombiano.
        """
        try:
            res = model.generate_content(prompt)
            match = re.search(r'\{.*\}', res.text, re.DOTALL)
            return json.loads(match.group(0)) if match else self._coach_fallback(ds_name)
        except: return self._coach_fallback(ds_name)

    def _coach_fallback(self, name):
        return {
            "problema": f"La arquitectura de información en '{name}' padece una fragmentación que invisibiliza patrones críticos. Esta opacidad impide una gobernanza basada en evidencia.",
            "reto": "Integrar flujos masivos de datos para automatizar la identificación de riesgos sistémicos mediante modelos de analítica avanzada.",
            "solucion": "Diseño de un ecosistema de Machine Learning basado en detección de anomalías (Isolation Forest) y modelos predictivos escalables.",
            "impacto_social": "Democratización del acceso a la información y fortalecimiento de la transparencia institucional en beneficio de toda la ciudadanía colombiana."
        }

    def get_notebook(self, ds_id, ds_name, strategy, columns):
        model = genai.GenerativeModel(self.model_name)
        prompt = f"Genera JSON de un NOTEBOOK (.ipynb) para {ds_id}. Incluye comentarios de 'COACHING' que expliquen el porqué de cada paso. Solo JSON."
        try:
            res = model.generate_content(prompt)
            match = re.search(r'\{.*\}', res.text, re.DOTALL)
            return match.group(0)
        except: return "{}"

mentor = EliteMentor()

# ==========================================
# INTERFAZ Y FLUJO DE VALOR
# ==========================================
if "step" not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.markdown("### 💬 MENTOR ESTRATÉGICO")
    st.markdown("---")
    st.write("Cada proyecto es una oportunidad de liderar el cambio en Colombia.")
    if st.button("🔄 REINICIAR CONSULTORÍA"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

if st.session_state.step == 1:
    st.markdown('<div class="coach-msg">¡Bienvenido! Hoy no solo buscamos datos, buscamos soluciones estructurales para el país.</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([2, 1, 1])
    q = c1.text_input("Ingresa tu Reto Estratégico:", placeholder="Ej: Corrupción, Salud, Movilidad...")
    depto = c2.selectbox("Dpto:", ["NACIONAL", "BOGOTA", "ANTIOQUIA", "VALLE", "ATLANTICO", "BOLIVAR"])
    ciudad = c3.text_input("Ciudad:")

    if st.button("🚀 INICIAR DESCUBRIMIENTO DE ALTO IMPACTO", use_container_width=True):
        if q:
            with st.status("Auditando Datos y Generando Visión...") as status:
                query = f"{q} {depto if depto != 'NACIONAL' else ''} {ciudad}"
                res = requests.get(f"https://www.datos.gov.co/api/catalog/v1?q={query}&limit=5").json()
                results = []
                for item in res.get('results', []):
                    r = item.get('resource', {})
                    ds_id = r.get('id'); name = r.get('name')
                    # Metadatos Master
                    try:
                        cat = requests.get(f"https://api.us.socrata.com/api/catalog/v1?ids={ds_id}", timeout=3).json()
                        rows = cat['results'][0]['resource']['row_count']
                        v_res = requests.get(f"https://www.datos.gov.co/api/views/{ds_id}.json").json()
                        cols_meta = [{"Variable": c['name'], "Tipo": c['dataTypeName'], "Desc": c.get('description', 'N/A')} for c in v_res.get('columns', [])]
                    except: rows = 0; cols_meta = []
                    
                    analysis = mentor.analyze_deep(q, name, rows, [c['Variable'] for c in cols_meta])
                    results.append({"id": ds_id, "name": name, "rows": rows, "cols": cols_meta, "entidad": r.get('attribution'), "desc": r.get('description'), **analysis})
                st.session_state.results = results
                status.update(label="¡Visión Estratégica Generada!", state="complete")

    if "results" in st.session_state:
        for d in st.session_state.results:
            with st.container():
                st.markdown(f"### {d['name']}")
                if d['rows'] > 10000:
                    st.markdown(f"<span class='big-data-badge'>💎 VOLUMEN MASIVO DETECTADO: {d['rows']:,} REGISTROS</span>", unsafe_allow_html=True)
                
                cl, cr = st.columns(2)
                cl.markdown(f"<div class='pillar-box' style='border-left-color: #ef4444;'>🔴 <b>EL PROBLEMA:</b><br>{d['problema']}</div>", unsafe_allow_html=True)
                cl.markdown(f"<div class='pillar-box' style='border-left-color: #38bdf8;'>🎯 <b>EL RETO:</b><br>{d['reto']}</div>", unsafe_allow_html=True)
                cr.markdown(f"<div class='pillar-box' style='border-left-color: #10b981;'>✅ <b>LA SOLUCIÓN:</b><br>{d['solucion']}</div>", unsafe_allow_html=True)
                cr.markdown(f"<div class='pillar-box' style='border-left-color: #8b5cf6;'>🌎 <b>EL IMPACTO:</b><br>{d['impacto_social']}</div>", unsafe_allow_html=True)
                
                if st.button(f"🛠️ DESARROLLAR PROYECTO: {d['id']}", key=f"btn_{d['id']}"):
                    st.session_state.selected = d; st.session_state.step = 2; st.rerun()
                st.divider()

elif st.session_state.step == 2:
    ds = st.session_state.selected
    st.markdown(f"## 🏆 Liderando el Proyecto: {ds['name']}")
    
    with st.spinner("Desarrollando Arquitectura de Datos Profesional..."):
        if "nb_json" not in st.session_state:
            st.session_state.nb_json = mentor.get_notebook(ds['id'], ds['name'], ds, [c['Variable'] for c in ds['cols']])

    t1, t2, t3 = st.tabs(["📋 Ficha Estratégica", "📊 Diccionario de Datos", "💾 Guardar Notebook (.ipynb)"])
    
    with t1:
        st.info(ds['desc'])
        st.markdown(f"[🔗 Ver Fuente Oficial en Datos.gov.co](https://www.datos.gov.co/d/{ds['id']})")
        c1, c2, c3 = st.columns(3); c1.metric("Registros", ds['rows']); c2.metric("Variables", len(ds['cols'])); c3.metric("Entidad", ds['entidad'][:25])
        if st.button("⬅️ VOLVER AL BUSCADOR"): st.session_state.step = 1; del st.session_state["nb_json"]; st.rerun()

    with t2:
        st.markdown("#### Diccionario de Ingeniería de Datos")
        st.table(pd.DataFrame(ds['cols']))

    with t3:
        filename = f"proyecto_{ds['id']}.ipynb"
        path = os.path.join(WORKSPACE_PATH, filename)
        st.markdown(f'<div class="coach-msg">Tu desarrollo está listo. Se guardará en: `{path}`</div>', unsafe_allow_html=True)
        if st.button("🚀 CREAR ARCHIVO .ipynb FÍSICO EN MI PC"):
            with open(path, "w", encoding="utf-8") as f: f.write(st.session_state.nb_json)
            st.balloons(); st.success(f"¡Notebook '{filename}' creado con éxito!")

st.markdown("---")
st.caption("v13.0 • Elite Edition • Inspirado en tu Historia • MinTIC 2026")
