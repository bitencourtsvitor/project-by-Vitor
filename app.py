import streamlit as st
import google.generativeai as genai


genai.configure(api_key=st.secrets["general"]["api_key"])
model = genai.GenerativeModel('models/gemini-2.5-flash')  # <-- linha corrigida

st.set_page_config(page_title="CineIA", page_icon="🎬")
st.title("🎬 CineIA: Seu Próximo Filme")
st.markdown("Descubra filmes baseados no seu estado de espírito atual.")

with st.sidebar:
    st.header("Preferências")
    genero = st.multiselect("Gêneros favoritos:",
                            ["Ação", "Drama", "Sci-Fi", "Comédia", "Terror", "Documentário"])
    tempo = st.slider("Duração máxima (minutos):", 60, 240, 120)

mood = st.text_area("Descreva como você está se sentindo ou o que busca no filme:",
                    placeholder="Ex: Quero um filme de ficção científica com reviravoltas na história.")

botao_recomendar = st.button("Buscar Recomendações")

if botao_recomendar:
    if not mood:
        st.warning("Por favor, descreva o que você deseja assistir!")
    else:
        with st.spinner("Analisando catálogo cinematográfico..."):
            prompt = f"""
            Você é um especialista em cinema.
            Recomende 3 filmes para alguém que gosta de {', '.join(genero)} e que durem até {tempo} minutos.
            O usuário descreveu o clima do filme como: '{mood}'.
            Para cada filme, forneça: Título, Ano e uma frase curta do porquê combina com o pedido.
            """
            try:
                response = model.generate_content(prompt)
                st.success("Aqui estão minhas sugestões:")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")

st.caption("Desenvolvido na disciplina de IHC – Graduação em IA e Ciência de Dados – Universidade Franciscana (UFN)")
