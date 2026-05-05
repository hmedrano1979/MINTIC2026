import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import requests

# -------------------------------------------------------------------------
# PROYECTO: ANALÍTICA AVANZADA CONTRA LA CORRUPCIÓN (PIDA)
# ENFOQUE: DETECCIÓN DE ANOMALÍAS Y ANÁLISIS ESTRUCTURAL
# -------------------------------------------------------------------------

def cargar_datos():
    print("🚀 Conectando con el Portal de Datos Abiertos de Colombia...")
    url = "https://www.datos.gov.co/resource/k5ma-yb9b.json?$limit=5000"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data)
        print(f"✅ Datos cargados exitosamente: {df.shape[0]} registros encontrados.")
        return df
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return None

def preprocesamiento(df):
    print("🛠️ Iniciando limpieza y preprocesamiento técnico...")
    # Eliminar columnas con demasiados nulos
    df = df.dropna(axis=1, thresh=int(0.5*len(df)))
    
    # Codificación de variables categóricas para el modelo
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna('No disponible')
        df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
    
    return df

def detectar_anomalias(df):
    print("🤖 Ejecutando Modelo de Machine Learning: Isolation Forest...")
    # Seleccionar solo columnas numéricas/codificadas para el modelo
    features = df.select_dtypes(include=[np.number]).columns
    model = IsolationForest(contamination=0.05, random_state=42)
    
    df['score_anomalia'] = model.fit_predict(df[features])
    # -1 son anomalías, 1 es comportamiento normal
    anomalias = df[df['score_anomalia'] == -1]
    print(f"⚠️ Se han detectado {len(anomalias)} registros con patrones atípicos/potencial riesgo.")
    return df, anomalias

def generar_visualizaciones(df):
    print("📊 Generando reportes visuales de impacto...")
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # Ejemplo: Distribución de registros por alguna categoría (ajustar según columnas reales)
    if 'entidad' in df.columns:
        df['entidad'].value_counts().head(10).plot(kind='bar', color='#0ea5e9')
        plt.title("Top 10 Entidades en el Dataset PIDA")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    df_raw = cargar_datos()
    if df_raw is not None:
        df_proc = preprocesamiento(df_raw)
        df_final, riesgos = detectar_anomalias(df_proc)
        generar_visualizaciones(df_final)
        print("\n🏆 PROYECTO FINALIZADO: El desarrollo está listo para auditoría estratégica.")
