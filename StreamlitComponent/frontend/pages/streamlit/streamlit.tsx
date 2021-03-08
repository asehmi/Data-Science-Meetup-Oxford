import React, { useState, useEffect } from 'react'
import {
  withStreamlitConnection,
  ComponentProps,
  Streamlit,
} from 'streamlit-component-lib'

import STORAGE from '../../utils/storage'

// All values in seconds
const HEARTBEAT_INTERVAL_SECONDS = 5

const FRAME_HEIGHT = 45

const StreamlitComponent = (props: ComponentProps) => {

  console.log('======== Streamlit component ========')

  const getToken = async () => {
    const ret = await STORAGE.getItem('token')
    return ret
  }
  const getTokenExpiry = async () => {
    const ret = await STORAGE.getItem('tokenExpiry')
    return ret
  }
  const getUserInfo = async () => {
    // const resp = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/me`)
    // const me = await resp.json()
    const user = await STORAGE.getItem('user')
    console.log('STC getUserInfo: ' + user)
    const me = JSON.parse(String(user))
    if (me) {
      const name = me.name || `${me.given_name} ${me.family_name}` || me.nickname || me.email
      const email = me.email || me.sub
      console.log('STC getUserInfo: ' + name + ' | ' + email)
      return { user: name, email: email }
    } else {
      return { user: null, email: null }
    }
  }

  const [heartbeater, setHeartbeater] = useState(true)

  const [hostname, setHostname] = useState('None')
  const [message, setMessage] = useState('None')
  const [userInfo, setUserInfo] = useState({ user: null, email: null })
  const [token, setToken] = useState(null)
  const [tokenExpiry, setTokenExpiry] = useState(null)
  const [state, setState] = useState({
    hostname: hostname, message: message, isError: false, error: null,
    token: { value: null, expiry: null },
    userinfo: null
  })

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
      Streamlit.setComponentValue({ name: name, data: data })
    } else {
      Streamlit.setComponentValue({ name: 'onError', data: data })
    }
  }

  const updateStateAndNotifyHost = async (msg: string = null, error: string = null) => {
    setMessage(msg || message)
    try {
      const _userInfo = await getUserInfo()
      setUserInfo(_userInfo)
      const _token = await getToken()
      setToken(_token)
      const _tokenExpiry = await getTokenExpiry()
      setTokenExpiry(_tokenExpiry)
      var _state = {
        hostname: hostname, message: msg || message, isError: false, error: error,
        token: { value: _token, expiry: _tokenExpiry }, userinfo: _userInfo
      }
      setState(_state)
    } catch (err) {
      console.log(`updateStateAndNotifyHost error: ${err}`)
    }
    await sendEvent('onStatusUpdate', _state)
  }

  // !! This function is the main driver of events in this component !!
  // Must be run inside useEffect hook... see below hook with heartbeater dependency
  // (i.e. runs everytime the beat pulses)
  const listenForTokenChangeAndNotifyHost = async () => {
    const heartbeat = setTimeout(async () => {

      const currToken = await getToken()
      console.log(`>> STC BEAT << (${token}, ${currToken})`)
      if (token !== currToken) {
        // logged in change
        if (currToken) {
          console.log('STC User, Token, Expiry set')
          updateStateAndNotifyHost('Logged in')
        // logged out change
        } else {
          console.log('STC User, Token, Expiry cleared')
          updateStateAndNotifyHost('Logged out')
        }
      }

      // Ping the component API every second beat to keep the server alive!
      if (heartbeater) {
        const resp = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/ping`)
        const ping = await resp.json()
        console.log(ping)
      }

      // Simulate a pulse by flip-flopping the flag; this drives the useEffect hook
      setHeartbeater(!heartbeater)

    }, HEARTBEAT_INTERVAL_SECONDS * 1000)

    return heartbeat
  }

  useEffect(() => {
    const heartbeat = listenForTokenChangeAndNotifyHost()
    heartbeat.then(() => clearTimeout())
  }, [heartbeater])

  // One shot initializer for props
  useEffect(() => {
    initializeProps(props)
    Streamlit.setFrameHeight(FRAME_HEIGHT)
  }, [])

  // One shot initializer for state
  useEffect(() => {
    const initState = async () => {
      try {
        const _userInfo = await getUserInfo()
        setUserInfo(_userInfo)
        const _token = await getToken()
        setToken(_token)
        const _tokenExpiry = await getTokenExpiry()
        setTokenExpiry(_tokenExpiry)
      } catch (err) {
        console.log(`useEffect initializer error: ${err}`)
      }
    }
    initState()
  }, [])

  useEffect(() => {
    updateStateAndNotifyHost()
  }, [hostname])

  // ----------------------------------------------------

  // Many examples here: https://stackoverflow.com/questions/847185/convert-a-unix-timestamp-to-time-in-javascript
  const timestampToDateString = (timestamp: string): string => {
    const a = new Date(parseInt(timestamp) * 1000)
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const year = a.getFullYear()
    const month = months[a.getMonth()]
    const date = a.getDate()
    const hour = a.getHours()
    const min = a.getMinutes()
    const sec = a.getSeconds()
    const time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec
    return time
  }

  const handleLoginWindowOpener = async () => {
    const W = 425
    const H = 525

    // Fixes dual-screen position                             Most browsers      Firefox
    const dualScreenLeft = window.screenLeft !==  undefined ? window.screenLeft : window.screenX
    const dualScreenTop = window.screenTop !==  undefined   ? window.screenTop  : window.screenY

    const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width
    const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height

    const systemZoom = 1
    // const systemZoom = width / window.screen.availWidth
    const left = (width - W) / 2 / systemZoom + dualScreenLeft
    const top = (height - H) / 2 / systemZoom + dualScreenTop
    const settings = `scrollbars=yes, width=${W / systemZoom}, height=${H / systemZoom}, top=${top}, left=${left}`
    // console.log(settings)
    const popup = window.open('/','_blank', settings)

    if (window.focus) popup.focus()
  }

  // ----------------------------------------------------

  return (
    <header>
      <span className="text-md text-pink-600">
        <button onClick={handleLoginWindowOpener}>{token ? 'Logout' : 'Login'}</button>
      </span>
      <span className="text-md text-gray-600">
        {' | '}{hostname} {tokenExpiry ? ` (current login valid till ${timestampToDateString(tokenExpiry)})` : ' (logged out)'}
      </span>
    </header>
  )
}

export default withStreamlitConnection(StreamlitComponent)
