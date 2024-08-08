import tabs as pg
import streamlit as st
from streamlit_option_menu import option_menu

style = """
<style>
# MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

pages = ["User Data", "Personality Based Questions", "Career Based Questions", "Report"]

with st.sidebar:
    selected = option_menu(
        "Navigate to",
        options=pages,
        # menu_icon="cast",
        default_index=0 if st.session_state.first_visit else st.session_state.selected_index,
        # expanded=True,
    )

st.session_state.selected_index = pages.index(selected)
st.session_state.first_visit = False

functions = {
    "User Data": pg.show_user_data,
    "Personality Based Questions": pg.show_p_qs,
    "Career Based Questions": pg.show_c_qs,
    "Report": pg.show_report,
}

go_to = functions.get(selected)
if go_to:
    try:
        go_to()
    except Exception as e:
        print(e)
