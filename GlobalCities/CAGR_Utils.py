import pandas as pd
import numpy as np

# Simple CAGR calculation, designed to be used with df.apply()
def CAGR(row, last_col, first_col, num_periods):
    '''Calculate compound growth rate on a row x of a pandas df'''
    val_T = float(row[last_col])
    val_t = float(row[first_col])
    return (val_T/val_t)**(1./num_periods)-1

# Rolling CAGR calculation template:
#
# df_unpivoted is an unpivoted df with at least Id, Year and Value columns. Manually, the rolling CAGR steps are:
#
#   df_unpivoted['Year+5'] = df_unpivoted.loc[:,'Year'] + 5
#   df_rolling_cagr = pd.merge(df_unpivoted, df_unpivoted, how='inner', left_on=['Id', 'Year'], right_on=['Id', 'Year+5'], suffixes=['_start', '_end'])
#   df_rolling_cagr = df_rolling_cagr[['Id', 'Year_start', 'Value_start', 'Year_end', 'Value_end']]
#   df_rolling_cagr['CAGR (5Y)'] = ((df_rolling_cagr.loc[:,'Value_end'] / df_rolling_cagr.loc[:,'Value_start'])**(0.2)) - 1
#   df_unpivoted = pd.merge(df_unpivoted, df_rolling_cagr, how='left', left_on=['Id', 'Year'], right_on=['Id', 'Year_start'])
#   df_unpivoted['CAGR (5Y)'].replace([np.inf, -np.inf, np.nan], 0.0, inplace=True)
#   df_unpivoted = df_unpivoted[['Id', 'Year', 'Value', 'CAGR (5Y)']]
#
def CAGR_Rolling(df_unpivoted, num_periods=5, cagr_col='CAGR (5Y)', id_vars=['Id'], value_var_col='Year', value_col='Value', sort=True):
    value_var_num_periods = value_var_col + '+' + str(num_periods)
    df_unpivoted.loc[:,value_var_num_periods] = df_unpivoted.loc[:,value_var_col] + num_periods
    df_cagr_inner = pd.merge(df_unpivoted, df_unpivoted, how='inner', left_on=id_vars+[value_var_col], right_on=id_vars+[value_var_num_periods], suffixes=['_start', '_end'])
    df_cagr_inner = df_cagr_inner[id_vars+[value_var_col+'_start', value_col+'_start', value_var_col+'_end', value_col+'_end']]
    df_cagr_inner.loc[:,cagr_col] = ((df_cagr_inner.loc[:,value_col+'_end'] / df_cagr_inner.loc[:,value_col+'_start'])**(1./num_periods)) - 1
    df_cagr_left_outer = pd.merge(df_unpivoted, df_cagr_inner, how='left', left_on=id_vars+[value_var_col], right_on=id_vars+[value_var_col+'_start'])
    df_cagr_left_outer[cagr_col].replace([np.inf, -np.inf, np.nan], 0.0, inplace=True)
    if (sort):
        df_cagr = df_cagr_left_outer[id_vars+[value_var_col, value_col, cagr_col]].sort_values(id_vars+[value_var_col])
        return df_cagr
    else:
        return df_cagr_left_outer[id_vars+[value_var_col, value_col, cagr_col]]
 