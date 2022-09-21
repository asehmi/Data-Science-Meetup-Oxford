# How to use:
#
# import streamlit_debug
# streamlit_debug.set(flag=False, wait_for_client=True, host='localhost', port=6789)
#
# Requires corresponding entries in launch.json:
#
# {
#     // Use IntelliSense to learn about possible attributes.
#     // Hover to view descriptions of existing attributes.
#     // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
#     "version": "0.2.0",
#     "configurations": [
#         {
#             "name": "Python: Current File",
#             "type": "python",
#             "request": "launch",
#             "program": "${file}",
#             "console": "integratedTerminal",
#             "env": {"DEBUG": "true"}
#         },
#         {
#             "name": "Python: debugpy Remote Attach",
#             "type": "python",
#             "request": "attach",
#             "connect": {
#                 "port": 6789,
#                 "host": "127.0.0.1",
#             },
#             "justMyCode": false,
#             "redirectOutput": true,
#             "logToFile": true,
#             // "debugAdapterPath": "${workspaceFolder}/src/debugpy/adapter",
#         },
#     ]
# }
#
# When the streamlit_debug flag=True and wait_for_client=True, you'll need to activate "Python: debugpy Remote Attach" debug session.
#
import streamlit as st
import logging

_DEBUG = False
def set(flag: bool=False, wait_for_client=False, host='localhost', port=8765):
    global _DEBUG
    _DEBUG = flag
    try:
        # To prevent debugpy loading again and again because of
        # Streamlit's execution model, we need to track debugging state 
        if 'debugging' not in st.session_state:
            st.session_state.debugging = None

        if _DEBUG and not st.session_state.debugging:
            # https://code.visualstudio.com/docs/python/debugging
            import debugpy
            if not debugpy.is_client_connected():
                debugpy.listen((host, port))
            if wait_for_client:
                logging.info(f'>>> Waiting for debug client attach... <<<')
                debugpy.wait_for_client() # Only include this line if you always want to manually attach the debugger
                logging.info(f'>>> ...attached! <<<')
            # debugpy.breakpoint()

            if st.session_state.debugging == None:
                logging.info(f'>>> Remote debugging activated (host={host}, port={port}) <<<')
            st.session_state.debugging = True
        
        if not _DEBUG:
            if st.session_state.debugging == None:
                logging.info(f'>>> Remote debugging in NOT active <<<')
            st.session_state.debugging = False
    except Exception as e:
        print(str(e))
        # Ignore... e.g. for cloud deployments
        pass
