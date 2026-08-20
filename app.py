import streamlit as st
import pdfplumber
import plotly.express as px
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="Nestlé AI | Sustentabilidade & ESG",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #6B4C2A; }
    .stButton > button {
        background-color: #003F87;
        color: white;
        border: none;
        border-radius: 4px;
    }
    .stButton > button:hover {
        background-color: #002966;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #6B4C2A;
        border-radius: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003F87;
        color: white;
    }
    div[data-testid="metric-container"] {
        background-color: #F5F0EB;
        border: 1px solid #6B4C2A;
        border-radius: 8px;
        padding: 16px;
    }
    div[data-testid="metric-container"] label {
        color: #6B4C2A;
        font-weight: bold;
    }
    div[data-baseweb="radio"] input:checked + div {
        background-color: #003F87 !important;
        border-color: #003F87 !important;
    }
    div[data-baseweb="radio"] input + div {
        border-color: #6B4C2A !important;
    }
</style>
""", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo.png", width=120)
with col_title:
    st.title("Nestlé | Assistente de Sustentabilidade com IA Generativa")
    st.markdown("Demonstração de como a IA Generativa pode transformar relatórios e dashboards de ESG em respostas automáticas, insights e análises operacionais.")

st.divider()

tab1, tab2 = st.tabs(["Dashboard ESG", "Assistente IA"])

MARROM = "#6B4C2A"
AZUL = "#003F87"
MARROM_CLARO = "#A0785A"
AZUL_CLARO = "#6699CC"

with tab1:
    st.subheader("Dashboard de Sustentabilidade, Nestlé 2023")
    st.markdown("*KPIs extraídos do Creating Shared Value & Sustainability Report 2023*")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Redução de Emissões GEE", "-13,4%", "vs 2018")
    col2.metric("Agricultores em Prog. Regenerativo", "688.000", "+95.000 vs 2022")
    col3.metric("Embalagens Recicláveis", "82,5%", "+4,5% vs 2022")
    col4.metric("Famílias Cacau Beneficiadas", "142.000", "+12.000 vs 2022")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        df_ghg = pd.DataFrame({
            "Ano": [2018, 2019, 2020, 2021, 2022, 2023],
            "Emissões (Mt CO2e)": [92.4, 88.1, 84.3, 80.9, 82.1, 80.0]
        })
        fig1 = px.line(df_ghg, x="Ano", y="Emissões (Mt CO2e)",
                      title="Evolução das Emissões de GEE (Mt CO2e)",
                      markers=True,
                      color_discrete_sequence=[MARROM])
        fig1.add_hline(y=46.2, line_dash="dash", line_color=AZUL,
                      annotation_text="Meta 2030: -50%")
        fig1.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        df_agri = pd.DataFrame({
            "Ano": [2020, 2021, 2022, 2023],
            "Agricultores (mil)": [186, 372, 593, 688]
        })
        fig2 = px.bar(df_agri, x="Ano", y="Agricultores (mil)",
                     title="Agricultores em Programas Regenerativos (mil)",
                     color="Agricultores (mil)",
                     color_continuous_scale=[MARROM_CLARO, MARROM])
        fig2.add_hline(y=500, line_dash="dash", line_color=AZUL,
                      annotation_text="Meta 2025: 500k")
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        df_emb = pd.DataFrame({
            "Categoria": ["Recicláveis", "Em transição", "Não recicláveis"],
            "Percentual (%)": [82.5, 10.2, 7.3]
        })
        fig3 = px.pie(df_emb, values="Percentual (%)", names="Categoria",
                     title="Status das Embalagens Nestlé 2023",
                     color_discrete_sequence=[MARROM, AZUL, MARROM_CLARO])
        fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        df_energy = pd.DataFrame({
            "Fonte": ["Energia Renovável", "Energia Convencional"],
            "Percentual (%)": [64.3, 35.7]
        })
        fig4 = px.pie(df_energy, values="Percentual (%)", names="Fonte",
                     title="Matriz Energética Nestlé 2023",
                     color_discrete_sequence=[MARROM, AZUL_CLARO])
        fig4.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.info("É exatamente sobre esses dados que a IA Generativa atuaria, respondendo perguntas, identificando desvios em relação às metas, gerando relatórios automáticos e prevendo cenários futuros. Acesse a aba Assistente IA para ver na prática.")

with tab2:
    st.subheader("Assistente de IA Generativa")
    st.markdown("Faça perguntas sobre os dados do dashboard ou carregue o relatório PDF da Nestlé.")

    modo = st.radio("Como você quer interagir?",
                    ["Perguntar sobre o Dashboard", "Carregar Relatório PDF"])

    if modo == "Perguntar sobre o Dashboard":
        st.markdown("**Exemplos de perguntas:**")
        st.markdown("- Qual é o progresso da Nestlé em relação à meta de redução de emissões?")
        st.markdown("- Como está a evolução dos agricultores em programas regenerativos?")
        st.markdown("- Quais ações você recomenda para acelerar a reciclabilidade das embalagens?")
        st.markdown("- A Nestlé vai atingir a meta de 500k agricultores em 2025?")

        pergunta = st.text_input("Faça sua pergunta sobre os dados de sustentabilidade:")

        dados_dashboard = """
        KPIs Nestlé Sustentabilidade 2023, Creating Shared Value Report:

        EMISSOES DE GEE:
        Redução total desde 2018: -13,4%
        Meta 2030: reduzir 50% vs 2018
        Evolução: 2018: 92,4 Mt, 2019: 88,1 Mt, 2020: 84,3 Mt, 2021: 80,9 Mt, 2022: 82,1 Mt, 2023: 80,0 Mt

        AGRICULTURA REGENERATIVA:
        Agricultores no programa 2023: 688.000
        Meta 2025: 500.000 (ja superada)
        Evolução: 2020: 186k, 2021: 372k, 2022: 593k, 2023: 688k

        EMBALAGENS:
        Reciclaveis ou reutilizaveis: 82,5%
        Em transição: 10,2%
        Nao reciclaveis: 7,3%
        Meta 2025: 100% reciclaveis ou reutilizaveis

        ENERGIA:
        Energia renovavel: 64,3%
        Energia convencional: 35,7%

        IMPACTO SOCIAL:
        Familias de produtores de cacau beneficiadas: 142.000
        Crescimento vs 2022: +12.000 familias
        """

        if st.button("Perguntar", type="primary"):
            if not pergunta:
                st.error("Digite uma pergunta.")
            else:
                with st.spinner("Analisando os dados e gerando resposta..."):
                    resposta = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "Você é um assistente especialista em sustentabilidade e ESG da Nestlé. Analise os dados fornecidos e responda de forma objetiva, com insights relevantes, comparações com as metas e recomendações práticas quando pertinente."
                            },
                            {
                                "role": "user",
                                "content": f"Com base nos dados de sustentabilidade abaixo, responda: {pergunta}\n\nDADOS:\n{dados_dashboard}"
                            }
                        ]
                    )
                    st.success("Resposta gerada!")
                    st.markdown("### Resposta:")
                    st.markdown(resposta.choices[0].message.content)

    else:
        uploaded_file = st.file_uploader("Carregue o Relatório de Sustentabilidade da Nestlé (PDF)", type="pdf")
        pergunta = st.text_input("Qual é sua pergunta sobre o relatório?",
                                placeholder="Ex: Quais são as metas de redução de emissões até 2030?")

        if st.button("Perguntar", type="primary"):
            if not uploaded_file:
                st.error("Carregue um PDF primeiro.")
            elif not pergunta:
                st.error("Digite uma pergunta.")
            else:
                with st.spinner("Analisando o documento..."):
                    texto = ""
                    with pdfplumber.open(uploaded_file) as pdf:
                        for page in pdf.pages:
                            texto += page.extract_text() or ""

                    texto_limitado = texto[:12000]

                    resposta = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "Você é um assistente especialista em sustentabilidade e ESG da Nestlé. Responda perguntas com base nos dados fornecidos do relatório oficial. Seja objetivo, use dados numéricos quando disponíveis e forneça insights relevantes."
                            },
                            {
                                "role": "user",
                                "content": f"Com base nos dados abaixo do relatório da Nestlé, responda: {pergunta}\n\nDADOS DO RELATÓRIO:\n{texto_limitado}"
                            }
                        ]
                    )

                    st.success("Resposta gerada!")
                    st.markdown("### Resposta:")
                    st.markdown(resposta.choices[0].message.content)

st.divider()
st.markdown("*Protótipo desenvolvido por Natália Santana*")