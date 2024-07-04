
import tabs as pg
import streamlit as st
from streamlit_option_menu import option_menu

pages = ["User Data", "Career Based Questions", "Personality Based Questions", "Report"]

with st.sidebar:
    selected = option_menu(
        "Navigate to",
        options = pages,
        # menu_icon="cast",
        default_index=0,
        )

functions = {
    "User Data": pg.show_user_data,
    "Career Based Questions": pg.show_c_qs,
    "Personality Based Questions": pg.show_p_qs,
    "Report": pg.show_report,
}

go_to = functions.get(selected)
if go_to:
    try:
        go_to()
    except Exception as e:
        print(e)
