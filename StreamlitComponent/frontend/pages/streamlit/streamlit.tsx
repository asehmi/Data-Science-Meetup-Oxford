import React, { useState, useEffect } from 'react';
import {
  withStreamlitConnection,
  ComponentProps,
  Streamlit,
} from 'streamlit-component-lib';
import MyButton from '../../components/MyButton'

// All values in seconds
const HEARTBEAT_INTERVAL = 5
const WAIT_INTERVAL = 2
const LISTENER_TIMEOUT = 120

const SHOW_UI = false
const FRAME_HEIGHT = SHOW_UI ? 80 : 45

const StreamlitComponent = (props: ComponentProps) => {

  console.log('======== Streamlit component ========')

  // return something "falsy", but not null
  const getToken = () => { return window.localStorage.getItem('token') || '' }
  const getTokenExpiry = () => { return window.localStorage.getItem('tokenExpiry') || '' }

  const [heartbeatInterval, setHeartbeatInterval] = useState(HEARTBEAT_INTERVAL)

  const [hostname, setHostname] = useState('None')
  const [message, setMessage] = useState('')
  const [token, setToken] = useState(getToken())
  const [tokenExpiry, setTokenExpiry] = useState(getTokenExpiry())
  const [state, setState] = useState({ hostname: hostname, message: message, isError: false, error: null,
                                       token: { value: getToken(), expiry: getTokenExpiry() } })

  const initializeProps = async (props: ComponentProps) => {
    if ('hostname' in props.args && 'initial_state' in props.args) {
      setHostname(props.args.hostname)
      setMessage(props.args.initial_state['message'])
      delete props.args.hostname
      delete props.args.initial_state
    }
  }

  const sendEvent = async (name: string, data: any) => {
    if (props.args.events.includes(name)) {
      Streamlit.setComponentValue({name: name, data: data})
    } else {
      Streamlit.setComponentValue({name: 'onError', data: data})
    }
  }

  // Can be run outside useEffect hook
  const listenForTokenChangeWithTimeout = async () => {
    let listenerTimeout = LISTENER_TIMEOUT
    while (listenerTimeout > 0) {
      console.log('tokenChangeListenerWithTimeout')
      if (token != getToken()) {
        setToken(getToken())
        break
      }
      await new Promise(r => setTimeout(r, 1000));
      listenerTimeout -= 1
    }
  }

  // Must be run inside useEffect hook
  const listenForTokenChangeAndNotifyHost = async () => {
    if (heartbeatInterval > 0) {
      setTimeout(() => setHeartbeatInterval(heartbeatInterval - 1), 1000)
    } else {
      if (token != getToken()) {
        if (getToken()) { // logged in change
          const resp = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/me`)
          const me = await resp.json()
          updateStateAndNotifyHost(me.given_name || me.name || me.nickname || me.email)
        } else {          // logged out change
          updateStateAndNotifyHost('')
        }
      }
      setHeartbeatInterval(HEARTBEAT_INTERVAL)
    }
  }

  const updateStateAndNotifyHost = async (msg: string = null, error: string = null) => {
    var _message = msg || message
    setMessage(_message)
    setToken(getToken())
    setTokenExpiry(getTokenExpiry())
    var _state = { hostname: hostname, message: _message, isError: false, error: error,
                   token: { value: getToken(), expiry: getTokenExpiry() } }
    setState(_state)

    await sendEvent('onStatusUpdate', _state)
  }
  
  // TEST ONLY ------------------------------------------
  const handleLoginRequest = async () => {
    await sendEvent('onActionRequest', {
      action: 'AppAuthRequest',
      props: {
        label: 'Authentication requested',
        type: 'GET',
        auth_url: `${process.env.NEXT_PUBLIC_API_BASE_URL}`,
      }
    })

    await listenForTokenChangeWithTimeout()

    console.log('CALLING UpdateToken onActionRequest')
    await sendEvent('onActionRequest', {
      action: 'UpdateToken',
      token: { value: getToken(), expiry: getTokenExpiry() },
    })

    // Requires wait else st comms channel swallows messages
    await new Promise(r => setTimeout(r, WAIT_INTERVAL * 1000));

    console.log('CALLING updateStateAndNotifyHost')
    await updateStateAndNotifyHost()
  }

  // TEST ONLY ------------------------------------------
  const handleLogoutRequest = async () => {
    await sendEvent('onActionRequest', {
      action: 'AppAuthRequest',
      props: {
        label: 'Authentication requested',
        type: 'GET',
        auth_url: `${process.env.NEXT_PUBLIC_API_BASE_URL}`,
      }
    })

    await listenForTokenChangeWithTimeout()

    console.log('CALLING UpdateToken onActionRequest')
    await sendEvent('onActionRequest', {
      action: 'UpdateToken',
      token: { value: getToken(), expiry: getTokenExpiry() },
    })
  }
  
  // TEST ONLY ------------------------------------------
  const handleSendTokenUpdateAction = async () => {
    console.log('CALLING UpdateToken onActionRequest')

    await sendEvent('onActionRequest', {
      action: 'UpdateToken',
      token: { value: getToken(), expiry: getTokenExpiry() },
    })

    // Requires wait else st comms channel swallows messages
    await new Promise(r => setTimeout(r, WAIT_INTERVAL * 1000));

    setToken(getToken())
    setTokenExpiry(getTokenExpiry())

    console.log('CALLING updateStateAndNotifyHost')
    await updateStateAndNotifyHost()
  }
  // ----------------------------------------------------

  // Many examples here: https://stackoverflow.com/questions/847185/convert-a-unix-timestamp-to-time-in-javascript
  const timestampToDateString = (timestamp: string): string => {
    const a = new Date(parseInt(timestamp) * 1000);
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const year = a.getFullYear();
    const month = months[a.getMonth()];
    const date = a.getDate();
    const hour = a.getHours();
    const min = a.getMinutes();
    const sec = a.getSeconds();
    const time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
  }

  useEffect(() => {
    initializeProps(props)
    Streamlit.setFrameHeight(FRAME_HEIGHT)
  }, [])

  useEffect(() => {
    listenForTokenChangeAndNotifyHost()
  })

  useEffect(() => {
    console.log('Access token: ' + (token ? token.slice(0,10) + '...' : 'No token in localStorage!'))
    console.log('Access token expiry: ' + (tokenExpiry ? tokenExpiry + '...' : 'No token expiry in localStorage!'))
  }, [token, tokenExpiry])

  useEffect(() => {
    updateStateAndNotifyHost()
  }, [hostname])
 
  return (
    <header>
        <div className="container my-0 max-w-xl space-x-3">
          {SHOW_UI && (<MyButton label='Login' onClickHandler={handleLoginRequest} props={props}/>)}
          {SHOW_UI && (<MyButton label='Logout' onClickHandler={handleLogoutRequest} props={props}/>)}
          {/* TEST ONLY --------------------------------------------------------------------------------------- */}
          {/* <MyButton label='Send Token Update' onClickHandler={handleSendTokenUpdateAction} props={props} /> */}
          {/* ------------------------------------------------------------------------------------------------- */}
        </div>
        <p/>
        <div className="text-md text-pink-600">
        {message || hostname} | {token ? 'You\'re logged in and authorized to use the app.' : 'Signed out.'}{tokenExpiry ? ' | Token expires on ' + timestampToDateString(tokenExpiry) : ''}
        </div>
    </header>
  );
}

export default withStreamlitConnection(StreamlitComponent)
