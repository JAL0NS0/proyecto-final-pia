import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
from PIL import Image
import numpy as np
import time
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="SenseLink-AI Demo",
    page_icon="👁️",
    layout="wide"
)

# --- ESTILO CSS PERSONALIZADO (Opcional, para que se vea más Pro) ---
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        color: white;
        background-color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("👁️ SenseLink-AI")
st.sidebar.markdown("---")
st.sidebar.success("Estado: Sistema Listo")

# Configuración del Modelo
model_path = 'models/best.pt'  # <--- ASEGÚRATE QUE ESTA RUTA SEA CORRECTA

# Selector de confianza
conf_threshold = st.sidebar.slider(
    "Umbral de Confianza", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.25, 
    step=0.05
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Clases Detectables:")
classes = ["Semaforo Verde", "Semaforo Rojo", "Semaforo Amarillo", 
           "Escaleras", "Zebra", "Podotactil", "Bache"]
for c in classes:
    st.sidebar.markdown(f"- {c}")

# --- FUNCIÓN PARA CARGAR EL MODELO (Cacheada para velocidad) ---
@st.cache_resource
def load_model(path):
    try:
        model = YOLO(path)
        return model
    except Exception as e:
        return None

# --- LÓGICA PRINCIPAL ---
st.title("🚦 Demo de Detección de Riesgos Urbanos")
st.write("Sube una imagen o video para probar el modelo **YOLO11n** optimizado para Raspberry Pi.")

# Cargar modelo
model = load_model(model_path)

if model is None:
    st.error(f"❌ No se encontró el modelo en: {model_path}. Por favor verifica la ruta.")
else:
    # Selector de tipo de archivo
    option = st.selectbox("¿Qué deseas probar?", ("Imagen Estática", "Video"))

    # --- LÓGICA PARA IMÁGENES ---
    if option == "Imagen Estática":
        uploaded_file = st.file_uploader("Sube una foto...", type=['jpg', 'png', 'jpeg'])

        if uploaded_file is not None:
            # Mostrar imagen original y procesada en dos columnas
            col1, col2 = st.columns(2)
            
            with col1:
                image = Image.open(uploaded_file)
                st.image(image, caption='Imagen Original', use_container_width=True)
                
            # Botón para ejecutar
            if st.button("🔍 Detectar Peligros"):
                with st.spinner('Procesando...'):
                    # Inferencia
                    start_time = time.time()
                    results = model.predict(image, conf=conf_threshold)
                    end_time = time.time()
                    
                    # Extraer métricas de velocidad internas de YOLO
                    speed = results[0].speed
                    inference_time = speed['inference']
                    
                    # Plotear resultado
                    res_plotted = results[0].plot()
                    res_image = Image.fromarray(res_plotted[..., ::-1]) # Convertir BGR a RGB

                with col2:
                    st.image(res_image, caption='Detección SenseLink', use_container_width=True)
                
                # Mostrar Métricas
                st.markdown("### ⏱️ Métricas de Rendimiento")
                m1, m2, m3 = st.columns(3)
                m1.metric("Tiempo de Inferencia", f"{inference_time:.1f} ms")
                m2.metric("Velocidad Total", f"{(end_time - start_time)*1000:.1f} ms")
                m3.metric("Objetos Detectados", len(results[0].boxes))

    # --- LÓGICA PARA VIDEO ---
    elif option == "Video":
        uploaded_video = st.file_uploader("Sube un video MP4...", type=['mp4', 'avi', 'mov'])

        if uploaded_video is not None:
            # Guardar video temporalmente
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(uploaded_video.read())
            
            vf = cv2.VideoCapture(tfile.name)
            
            stframe = st.empty() # Placeholder para el video
            metrics_placeholder = st.empty() # Placeholder para métricas
            
            stop_button = st.button("⏹️ Detener Video")
            
            while vf.isOpened() and not stop_button:
                ret, frame = vf.read()
                if not ret:
                    break
                
                # Inferencia sobre el frame
                results = model.predict(frame, conf=conf_threshold)
                
                # Dibujar cajas
                frame_plotted = results[0].plot()
                
                # Calcular FPS instantáneos
                speed = results[0].speed
                inf_ms = speed['inference']
                fps = 1000.0 / (inf_ms + 0.1) # Evitar división por cero
                
                # Mostrar en Streamlit (Convertir BGR a RGB)
                stframe.image(frame_plotted, channels="BGR", use_container_width=True)
                
                # Actualizar métricas en tiempo real
                metrics_placeholder.markdown(f"""
                **Métricas en Vivo:**
                - Inferencia: `{inf_ms:.1f} ms`
                - FPS Estimados: `{fps:.1f}`
                """)
                
            vf.release()
            tfile.close()

# Footer
st.markdown("---")
st.caption("Desarrollado para el proyecto SenseLink - 2025")