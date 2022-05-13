# Streamlit Next.js Component, Auth0 Authentication, Event-Based Messaging & Serverless APIs

> Arvindra Sehmi, CloudOpti Ltd. | [LinkedIn](https://www.linkedin.com/in/asehmi/)
> (Updated: 13 May, 2022)

This application has been retired and replaced by the tutorial article below written for the [Auth0](https://auth0.com/) blog.

---

![Auth0 Guest Authors Logo](https://github.com/auth0-blog/streamlit-asehmi/blob/main/article-1/code/components/hero/app/images/logo.png)

[**This article is published in full on the Auth0 developer blog**](https://auth0.com/blog/)


# Introduction to Streamlit and Streamlit Components

**TL;DR:** [Streamlit](https://www.streamlit.io/) is an open-source app framework for Machine Learning and Data Science teams. You can create beautiful data apps in hours. All in pure Python. Streamlit was released in October 2019 and was recently [acquired by Snowflake](https://blog.streamlit.io/snowflake-to-acquire-streamlit/). There's huge excitement about it in the Data Science community. It's not just for Data Science though. With its component extensibility architecture, you can build and integrate most kinds of web frontends into Streamlit apps. This article will show you how to build Streamlit apps and custom Streamlit Components, with the end goal of implementing Auth0 authentication of Streamlit apps using Streamlit Components. My experience with Streamlit can be verified on the official page of [Streamlit Creators](https://streamlit.io/creators).

Don't take my word for it that Streamlit is extremely popular and worth taking a serious look at. Here's a chart I [found](https://towardsdatascience.com/10-features-your-streamlit-ml-app-cant-do-without-implemented-f6b4f0d66d36) showing the extremely rapid adoption rate of Streamlit compared to other similar tools.

![Streamlit Rapid Adoption Rate](https://i.ibb.co/X4SPdLR/streamlit-rapid-adoption-rate.png)

Why is that so?

### Streamlit focuses on simplicity

> "_How can we make a machine learning script and convert it into an app as simple as possible, so that it basically feels like a scripting exercise?_", Inventor of Streamlit, Adrien Treuille (PhD)

[Streamlit](https://www.streamlit.io/) is a single Python package that you install through `pip`, that gives you a set of functions which:

* Can be _interleaved_ into an existing _ML code script_
* Essentially making the ML code _parameterizable_
* Does a little bit of _layout_, and
* _Magically_ turns your ML code into a _beautiful app_

Inspiration is drawn from Jupyter, ipywidgets, R-Shiny, Voila, React, etc., but more as a guiding light than a software architecture. There are significant technical differences in the implementation of Streamlit, which is based on a [_declarative data flow model_](https://en.wikipedia.org/wiki/Dataflow_programming), not wiring callbacks.

Python frameworks such as [scikit-learn](https://scikit-learn.org/stable/), [spaCy](https://spacy.io/), [Pandas](https://pandas.pydata.org/), and various visualization frameworks such as [Altair](https://altair-viz.github.io/), [Plotly](https://plotly.com/graphing-libraries/) and [Matplotlib](https://matplotlib.org) all work seamlessly with Streamlit.

### Streamlit supports many uses

* Every single data analysis team needs to create apps. They're a focal point - like the bonfire of the team. It’s where team members get together and communicate.
* Apps are a crucial part of the ML (data analysis) workflow, especially in a non-trivial project.
* This applies not only to internal apps. Machine learning researchers and data scientists need to build apps for external consumption too. Other teams need to consume models in various different ways, and it ought to be much easier to build the required but different application layers to do that.

I'm a big fan of Streamlit and use it extensively for serious work and play. In a previous job I had developed several in-house apps that I needed to share externally with clients and colleagues, so adding security and authentication features was imperative. As you'll see in this article Streamlit's embedded components extensibility architecture and native session state management will help realize this security objective.

Here is the [GitHub repository](https://github.com/auth0-blog/streamlit-asehmi) for this article.

[**Read the full article...**](https://auth0.com/blog/introduction-to-streamlit-and-streamlit-components/)


Enjoy!
