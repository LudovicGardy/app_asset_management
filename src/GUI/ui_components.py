import streamlit as st


def init_page_config(page_config):  ### Must be called before any other st. function
    st.set_page_config(
        page_title=page_config().get("page_title"),
        page_icon=page_config().get("page_icon"),
        layout=page_config().get("layout"),
        initial_sidebar_state=page_config().get("initial_sidebar_state"),
    )


def display_sidebar(self, page_config):
    self.openai_api_key = ""

    with st.sidebar:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(str(page_config().get("page_logo")), width=60)
        with col2:
            st.write(str(page_config().get("sidebar_title")))

        st.write(str(page_config().get("page_subtitle")))
        st.caption(str(page_config().get("page_description")))

        st.divider()
        with st.expander("Chatbot (Optionnel)"):
            self.chatbot_checkbox = st.checkbox("Activer le chat bot", False)
            self.selected_model = st.selectbox(
                "Modèle",
                ["GPT 3.5", "GPT 4", "Llama2-7B", "Llama2-13B", "Mistral"],
                index=1,
            )
            self.model_api_key = st.text_input(
                "Entrez une clé API 🔑",
                type="password",
                help="Trouvez votre clé [OpenAI](https://platform.openai.com/account/api-keys) ou [Replicate](https://replicate.com/account/api-tokens).",
            )
            st.info(
                "ℹ️ Votre clé API n'est pas conservée. Elle sera automatiquement supprimée lorsque vous fermerez ou rechargerez cette page."
            )

            if self.chatbot_checkbox:
                if "GPT" in self.selected_model:
                    if not self.model_api_key:
                        st.warning("⚠️ Entrez une clé API **Open AI**.")
                else:
                    # st.warning('⚠️ Entrez une clé API **Repliacte**.')
                    st.error(
                        "⚠️ Ce modèle n'est pas encore disponible. Veuillez utiliser GPT."
                    )
                # st.stop()

            # st.markdown('Pour obtenir une clé API, rendez-vous sur le site de [openAI](https://platform.openai.com/api-keys).')

    return self


def init_session_state():
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4"
