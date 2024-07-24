from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
app= Flask(__name__)
motor = pd.read_csv("olx.csv")

model = pickle.load(open("MotorPriceModel.pkl",'rb'))

@app.route('/')
def index():
    Companies = sorted(motor['company'].unique())
    motor_models = sorted(motor['name'].unique())
    Year = sorted(motor['year'].unique(),reverse=True)
    fuel_types = motor['fuel_type'].unique()
    Companies.insert(0,"Select company")
    return render_template("index.html", companies = Companies, motor_models=motor_models, Years= Year, fuel_types= fuel_types)

@app.route('/predict', methods = ['POST'])
def predict():
    Company = request.form.get('company')
    motor_model = request.form.get('motor_models')
    Year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel')
    kms_driven = int(request.form.get('kilo'))
    print(company,motor_model, year,fuel_type,kms_driven)
    
    prediction = model.predict(pd.DataFrame([[motor_model, company, year, kms_driven, fuel_type]], columns=['name','company','year','kms_driven','fuel_type']))
    return str(np.round(prediction[0],2))

if __name__ == "__main__":
    app.run(debug = True)