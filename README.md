# bigdatafecaf.

![newplot](https://github.com/user-attachments/assets/7dfa1d62-cf1a-49a9-a966-c7bd3c936049)


Código Original:
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
    return create_engine(os.getenv("DATABASE_URL"))

# Função para criar tabela no PostgreSQL
def create_table(engine, df):
    df.to_sql('temperature_logs', engine, if_exists='replace', index=False)

# Upload do arquivo CSV
st.title("Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)
    st.write("Estrutura do Dataset:")
    st.write(df.head())
    
    # Conectar ao banco de dados
    engine = get_db_connection()
    
    # Criar tabela no PostgreSQL
    create_table(engine, df)
    st.success("Dados enviados para o banco de dados.")
    
    # Ler dados do banco de dados
    query = "SELECT * FROM temperature_logs"
    data = pd.read_sql(query, engine)
    
    # Visualização dos dados com Plotly
    st.title("Visualização dos Dados")
    fig = px.line(data, x='noted_date', y='temp', title='Série Temporal de Temperaturas')
    st.plotly_chart(fig)

Código Atualizado:

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
    df.to_sql('temperature_logs', engine, if_exists='replace', index=False)

# Upload do arquivo CSV
st.title("Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

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
    fig = px.line(data, x='noted_date', y='temp', title='Série Temporal de Temperaturas')
    st.plotly_chart(fig)

Comentários sobre as Mudanças:
Importação das Bibliotecas: Não houve mudanças.

Carregar Variáveis de Ambiente: Carregamento das variáveis de ambiente usando dotenv permanece o mesmo.

Função para Criar Conexão com o Banco de Dados:

Antes: A função simplesmente pegava a URL do banco de dados da variável de ambiente DATABASE_URL.

Depois: Adicionou lógica para verificar se a URL do banco de dados está definida ou se está apontando para localhost. Se estiver usando localhost, um banco de dados SQLite é usado como alternativa. Mensagens de aviso e informação são mostradas ao usuário através do Streamlit.

Função para Criar Tabela no PostgreSQL:

Permanece a mesma.

Upload do Arquivo CSV e Leitura:

Não houve mudanças.

Conectar ao Banco de Dados e Criar Tabela:

Adicionou lógica para verificar se o engine é None antes de tentar criar a tabela no banco de dados.

Adicionou tratamento de exceção ao tentar criar a tabela no banco de dados e, em caso de falha, usa o DataFrame carregado diretamente.

Visualização dos Dados com Plotly:

Não houve mudanças.