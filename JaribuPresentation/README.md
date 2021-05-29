# Jaribu - Streamlit 101
> _A introduction to Streamlit framework to build data apps fast!_

> Arvindra Sehmi, Oxford Economics Ltd. | [Website](https://www.oxfordeconomics.com/) | [LinkedIn](https://www.linkedin.com/in/asehmi/)

> Updated: 29 May, 2021

---

### Running the Streamlit presentation app

Ensure you have installed package requirements with the commands:

```bash
# change to the Streamlit <app root folder>, e.g.
cd ./jaribu-presentation
pip install -r requirements.txt
```
Now run Streamlit with `jaribu_streamlit_101.py`:

```bash
# I prefer to set the port number too
streamlit run --server.port 4001 jaribu_streamlit_101.py
```

# Introduction

Streamlit is an open-source app framework for Machine Learning and Data Science teams. You can create beautiful data apps in hours. All in pure Python. Streamlit was released in October 2019 and there's huge excitement about it in the Data Science community.

The inventor of `Streamlit`, **Adrien Treuille (PhD)**, is a machine learning and computer graphics engineer who spent his career to-date developing serious multi-player games where users manipulate fundamental building-block molecules in a virtual environment to discover next-generation therapeutics.

> "_I see these crazy scientific computing games as precursors to Streamlit, because what we did was sort of translate one world into another… `Computing`, basically. In Streamlit, we are essentially `translating the world of app development` into a sort of `language of machine learning`._"'

## What does Streamlit aim to achieve?

* There are a lot of barriers for data scientists (and economists) to implement decent front-ends which would make their _cool stuff_ understandable and useful to others. 
* Front-end engineering is hard! It's a super-power that people probably wish they had, but can't spend time investing in the skills... not to mention the technology and frameworks change so fast - wired today, tired tomorrow. :(
* Streamlit's starting point was to look at the machine learning engineering workflow, and asked the question:

> "_How can we make a machine learning script and convert it into an app as simply as possible, so that it basically feels like a scripting exercise?_"

* A single package that you can install through `pip`, which gives you a bunch of functions which can be:
    * `Interleaved` into an existing `ML code script`
    * Essentially making the ML code `parameterizable`
    * Does a little bit of `layout`, and
    * `Magically` turns your ML code into a `beautiful app`
* Inspiration drawn from `Jupyter`, `ipywidgets`, `R-Shiny`, `Voila`, `React`, etc., but more as a guiding light than software architecture. There is a fairly significant technical difference in the implementation. Existing frameworks (like Shiny, ipywidgets) are based on `wiring callbacks` which, if you have enough of them, leads to an untestable mess. Streamlit is based on a `declarative data flow model`.

> "_We have a multi-threaded server that starts in the background, there’s `WebSockets shuttling information back and forth to the browser`, there’s a whole `browser app that’s interpreting this and creating what you see on the screen`... But all of that kind of goes away from the user’s perspective, and you just get really a couple dozen magical Python commands that transform a machine learning script or a data science script into an app that you can use and share with others._"

---

### _Install this app for much more..._
