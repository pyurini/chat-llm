from openai import OpenAI
import streamlit as st

st.title("sabichão")

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

MODELOS = {
    "Nemotron 3.5 Lightning": "nvidia/nemotron-3.5-lightning:free",
    "Laguna S 2.1 (respostas mais rápidas)": "poolside/laguna-s-2.1:free",
    "Nemotron 3 Ultra (Processamento complexo, porém 30s para resposta)" : "nvidia/nemotron-3-ultra-550b-a55b:free",
    "Ling 3.0 Flash Fin (Finanças)": "inclusionai/ling-3.0-flash-fin:free",
    "Dots3-Note Preview (Raciocínio, Up de imagens e long context)": "dots-studio/dots-3-note-preview:free",
}

modelo_nome = st.selectbox(
    "Escolha o modelo",
    list(MODELOS.keys())
)

modelo = MODELOS[modelo_nome]

if "openrouter_model" not in st.session_state:
    st.session_state["openrouter_model"] = modelo

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        stream = client.chat.completions.create(
    model=modelo,
    messages=[
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ],
    stream=True,
)

        response = st.write_stream(stream)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })