# My Streamlit Template App

Small Streamlit app template Using Streamlit to build a Web App 

# Getting started

Learn all about Streamlit here: [API Docs](https://docs.streamlit.io/index.html) **|** [GitHub](https://github.com/streamlit/streamlit)

## Installation

* Open a `conda console` window
* If necessary, run `conda activate` for the env in which you want to install package requirements. See [managing conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

**Note**: to use `Streamlit` you’ll need Python 3.5 or above.

### Newbie install

`pip install streamlit`

`pip install --upgrade streamlit`

### Pro install

* Put package dependencies in `requirements.txt` and include with your app distro

`pip install -r requirements.txt`

* Alternatively, provide an `environment.yml` for use with `conda env create` and include with your app distro

`conda env create -f environment.yml`

* Include a `setup.py` script with your app if any special installation actions need to be performed

`python setup.py`

* Useful `Streamlit` CLI commands:

`streamlit config show`

`streamlit cache clear`

## Running your app (local)

* Create a file `<your app>.py` (typically named, `app.py`)
* Add `import streamlit as st`
* Write some `python code`, and save
* In the `conda console`, from `<your app> directory`, type:

`streamlit run [--server.port <port number>] <your app>.py`

* If you don't specify a server port, `<your app>` will open a bowser window with the default port: [http://localhost:8765/](http://localhost:8765/).
* Yes... it's as simple as that!

## Running you app (server)

When running you app on a server you should run it in `headless` mode. There are a few ways to do this:

1. Create a `config.toml` file in `.streamlit` sub-folder of your app folder, and add:

```
[server]
headless = true
```

2. Or, set the environment variable `STREAMLIT_SERVER_HEADLESS=true`
3. Or, when running your app from the command line, pass the `--server.headless true` parameter like:

`streamlit run --server.headless true <your_app>.py `

# Debugging in VS Code

## Basic

* Use a Python unit testing framework. I've used `unittest`. See [unittest docs](https://docs.python.org/2/library/unittest.html).
* **Or**... add an environment DEBUG flag to your project's VS Code `launch.json` file (in `.vscode` folder), like this, which you can use like a DEBUG switch:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {"DEBUG": "true"}
        }
    ]
}
```

* **Or..** to be `12factor` compliant, it's a good idea to `pip install django-environ`, and `import settings`. Read [the docs](https://django-environ.readthedocs.io/en/latest/).
* Always `import logging` and use `logging.info()`, `logging.debug()`, `logging.error()` to report to the console (`print()` doesn't work in Streamlit unless run from the console).

## Advanced

See this artcile for details: [How to use Streamlit with VS Code](https://awesome-streamlit.readthedocs.io/en/latest/vscode.html)

Essentially follow these steps:

1. `pip install ptvsd`
2. Add the following snippet in your `<your-app_name>.py` file.

```python
import ptvsd
ptvsd.enable_attach(address=('localhost', 5678))
ptvsd.wait_for_attach() # Only include this line if you always wan't to attach the debugger
```

3. Then start your Streamlit app

`streamlit run <your-app_name>.py`

4. From the `Debug` sidebar menu configure `Remote Attach: Attach to a remote ptvsd debug server` and update your `launch.json` file with the details below.
```json
{
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "port": 5678,
    "host": "localhost",
    "justMyCode": true,
    "redirectOutput": true,
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "."
        }
    ]
}
```

5. Make sure you manually insert the `redirectOutput` setting.
6. By default you will be debugging your own code only. If you wan’t to debug into streamlit code, then change `justMyCode` setting from `true` to `false`.
7. Finally, attach the debugger by clicking the debugger play button.

## Profiling your app

Since `Streamlit` apps are stateless and executed top-down in full at every change, you need to be wary of performance issues. At some point you'll hit
some unacceptable limits. Good server app design principles still apply with `Streamlit` apps. So, when `@st.cache()` just isn't enough, profile you code,
and consider using well-understood server design techniques such as using a database, search index, or microservices.

```python
import contextlib
import time
import pandas as pd
import streamlit as st

@contextlib.contextmanager
def profile(name):
    start_time = time.time()
    yield  # <-- your code will execute here
    total_time = time.time() - start_time
    print('%s: %.4f ms' % (name, total_time * 1000.0))

with profile('load_data'):
    df = pd.read_excel('very_large_file.xlsx',nrows=1000000)
```

## Crosstalk!

The `Streamlit` architecture is such that each connected user has her own session object in the server, and her own separate thread where the app’s source 
file is executed. While the source file executes, the `Streamlit` library in that thread can only write to that specific session object
(because that’s the only session it has a reference to).

Then, the `Streamlit` server periodically loops through its `websocket-to-session` dict and writes any outstanding messages from each session 
into its corresponding websocket.

In theory, there should be no crosstalk between sessions! Issues have been reported when running on Google Compute Engine in a Docker container.
if the app is behind a proxy, it might make all users appear to be visiting from the same IP address.

Ensure you have the latest `Streamlit` version installed as [this issue](https://discuss.streamlit.io/t/crosstalk-between-streamlit-sessions-with-multiple-users/319/3)
is being actively adressed by the developers.

---
See this video by Dan Taylor: [Get Productive with Python in Visual Studio Code](https://www.youtube.com/watch?v=6YLMWU-5H9o), for useful tips on using vscode for Python development.

Enjoy!
