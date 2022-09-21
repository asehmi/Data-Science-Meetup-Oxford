import json
import pandas as pd
import streamlit as st

from CAGR_Utils import CAGR_Rolling

@st.cache(persist=True)
def load_data(region_type):
    if region_type == 'Countries':
        gc_data = load_data_countries()
    elif region_type == 'Cities':
        gc_data = load_data_cities()
    else:
        gc_countries = load_data_countries()
        gc_cities = load_data_cities()
        gc_data = pd.concat([gc_countries, gc_cities],ignore_index=True,axis=0,sort=False)
        gc_data.reset_index()

    return gc_data

@st.cache(persist=True)
def load_data_countries():
    gc_data_countries = pd.read_excel('./data/GCFS Countries (GDP, Labour, Population, Incomes) SAMPLE.xlsx', keep_default_na=False, na_values=["NA"], engine='openpyxl')
    return gc_data_countries

@st.cache(persist=True)
def load_data_cities():
    gc_data_cities = pd.read_excel('./data/GCFS Cities (GDP, Labour, Population, Incomes) SAMPLE.xlsx', keep_default_na = False, na_values = ['NA'], engine='openpyxl')
    return gc_data_cities

@st.cache(persist=True, allow_output_mutation=True)
def load_databank_locations():
    with open('./data/gcfs-tree.json', 'rt', encoding='utf8') as f:
        tree_str = f.read()

    treejson = json.loads(tree_str)
    databank = treejson[0]['Name']

    regions = [(region['Name'],region['Children']) for region in treejson[0]['Children']]

    # Walk source tree and build countries tree structure from 'By geographic level' branch,
    # which contains the country codes
    country_codes_dict = {}
    countries_json = {'label': databank, 'value': databank, 'children': []}
    city_codes_dict = {}
    cities_json = {'label': databank, 'value': databank, 'children': []}
    for (region, countries) in regions:
        if region == 'By geographic level':
            for country in countries:
                if country['Name'] == 'Countries':
                    country_codes_dict[country['Name']] = country['Code']
                    countries_json['children'].append({'label': country['Name'], 'value': country['Name'], 'children': []})
                elif country['Name'] == 'Cities':
                    city_codes_dict[country['Name']] = country['Code']
                    cities_json['children'].append({'label': country['Name'], 'value': country['Name'], 'children': []})

                for city in country['Children']:
                    if country['Name'] == 'Countries':
                        country_codes_dict[city['Name']] = city['Code']
                        countries_json['children'][0]['children'].append({
                            'label': city['Name'],
                            'value': json.dumps({'name': city['Name'], 'code': city['Code']})
                        })
                    elif country['Name'] == 'Cities':
                        city_codes_dict[city['Name']] = city['Code']
                        cities_json['children'][0]['children'].append({
                            'label': city['Name'],
                            'value': json.dumps({'name': city['Name'], 'code': city['Code']})
                        })

    # Walk source tree and build regions > countries > cities tree structure,
    # using the above countries structure to resolve the country codes
    # (this is because the non-'By geographic level' branches don't have country codes!)
    locations_list = []
    locations_json = {'label': databank, 'value': databank, 'children': [{'label': 'Locations', 'value': 'Locations', 'children': []}]}
    for i, (region, countries) in enumerate(regions):

        locations_json['children'][0]['children'].append({'label': region, 'value': region, 'children': []})

        for j, country in enumerate(countries):

            locations_json['children'][0]['children'][i]['children'].append({
                'label': country['Name'],
                'value': json.dumps({'name': country['Name'], 'code': country_codes_dict.get(country['Name'], None)}),
                'children': []
            })

            for city in country['Children']:

                city_name = city['Name'] if city['Name'] != country['Name'] else (city['Name'] + ' - City')
                locations_json['children'][0]['children'][i]['children'][j]['children'].append({
                    'label': city_name, 
                    'value': json.dumps({'name': city['Name'], 'code': city['Code']})
                })

                locations_list.append({
                    'Databank': databank,
                    'Region': region,
                    'Country': country['Name'],
                    'Location': city['Name'],
                    'Location Code': city['Code']
                })

    locations_df = pd.DataFrame.from_dict(locations_list)
    pruned_regions = [child for child in locations_json['children'][0]['children'] if child['label'] != 'By geographic level']
    locations_json['children'][0]['children'] = pruned_regions

    return (locations_df, locations_json, countries_json, cities_json)

@st.cache(persist=True)
def load_geojson():
    geojson = pd.read_json('./data/gcfs-geojson.json', orient='records')
    geojson = pd.read_json(geojson['properties'].to_json(orient='records'),orient='records')
    geojson = geojson[['locationCode','latitude','longitude']]
    return geojson

@st.cache(persist=True)
def clean_and_reshape_data(gc_data, geojson):
    # UNPIVOT DATA
    value_vars = list(gc_data.filter(regex=('\\d')).columns)
    # value_vars
    # unpivot the dataframe on all years 
    gc_data_unpivoted = pd.melt(gc_data, id_vars=['Location','Indicator','Measurement','Units','Scale', 'Location Code'], \
         value_vars=value_vars, var_name='Year', value_name='Value').astype({'Year':'int16','Value':'float64'})
    gc_data_unpivoted = gc_data_unpivoted.sort_values(['Location','Indicator','Measurement','Units','Scale','Year'])
    gc_data_unpivoted.loc[:,'Value'].fillna(method='bfill', inplace = True)
    # st.dataframe(gc_data_unpivoted.head(100))

    # GENERATE ROLLING CAGR SERIES AND APPEND
    gc_data_cagr_3y = CAGR_Rolling(gc_data_unpivoted, num_periods=3, cagr_col='CAGR (3Y)', \
        id_vars=['Location', 'Indicator', 'Measurement', 'Units', 'Scale', 'Location Code'], \
        value_var_col='Year', value_col='Value')
    gc_data_cagr_3y = gc_data_cagr_3y.drop(['Value'], axis=1)
    gc_data_cagr_3y = gc_data_cagr_3y.rename(columns={'CAGR (3Y)': 'Value'})
    gc_data_cagr_3y.loc[:,'Measurement'] = 'CAGR (3Y)'
    gc_data_cagr_3y.loc[:,'Units'] = '%'
    # st.dataframe(gc_data_cagr_3y.head(100))

    # append data frames (they both have identical columns)
    gc_data_unpivoted = pd.concat([gc_data_unpivoted, gc_data_cagr_3y],ignore_index=True,axis=0,sort=False)
    gc_data_unpivoted.reset_index()

    gc_data_unpivoted.loc[:,'Units > Scale'] = \
        [(gc_data_unpivoted.loc[i,'Units'] + (', ' + gc_data_unpivoted.loc[i,'Scale']) \
        if len(gc_data_unpivoted.loc[i,'Scale']) != 0 \
        else gc_data_unpivoted.loc[i,'Units']) \
        for i in gc_data_unpivoted.index ]

    # JOIN UNPIVOTED DATA WITH GEOJSON
    # merge filtered data with geojson to get lat/lon columns; throw away [locationCode] from geojson
    merged = pd.merge(gc_data_unpivoted, geojson, how='left', left_on='Location Code', right_on='locationCode') \
                [['Location', 'Indicator', 'Measurement', 'Units', 'Scale', 'Year', 'Value', 'Location Code', 'Units > Scale', 'longitude', 'latitude']]
    # st.dataframe(merged.head(100))
    # st.dataframe(merged.tail(100))

    return gc_data_unpivoted, merged
