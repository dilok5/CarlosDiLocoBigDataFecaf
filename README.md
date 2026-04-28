 # 🌡️ Big Data FECAF - Dashboard IoT  Projeto focado na ingestão, persistência e visualização de dados de sensores IoT, desenvolvido para a disciplina de **Big Data**. A aplicação utiliza **Streamlit** para a interface, **PostgreSQL (Render)** para persistência e **Plotly** para análise gráfica. <img width="704" height="450" alt="newplot" src="https://github.com/user-attachments/assets/766e6f17-c352-471e-8b48-c8545129064c" />
 
 
 ## 🛠️ Tecnologias Utilizadas  * **Streamlit**: Framework de interface web.  * **Pandas**: Processamento e análise de dados.  * **SQLAlchemy**: Gestão de conexão com banco de dados.  * **PostgreSQL**: Banco de dados relacional hospedado no Render.com.  * **Plotly**: Geração de gráficos de séries temporais.  ---  ## 💻 Evolução do Desenvolvimento  Abaixo, apresento a comparação entre a primeira versão do sistema e a versão final otimizada, detalhando as melhorias de resiliência aplicadas.  ### Código Original  O código original era uma implementação direta para validar a conexão e o upload:  ```python  import streamlit as st  import pandas as pd  from sqlalchemy import create_engine  import plotly.express as px  import os  from dotenv import load_dotenv  load_dotenv()  # Função para criar conexão com o banco de dados  def get_db_connection():      return create_engine(os.getenv("DATABASE_URL"))  # Função para criar tabela no PostgreSQL  def create_table(engine, df):      df.to_sql('temperature_logs', engine, if_exists='replace', index=False)  # Upload do arquivo CSV  st.title("Upload de Arquivo CSV")  uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")  if uploaded_file is not None:      # Leitura do arquivo CSV      df = pd.read_csv(uploaded_file)      st.write("Estrutura do Dataset:")      st.write(df.head())      # Conectar ao banco de dados      engine = get_db_connection()      # Criar tabela no PostgreSQL      create_table(engine, df)      st.success("Dados enviados para o banco de dados.")      # Ler dados do banco de dados      query = "SELECT * FROM temperature_logs"      data = pd.read_sql(query, engine)      # Visualização dos dados com Plotly      st.title("Visualização dos Dados")      fig = px.line(data, x='noted_date', y='temp', title='Série Temporal de Temperaturas')      st.plotly_chart(fig)   `

### Código Atualizado (Versão Final)

A versão final inclui camadas de proteção contra falhas de conexão e suporte a banco de dados local (SQLite) caso a conexão externa falhe:

Python

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import streamlit as st  import pandas as pd  from sqlalchemy import create_engine  import plotly.express as px  import os  from dotenv import load_dotenv  # Carregar variáveis de ambiente  load_dotenv()  # Função para criar conexão com o banco de dados  def get_db_connection():      db_url = os.getenv("DATABASE_URL")      if not db_url or "localhost" in db_url or "127.0.0.1" in db_url:          # Se a variável não estiver definida ou apontando para localhost, use SQLite          st.warning("DATABASE_URL não definida ou apontando para localhost. Usando SQLite.")          db_url = "sqlite:///temp_database.db"          st.info(f"Usando banco de dados local: {db_url}")      else:          st.info(f"Conectando ao banco de dados com URL: {db_url}")      try:          return create_engine(db_url)      except Exception as e:          st.error(f"Falha ao conectar ao banco de dados: {e}")          st.warning("Alternando para banco de dados SQLite")          return create_engine("sqlite:///temp_database.db")  # Função para criar tabela no PostgreSQL  def create_table(engine, df):      df.to_sql('temperature_logs', engine, if_exists='replace', index=False)  # Upload do arquivo CSV  st.title("Upload de Arquivo CSV")  uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")  if uploaded_file is not None:      # Leitura do arquivo CSV      df = pd.read_csv(uploaded_file)      st.write("Estrutura do Dataset:")      st.write(df.head())      # Conectar ao banco de dados      engine = get_db_connection()      if engine is not None:          try:              # Criar tabela no banco de dados              create_table(engine, df)              st.success("Dados enviados para o banco de dados.")              # Ler dados do banco de dados              query = "SELECT * FROM temperature_logs"              data = pd.read_sql(query, engine)          except Exception as e:              st.error(f"Database operation failed: {e}")              data = df  # Fall back to using the uploaded dataframe directly      else:          st.warning("Using uploaded data directly without database.")          data = df      # Visualização dos dados com Plotly      st.title("Visualização dos Dados")      fig = px.line(data, x='noted_date', y='temp', title='Série Temporal de Temperaturas')      st.plotly_chart(fig)   `

📝 Comentários sobre as Mudanças
--------------------------------

### 1\. Conexão com o Banco de Dados

*   **Antes**: A função simplesmente capturava a URL da variável de ambiente DATABASE\_URL.
    
*   **Depois**: Implementação de lógica para verificar se a URL está definida ou se aponta para localhost. Caso a conexão externa não esteja disponível, o sistema alterna automaticamente para **SQLite**, mantendo a aplicação funcional em ambiente local. Mensagens de status (st.info, st.warning) foram adicionadas para transparência.
    

### 2\. Persistência e Tratamento de Erros

*   Adição de verificação de integridade do engine.
    
*   Implementação de blocos try/except para operações de banco de dados. Caso ocorra uma falha na criação da tabela ou na consulta, o sistema agora utiliza o DataFrame carregado na memória (data = df) como plano de contingência, evitando interrupções na visualização.
    

### 3\. Visualização

*   Melhoria no fluxo de dados: o gráfico agora busca as informações persistidas diretamente do banco de dados, validando o ciclo completo de ingestão e leitura da arquitetura de Big Data proposta.
    

🚀 Como Executar
----------------

1.  Clone o repositório.
    
2.  Instale as dependências: pip install -r requirements.txt.
    
3.  Configure o arquivo .env com sua DATABASE\_URL.
    
4.  Execute o comando: streamlit run main.py.
