from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
import pickle
app = Flask(__name__)

@app.route('/',methods=['post','get']) # will use get for the first page-load, post for the form-submit
def predict(): # this function can have any name
    try:
        model = load_model('mymodel.h5') # the mymodel.h5 file was created in Colab, downloaded and uploaded using Filezilla
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)

        age = request.form.get('age') 
        resting_BP = request.form.get('restingBP')
        cholesterol = request.form.get('cholesterol')
        fasting_BS = request.form.get('fasting')
        max_HR = request.form.get('maxHR')
        old_peak = request.form.get('oldPeak')
        
        # F or M
        gender = request.form.get('gender')
        female = 0
        male = 0
        if gender == 'F':
            female = 1
        elif gender == 'M':
            male = 1
       
        
         # Chest pain NAP TA ATA NAP
        chest_pain = request.form.get('chestPain')
        chest_ATA = 0
        chest_NAP = 0
        chest_TA = 0
        chest_ASY = 0
        if chest_pain == 'ATA':
            chest_ATA = 1
        elif chest_pain == 'NAP':
            chest_NAP = 1
        elif chest_pain == 'TA':
            chest_TA = 1
        elif chest_pain == 'ASY':
            chest_ASY = 1
      
        
         # Resting ECG ST N
        resting_ECG = request.form.get('ECG')
        ECG_normal = 0
        ECG_st = 0
        ECG_lvh = 0

        if resting_ECG == 'N':
            ECG_normal = 1
        elif resting_ECG == 'ST':
            ECG_st = 1
        elif resting_ECG == 'LVH':
            ECG_lvh = 1
     
        
        # Exercise angina YES NO
        exercise_angina = request.form.get('angina')
        angina_YES = 0
        angina_NO = 0

        if exercise_angina == 'Y':
            angina_YES = 1
        elif exercise_angina == 'N':
            angina_NO = 1
  

        # ST Slope Down Flat Up
        ST_slope = request.form.get('STSlope')

        slope_down = 0
        slope_flat = 0
        slope_up = 0

        if ST_slope == 'DOWN':
            slope_down = 1
        elif ST_slope == 'FLAT':
            slope_flat = 1
        elif ST_slope == 'UP':
            slope_up = 1
      
    
        my_array = [age, resting_BP, cholesterol, fasting_BS, max_HR, old_peak, female, male, chest_ASY, chest_ATA, chest_NAP, chest_TA, ECG_lvh, ECG_normal, ECG_st, angina_NO, angina_YES, slope_down, slope_flat, slope_up]

    

        if any(value is None for value in my_array):
        # check if any number is missing
            return render_template('index.html', result='Missing inputs')
        # calling render_template will inject the variable 'result' and send index.html to the browser
        else:
            arr = np.array([[float(value) for value in my_array]]) # cast string to decimal number, and make 2d numpy array.
            scaled_array = scaler.transform(arr)
            predictions = model.predict(scaled_array) # make new prediction
            if predictions[0][0] < 0.5:
                return render_template('index.html', result=str(predictions[0][0]), risk=str('Low risk of heart failure'))
            else:
                return render_template('index.html', result=str(predictions[0][0]), risk=str('High risk of heart failure!'))
        # the result is set, by asking for row=0, column=0. Then cast to string.
    except Exception as e:
        return render_template('index.html', result='error ' + str(e))

if __name__ == '__main__':
    app.run()