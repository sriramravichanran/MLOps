from flask import Flask, render_template, request
from src.logger import get_logger
import joblib
from config.config_paths import MODEL_OUTPUT_PATH
import numpy as np
import pandas as pd

logger = get_logger(__name__)

app = Flask(__name__)

model_loaded = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        V12 = int(request.form["V12"])
        Amount = int(request.form["Amount"])
        V4 = int(request.form["V4"])
        V3 = int(request.form["V3"])
        V2 = int(request.form["V2"])
        V10 = int(request.form["V10"])
        V18 = int(request.form["V18"])
        V13 = int(request.form["V13"])
        V14 = int(request.form["V14"])
        V1 = int(request.form["V1"])
        Time = int(request.form["Time"])
        V20 = int(request.form["V20"])
        V22 = int(request.form["V22"])
        V5 = int(request.form["V5"])
        V9 = int(request.form["V9"])
        V7 = int(request.form["V7"])
        V21 = int(request.form["V21"])
        V24 = int(request.form["V24"])
        V26 = int(request.form["V26"])
        V27 = int(request.form["V27"])

        features = pd.DataFrame(
    [[V12, Amount, V4, V3, V2, V10, V18, V13, V14, V1,
      Time, V20, V22, V5, V9, V7, V21, V24, V26, V27]],
    columns=[
        'V12', 'Amount', 'V4', 'V3', 'V2',
        'V10', 'V18', 'V13', 'V14', 'V1',
        'Time', 'V20', 'V22', 'V5', 'V9',
        'V7', 'V21', 'V24', 'V26', 'V27'
    ]
)

        prediction = model_loaded.predict(features)

        return render_template('index.html',prediction = prediction[0])
    
    return render_template("index.html",prediction= None)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)