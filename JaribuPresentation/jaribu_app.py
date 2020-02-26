import numpy as np
import pandas as pd
import streamlit as st

def demo1():
    st.title('Demo 1')
    st.header('Simple markdown text output')
 
    # show simple text output
    with st.echo():
        st.write(
            '''
            ## Eat.
            ## Sleep.
            ## Be Awesome.
            ## Repeat.
            '''
        )

def demo2():
    st.title('Demo 2')
    st.header('Selecting table rows')
 
    # https://gist.github.com/treuille/e8f07ebcd92265a68ecec585f7594918
    with st.echo():
        # Load some example data.
        DATA_URL = \
            "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
        data = st.cache(pd.read_csv)(DATA_URL, nrows=1000)

        # Select some rows using st.multiselect. This will break down when you have >1000 rows.
        st.write('### Full Dataset', data)
        selected_indices = st.multiselect('Select rows:', data.index)
        selected_rows = data.iloc[selected_indices]
        st.write('### Selected Rows', selected_rows)

def demo3():
    st.title('Demo 3')
    st.header('Uber pickups in NYC')

    with st.echo():
        DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

        # Load data and convert 
        @st.cache(persist=True, allow_output_mutation=True)
        def load_data(nrows):
            data = pd.read_csv(DATA_URL, nrows=nrows)
            data = data.rename(columns={'Lat': 'lat', 'Lon':'lon'})
            return data

        # Load 10,000 rows of data into the dataframe.
        data = load_data(10000)

        # Display data
        st.dataframe(data)

        if st.checkbox('Show map'):
            # Display map
            st.map(data)

def demo4():
    st.title('Demo 4')
    st.header('Uber pickups in NYC (interactive)')

    with st.echo():
        DATE_COLUMN = 'date/time'
        DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

        @st.cache(persist=True, allow_output_mutation=True)
        def load_data(nrows):
            data = pd.read_csv(DATA_URL, nrows=nrows)
            lowercase = lambda x: str(x).lower()
            data.rename(lowercase, axis='columns', inplace=True)
            data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
            return data

        # Create a text element and let the reader know the data is loading.
        data_load_state = st.text('Loading data...')
        # Load 20,000 rows of data into the dataframe.
        data = load_data(20000)
        # Notify the reader that the data was successfully loaded.
        data_load_state.text('Loading data...done! {} rows (using st.cache)'.format(data.shape[0]))

        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(data)

        st.subheader('Number of pickups by hour')
        hist_values = np.histogram(
            data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)

        st.subheader('Map of all pickups')
        hour_to_filter = st.slider('Select hour', 0, 23, 12)  # min: 0h, max: 23h, default: 17h
        if hour_to_filter == 18:
            st.balloons()
        filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
        st.subheader(f'Map of all pickups at {hour_to_filter}:00')
        st.map(filtered_data)

        if st.checkbox('Show filtered raw data'):
            st.write(filtered_data)
