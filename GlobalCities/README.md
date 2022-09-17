# Global cities explorer

This application gives a snapshot of Oxford Economics' Global Cities Forecasts Service, providing an insight into global cities GDP, population, employment and household income.

The Global Cities Forecasts and other data services can be found on the [Global Data Workstation](https://data.oxfordeconomics.com/).

## Global cities

In this era of market transformation and rapid urbanisation, cities are fast becoming dominant drivers of global economic and business growth. Half of the world’s population lives in urban areas, producing more than 80% of global GDP. By 2030, six out of ten people will live in cities, with their share of global GDP rising to 90%. It is no longer enough to go to market by country, as sub-regional and city trends need to be taken into consideration for finding new markets or making location-based investment decisions.

Oxford Economics' Cities and Regions services provide historical data and forecasts on over 3,000 worldwide cities and sub-regions. This unparalleled set of forecast databanks measures, benchmarks and forecasts performance in key locations around the world. We offer regularly updated annual forecasts for key economic, labour-market and industry variables. Our Cities & Regions services provide economic and demographic projections to 2030 that are consistent with our global economic and industry forecasts, in addition to an archive for historical trend analysis.

Detailed economic forecasts to 2040 for 900 cities using consistent definitions of cities, sectors, demographics, and spending behaviour to allow comparison of the prospects and trends for cities across different continents. Clients can make top-level decisions about market and investment strategies, comparing like with like.

What’s included?

- **Broad Global Coverage**. Forecasts for 900 cities in 164 countries. All forecasts are consistent with our country and industry forecasts, providing a level basis for analysis.
- **Extensive data by location**. Consistent and comparable annual data and forecasts for total GDP, the labour market, population and income, consumer spending by category, and retail sales.
- **Long-term forecasts**. The data generally refers back to 2000, and the forecast horizon is 2040. To ensure you have the latest information for these dynamic and rapidly changing markets, we update our forecasts on an annual basis.
- **Methodology report**. Explanation of data sources, urban definitions, forecast methods and approaches to estimate and fill missing data, as well as an outline of the linkages to our Global Economic Model.
- **Advanced analytical functions**. Our web-based databank allows users to quickly build custom queries with complete flexibility and view the data in tables, charts, and maps. Numbers may be represented as absolutes, percentages, and even differences between time periods. All data are annotated by source, date of update, and analyst. Searches can be saved for later reference and downloaded to Excel.

## Find out more about Oxford Economics data services

[Data Solutions](https://www.oxfordeconomics.com/our-data-solutions/)

[Data API](https://support.oxfordeconomics.com/support/solutions/articles/52000028728)

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

Enjoy!
