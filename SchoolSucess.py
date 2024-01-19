"""
Name: Zhe Wei Zhang
Email: zhewei.zhang82@myhunter.cuny.edu
Resources: Classnotes
"""
import pandas as pd

def import_data(file_name):
    '''a'''
    df = pd.read_csv(file_name)
    df = df[['dbn','school_name','NTA','graduation_rate','pct_stu_safe',
             'attendance_rate','college_career_rate','language_classes',
             'advancedplacement_courses','method1','overview_paragraph']]
    df = df.dropna(subset=['graduation_rate'])
    return df

def impute_numeric_cols(df):
    '''a'''
    df1 = df['pct_stu_safe'].median()
    df2 = df['attendance_rate'].median()
    df3 = df['college_career_rate'].median()

    df['pct_stu_safe'].fillna(df1)
    df['attendance_rate'].fillna(df2)
    df['college_career_rate'].fillna(df3)
    return df

def compute_count_col(df,col):
    '''a'''
    series = df[col].str.count(',')
    return series

def encode_categorical_col(col):
    '''a'''
    df = col.str.get_dummies(sep=', ')
    df = df.sort_index(axis = 1,ascending= True)
    return df

def split_test_train(df, xes_col_names, y_col_name, frac=0.25, random_state=922):
    '''a'''
    df_test = df.sample(frac = frac, random_state = random_state)
    df_train = df
    df_train = df_train.drop(df_test.index)
    return df_train[xes_col_names],df_test[xes_col_names],df_train[y_col_name],df_test[y_col_name]

# linear reg model
def compute_lin_reg(xes, yes):
    '''a'''
    sd_x = xes.std()
    sd_y = yes.std()
    rad = xes.corr(yes)
    theta_1 = rad * (sd_y/sd_x)
    theta_0 = yes.mean() - (theta_1 * xes.mean())
    return theta_0, theta_1

#evals
def predict(xes, theta_0, theta_1):
    '''a'''
    xay = pd.Series(xes)
    return xay.map(lambda x: x *theta_1 + theta_0)

def mse_loss(y_actual,y_estimate):
    '''a'''
    mse1 = 0
    car = y_actual - y_estimate
    for iai in car:
        mse1 += iai ** 2
    return mse1 / y_actual.count()

def rmse_loss(y_actual,y_estimate):
    '''a'''
    return mse_loss(y_actual,y_estimate) ** (1/2)

def compute_error(y_actual,y_estimate,loss_fnc=mse_loss):
    '''a'''
    return loss_fnc(y_actual,y_estimate)

def test_compute_count_col(compute_fnc=compute_count_col):
    '''a'''
    data = {'Name': ['A,B,C']}
    df = pd.DataFrame(data)
    data2 = [3]
    df2 = pd.Series(data2)
    return compute_fnc(df,'Name').equals(df2)

def test_predict(predict_fnc=predict):
    '''a'''
    dict1 = {'0':1,
             '1':2}
    dict2 = {'0':2,
             '1':3}
    ser = pd.Series(dict1)
    ser2 = pd.Series(dict2)
    ser3 = [1]
    if pd.Series(predict(ser3,1,1)).equals(42):
        return False
    abc = pd.Series(predict_fnc(ser,1,1)).equals(ser2)
    return abc

def test_mse_loss(loss_fnc=mse_loss):
    '''a'''
    data1= [10,2,8]
    data2= [4,2,11]
    ser1 = pd.Series(data1)
    ser2 = pd.Series(data2)
    return loss_fnc(ser1,ser2) == 15
