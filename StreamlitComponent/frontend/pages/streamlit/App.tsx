import React, { useState, useEffect } from 'react';
import {
  withStreamlitConnection,
  ComponentProps,
  Streamlit,
} from 'streamlit-component-lib';

let numClicks: number = 0
let hostname: string = 'No Hostname'
let action: string = 'No Action'
let message: {} = {'ping': 'No Message'}

function App(props: ComponentProps) {

  const [state, setState] = useState({hostname: hostname, numClicks: numClicks, message: message, isError: false, error: ''})
  const [clicks, setClicks] = useState(numClicks)
  
  const initializeProps = (props: ComponentProps) => {
    if ('hostname' in props.args) {
      hostname = props.args.hostname
      delete props.args.hostname
    }
    if ('initial_state' in props.args) {
      message = props.args.initial_state['message']
      action = props.args.initial_state['action']
      setState({hostname: hostname, numClicks: clicks, message: message, isError: false, error: ''})
      delete props.args.initial_state
    }
  }

  const registerEventReporters = (props: ComponentProps) => {
    // register an event sender for each event
    if ("events" in props.args) {
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

  const reportEvent = (event_name: string, data: any) => {
    try {
      props.args.event_name(data)
    } catch {
      Streamlit.setComponentValue({name: event_name, data: data})
    }
  }

  initializeProps(props)
  registerEventReporters(props)

  useEffect(() => {
    Streamlit.setFrameHeight(80)
  })

  useEffect(() => {
    reportEvent('onStatusUpdate', state)
  }, [clicks])

  const handleStatusUpdate = async () => {
    setClicks(numClicks += 1)
    setState({hostname: hostname, numClicks: numClicks, message: message, isError: false, error: ''})
  }
  
  const handleDirectActionRequest = async () => {
    // Fetcher impl with browser fetch()
    const response = await fetch('http://localhost:8888/api/ping', {
      mode: 'cors' // allow CORS
    })
    const message = await response.json()
    console.log(message)
    setState({hostname: hostname, numClicks: numClicks, message: message, isError: false, error: ''})
  }

  const handleHostActionRequest = async () => {
    reportEvent('onActionRequest', {
      action: 'WebRequest',
      props: {
        label: 'Ping Flask Server',
        type: 'GET',
        url: 'http://localhost:8888/api/ping',
        headers: null,
        body: null
      }
    })
  }
  
  return (
    <div className="app">
      <header className="app-header">
          <div>
            <button onClick={() => handleStatusUpdate()} disabled={props.disabled}>
              {action}
            </button>
            {' | '}
            <button onClick={() => handleDirectActionRequest()} disabled={props.disabled}>
              Direct Action Request
            </button>
            {' | '}
            <button onClick={() => handleHostActionRequest()} disabled={props.disabled}>
              Host Action Request
            </button>
            <p/>
            <div>
              Host: {state.hostname} | Message: {state.message['ping']} | Clicks: {state.numClicks}
            </div>
          </div>
      </header>
    </div>
  );
}

export default withStreamlitConnection(App)

