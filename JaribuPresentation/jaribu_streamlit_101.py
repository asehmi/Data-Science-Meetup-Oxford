import streamlit as st

from jaribu_app import *

st.sidebar.image('./oe_logo_new.png', use_column_width=True, format='png')

st.sidebar.info(
    '''
    # Streamlit 101

    * DS-OX Meetup | Feb 26, 2020
    * Jaribu | Jan 16, 2020
    
    `Arvindra Sehmi`
    `asehmi@oxfordeconomics.com`

    '''
)

if st.sidebar.checkbox('Introduction to Streamlit', True):
    '''
    # Introduction to Streamlit

    Streamlit is an open-source app framework for Machine Learning and Data Science teams. You can create beautiful data apps in hours. All in pure Python. Streamlit was released in October 2019 and there's huge excitement about it in the Data Science community.

    The inventor of `Streamlit`, **Adrien Treuille (PhD)**, is a machine learning and computer graphics engineer who spent his career to-date developing serious multi-player games where users manipulate fundamental building-block molecules in a virtual environment to discover next-generation therapeutics.
    '''

    st.info ('_I see these crazy scientific computing games as precursors to Streamlit, because what we did was sort of translate one world into another… `Computing`, basically. In Streamlit, we are essentially `translating the world of app development` into a sort of `language of machine learning`._')

    '''
    ## What does Streamlit aim to achieve?

    * There are a lot of barriers for data scientists (and economists) to implement decent front-ends which would make their _cool stuff_ understandable and useful to others. 
    * Front-end engineering is hard! It's a super-power that people probably wish they had, but can't spend time investing in the skills... not to mention the technology and frameworks change so fast - wired today, tired tomorrow. :(
    * Streamlit's starting point was to look at the machine learning engineering workflow, and asked the question:
    '''

    st.info('"_How can we make a machine learning script and convert it into an app as simply as possible, so that it basically feels like a scripting exercise?_"')

    '''
    * A single package that you can install through `pip`, which gives you a bunch of functions which can be:
        * `Interleaved` into an existing `ML code script`
        * Essentially making the ML code `parameterizable`
        * Does a little bit of `layout`, and
        * `Magically` turns your ML code into a `beautiful app`
    * Inspiration drawn from `Jupyter`, `ipywidgets`, `R-Shiny`, `Voila`, `React`, etc., but more as a guiding light than software architecture. There is a fairly significant technical difference in the implementation. Existing frameworks (like Shiny, ipywidgets) are based on `wiring callbacks` which, if you have enough of them, leads to an untestable mess. Streamlit is based on a `declarative data flow model`.
    '''

    st.info('"_We have a multi-threaded server that starts in the background, there’s `WebSockets shuttling information back and forth to the browser`, there’s a whole `browser app that’s interpreting this and creating what you see on the screen`... But all of that kind of goes away from the user’s perspective, and you just get really a couple dozen magical Python commands that transform a machine learning script or a data science script into an app that you can use and share with others._"')

    '''
    * Every single data analysis team needs to create apps. They're a focal point - like the bonfire of the team. It’s where team members get together and communicate.
    * App are actually a really crucial part of the ML (data analysis) workflow, especially in a non-trivial project.
    * `Not just for internal apps`. Machine learning and data scientists need to build `apps for external consumption` too. Other teams need to consume models in various different ways, and it ought to much easier to build the required, but different, application layers to do that.
    '''

    st.info('"_These tools require `constant new features`, so it’s really `empowering to be able to create them yourself` easily and beautifully, and then `directly iterate on them and directly serve them` to your users, be they other members of your team or other people in the company. So that’s really the power of being able to `write apps quickly and easily`, and `in a flow that you might expect`, and I think that’s why the community has been so receptive._"')

if st.sidebar.checkbox('Getting started', False):
    '''
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
    '''

