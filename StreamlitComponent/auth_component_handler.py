import requests
import json
import streamlit.components.v1 as components

from __init__ import session_state, check_token

from modules.auth0_login_component import run_login_component

# --------------------------------------------------------------------------------

EVENTS = ['onStatusUpdate', 'onAdhocReport', 'onActionRequest', 'onError']
PROPS = {'hostname':'Auth0 Login Demo App', 'initial_state': {'message': session_state.message}}

# --------------------------------------------------------------------------------
def handle_event(event):
    if not event:
        # return the preserved report
        return session_state.report
    
    name = event.name
    data = event.data

    report = []
    if (not name or not data):
        print('>>> WARNING! - Null name or data. <<<')
        report.append('>>> WARNING! - Null name or data. <<<')
        session_state.report = report
        return report

    props = data.get('props', None)
    action = data.get('action', None)

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
        elif action == 'UpdateTokenUserInfo':
            sessioninfo = data.get('sessioninfo', None)
            user = sessioninfo.get('user', None) if sessioninfo else None
            token = sessioninfo.get('token', None) if sessioninfo else None
            if (user and token and user['email'] and token['value']):
                session_state.email = user['email']
                session_state.user = user['name']
                session_state.token = token
            else:
                session_state.email = None
                session_state.user = None
                session_state.token = {'value': None, 'value_id_token': None, 'expiry': None}

    elif name == 'onStatusUpdate':
        sessioninfo = data.get('sessioninfo', None)
        user = sessioninfo.get('user', None) if sessioninfo else None
        token = sessioninfo.get('token', None) if sessioninfo else None
        if (user and token and user['email'] and token['value']):
            session_state.email = user['email']
            session_state.user = user['name']
            session_state.token = token
        else:
            session_state.email = None
            session_state.user = None
            session_state.token = {'value': None, 'value_id_token': None, 'expiry': None}

    session_state.report = report
    
    return report

# --------------------------------------------------------------------------------

def init():
    run_login_component(EVENTS, PROPS, handle_event)
