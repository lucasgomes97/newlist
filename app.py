import streamlit as st
from xhtml2pdf import pisa
import tempfile
import openai
import os
from dotenv import load_dotenv
import random

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
def gerar_Introdução(texto_inicial=""):
    prompt = (
        "Crie um parágrafo introdutório sob o título 'Resumo da newsletter', iniciando com a frase: "
        "'Na edição de hoje vamos...'. Apresente uma visão geral do conteúdo abordado de maneira bem resumida."
        f"\n\nTema base: {texto_inicial}"
    )
    return gerar_resposta(prompt)


def gerar_frase_motivacional():
    prompt = (
        "Crie uma frase motivacional inspirada no universo da Inteligência Artificial, podendo abordar inovações, "
        "aprendizados ou reflexões sobre o impacto da IA no mundo."
    )
    return gerar_resposta(prompt)


def gerar_tema_principal(texto_inicial=""):
    prompt = (
        "Desenvolva um artigo com o tema a seguir, com argumentação consistente, fundamentação teórica e baseado em fontes confiáveis, "
        "preferencialmente artigos científicos do Google Scholar. Traga bastante conteúdo rico, dados e explicações relevantes.\n\n"
        f"Tema: {texto_inicial}"
    )
    return gerar_resposta(prompt)


def gerar_ias_para_maiores():
    prompt = (
        "Liste e explique 3 principais notícias das últimas semanas no campo da Inteligência Artificial, "
        "com foco em impactos geopolíticos, automações ou movimentações de grandes empresas (big techs)."
    )
    return gerar_resposta(prompt)


CURSOS_JEDAI = [
    ("Caminhos Digitais: Marketing moldado para você", "https://jedai.ai/sabre/caminhos-digitais-marketing-moldado-para-voce/"),
    ("Observabilidade com IA", "https://jedai.ai/sabre/observabilidade-com-ia/"),
    ("Criação de Aplicações Interativas com Streamlit, API da OpenAI, Python e PostgreSQL", "https://jedai.ai/sabre/criacao-de-aplicacoes-interativas-com-streamlit-api-da-openai-python-e-postgresql/"),
    ("Programação com Inteligência Artificial simples para qualquer profissional - Muito além do ChatGPT", "https://jedai.ai/sabre/programacao-com-inteligencia-artificial-simples-para-qualquer-profissional-muito-alem-do-chatgpt//"),
    ("Pesquisa e Inteligência de Mercado com IA", "https://jedai.ai/sabre/pesquisa-e-inteligencia-de-mercado-com-ia/"),
    ("Geração em massa de Títulos e Meta Descriptions de textos de blog", "https://jedai.ai/sabre/geracao-em-massa-de-titulos-e-meta-descriptions-de-textos-de-blog/"),
    ("Preenchimento por Inteligência Artificial de Campos Anúncios Google Ads", "https://jedai.ai/sabre/preenchimento-por-inteligencia-artificial-de-campos-anuncios-google-ads/"),
    ("Geração em massa de Títulos e Meta Descriptions de blogs de todo SiteMap", "https://jedai.ai/sabre/geracao-em-massa-de-titulos-e-meta-descriptions-de-blogs-de-todo-sitemap/"),
    ("Programação com IA simples para qualquer profissional - Muito além do ChatGPT", "https://jedai.ai/sabre/programacao-com-chatgpt/"),
    # adicione mais cursos conforme necessário
]

def gerar_jedai():
    titulo, link = random.choice(CURSOS_JEDAI)
    prompt = (
        f"O curso '{titulo}' disponível na plataforma JedAI ({link}) é uma excelente oportunidade para aprofundar o conhecimento em Inteligência Artificial. "
        f"Escreva um texto explicando o que o curso aborda, por que ele é relevante, quem pode se beneficiar dele e como ele pode ser aplicado na prática de forma resumida e direta."
    )
    return gerar_resposta(prompt)


def gerar_comunidade():
    prompt = (
        "Convide o leitor a participar da nossa comunidade open source de IA, explicando objetivos, formas de contribuir e benefícios de fazer parte dessa rede colaborativa,de forma resumida e direta."
    )
    return gerar_resposta(prompt)


def gerar_referencias():
    prompt = (
        "Liste possíveis referências acadêmicas e artigos utilizados para embasar conteúdos relacionados à Inteligência Artificial."
    )
    return gerar_resposta(prompt)


# Função auxiliar para OpenAI
def gerar_resposta(prompt):
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700
    )
    return resposta.choices[0].message.content.strip()

# Função OpenAI - correção ortográfica
def corrigir_texto(texto_original):
    prompt = f"Revise e corrija ortografia e gramática do texto abaixo, mantendo o sentido original:\n\n{texto_original}"
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500
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
        temperature=0.7,
        max_tokens=500
    )
    return resposta.choices[0].message.content.strip()


def resumir_para_duas_paginas(texto_original):
    prompt = (
        f"Resuma o conteúdo a seguir de forma clara e objetiva, mantendo os principais títulos e conteúdo de cada seção. "
        "O resumo deve ter 3 páginas e deve incluir as seguintes seções, com os títulos e os principais conteúdos de cada uma, somente o Tema principal que não resuma, não precisa: \n"
        "- Resumo da newsletter\n"
        "- Frase motivacional\n"
        "- Tema principal\n"
        "- IAs para Maiores\n"
        "- Deep Learning com a JedAI\n"
        "- Comunidade de IA Open Source\n\n"
        "O objetivo é criar um texto conciso, informativo e bem estruturado, mantendo a essência de cada seção e sem perder "
        "os dados e argumentos relevantes. Certifique-se de que a estrutura das seções e os títulos sejam preservados de maneira clara.As referencias pode descartar. "
        f"\n\nConteúdo original:\n{texto_original}"
    )
    return gerar_resposta(prompt)

# Interface Streamlit
st.set_page_config(
    page_title="Gerador de Conteúdo para Newsletter",
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
            <h1 style="font-family: Times New Roman; margin: 0;">Gerador de Conteúdo para Newsletter </h1>
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
        - ⚠️ A visualização será atualizada ao clicar fora do campo ou pressionar `Ctrl+Enter`.
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
                # Parte do texto que não deve ser resumida (por exemplo, o tema principal)
                parte_nao_resumida = "<h2><strong>Tema principal</strong></h2>" + gerar_tema_principal(texto)
                
                # Outras partes que podem ser resumidas
                partes = [
                    "<h2><strong>Resumo da newsletter</strong></h2>" + gerar_Introdução(texto),
                    "<h2><strong>Frase motivacional</strong></h2>" + gerar_frase_motivacional(),
                    "<h2><strong>IAs para Maiores</strong></h2>" + gerar_ias_para_maiores(),
                    "<h2><strong>Deep Learning com a JedAI</strong></h2>" + gerar_jedai(),
                    "<h2><strong>Comunidade de IA Open Source</strong></h2>" + gerar_comunidade(),
                    "<h2><strong>Referências</strong></h2>" + gerar_referencias(),
                ]
                   # Junta as partes que devem ser resumidas em um só texto
                texto_completo = "\n\n" + "\n\n".join(partes)

                # Agora, resume o conteúdo para duas páginas
                texto_resumido = resumir_para_duas_paginas(texto_completo)
                
                # Junta a parte não resumida com o conteúdo resumido
                texto_final = parte_nao_resumida + "\n\n" + texto_resumido
                
                # Atualiza a variável texto
                texto = texto_final

                # Exibe o texto final no formato correto (ABNT)
                html_formatado = formatar_abnt(texto_final)
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