if st.sidebar.checkbox('Let\'s code', False):
    demos = st.sidebar.multiselect('Select demo', ['Demo 1', 'Demo 2', 'Demo 3', 'Demo 4'])
    if 'Demo 1' in demos:
        demo1()
    if 'Demo 2' in demos:
        demo2()
    if 'Demo 3' in demos:
        demo3()
    if 'Demo 4' in demos:
        demo4()

if st.sidebar.checkbox('Debugging in VS Code', False):
    '''
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

    '''

if st.sidebar.checkbox('Jupyter vs Streamlit', False):
    '''
    # Can you use Streamlit instead of Jupyter Notebooks?

    ### Streamlit is not a single file only approach to app development
    * Single file apps are great for getting started. But as your app grows you must refactor the project into folders/files/modules/packages. You then import whatever you need in your main app.py file.
    * Hot-reloading on deeply nested modules is a bit flaky though (but will you really have deeply nested modules in a simple app?). See [issue 366](https://github.com/streamlit/streamlit/issues/366)

    ### The Streamlit dev workflow is much more efficient than Jupyter Notebook's
    * You work in an efficient editor.
    * The iterative cycle of change-run-evaluate is fast and automated in Streamlit.
    * You naturally evolve towards quality code modules and a working app being the final deliverable, not a Notebook which further conversion required to build an app.
    * More with less - Streamlit is much easier, efficient and productive.
    * Streamlit solves all the problems of Notebooks pointed out by Joel Grus in [I don’t like notebooks](https://www.youtube.com/watch?v=7jiPeIFXb6U).
    * `Jupyter Notebooks for Visual Studio Code` addresses some of the failings of native JNs. See [this video](https://www.youtube.com/watch?v=FSdIoJdSnig) for details.

    ### The product produced by Streamlit is much nicer than a Notebook
    * You can control the output of your code, markdown and results.
    * You don’t have those clunky code cells.
    * You don’t spend tons of time googling and trying out how to use nbformatter.
    * Finished dashboard-like products are easy to make.

    ### How about the software development experience?
    * You seldom want to show people the numerous intermediate code steps in a notebook. From a literate programming perspective, code cells with many lines of boiler-plate pandas or matplotlib code are distracting.
    * With Streamlit you can show selected parts of your code (which simultaneously get executed!) using `st.echo()`.
    * Running the full app during hot-reload is a great feature keeping all state aligned as expected. With notebooks it's very easy to get confused about which cells have run and in which order.
    * Notebook re-runs can take forever compared to Streamlit, because of data and python compilation caching, so fast iterations come easily.
    * The hassles of managing notebook kernels, Jupyter extensions etc. mean you can spend a lot of time on Google and Stack overflow looking for solutions.
    * In the end you need to deploy solutions. Streamlit is yet another web app, so easy to deploy to Azure, Heroku, AWS, etc.

    ### In favour of Jupyter notebooks
    * The larger community, larger library of widgets and export to pdf functionality.
    * Notebooks still provide the best environment for ad-hoc exploratory data analysis.

    ## Quote from Adrien Treuille
    '''

    st.info('"We ourselves use Jupyter alongside Streamlit, so `they don’t exclude one another at all`. Jupyter, we feel, is `centered on the EDA workflow - exploratory data analysis workflow` - and it’s a fantastic tool for that... And then it sort of branched out into making apps a little bit more, being an expository tool of various kinds... And those are all great, adjacent use cases. Streamlit was really founded on the idea of building interactive apps really easily. So we have a different workflow; I think it’s very, very `simple`, it’s very `lightweight`, it’s `super-easy to understand`, and it’s `slightly difficult to describe`. **You just have to try it**. In essence, we allow you to sprinkle these interactive widgets throughout your code, and then we sort of organize it into an app very easily. I think it’s that simplicity that the community has really responded to."')

