
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
    if not db_url or "localhost" in db_url or "127.0.0.1" in db_url:
        # Se a variável não estiver definida ou apontar para localhost, use SQLite
        st.warning("DATABASE_URL não definida ou apontando para localhost. Usando SQLite.")
        db_url = "sqlite:///temp_database.db"
        st.info(f"Usando banco de dados local: {db_url}")
    else:
        st.info(f"Conectando ao banco de dados com URL: {db_url}")
    
    try:
        return create_engine(db_url)
    except Exception as e:
        st.error(f"Falha ao conectar ao banco de dados: {e}")
        st.warning("Alternando para banco de dados SQLite")
        return create_engine("sqlite:///temp_database.db")
     
# Função para criar tabela no PostgreSQL
def create_table(engine, df):
    df.to_sql('temperature_logs', engine,
        if_exists='replace', index=False)

# Upload do arquivo CSV
st.title("Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Upload CSV temperature data file",
        type="csv")

if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)
    st.write("Estrutura do Dataset:")
    st.write(df.head())
  
    # Conectar ao banco de dados
    engine = get_db_connection()
    
    if engine is not None:
        try:
            # Criar tabela no banco de dados
            create_table(engine, df)
            st.success("Dados enviados para o banco de dados.")
        
            # Ler dados do banco de dados
            query = "SELECT * FROM temperature_logs"
            data = pd.read_sql(query, engine)
        except Exception as e:
            st.error(f"Database operation failed: {e}")
            data = df  # Fall back to using the uploaded dataframe directly
    else:
        st.warning("Using uploaded data directly without database.")
        data = df
  
    # Visualização dos dados com Plotly
    st.title("Visualização dos Dados")
    fig = px.line(data,
                  x='noted_date',
                  y='temp',
                  title='Série Temporal de Temperaturas')
    st.plotly_chart(fig)
