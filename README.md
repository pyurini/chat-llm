# Sabichão - Chat Local com LLMs via Streamlit e OpenRouter

<p align="center">
  <img src="https://img.shields.io/badge/Python-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit Version">
  <img src="https://img.shields.io/badge/OpenRouter-API-orange?logo=openai&logoColor=white" alt="OpenRouter API">

## Sobre o Projeto

**Sabichão** é um chatbot local desenvolvido com [Streamlit](https://streamlit.io/) que permite interagir com diversos modelos de linguagem (LLMs) através da [API do OpenRouter](https://openrouter.ai/). O projeto oferece uma interface simples e intuitiva para conversar com diferentes modelos de IA gratuitos, incluindo modelos especializados para finanças, raciocínio complexo e geração de imagens.

A aplicação mantém o histórico da conversa na sessão do Streamlit e exibe as respostas do modelo em tempo real, por meio de streaming.

---

## Começando

### Pré-requisitos

- Python 3.9 ou superior
- Conta no [OpenRouter](https://openrouter.ai/)
- Chave de API do OpenRouter

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/pyurini/chat-llm.git
cd chat-llm
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure sua chave de API do OpenRouter:

Crie um arquivo `.streamlit/secrets.toml` na raiz do projeto:

```toml
OPENROUTER_API_KEY = "sua-chave-api-aqui"
```

> Se estiver implantando na Streamlit Cloud, configure essa mesma chave em **Settings → Secrets** do app, em vez de versionar o arquivo `secrets.toml`.

5. Execute a aplicação:

```bash
streamlit run main.py
```

---

## Uso

Após iniciar a aplicação:

1. Selecione um modelo de linguagem na lista suspensa.
2. Digite sua pergunta ou mensagem no campo de entrada (chat input).
3. Aguarde a resposta em tempo real (streaming).

O histórico da conversa é mantido em `st.session_state` enquanto a sessão do navegador estiver ativa. Ao recarregar a página, o histórico é reiniciado.

### Modelos disponíveis

| Modelo | Identificador (OpenRouter) | Descrição |
|---|---|---|
| Nemotron 3.5 Lightning | `nvidia/nemotron-3.5-lightning:free` | Modelo NVIDIA rápido e eficiente |
| Laguna S 2.1 | `poolside/laguna-s-2.1:free` | Respostas mais rápidas para consultas gerais |
| Nemotron 3 Ultra | `nvidia/nemotron-3-ultra-550b-a55b:free` | Processamento complexo (resposta em até 30s) |
| Ling 3.0 Flash Fin | `inclusionai/ling-3.0-flash-fin:free` | Especializado em finanças |
| Dots3-Note Preview | `dots-studio/dots-3-note-preview:free` | Raciocínio avançado, suporte a imagens e contexto longo |

> Todos os modelos listados usam o sufixo `:free` do OpenRouter. Disponibilidade e limites de uso podem mudar conforme a política do provedor vale conferir o [catálogo de modelos](https://openrouter.ai/models) antes de publicar a aplicação.

---

## Configuração

### Variáveis de ambiente / secrets

A aplicação lê a chave de API a partir de `st.secrets`, não de uma variável de ambiente do sistema operacional. Certifique-se de que o arquivo `.streamlit/secrets.toml` contenha:

```toml
OPENROUTER_API_KEY = "sua_chave_api_openrouter"
```

### Estrutura de arquivos

```
chat-llm/
├── main.py              # Aplicação principal
├── .streamlit/
│   └── secrets.toml    # Configurações secretas (não versionar)
└──README.md
└── requirements.txt    # Dependências do projeto
```

### `Secrets.toml`
Para ser possível inserir sua própria api key e usar as variáveis do código basta renomear a pasta **.streamlit-example** e seu arquivo **example-secrets.toml** retirando a palavra "example" de seus nomes. Assim colocando sua chave api do Open router e utilizando seus modelos.

### `requirements.txt`

```txt
streamlit
openai
```

---

### Observação sobre o modelo selecionado

Atualmente, `st.session_state["openrouter_model"]` é definido **apenas na primeira execução** (bloco `if "openrouter_model" not in st.session_state`) e nunca é atualizado depois. Como a chamada à API usa a variável local `modelo` (recalculada a cada rerun a partir do `selectbox`), trocar o modelo na interface já funciona corretamente para as próximas mensagens mas o valor salvo em `st.session_state["openrouter_model"]` fica desatualizado e não é usado em nenhum outro lugar do código. Se a intenção é apenas manter o nome do modelo atual disponível na sessão (por exemplo, para exibir em outro componente), vale substituir o bloco por:

```python
st.session_state["openrouter_model"] = modelo
```

sem a condicional, para que ele reflita sempre o modelo selecionado.

---

## Opções de implementações futuras

- Adicionar botão para limpar o histórico da conversa (`st.session_state.messages = []`).
- Tratar erros de chamada à API (rate limit, chave inválida, modelo indisponível).
- Persistir o histórico entre sessões (arquivo local ou banco de dados).
- Exibir o modelo atualmente selecionado na barra lateral (`st.sidebar`).
- Adicionar carregamento de mídia.
- Contador de tokens gastos
---