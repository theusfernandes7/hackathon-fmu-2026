# 🥩 Bovinu'S Augusta — Sistema de Gestão de Buffet

Sistema desenvolvido durante o **Hackathon FMU 2026**, com o objetivo de auxiliar a gestão operacional de um buffet por meio do controle de alimentos, refeições, sobras e acompanhamento de comandas.

O projeto utiliza Python, Streamlit, FastAPI e MySQL, integrando diferentes módulos em uma única solução.

---

## 📌 Sobre o projeto

O Bovinu'S Augusta possui dois módulos principais:

### 🍽️ 1. Controle de alimentos e refeições

Desenvolvido com Streamlit e integrado ao banco de dados MySQL.

Principais funcionalidades:

- Registro de alimentos disponibilizados.
- Seleção de refeições, como almoço e jantar.
- Registro da quantidade disponibilizada e das sobras.
- Cálculo do consumo aparente.
- Cálculo do percentual de sobras.
- Histórico de registros.
- Indicadores e gráficos.
- Exportação de dados em CSV.
- Persistência dos registros no MySQL.

### 📋 2. Controle de comandas

Desenvolvido com Streamlit e integrado à API FastAPI.

O módulo acompanha três etapas do atendimento:

| Etapa | Descrição |
|---|---|
| ENTRADA | Registra o início do atendimento. |
| PESAGEM | Registra o horário da pesagem e o tempo desde a entrada. |
| SAIDA | Finaliza o atendimento e calcula os tempos correspondentes. |

Principais funcionalidades:

- Registro das etapas das comandas.
- Identificação por código.
- Consulta de comandas em andamento.
- Acompanhamento do status.
- Armazenamento dos horários no MySQL.
- Cálculo dos tempos de atendimento.
- Exibição de indicadores e métricas.

---

## 🏗️ Arquitetura do sistema

O projeto utiliza três componentes principais:

| Componente | Tecnologia | Responsabilidade |
|---|---|---|
| Interface | Streamlit | Interface de interação com o usuário. |
| API | FastAPI | Processamento das etapas das comandas. |
| Banco de dados | MySQL | Armazenamento e consulta dos registros. |

### Fluxo de funcionamento

**Controle de alimentos:**

Streamlit → MySQL → armazenamento e consulta dos registros.

**Controle de comandas:**

Streamlit → FastAPI → MySQL → retorno das informações para a interface.

---

## 🗄️ Banco de dados

**Nome do banco:** `bobinus_augusta`

O banco possui as seguintes tabelas:

| Tabela | Finalidade |
|---|---|
| `alimentos` | Armazena os alimentos cadastrados. |
| `refeicoes` | Armazena os tipos de refeições. |
| `controle_refeicao` | Armazena os registros de disponibilização e sobras. |
| `sessoes_comanda` | Armazena as sessões e os tempos das comandas. |

São utilizados relacionamentos entre tabelas, chaves primárias e chaves estrangeiras para organizar os dados e manter sua integridade.

---

## 🛠️ Tecnologias utilizadas

- Python
- Streamlit
- FastAPI
- Uvicorn
- MySQL
- MySQL Connector/Python
- Pandas
- Matplotlib
- Requests

---

## 📁 Estrutura do projeto

```text
Bovinus_augusta/
│
├── app.py
├── Bovinus_Back.py
├── conexao.py
├── requirements.txt
├── README.md
│
├── pages/
│   └── 2_Controle_de_Comandas.py
│
├── screenshots/
│   └── Capturas de tela do sistema
│
└── presentation/
    └── Bovinus_Augusta_Slides.pptx
```

### Descrição dos arquivos

| Arquivo | Descrição |
|---|---|
| `app.py` | Aplicação principal de controle de alimentos e refeições. |
| `Bovinus_Back.py` | API responsável pelo processamento das comandas. |
| `conexao.py` | Configuração da conexão com o MySQL. |
| `requirements.txt` | Lista de dependências Python. |
| `pages/2_Controle_de_Comandas.py` | Página de controle e acompanhamento das comandas. |
| `screenshots/` | Capturas de tela das funcionalidades do sistema. |
| `presentation/` | Apresentação do projeto em PowerPoint. |

---

## 🚀 Como executar o projeto

### 1. Pré-requisitos

É necessário ter instalado:

- Python 3.
- MySQL Server.
- MySQL Workbench (recomendado).
- Git (opcional, para clonar o repositório).

### 2. Clonar o repositório

```bash
git clone https://github.com/theusfernandes7/hackathon-fmu-2026.git
```

Acesse a pasta:

```bash
cd hackathon-fmu-2026
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Inicie o MySQL Server.

O banco de dados `bobinus_augusta` e suas quatro tabelas precisam estar criados antes de executar a aplicação.

Confira as configurações de conexão nos arquivos:

- `conexao.py`
- `Bovinus_Back.py`

Configure host, porta, usuário, senha e nome do banco de acordo com seu ambiente MySQL.

### 5. Iniciar a API

Abra um terminal na pasta do projeto e execute:

```bash
python -m uvicorn Bovinus_Back:app --reload
```

A API ficará disponível localmente em:

`http://127.0.0.1:8000`

