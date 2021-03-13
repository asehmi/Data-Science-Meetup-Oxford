import streamlit as st

def main(title):
    st.sidebar.header('Settings')

    actions = {'nothing': ':frowning:', 'something': ':smile:', 'everything': ':sunglasses:'}
    competence = st.sidebar.slider('Select competence level', min_value=1, max_value=3)
    action = list(actions.keys())[competence-1]

    st.title(title)
    st.write(f'## Welcome to another app that does {action}! {actions[action]}')
