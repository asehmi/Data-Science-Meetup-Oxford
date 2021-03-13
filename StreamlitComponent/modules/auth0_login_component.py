from datetime import datetime
import streamlit.components.v1 as components
import asyncio

import settings

# --------------------------------------------------------------------------------

USE_COMPONENT_EVENT_QUEUE = True
COMPONENT_URL = f'{settings.COMPONENT_BASE_URL}/streamlit'

print('>>> CREATING COMPONENT <<<')
component_host = components.declare_component(name='ComponentHost', url=COMPONENT_URL)

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

DEFAULT_EVENTS = ['onStatusUpdate', 'onActionRequest', 'onError']

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

def run_login_component(events, props, event_handler):
    try:
        if USE_COMPONENT_EVENT_QUEUE:
            run_component_async(events, props, event_handler)
        else:
            run_component_sync(events, props, event_handler)
    except Exception as ex:
        print('>>> Exception running component <<<')
        print(str(ex))

# --------------------------------------------------------------------------------
# ASYNC QUEUE-BASED VERSION

async def component_event_consumer(queue, event_handler):
    while True:
        event = await queue.get()
        try:
            report = event_handler(event)
        except Exception as ex:
            print('>> Exception in event handler <<', str(ex))
            report = ['>> Exception in event handler <<', str(ex)]
        queue.task_done()
        print_report(report)

async def component_event_producer(queue, events, props):
    event = ComponentHost(key='login', events=events, **props)
    if event:
        await queue.put(event)

async def consumer_producer_runner(events, props, event_handler):
    # In Streamlit context there might not be an event loop
    # present, so need to create one. (loop, consumers, producers, queue
    # must all be set up in the same awaitable thread!)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    queue = asyncio.Queue()

    consumer = asyncio.create_task(component_event_consumer(queue, event_handler))
    producer = asyncio.create_task(component_event_producer(queue, events, props))
    await asyncio.gather(producer)
    await queue.join()
    consumer.cancel

# will terminate only when app is closed (i.e., there's no explicit producer/consumer thread termination)
def run_component_async(events, props, event_handler):
    asyncio.run(consumer_producer_runner(events, props, event_handler))

# --------------------------------------------------------------------------------
# SYNCHRONOUS VERSION

def run_component_sync(events, props, event_handler):
    event = ComponentHost(key='login', events=events, **props)
    if event:
        try:
            report = event_handler(event)
        except Exception as ex:
            print('>> Exception in event handler <<', str(ex))
            report = ['>> Exception in event handler <<', str(ex)]
        print_report(report)

# --------------------------------------------------------------------------------
def print_report(report):
    print(f'\n### [{datetime.now()}] Component event handler report ####')
    print(report)