if st.sidebar.checkbox('Summary', False):
    '''
    # Summary

    ## My impressions of Streamlit

    * On the _data-analytics-ease-of-use_ curve, the use case for Streamlit apps lies somewhere between Power BI/Tableau on the high end and Jupyter Notebooks in the middle; with regular Python/R programming sitting towards the low end.
        * Almost everything you can do in Python is available to the developer in Streamlit.
        * It's powerful enough already to be ideal for small to medium data science-rich business solutions and experimental or exploratory analytics.
        * As with Jupyter Notebooks, literate programming (not in the true Knuth sense) is easy, because Streamlit comes with native Markdown and Latex support.
    * A design principle of Streamlit is that there's just enough (and not more) UI functionality out-of-the-box to make serious, small, specific custom web apps.
        * This addresses 80% of a data science worker's needs.
        * I've used it quite a bit in small AI/ML experiments and really appreciate being able to quickly create a UI to view results and control the experiments.
        * Some say Streamlit is the _React or Shiny for Python_ - I think we're some way from that (ObservableHQ would be a closer fit). There's a decent discussion going on [here](https://github.com/streamlit/streamlit/issues/327).
    * The code is developed and debugged in VS Code (with Python extensions)
        * Streamlit supports hot-reloading and native data caching, making the framework super-productive for iterative AI/ML app experiments.
        * The app state is always consistent because the code is executed from the top whenever any change event is raised. That sounds awfully slow, but it isn't in practice - remember the primary use case is supposed to be about building _simple UI_ for simple _data analysis tools_, and native data caching helps with speed a lot.
        * You can run apps normally in the console even though they contain some Streamlit UI magic in the source code.
    '''
    if st.checkbox('🙏🏾', False):
        '''
        ## Eat.
        ## Sleep.
        ## Be Streamlit.
        ## Repeat.
        ---
        # Thank you!
        '''

if st.sidebar.checkbox('Resources', False):
    '''
    # Resources

    - [Awesome Streamlit Docs](https://awesome-streamlit.readthedocs.io/en/latest/index.html)
    - [Awesome Streamlit App Gallery](https://awesome-streamlit.org/)
    - [Streamlit Discussion Forum](https://discuss.streamlit.io/)
    - [Will Streamlit cause the extinction of Flask?](https://towardsdatascience.com/part-2-will-streamlit-cause-the-extinction-of-flask-395d282296ed)
    - [CSS Hacks!](https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/23)
    '''

if st.sidebar.checkbox('Videos', False):
    '''
    # Videos
    '''
    st.markdown('''
        <iframe width="560" height="315" src="https://www.youtube.com/embed/B2iAodr0fOo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        ''', unsafe_allow_html=True)
    st.markdown('''
        <iframe width="560" height="315" src="https://www.youtube.com/embed/R2nr1uZ8ffc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        ''', unsafe_allow_html=True)
    st.markdown('''
        <iframe width="560" height="315" src="https://www.youtube.com/embed/sxLNCDnqyFc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        ''', unsafe_allow_html=True)
    st.markdown('''
        <iframe width="560" height="315" src="https://www.youtube.com/embed/VtrFjkSGgKM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        ''', unsafe_allow_html=True)
    st.markdown('''
        <iframe width="560" height="315" src="https://www.youtube.com/embed/z8vgmvtgxCs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        ''', unsafe_allow_html=True)

st.sidebar.markdown('---')

def set_default_block_container_style(
    max_width: int = 1100, max_width_100_percent: bool = False,
    padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10,
    color: str = 'black', background_color: str = 'white'):

    if max_width_100_percent:
        max_width_str = f'max-width: 100%;'
    else:
        max_width_str = f'max-width: {max_width}px;'

    st.markdown(
        f'''
        <style>
            .reportview-container .sidebar-content {{
                padding-top: {padding_top}rem;
            }}
            .reportview-container .main .block-container {{
                {max_width_str}
                padding-top: {padding_top}rem;
                padding-right: {padding_right}rem;
                padding-left: {padding_left}rem;
                padding-bottom: {padding_bottom}rem;
            }}
            .reportview-container .main {{
                color: {color};
                background-color: {background_color};
            }}
        </style>
        ''',
        unsafe_allow_html=True,
    )

if __name__ == '__main__':
    set_default_block_container_style(max_width_100_percent = False, padding_left = 0, padding_right = 10)
