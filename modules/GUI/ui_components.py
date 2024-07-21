import streamlit as st
import random
import time

def init_page_config(page_config): ### Must be called before any other st. function
    st.set_page_config(page_title=page_config().get('page_title'), 
                page_icon = page_config().get('page_icon'),  
                layout = page_config().get('layout'),
                initial_sidebar_state = page_config().get('initial_sidebar_state'))
    
def display_sidebar(page_config):
    with st.sidebar:

        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(str(page_config().get('page_logo')), width=60)
        with col2:
            st.write(str(page_config().get('sidebar_title')))

        st.write(str(page_config().get('page_subtitle')))
        st.caption(str(page_config().get('page_description')))

        st.divider()

def init_session_state():
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4"