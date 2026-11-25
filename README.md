# 🥩 Bovinu'S Augusta — Controle de Buffet

Sistema desenvolvido durante o **Hackathon Tech FMU 2026.2**, com o objetivo de auxiliar no controle das quantidades de alimentos disponibilizadas no buffet e das sobras ao final das refeições.

## 📌 Sobre o projeto

O controle das quantidades de alimentos disponibilizadas e das sobras é importante para compreender melhor o funcionamento de um buffet.

O Bovinu'S Augusta propõe uma solução digital para registrar essas informações, calcular indicadores e organizar os dados, facilitando a análise e apoiando a tomada de decisões.

## 🎯 Problema identificado

A falta de um acompanhamento organizado das quantidades disponibilizadas e das sobras pode dificultar a análise do consumo do buffet e o planejamento das quantidades para futuras refeições.

## 💡 Nossa solução

Desenvolvemos uma aplicação em Python com interface web utilizando Streamlit, permitindo registrar os alimentos, informar as quantidades disponibilizadas e as sobras ao final da operação.

A partir desses registros, o sistema calcula o consumo aparente e o percentual de sobras, apresentando os resultados de forma organizada.

## ⚙️ Funcionalidades

- Cadastro de alimentos e refeições.
- Registro da quantidade disponibilizada.
- Registro da quantidade de sobras.
- Cálculo automático do consumo aparente.
- Cálculo do percentual de sobras.
- Histórico de registros.
- Filtro por tipo de refeição.
- Resumo das quantidades por alimento.
- Visualização gráfica dos resultados.
- Exportação dos dados em CSV.

## 🧮 Indicadores utilizados

**Consumo aparente:**

Quantidade disponibilizada − Quantidade de sobras.

**Percentual de sobras:**

(Quantidade de sobras ÷ Quantidade disponibilizada) × 100.

Esses indicadores ajudam a analisar a relação entre as quantidades disponibilizadas e as sobras registradas.

> **Importante:** O consumo apresentado é aparente, calculado a partir dos registros. O sistema não mede diretamente o que cada cliente consumiu.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento.
- **Streamlit:** criação da interface web.
- **Pandas:** organização e manipulação dos dados.
- **Matplotlib:** visualização gráfica.
- **GitHub:** versionamento e armazenamento do código.

## 📂 Estrutura do projeto

```text
hackathon-fmu-2026/
│
├── app.py
├── README.md
└── LICENSE
```

## 🚀 Como executar o projeto

1. Instale o Python.
2. Instale as dependências:

```bash
pip install streamlit pandas matplotlib
```

3. Execute o aplicativo:

```bash
streamlit run app.py
```

4. Acesse o endereço disponibilizado pelo Streamlit no navegador.

## 📊 Resultados e demonstração

**Capturas de tela:** serão adicionadas imagens da aplicação em funcionamento.

**Vídeo de demonstração:** link a ser adicionado.

**Apresentação do projeto:** arquivo a ser disponibilizado.

## 🔎 Limitações atuais

Nesta versão, os registros são mantidos durante a sessão de utilização da aplicação. Ainda não existe integração com um banco de dados para armazenamento permanente.

O sistema também não realiza pesagem automática nem identifica individualmente o consumo dos clientes. Os dados são informados manualmente pelo usuário.

## 👥 Desenvolvimento

Projeto desenvolvido para o **Hackathon Tech FMU 2026.2**, com foco em tecnologia aplicada à gestão e ao acompanhamento operacional da Bovinu'S.

---

**Bovinu'S Augusta — Tecnologia para apoiar decisões mais inteligentes.**
