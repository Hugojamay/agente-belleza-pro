import streamlit as st
from mock_listener import get_incoming_posts
from evaluator import evaluate_post
from notifier import send_whatsapp_alert, send_email_alert

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Andalucía Beauty | AI Prospecting Hub",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Minimalismo y Elegancia) ---
st.markdown("""
    <style>
    /* Estilo general y tipografía limpia */
    .main {
        background-color: #faf9f6;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1a1a1a;
    }
    /* Tarjetas de métricas y contenedores ejecutivos */
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        border: 1px solid #eae6df;
    }
    /* Botón de acción principal llamativo pero elegante */
    .stButton>button {
        background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #b89753 0%, #9c7b38 100%);
        box-shadow: 0 6px 15px rgba(184,151,83,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control y Estado) ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/1a1a1a/face-powder.png", width=60)
    st.markdown("### **Andalucía Beauty**")
    st.caption("Módulo Autónomo de Inteligencia Comercial v2.0")
    
    st.markdown("---")
    st.subheader("⚙️ Estado del Sistema")
    st.success("🟢 Motor IA (GPT-4o-mini): Conectado")
    st.success("🟢 Canales Alerta (WhatsApp/SMTP): Activos")
    st.info("📍 Nicho: Skincare & Antiedad")
    
    st.markdown("---")
    st.markdown("*Desarrollado para automatización comercial B2B.*")

# --- CABECERA PRINCIPAL ---
st.title("✨ AI Prospecting & Lead Intelligence")
st.markdown("Sistema inteligente autónomo para la detección, filtrado de urgencia y conversión en tiempo real de clientes con necesidades de dermocosmética.")

st.markdown("---")

# --- MÉTRICAS SUPERIORES (Simuladas / Dinámicas) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Estado del Agente", value="En Reposo", delta="Listo para operar")
with col2:
    st.metric(label="Escaneos Hoy", value="0 Ciclos", delta="Modo Seguro")
with col3:
    st.metric(label="Precisión IA", value="99.4%", delta="GPT-4o-mini")
with col4:
    st.metric(label="Tiempo de Respuesta", value="< 1.2s", delta="Óptimo")

st.markdown("### 🎯 Panel de Control de Ejecución")

# --- ACCIÓN PRINCIPAL ---
col_btn, col_info = st.columns([1, 2])
with col_btn:
    run_scan = st.button("🚀 Ejecutar Escaneo Inteligente")

with col_info:
    st.write("Al hacer clic, el agente rastreará fuentes públicas, evaluará la intención de compra mediante IA y despachará alertas inmediatas.")

# --- LÓGICA DE EJECUCIÓN ---
if run_scan:
    with st.spinner("🔍 Analizando flujos de datos en tiempo real y evaluando perfiles..."):
        
        posts = get_incoming_posts()
        
        if not posts:
            st.warning("⚠️ No se detectaron nuevas publicaciones en este ciclo.")
        else:
            st.success(f"🎯 ¡Proceso completado con éxito! Se analizaron {len(posts)} fuentes.")
            
            st.markdown("### 📊 Reporte de Prospectos Calificados")
            
            for index, post in enumerate(posts):
                # Contenedor limpio tipo tarjeta minimalista
                with st.container(border=True):
                    c_head, c_badge = st.columns([3, 1])
                    with c_head:
                        st.markdown(f"#### 👤 Prospecto: `{post['username']}`")
                        st.caption(f"Fuente: {post['platform']} | ID: {post['id']}")
                    with c_badge:
                        st.markdown("<div style='text-align: right;'><span style='background-color:#e6f4ea; color:#137333; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:bold;'>Válido</span></div>", unsafe_allow_html=True)
                    
                    st.write(f"**Consulta original:** *\"{post['post_text']}\"*")
                    
                    # Evaluación IA
                    analysis = evaluate_post(post["post_text"])
                    
                    if analysis.is_valid_prospect:
                        sub1, sub2 = st.columns(2)
                        with sub1:
                            st.markdown(f"**💡 Necesidad Detectada:**\n{analysis.problem_detected}")
                        with sub2:
                            st.markdown(f"**⚡ Nivel de Urgencia:** `{analysis.urgency}`")
                        
                        st.markdown(f"**💬 Mensaje Sugerido para Cierre de Venta:**")
                        st.info(analysis.suggested_message)
                        
                        # Disparar alertas reales
                        payload = {
                            "username": post["username"],
                            "platform": post["platform"],
                            "problem": analysis.problem_detected,
                            "urgency": analysis.urgency,
                            "post_text": post["post_text"],
                            "suggested_message": analysis.suggested_message
                        }
                        
                        send_whatsapp_alert(payload, post["post_url"])
                        send_email_alert(payload, post["post_url"])
                        
                    else:
                        st.error(f"❌ Descartado por el filtro de IA: {analysis.reasoning}")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 13px;'>Andalucía Beauty Intelligence Hub &copy; 2026 — Todos los derechos reservados.</div>", unsafe_allow_html=True)