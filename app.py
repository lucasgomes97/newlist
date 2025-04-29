import streamlit as st
from xhtml2pdf import pisa
import tempfile
import openai
import os
from dotenv import load_dotenv

# === CONFIGURAÇÕES ===

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para formatar texto estilo ABNT
def formatar_abnt(texto):
    parágrafos = texto.strip().split('\n')
    corpo = ''
    for p in parágrafos:
        p = p.strip()
        if p == '':
            continue
        if p.startswith('#'):
            titulo = p.replace('#', '').strip()
            corpo += f'<p style="text-align: center; font-weight: bold; font-family: Times New Roman; font-size: 12pt; margin-top: 12pt;">{titulo}</p>'
        else:
            corpo += f'<p style="text-align: justify; text-indent: 1.25cm; font-family: Times New Roman; font-size: 12pt; line-height: 1.5;">{p}</p>'
    
    html = f'''
    <html>
    <head>
        <style>
            @page {{
                margin-left: 3cm;
                margin-right: 2cm;
                margin-top: 3cm;
                margin-bottom: 2cm;
            }}
        </style>
    </head>
    <body>
        {corpo}
    </body>
    </html>
    '''
    return html

# Geração de PDF
def gerar_pdf(html):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pisa.CreatePDF(html, dest=tmp_file)
        return tmp_file.name

# Função OpenAI - geração de texto
def gerar_completado(texto_inicial):
    prompt = (
        "Prossiga com a continuação do texto a seguir de forma clara, formal e bem estruturada. "
        "Fundamente a resposta com base teórica sempre que possível, utilizando referências confiáveis. "
        "preferencialmente artigos científicos indexados em plataformas como o Google Scholar. "
        "Mostre as referências."
        "Mantenha a coerência textual e a consistência argumentativa ao desenvolver o conteúdo:\n\n"
        f"{texto_inicial}"
    )
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return resposta.choices[0].message.content.strip()

# Função OpenAI - correção ortográfica
def corrigir_texto(texto_original):
    prompt = f"Revise e corrija ortografia e gramática do texto abaixo, mantendo o sentido original:\n\n{texto_original}"
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1000
    )
    return resposta.choices[0].message.content.strip()


def obter_assuntos_em_alta():
    prompt = (
        "Liste de forma clara e objetiva os 10 assuntos mais comentados atualmente sobre tecnologia, "
        "incluindo temas que envolva assuntos como inteligência artificial, segurança digital, tendências em desenvolvimento de software, etc. Resumindo assuntos tech "
        "Apresente como uma lista breve e relevante para quem quer escrever conteúdo."
    )
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=500
    )
    return resposta.choices[0].message.content.strip()

# Interface Streamlit
st.set_page_config(
    page_title="Gerador de Conteúdo para Newlist",
    page_icon="https://raw.githubusercontent.com/lucasgomes97/newlist/main/logo.png",
    layout="wide"
) # Título da aba


# === Estilo personalizado: fundo preto e texto branco ===
st.markdown(
    """
    <style>
        .stApp {
            background-color: #030404;
            color: white;
        }

        h1, h2, h3, h4, h5, h6, p, div, label, input, textarea {
            color: white !important;
        }

        .stTextArea textarea {
            background-color: #222;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Adiciona título centralizado no topo da tela
st.markdown(
    '''
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="flex: 1; text-align: left;">
            <!-- Exibe a imagem diretamente com o método st.image -->
            <img src="https://raw.githubusercontent.com/lucasgomes97/newlist/main/ChatGPT%20Image%2029%20de%20abr.%20de%202025%2C%2011_13_54.png" width="150">
        </div>
        <div style="flex: 2; text-align: center;">
            <h1 style="font-family: Times New Roman; margin: 0;">Gerador de Conteúdo para Newlist</h1>
        </div>
        <div style="flex: 1;"></div>
    </div>
    ''',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.header("✍️ Digite seu texto")

    with st.expander("ℹ️ Dicas de uso"):
        st.markdown("""
        - Use `#` no início de uma linha para criar um **título centralizado em negrito**, isso se for gerar manualmente, caso use a IA não é necessário.
        - Pule uma linha clicando `Enter` entre parágrafos para separá-los corretamente.
        - ⚠️ A visualização será atualizada ao sair do campo ou pressionar `Ctrl+Enter`.
        - O texto será automaticamente formatado com:
            - Fonte **Times New Roman**, tamanho 12.
            - **Espaçamento 1,5** entre linhas.
            - Texto **justificado** com **recuo de parágrafo (1,25 cm)**.
        - Ao clicar em **Corrigir Ortografia**, o texto que você escreveu será revisado pela IA e corrigido, se usar as outras opções não precisa corrigir 😊.
        - Com **Gerar Continuação com IA**, o conteúdo que você escreveu será estendido automaticamente com base em artigos publicados no google scholar.
        - Ao Final tem a opção de exportar um `PDF` formatado onde você pode renomear seu arquivo.
        """)

    texto = st.text_area("Conteúdo:", height=370, placeholder="Digite aqui seu conteúdo...")

    col_sugestao, col_btn1, col_btn2 = st.columns([1.2, 1.5, 1.5])

with col_sugestao:
    if st.button("🔍 Não sabe sobre o que escrever ? Clique aqui e veja as  Tendências Atuais"):
        with st.spinner("🔄 Carregando tendências, por favor aguarde..."):
            sugestoes = obter_assuntos_em_alta()
            if texto.strip():
                texto += f"\n\n{sugestoes}"
            else:
                texto = sugestoes

with col_btn1:
    if st.button("🧠 Gerar Continuação com IA"):
        if texto.strip():
            with st.spinner("✍️ Gerando conteúdo com IA, por favor aguarde..."):
                texto_gerado = gerar_completado(texto)
                texto += "\n\n" + texto_gerado
        else:
            st.warning("Digite algo antes de gerar conteúdo.")

with col_btn2:
    if st.button("📝 Corrigir Ortografia"):
        if texto.strip():
            with st.spinner("🛠️ Corrigindo ortografia, por favor aguarde..."):
                texto = corrigir_texto(texto)
        else:
            st.warning("Digite algo antes de corrigir.")



with col2:
    st.header("📄 Visualização Formatada")
    if texto:
        html_formatado = formatar_abnt(texto)
        st.markdown(html_formatado, unsafe_allow_html=True)

        caminho_pdf = gerar_pdf(html_formatado)
        nome_pdf = st.text_input("📎 Nome do arquivo PDF", value="texto_abnt.pdf")

        if nome_pdf and not nome_pdf.endswith(".pdf"):
            nome_pdf += ".pdf"

        with open(caminho_pdf, "rb") as f:
            st.download_button("📥 Salvar PDF formatado", f, file_name=nome_pdf, mime="application/pdf")

    else:
        st.info("Digite algo ao lado para ver o resultado.")

