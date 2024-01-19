"""
Name: Zhe Wei Zhang
Email: zhewei.zhang82@myhunter.cuny.edu
Resources: Classnotes
"""
from datetime import datetime
import pandas as pd
import pandasql as ps

def make_df(file_name):
    '''a'''
    df = pd.read_csv(file_name)
    df.dropna(subset=['TYP_DESC', 'INCIDENT_DATE', 'INCIDENT_TIME', 'BORO_NM'], inplace=True)
    return df

def compute_time_delta(start, stop):
    '''a'''
    format1 = '%m/%d/%Y %I:%M:%S %p'
    startd = datetime.strptime(start, format1)
    stopd = datetime.strptime(stop, format1)
    difference = (stopd - startd).total_seconds()
    return int(difference)

def select_boro_column(_df):
    '''a'''
    qqq = "SELECT BORO_NM FROM _df"
    result_df = ps.sqldf(qqq, locals())
    return result_df

def select_by_boro(_df, boro_name):
    '''a'''
    boro_name = boro_name.upper()
    qqq = f"SELECT * FROM _df WHERE upper(BORO_NM) = '{boro_name}'"
    result_df = ps.sqldf(qqq, locals())
    return result_df

def new_years_count(_df, boro_name):
    '''a'''
    boro_name = boro_name.upper()
    qqq = f"""
        SELECT COUNT(*) AS "COUNT(*)"
        FROM _df
        WHERE upper(BORO_NM) = '{boro_name}'
        AND incident_date = '01/01/2021'
    """
    result_df = ps.sqldf(qqq, locals())
    return result_df

def incident_counts(_df):
    '''a'''
    qqq = """
        SELECT TYP_DESC, COUNT(*) AS "COUNT(*)"
        FROM _df
        GROUP BY TYP_DESC
        ORDER BY TYP_DESC
    """
    result_df = ps.sqldf(qqq, locals())
    return result_df

def top_10(_df, boro_name):
    '''a'''
    boro_name = boro_name.upper()
    qqq = f"""
        SELECT TYP_DESC, COUNT(*) AS "COUNT(*)"
        FROM _df
        WHERE upper(BORO_NM) = '{boro_name}'
        GROUP BY TYP_DESC
        ORDER BY "COUNT(*)" DESC
        LIMIT 10
    """
    result_df = ps.sqldf(qqq, locals())
    return result_df
