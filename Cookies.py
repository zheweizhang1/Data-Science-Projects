"""
Name: Zhe Wei Zhang
Email: zhewei.zhang82@myhunter.cuny.edu
Resources: Classnotes
"""
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

def import_data(csv_file, names=None):
    '''a'''
    df = pd.read_csv(csv_file)
    df = df.drop(['DATE'],axis = 1)
    if names is None:
        df = df.apply(lambda col: pd.to_numeric(col, errors ='coerce'))
        df = df.dropna()
        return df
    df = df.rename(columns = names)
    df = df.apply(lambda col: pd.to_numeric(col, errors ='coerce'))
    df = df.dropna()
    return df

def split_data(df, xes_col_names, y_col_name, test_size = 0.33, random_state = 106):
    '''a'''
    df1 = df[xes_col_names]
    df2 = df[y_col_name]
    return train_test_split(df1, df2, test_size = test_size,random_state = random_state)

def fit_lin_reg(x_train, y_train):
    '''a'''
    reg = LinearRegression().fit(x_train, y_train)
    with open('reg.pickle','wb') as fac:
        return pickle.dump(reg, fac, pickle.HIGHEST_PROTOCOL)

def encode_poly(df, x_col, deg=2):
    '''a'''
    df1 = df[[x_col]]
    df2 = df1.to_numpy()
    poly = PolynomialFeatures(deg)
    poly_features = poly.fit_transform(df2)
    return poly_features

def fit_poly(xes, yes, epsilon=0.01, verbose=False):
    '''a'''
    error = 101
    deg = 0
    xes = xes.to_numpy()
    yes = yes.to_numpy()
    x_pol = 1
    while error > epsilon:
        if (deg >= 5) & (error > epsilon):
            return None
        deg += 1
        poly_features = PolynomialFeatures(deg)
        x_pol = poly_features.fit_transform(xes)
        model = LinearRegression(fit_intercept=False).fit(x_pol, yes)
        y_pred = model.predict(x_pol)
        error = mean_squared_error(yes, y_pred)
        if verbose:
            print (f'MSE cost for deg {deg} poly model: {error:.3f}')
    return deg

def fit_with_regularization(xes, yes, poly_deg=2, reg = "lasso"):
    '''a'''
    poly_features = PolynomialFeatures(poly_deg)
    x_pol = poly_features.fit_transform(xes)
    if reg == "ridge":
        model = RidgeCV().fit(x_pol, yes)
        with open('model.pickle','wb') as fac:
            return pickle.dump(model, fac, pickle.HIGHEST_PROTOCOL)
    else:
        model = LassoCV().fit(x_pol, yes)
        with open('model.pickle','wb') as fac:
            return pickle.dump(model, fac, pickle.HIGHEST_PROTOCOL)

def predict_using_trained_model(mod_pkl, xes, yes):
    '''a'''
    choc3 = pickle.loads(mod_pkl)
    y_pred = choc3.predict(xes)

    mse = mean_squared_error(yes, y_pred)
    rtwo = r2_score(yes, y_pred)
    return mse, rtwo

def test_encode_poly():
    '''a'''
    data = [3.328]
    df = pd.DataFrame(data, columns=['Numbers'])
    x_col = 'Numbers'
    array = [[ 1., 3.328, 11.076]]
    if (encode_poly(df,x_col,) == array).all():
        return True
    return False
