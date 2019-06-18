from flask import Flask, jsonify,render_template, request
import tensorflow
import time,os
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

import numpy as np #модуль для численных манипуляций с большим объемом данных
import pandas as pd #модуль для работы с таблицами


@app.route('/')
def dash_overview():
	return render_template('index.html')
	
@app.route('/api', methods=['POST'])
def UploadFiles():
    
    upload = request.files.get()
    upload.save(upload.filename)
    print(upload.filename)
    start_time = time.time()
    #table = (pd.read_csv('test/'+uploadinc.filename,sep=' ',header=None,dtype={0:'str',1:'str'}))
    #if len(table.T) == 2:
    #    del table[0]
    #a = table.T.astype('float')
    #print(a)
    #b = list(a.iloc[0])
    #b.insert(0,float(uploadinc.filename[:-4]))
    #testt = np.array(b)
    #test_pool = Pool(testt)
    #print(len(b))
    #print(len(a))
    #preds = model.predict(test_pool)
    #print(sqrt(mean_squared_error(y_test, preds)))
    #print(mean_absolute_error(y_test, preds))
    print("--- %s seconds ---" % (time.time() - start_time))
    return jsonify({"BIS-index":"29.2344123123"})
    
#if __name__ == '__main__':
  #  app.run(,use_reload=True)
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False, host='0.0.0.0', port=3334)