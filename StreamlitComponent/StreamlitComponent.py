from pathlib import Path
from flask.globals import session
import requests
import time
from datetime import datetime
import json
import streamlit as st
import streamlit.components.v1 as components
from collections import namedtuple
import SessionState

import ptvsd
ptvsd.enable_attach(address=('localhost', 9004))
# ptvsd.wait_for_attach() # Only include this line if you always want to manually attach the debugger

# --------------------------------------------------------------------------------

st.set_page_config(
    page_title="Streamlit Component",
    initial_sidebar_state="expanded",
    layout="centered",
)
st.title('Streamlit Component')
hide_menu_style = """
    <style>
    #MainMenu {visibility: visible;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown('Experiments with Streamlit\'s component API')

# --------------------------------------------------------------------------------

# Session State variables:
# 
# "session_state.message" can be set to the response received from a web request
# delegated to the streamlit host by the hosted component. The response result is
# stored in session_state.message. A streamlit rerun is forced which causes the component
# to be remounted and session_state.message is plucked out and passed to the component.
session_state = SessionState.get(
    message='No Message',
    token={'value': None, 'expiry': datetime.now()},
    report=[],
    rerun=False
)

# --------------------------------------------------------------------------------

URL = 'http://localhost:3001/streamlit'

_RELEASE = False
if not _RELEASE:
    component_host = components.declare_component(name='ComponentHost', url=URL)
else:
    build_dir = (Path(__file__).parent/"frontend"/"build").resolve()
    component_host = components.declare_component(name='ComponentHost', path=build_dir)

DEFAULT_EVENTS = ['onStatusUpdate', 'onAdhocReport', 'onActionRequest', 'onError']

ComponentEvent = namedtuple('ComponentEvent', ['name', 'data', 'source'])

def ComponentHost(key=None, events=DEFAULT_EVENTS, **props):
    """Wrapper component for component_host.

    A generic remote component host, e.g. React app authenticating with Auth0 identity provider.

    All props are forwarded to the component. Methods are not supported.

    Parameters
    ----------
    key : str, optional
        Unique value to isolate multiple components in an app from each other.
    events : list, optional
        Events the host app subscribes to

    Returns
    -------
    ComponentEvent
        Object holding an event name (obj.event) and data (obj.data).
        Both attributes can be set to `None`.

    """
    # Allowed props
    props = {prop: value for prop, value in props.items() if prop in [
        'hostname', 'initial_state'
    ]}
    # Default prop value
    props.setdefault('hostname', 'Default Host')
    props.setdefault('initial_state', {'message': 'Default Message', 'action': 'Default Action'})
    props.setdefault('events', DEFAULT_EVENTS)
    props.setdefault("width", "100%") # built-in prop, height is set in the component itself

    # Run declared component
    event = component_host(key=key, **props) or {}

    # Filter by allowed events
    event_name = event.get('name', None)
    if event_name in events:
        return ComponentEvent(event_name, event.get('data', None), component_host)
    else:
        return ComponentEvent('onError', {'message': f'Component event {event_name} is not allowed.'}, component_host)

# --------------------------------------------------------------------------------

# Minimal event reporter
def handleEvent(event):

    if (not event) or session_state.rerun:
        # to ensure we don't rerun through this code
        session_state.rerun = False
        # return the preserved report (surviving the rerun)
        return session_state.report
    
    name = event.name
    data = event.data
    props = data.get('props', None)
    action = data.get('action', None)

    report = []
    report.append(name)
    report.append(data)

    if name == 'onActionRequest':
        if action == 'WebRequest':

            label = props['label']
            request_type = props.get('type', 'GET')
            url = props['url']
            headers = props.get('headers', {})
            data = props.get('data', None)
            useauth = props['useauth']
            auth_kind = props['auth_kind']

            if useauth:
                if check_token(session_state.token):
                    auth_header = {}
                    if auth_kind == 'BEARER':
                        auth_header = {"Authorization": f"Bearer {session_state.token['value']}"}
                    elif auth_kind == 'ACCESSTOKEN':
                        auth_header = {"accesstoken": f"{session_state.token['value']}"}
                    if headers:
                        headers.update(auth_header)
                    else:
                        headers = auth_header
                else:
                    report.append({'error': 'Authentication token not available or expired! Please log in.'})

                    return report

            if request_type.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif request_type.upper() == 'POST':
                response = requests.post(url, headers=headers, data=data)
            else:
                response = None

            if response and response.ok:
                text = json.loads(response.text)
            else:
                text = f'ERROR: {json.loads(response.text)}'

            signal_component_rerun_with_message(text)

            report.append(f'{label} Response: {text}')

        elif action == 'LoginAppRequest':
            components.iframe(src=props['login_url'], width=None, height=600, scrolling=True)

        elif action == 'LogoutAppRequest':
            components.iframe(src=props['logout_url'], width=None, height=600, scrolling=True)

    elif name == 'onStatusUpdate':
        token = data.get('token', None)
        if token:
            session_state.token = token

    session_state.report = report
    
    return report

def check_token(token):
    token_value = token['value']
    if token_value:
        token_expiry = datetime.fromtimestamp(int(token['expiry']))

        tnow = datetime.now()
        expired = tnow > token_expiry

        st.write('#### Access token')

        if not expired:
            st.info(f"Value: {token_value[0:60]}... \n\nExpiry: {token_expiry}")
            return True
        else:
            session_state.token['value'] = None
            st.info(f'Token expired on {token_expiry}!')
            return False

def run_component():
    if not _RELEASE:
        # Create instance of component with variable 'name_input'
        st.write('### _In Streamlit..._')
        name_input = st.text_input('Enter app name', value='Streamlit App')
        st.write('### _Next.js component below..._')
        event = ComponentHost(key='foo', events=DEFAULT_EVENTS, hostname=name_input, initial_state={'message': session_state.message, 'action': 'Click to force status update!'})
        st.write('### _In Streamlit..._')
        report = handleEvent(event)
        st.write('#### Component event handler report', report)

# HACK: Signals a one-time-only rerun of the component. This "simulates" passing a value from the
# component host (i.e. Streamlit app) _after_ the initialization of the component. With event passing
# from Component --> Host, we effectively have 2-way Component <--> Host communication!
def signal_component_rerun_with_message(item, add_to=False):
    if not session_state.rerun:
        session_state.rerun = True
        if add_to:
            if ( type(session_state.message) is dict and type(item) is dict):
                session_state.message.update(item)
            elif ( type(session_state.message) is list and type(item) is list):
                session_state.message.extend(item)
            elif ( type(session_state.message) is list):
                session_state.message.append(item)
            else:
                session_state.message = item
        else:
            session_state.message = item
    else:
        session_state.rerun = False

if __name__ == '__main__':
    run_component()
    if session_state.rerun:
        st.experimental_rerun()
    session_state.rerun = False
