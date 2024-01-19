"""
Name: Zhe Wei Zhang
Email: zhewei.zhang82@myhunter.cuny.edu
Resources: Classnotes
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering

def make_df(file_name):
    '''a'''
    df = pd.read_csv(file_name)
    df = df.dropna(subset=['TYP_DESC', 'INCIDENT_TIME', 'INCIDENT_DATE', 'Latitude', 'Longitude'])
    df = df[df['TYP_DESC'].str.contains('AMBULANCE')]
    return df

def add_date_time_features(df):
    '''a'''
    df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'])
    df['WEEK_DAY'] = df['INCIDENT_DATE'].dt.dayofweek
    df['INCIDENT_TIME'] = pd.to_datetime(df['INCIDENT_TIME'])
    df['INCIDENT_MIN'] = (df['INCIDENT_TIME'].dt.hour * 60 + df['INCIDENT_TIME'].dt.minute +
                          df['INCIDENT_TIME'].dt.second / 60)
    return df

def filter_by_time(df, days=None, start_min=0, end_min=1439):
    '''a'''
    if days is None:
        days = [0, 1, 2, 3, 4, 5, 6]
    dffiltered = df[(df['WEEK_DAY'].isin(days)) & (df['INCIDENT_MIN'] >= start_min)
                     & (df['INCIDENT_MIN'] <= end_min)]
    return dffiltered

def compute_kmeans(df, num_clusters = 8, n_init = 'auto', random_state = 1870):
    '''a'''
    lat_long_data = df[['Latitude', 'Longitude']]
    kmeans = KMeans(n_clusters=num_clusters, n_init=n_init, random_state=random_state)
    kmeans.fit(lat_long_data)
    cluster_centers = kmeans.cluster_centers_
    predicted_labels = kmeans.labels_
    return cluster_centers, predicted_labels

def compute_gmm(df, num_clusters = 8, random_state = 1870):
    '''a'''
    latlong = df[['Latitude', 'Longitude']]
    gmma = GaussianMixture(n_components=num_clusters, random_state=random_state)
    gmma.fit(latlong)
    predicted_labels = gmma.predict(latlong)
    return predicted_labels

def compute_agglom(df, num_clusters = 8, linkage='ward'):
    '''a'''
    latlong = df[['Latitude', 'Longitude']]
    agglom = AgglomerativeClustering(n_clusters=num_clusters, linkage=linkage)
    predicted_labels = agglom.fit_predict(latlong)
    return predicted_labels

def compute_spectral(df, num_clusters = 8, affinity='rbf',random_state=1870):
    '''a'''
    latlong = df[['Latitude', 'Longitude']]
    spectral = SpectralClustering(n_clusters=num_clusters,
                                  affinity=affinity, random_state=random_state)
    predicted_labels = spectral.fit_predict(latlong)
    return predicted_labels

def compute_explained_variance(df, k_vals = None, random_state = 1870):
    '''a'''
    if k_vals is None:
        k_vals = [1, 2, 3, 4, 5]
    lat_long_data = df[['Latitude', 'Longitude']]
    variances = []
    for kals in k_vals:
        kmeans = KMeans(n_clusters=kals, random_state=random_state)
        kmeans.fit(lat_long_data)
        variances.append(kmeans.inertia_)
    return variances

def test_add_date_time_features():
    '''a'''
    data = {
        'INCIDENT_DATE': ['07/04/2021', '07/04/2021', '07/04/2021'],
        'INCIDENT_TIME': ['00:01:51', '00:06:12', '00:12:12']
    }

    df = pd.DataFrame(data)
    df = add_date_time_features(df)
    expectedcolumns = ['INCIDENT_DATE', 'WEEK_DAY', 'INCIDENT_TIME', 'INCIDENT_MIN']
    columnspresent = all(col in df.columns for col in expectedcolumns)
    timecheck = df['INCIDENT_TIME'].tolist() == ['00:01:51', '00:06:12', '00:12:12']
    weekcheck = df['WEEK_DAY'].tolist() == [6, 6, 6]
    incidentmincheck = df['INCIDENT_MIN'].tolist() == [1.850000, 6.200000, 12.200000]
    test_result = (columnspresent and timecheck and
                   weekcheck and incidentmincheck)
    return test_result

def test_filter_by_time():
    '''a'''
    data = {
        'INCIDENT_DATE': ['11/01/2023', '11/02/2023', '11/03/2023'],
        'WEEK_DAY': [0, 1, 2],
        'INCIDENT_TIME': ['08:30:00', '12:45:00', '18:20:00'],
        'INCIDENT_MIN': [510, 765, 1100]
    }

    df = pd.DataFrame(data)
    dffi = filter_by_time(df, days=[0, 1, 2], start_min=600, end_min=1200)
    expected_rows = 2
    rowscheck = dffi.shape[0] == expected_rows
    weekdaycheck = all(day in [0, 1, 2] for day in dffi['WEEK_DAY'])
    incidentmincheck = all(600 <= minute <= 1200 for minute in dffi['INCIDENT_MIN'])
    testresult = rowscheck and weekdaycheck and incidentmincheck
    return testresult
