============================================================
SENSELINK: DEMO DE DETECCIÓN DE RIESGOS URBANOS
============================================================

Este directorio contiene la aplicación de demostración (Demo App) para visualizar 
el funcionamiento del modelo YOLO11n optimizado para Raspberry Pi Zero 2 W.

La aplicación utiliza Streamlit para ofrecer una interfaz web local donde se pueden 
cargar imágenes y videos para ver las detecciones y el tiempo de inferencia en tiempo real.

ESTRUCTURA DE CARPETAS
----------------------
SenseLink_Demo/
├── models/             # Debe contener tu archivo 'best.pt'
├── images/             # Imágenes de prueba listas para usar
├── app.py              # Código fuente de la aplicación
├── requirements.txt    # Lista de dependencias necesarias
└── README.txt          # Este archivo de instrucciones

REQUISITOS PREVIOS
------------------
- Python 3.8 o superior instalado en el sistema.
- Acceso a terminal o línea de comandos.

INSTRUCCIONES DE INSTALACIÓN
----------------------------

1. Abra una terminal en esta carpeta (Demo).

2. Cree un entorno virtual para aislar las librerías (Recomendado):
   
   Windows:
   python -m venv venv
   .\venv\Scripts\activate

   Mac/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. Instale las dependencias necesarias ejecutando:
   pip install -r requirements.txt

CÓMO EJECUTAR LA DEMO
---------------------

1. Una vez instaladas las dependencias, ejecute el siguiente comando:
   streamlit run app.py

2. Se abrirá automáticamente una pestaña en su navegador (usualmente http://localhost:8501).

3. En la interfaz:
   - Seleccione "Imagen Estática" o "Video" en el menú desplegable.
   - Arrastre o cargue los archivos desde la carpeta "images/" incluida en este paquete.
   - Presione el botón "🔍 Detectar Peligros".

CARACTERÍSTICAS DE LA DEMO
--------------------------
- Visualización lado a lado (Original vs Detección).
- Cálculo de tiempo de inferencia (ms) y FPS estimados.
- Ajuste de sensibilidad: Use el slider en la barra lateral izquierda para 
  filtrar detecciones con baja confianza (Umbral de Confianza).

SOLUCIÓN DE PROBLEMAS
---------------------
- Error "No se encontró el modelo": Asegúrese de que el archivo .pt se llame 
  exactamente 'best.pt' y esté dentro de la carpeta 'models/'.
- La app no abre: Verifique que no tenga otra instancia de Streamlit corriendo 
  en el mismo puerto. Presione Ctrl+C en la terminal para detenerla.
