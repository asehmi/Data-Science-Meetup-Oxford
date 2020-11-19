import os
import requests
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
)
st.title('Streamlit Component')
hide_menu_style = """
    <style>
    #MainMenu {visibility: visible;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown('Experiments with Streamlit\'s componenent API')

# --------------------------------------------------------------------------------

# session state variables
session_state = SessionState.get(delegated_web_request_result={'ping': 'No Message'}, rerun=False)

# --------------------------------------------------------------------------------

URL = 'http://localhost:3001/streamlit'
PROXY_URL = 'http://localhost:9009/app'

_RELEASE = False
if not _RELEASE:
    component_host = components.declare_component(name='ComponentHost', url=URL)
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, 'frontend/build')
    component_host = components.declare_component(name='ComponentHost', path=build_dir)

DEFAULT_EVENTS = ['onStatusUpdate', 'onError', 'onActionRequest']

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
        'hostname', 'initial_state', 'delegated_same_origin_web_response'
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
        return ComponentEvent('onError', f'Component event {event_name} is not allowed.', component_host)

# --------------------------------------------------------------------------------

# Minimal event reporter
def handleEvent(event):
    if not event:
        return []
    
    report = []
    if event.name == 'onActionRequest':
        report.append(f'Action Request: {event.name}')
        report.append(event.data)

        if event.data['action'] == 'WebRequest':
            response = requests.get(event.data['props']['url'])
            text = json.loads(response.text)

            session_state.delegated_web_request_result = text

            label = event.data['props']['label']
            report.append(f'{label} Response: {text}')

    elif event.name:
        report.append(event.name)
        report.append(event.data)

    return report

def run_component():
    if not _RELEASE:
        # Create instance of component with variable 'name_input'
        st.write('### _In Streamlit..._')
        name_input = st.text_input('Enter app name', value='Streamlit App')
        st.write('### _In React component..._')
        event = ComponentHost(key='foo', events=DEFAULT_EVENTS, hostname=name_input, initial_state={'message': session_state.delegated_web_request_result, 'action': 'Click Me!'})
        st.write('### _In Streamlit..._')
        report = handleEvent(event)
        st.write('#### Component event handler report', report)

if __name__ == '__main__':
    run_component()

    if not session_state.rerun:
        session_state.rerun = True
        st.experimental_rerun()
    else:
        session_state.rerun = False
