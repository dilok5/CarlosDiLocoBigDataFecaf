import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Função para criar conexão com o banco de dados
def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        st.warning("DATABASE_URL não encontrada. Usando SQLite local.")
        return create_engine("sqlite:///temp_database.db")
    
    try:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        return create_engine(db_url)
    except Exception as e:
        st.error(f"Falha ao conectar ao banco de dados: {e}")
        return create_engine("sqlite:///temp_database.db")
     
def create_table(engine, df):
    # Envia os dados para a tabela
    df.to_sql('temperature_logs', engine, if_exists='replace', index=False)

# --- Interface Streamlit ---
st.title("🌡️ Dashboard IoT - Upload de Temperaturas")

uploaded_file = st.file_uploader("Upload do arquivo CSV (Kaggle)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # AJUSTE 1: Converter data para formato datetime
    if 'noted_date' in df.columns:
        df['noted_date'] = pd.to_datetime(df['noted_date'])
    
    st.subheader("Visualização prévia dos dados (Top 5)")
    st.write(df.head())
  
    engine = get_db_connection()
    
    try:
        # AJUSTE 2: Garantir que a tabela seja criada corretamente
        create_table(engine, df)
        st.success("Dados persistidos no PostgreSQL (Render) com sucesso.")
    
        # Busca os dados do banco para garantir que a leitura está vindo de lá
        query = "SELECT * FROM temperature_logs ORDER BY noted_date ASC"
        data = pd.read_sql(query, engine)
        
        st.divider() # Linha visual para separar as seções
        
        st.title("Visualização da Série Temporal")
        fig = px.line(data, 
                      x='noted_date', 
                      y='temp', 
                      title='Variação de Temperatura ao Longo do Tempo')
        
        fig.update_layout(xaxis_title="Data da Leitura", yaxis_title="Temperatura (°C)")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Erro na operação de banco de dados: {e}")