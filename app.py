import streamlit as st
import json
from pages_PD.upload_page import PD_process
from streamlit_option_menu import option_menu

if "password" not in st.session_state:
    st.session_state["password"] = ""


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Пароль", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Неверный пароль")
    return False


def main(config):
    st.set_page_config(
    page_title="Parkinson-web",
    layout="wide",
    initial_sidebar_state="expanded",)

    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    if not check_password():
        st.stop()
    with st.sidebar:        
            app = option_menu(
                menu_title='Проект PD',
                options=['Загрузка Видео'],
                icons=['bi bi-1-square-fill','bi bi-2-square-fill'],
                default_index=0,
                styles={"container": {"padding": "5!important","background-color":'gray'},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"color":"white","font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},
        "menu-title": {"color": "white", "font-size": "21px"},
        "menu-title-icon": {"display": "none"} }
                
                )
    if app == 'Загрузка Видео':
        PD_process(config)


if __name__ == "__main__":
    # Загрузка конфигурации программы:
    with open("configs/config.json", "r", encoding="utf-8") as json_file:
        config = json.load(json_file)
    main(config)
    