A documentação interativa dos endpoints estará disponível em:

`http://127.0.0.1:8000/docs`

### 6. Iniciar o Streamlit

Abra um segundo terminal na pasta do projeto e execute:

```bash
python -m streamlit run app.py
```

A aplicação ficará disponível localmente em:

`http://localhost:8501`

**Importante:** mantenha os dois terminais em execução durante o uso do sistema. A página de comandas depende da API FastAPI para funcionar.

---

## 🔌 Endpoints da API

A API disponibiliza os seguintes endpoints:

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/api/bip` | Registra uma etapa da comanda. |
| GET | `/api/comandas/ativas` | Consulta as comandas em andamento. |
| GET | `/api/metricas/resumo` | Consulta os indicadores de atendimento. |

### Exemplo de requisição

Registro de entrada de uma comanda:

```json
{
  "codigo": "TESTE001",
  "etapa": "ENTRADA"
}
```

As etapas utilizadas são:

- `ENTRADA`
- `PESAGEM`
- `SAIDA`

---

## 📊 Indicadores do sistema

### Controle de alimentos

- Quantidade total disponibilizada.
- Quantidade total de sobras.
- Consumo aparente.
- Percentual de sobras.

### Controle de comandas

- Total de sessões registradas.
- Total de comandas finalizadas.
- Média de tempo até a pesagem.
- Média de tempo após a pesagem.
- Média de tempo total.
- Maior tempo até a pesagem.
- Maior tempo total.

---

## 🧪 Testes realizados

Durante o desenvolvimento, foram realizados testes para verificar o funcionamento dos módulos e sua integração.

- Conexão entre Python e MySQL.
- Registro e consulta de alimentos e refeições.
- Persistência dos registros após atualização da aplicação.
- Consulta de dados utilizando `INNER JOIN`.
- Testes dos endpoints da API.
- Registro das etapas de entrada, pesagem e saída.
- Verificação dos horários e tempos calculados no banco de dados.
- Integração entre Streamlit e FastAPI.
- Consulta de comandas ativas.
- Consulta das métricas de atendimento.

---

## 🔒 Segurança e configuração

O projeto foi desenvolvido para execução local durante o hackathon.

As credenciais de acesso ao MySQL devem ser configuradas de acordo com o ambiente de execução.

Não publique senhas ou outras informações confidenciais no repositório.

A API e o banco de dados não devem ser expostos publicamente sem a implementação de autenticação e medidas adequadas de segurança.

---

## 👥 Desenvolvimento

**Projeto:** Bovinu'S Augusta  
**Evento:** Hackathon FMU 2026  
**Repositório:** [GitHub — Hackathon FMU 2026](https://github.com/theusfernandes7/hackathon-fmu-2026)

---

## 🎯 Objetivo

Desenvolver uma solução integrada para auxiliar a gestão de um buffet, facilitando o controle de alimentos, o acompanhamento de sobras e o monitoramento do atendimento por comandas, contribuindo para uma operação mais organizada e eficiente.

---

## 🎥 Demonstração do projeto

Vídeo demonstrativo do Bovinu'S Augusta, apresentando o funcionamento dos módulos de controle de refeições, sobras e comandas.

[▶️ Assistir ao vídeo de demonstração](https://drive.google.com/file/d/1fEn884S894wCfxtoM-kV2ullkdTs3AHO/view?usp=drivesdk)

---

## 📑 Apresentação do projeto

Os slides apresentam o problema identificado, a proposta da solução, as funcionalidades desenvolvidas, a arquitetura do sistema e os resultados da integração.

[📥 Visualizar apresentação do projeto (PowerPoint)](presentation/Bovinus_Augusta_Slides.pptx)

---

## 🖥️ Capturas de tela do sistema

### Controle de comandas

<img width="1280" height="800" alt="Controle das comandas" src="https://github.com/user-attachments/assets/6ed87c1d-07a6-4f8d-831f-049a54b4b968" />

### Métricas de comanda

<img width="1280" height="800" alt="Metricas da Comanda" src="https://github.com/user-attachments/assets/a2d0041c-43ae-45f5-b9bd-99df1c8527e0" />

### Relatório e exportação

<img width="1280" height="800" alt="Relatório e exportação" src="https://github.com/user-attachments/assets/412d0d10-6a77-4ec8-8e91-ee8d67df6a39" />

### Resumo por alimento

<img width="1280" height="800" alt="Resumo por alimento" src="https://github.com/user-attachments/assets/dd98cc28-903a-4da5-807d-b55f5a384d06" />

### Tela principal

<img width="1280" height="800" alt="Tela Principal" src="https://github.com/user-attachments/assets/f30294ec-b3f0-46a1-8a70-122fac7e5e4f" />
