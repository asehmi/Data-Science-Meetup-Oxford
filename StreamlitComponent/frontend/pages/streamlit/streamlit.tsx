import React, { useState, useEffect } from 'react';
import {
  withStreamlitConnection,
  ComponentProps,
  Streamlit,
} from 'streamlit-component-lib';
import MyButton from '../../components/MyButton'

function StreamlitComponent(props: ComponentProps) {

  console.log('======== Streamlit component ========')

  const [hostname, setHostname] = useState('None')
  const [message, setMessage] = useState('None')
  const [action, setAction] = useState('None')
  
  const initializeProps = (props: ComponentProps) => {
    if ('hostname' in props.args && 'initial_state' in props.args) {
      setHostname(props.args.hostname)
      setMessage(props.args.initial_state['message'])
      setAction(props.args.initial_state['action'])
      delete props.args.hostname
      delete props.args.initial_state
    }
  }

  const [clicks, setClicks] = useState(0)
  const [token, setToken] = useState(window.localStorage.getItem('token'))
  const [tokenExpiry, setTokenExpiry] = useState(window.localStorage.getItem('tokenExpiry'))
  const [state, setState] = useState({ hostname: hostname, clicks: clicks, message: message, isError: false, error: null,
                                       token: { value: window.localStorage.getItem('token'),
                                                expiry: window.localStorage.getItem('tokenExpiry') } })

  const registerEventReporters = (props: ComponentProps) => {
    // register an event sender for each event
    if ('events' in props.args) {
      props.args.events.forEach((event: string) => {
        props.args[event] = (data?: any) => {
          Streamlit.setComponentValue({
            name: event,
            data: data
          })
        }
      })
      delete props.args.events
    }
  }

  const reportAdHocEvent = (data: any) => {
    Streamlit.setComponentValue({name: 'onAdhocReport', data: data})
  }

  initializeProps(props)
  registerEventReporters(props)

  useEffect(() => {
    Streamlit.setFrameHeight(250)
  }, [])

  useEffect(() => {
    console.log('Access token: ' + (token ? token.slice(0,10) + '...' : 'No token in localStorage!'))
    console.log('Access token expiry: ' + (tokenExpiry ? tokenExpiry + '...' : 'No token expiry in localStorage!'))
  }, [clicks, token])

  useEffect(() => {
    updateStateAndNotifyHost()
  }, [hostname])

  const updateStateAndNotifyHost = async (msg: string = null, hostUpdate: boolean = true, error: string = null) => {
    var _message = msg || message
    setMessage(_message)
    setClicks(state.clicks + 1)
    setToken(window.localStorage.getItem('token'))
    setTokenExpiry(window.localStorage.getItem('tokenExpiry'))
    var _state = { hostname: hostname, clicks: state.clicks + 1, message: _message, isError: false, error: error,
                   token: { value: window.localStorage.getItem('token'), expiry: window.localStorage.getItem('tokenExpiry') } }
    setState(_state)

    if (hostUpdate) {
      props.args.onStatusUpdate(_state)
    }
  }
  
  const handleClicks = async () => {
    updateStateAndNotifyHost()
  }

  const handleDirectActionRequest = async () => {
    const response = await fetch('/api/ping', {
      mode: 'cors' // allow CORS
    })
    const message = await response.json()
    updateStateAndNotifyHost(message)
  }

  const handleDirectActionRequestAuth = async () => {
    const response = await fetch('/api/pong', {
      mode: 'cors', // allow CORS
      headers: {'accesstoken': token}
    })
    const message = await response.json()
    var error = null
    if (message.error) {
      error = 'Authentication token not available or expired! Please log in.'
    }
    updateStateAndNotifyHost(message, true, error)
  }

  const handleHostActionRequest = async () => {
    props.args.onActionRequest({
      action: 'WebRequest',
      props: {
        label: 'Ping Next.js Server API',
        request_type: 'GET',
        url: 'http://localhost:3001/api/ping',
        headers: null,
        data: null,
        useauth: false,
        auth_kind: 'ACCESSTOKEN',
      }
    })
    updateStateAndNotifyHost(null, false)
  }
  
  const handleHostActionRequestAuth = async () => {
    props.args.onActionRequest({
      action: 'WebRequest',
      props: {
        label: 'SECURE Ping Next.js Server API',
        request_type: 'GET',
        url: 'http://localhost:8888/api/pong',
        headers: null,
        data: null,
        useauth: true,
        auth_kind: 'BEARER',
      }
    })
    updateStateAndNotifyHost(null, false)
  }
  
  const handleLoginAppRequest = async () => {
    props.args.onActionRequest({
      action: 'LoginAppRequest',
      props: {
        label: 'Login requested',
        type: 'GET',
        login_url: 'http://localhost:3001/api/login',
      }
    })

    // Wait till token appears in localstorage
    let retries = 20
    let ready = false
    while (!ready && retries > 0) {
      console.log('Waiting for token ' + '++++++++++++++++++++'.slice(0,retries))
      try {
          if (window.localStorage.getItem('token')) {
            ready = true
          } else {
            await new Promise(r => setTimeout(r, 2000));
            retries -= 1
          }
        } catch {
          await new Promise(r => setTimeout(r, 2000));
          retries -= 1
        }
    }

    updateStateAndNotifyHost()
  }
  
  const handleLogoutAppRequest = async () => {
    window.localStorage.removeItem('token')
    window.localStorage.removeItem('tokenExpiry')

    props.args.onActionRequest({
      action: 'LogoutAppRequest',
      props: {
        label: 'Logout requested',
        type: 'GET',
        logout_url: 'http://localhost:3001/api/logout',
      }
    })

    updateStateAndNotifyHost()
  }
  
  // Many examples here: https://stackoverflow.com/questions/847185/convert-a-unix-timestamp-to-time-in-javascript
  const timestampToDateString = (timestamp: string): string => {
    var a = new Date(parseInt(timestamp) * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
  }

  return (
    <header>
        <div className="container my-4 ml-1 max-w-xl space-x-4">
          <MyButton label='API call by component' onClickHandler={handleDirectActionRequest} props={props} />
          <MyButton label='API call by component (authenticated using Auth0)' onClickHandler={handleDirectActionRequestAuth} props={props} />
        </div>
        <div className="container my-4 ml-1 max-w-xl space-x-4">
          <MyButton label='API call via Streamlit host' onClickHandler={handleHostActionRequest} props={props} />
          <MyButton label='API call via Streamlit host (authenticated using Auth0)' onClickHandler={handleHostActionRequestAuth} props={props} />
        </div>
        <div className="container my-4 ml-1 max-w-xl space-x-4">
          <MyButton label={action} onClickHandler={handleClicks} props={props} />
          {!token && (<MyButton label='Login' onClickHandler={handleLoginAppRequest} props={props} />)}
          {token && (<MyButton label='Logout' onClickHandler={handleLogoutAppRequest} props={props} />)}
        </div>
        <p/>
        <div className="text-xs text-indigo-700">
          Host: {hostname} | Message: {JSON.stringify(state.message)} | Clicks: {clicks}<br/>
          Token: {token ? token.slice(0,60) + '...' : 'NULL'} | Expiry: {tokenExpiry ? timestampToDateString(tokenExpiry) : 'NULL'}
        </div>
    </header>
  );
}

export default withStreamlitConnection(StreamlitComponent)

