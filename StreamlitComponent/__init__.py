import streamlit as st
from datetime import datetime

import modules
import utils

# --------------------------------------------------------------------------------
messageboard = st.empty()

from utils import SessionState
# Session State variables:
session_state = SessionState.get(
    message='To use this application, please login...',
    token={'value': None, 'value_id_token': None, 'expiry': None},
    user=None,
    email=None,
    report=[],
)

# --------------------------------------------------------------------------------
def check_token(token):
    token_value = token['value']
    if token_value:
        token_expiry = datetime.fromtimestamp(int(token['expiry']))

        tnow = datetime.now()
        expired = tnow >= token_expiry

        if not expired:
            return True
        else:
            session_state.token['value'] = None
            return False
    else:
        return False
