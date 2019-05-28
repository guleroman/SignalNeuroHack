from flask import Flask, jsonify,render_template, request
import uuid, time,os
import requests
#
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

import catboost 
from catboost import Pool, CatBoostRegressor

import numpy as np #модуль для численных манипуляций с большим объемом данных
import pandas as pd #модуль для работы с таблицами
#from sklearn.ensemble import GradientBoostingRegressor #модуль для градиентного бустинга
from sklearn.metrics import mean_squared_error, mean_absolute_error #для подсчета значения MAE - абсолютной ошибки
from math import sqrt
def rmse(y_true, y_pred):
    return sqrt(mean_squared_error(y_true, y_pred))
#!pip install catboost
#%matplotlib inline

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
#
y_train = train['param'].values
y_test = test['param'].values
X_train = train
X_test = test 
del X_train['param']
del X_test['param']
X_train = X_train.values
X_test = X_test.values


train_pool = Pool(X_train, y_train)#, cat_features=[0,2,5])
#test_pool = Pool(X_test)
model = CatBoostRegressor()
model.load_model('model_2', format='catboost')

#@app.route('/api/<file_name>',methods=['GET'])
#def write_image(file_name):
#    start_time = time.time()
#    preds = model.predict(test_pool)
#    print(sqrt(mean_squared_error(y_test, preds)))
#    print(mean_absolute_error(y_test, preds))
#    print("--- %s seconds ---" % (time.time() - start_time))
#    return jsonify(mean_absolute_error(y_test, preds))
@app.route('/')
def dash_overview():
	return render_template('index.html')
	
@app.route('/upload', methods=['POST'])
def UploadFiles():
    print ("inside upload files")
    uploadinc = request.files.get('uploadinc')
    #uploadinc.save(uploadinc.filename)
    print(uploadinc.filename)
    start_time = time.time()
    table = (pd.read_csv('test/'+uploadinc.filename,sep=' ',header=None,dtype={0:'str',1:'str'}))
    if len(table.T) == 2:
        del table[0]
    a = table.T.astype('float')
    print(a)
    b = list(a.iloc[0])
    b.insert(0,float(uploadinc.filename[:-4]))
    testt = np.array(b)
    test_pool = Pool(testt)
    print(len(b))
    #print(len(a))
    preds = model.predict(test_pool)
    #print(sqrt(mean_squared_error(y_test, preds)))
    #print(mean_absolute_error(y_test, preds))
    print("--- %s seconds ---" % (time.time() - start_time))
    return jsonify(preds)
    
#if __name__ == '__main__':
  #  app.run(,use_reload=True)
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False, host='0.0.0.0', port=8060)