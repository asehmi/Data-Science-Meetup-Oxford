from pathlib import Path
import requests
from datetime import datetime
import json
import streamlit as st
import streamlit.components.v1 as components
import asyncio

import SessionState

from LayoutAndStyleUtils  import (Grid, Cell, BlockContainerStyler)
BlockContainerStyler().set_default_block_container_style()

from app import messageboard
messageboard.empty()

# --------------------------------------------------------------------------------
# Session State variables:
session_state = SessionState.get(
    message='To use this application, please login...',
    token={'value': None, 'expiry': None},
    user=None,
    report=[],
)

# --------------------------------------------------------------------------------

USE_COMPONENT_EVENT_QUEUE = True

# --------------------------------------------------------------------------------
URL = 'http://localhost:3001/streamlit'

_RELEASE = False
if not _RELEASE:
    print('>>> CREATING COMPONENT (DEV) <<<')
    component_host = components.declare_component(name='ComponentHost', url=URL)
else:
    print('>>> CREATING COMPONENT (RELEASE) <<<')
    build_dir = (Path(__file__).parent/"frontend"/"build").resolve()
    component_host = components.declare_component(name='ComponentHost', path=build_dir)

# --------------------------------------------------------------------------------
# !! Changed to a class from namedtuple so it can be serialized by asyncio Queue.put() !!

# from collections import namedtuple
# ComponentEvent = namedtuple('ComponentEvent', ['name', 'data', 'source'])
class ComponentEvent():
    name = None
    data = None
    source = None
    def __init__(self, name, data, source):
        self.name = name
        self.data = data
        self.source = source

DEFAULT_EVENTS = ['onStatusUpdate', 'onAdhocReport', 'onActionRequest', 'onError']

# --------------------------------------------------------------------------------
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
    event_data = event.get('data', None)
    if event_name in events:
        return ComponentEvent(event_name, event_data, component_host)
    elif event_name: # ignores null event
        return ComponentEvent('onError', {'message': f"Component event {event_name} is not allowed. (Data: {event_data})"}, component_host)

# --------------------------------------------------------------------------------

def run_login_component():
    try:
        if USE_COMPONENT_EVENT_QUEUE:
            run_component_async()
        else:
            run_component_sync()
    except Exception as ex:
        print('>>> Exception running component <<<')
        print(str(ex))

# --------------------------------------------------------------------------------
# ASYNC QUEUE-BASED VERSION

async def component_event_consumer(queue):
    while True:
        event = await queue.get()
        report = handle_event(event)
        queue.task_done()
        print_report(report)

async def component_event_producer(queue):
    event = ComponentHost(key='login', events=DEFAULT_EVENTS, hostname='Web Scraper App', initial_state={'message': session_state.message})
    if event:
        await queue.put(event)

async def consumer_producer_runner():
    # In Streamlit context there might not be an event loop
    # present, so need to create one. (loop, consumers, producers, queue
    # must all be set up in the same awaitable thread!)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    queue = asyncio.Queue()

    consumer = asyncio.create_task(component_event_consumer(queue))
    producer = asyncio.create_task(component_event_producer(queue))
    await asyncio.gather(producer)
    await queue.join()
    consumer.cancel

# will terminate only when app is closed (i.e., there's no explicit producer/consumer thread termination)
def run_component_async():
    asyncio.run(consumer_producer_runner())

# --------------------------------------------------------------------------------
# SYNCHRONOUS VERSION

def run_component_sync():
    event = ComponentHost(key='login', events=DEFAULT_EVENTS, hostname='Web Scraper & Text Analysis', initial_state={'message': session_state.message})
    if event:
        report = handle_event(event)
        print_report(report)

# --------------------------------------------------------------------------------
def print_report(report):
    print(f'\n### [{datetime.now()}] Component event handler report ####')
    print(report)

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

# --------------------------------------------------------------------------------
def handle_event(event):
    if not event:
        # return the preserved report
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

            report.append(f'{label} Response: {text}')

        elif action == 'AppAuthRequest':
            components.iframe(src=props['auth_url'], width=None, height=600, scrolling=True)

        # TEST ACTION ONLY
        elif action == 'UpdateToken':
            token = data.get('token', None)
            if token and len(token['value']):
                session_state.token = token
                session_state.user = data.get('message', None)
            else:
                session_state.token={'value': None, 'expiry': None}
                session_state.user = None

    elif name == 'onStatusUpdate':
        token = data.get('token', None)
        if token and len(token['value']):
            session_state.token = token
            session_state.user = data.get('message', 'NO USER')
        else:
            session_state.token={'value': None, 'expiry': None}
            session_state.user = None

    session_state.report = report
    
    return report

