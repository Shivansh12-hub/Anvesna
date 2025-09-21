from keras.models import load_model
import pickle
import numpy as np
from modelClass import LCAmodel



model = load_model(
    "GarbhSathi.keras", 
    custom_objects={"LCAmodel": LCAmodel}
)

with open("LabelEncoders.pkl", "rb") as f:
    LabelEncoders = pickle.load(f)


with open("model.pkl","rb") as f:
    riskmodel = pickle.load(f)    

def Encoded_val(sample_row):
    ld = []
    mask = []
    for key, val in sample_row.items():
        if val is not None:
            if key in LabelEncoders:
                if val in LabelEncoders[key].classes_:
                    encoded = LabelEncoders[key].transform([val])[0]
                else:
                    encoded = 0
                ld.append(encoded)
            else:
                ld.append(val)
            mask.append(1)
        else:
            ld.append(0.0)
            mask.append(0)
    return np.array(ld, dtype=np.float32), np.array(mask, dtype=np.float32)



def modelPred(sample_row):
        
    X, mask = Encoded_val(sample_row)

    X_input = X.reshape(1, -1)
    mask_input = mask.reshape(1, -1)
    pred = model.predict([X_input, mask_input])

    result = {}




    columns = [
        "age", 
        "pre_pregnancy_bmi",
        "gestational_age_weeks",
        "blood_pressure_systolic",
        "blood_pressure_diastolic",
        "hemoglobin_level",
        "number_of_prenatal_visits",
        "has_diabetes",
        "has_hypertension",
        "smoking_status",
        "alcohol_consumption",
       
    ]



    for i, m, v in zip(columns, mask, pred[0]):
        if m != 0:
            result[i] = sample_row[i]
        else:
            if i in LabelEncoders:
                v=int(round(v))
                if v<0 : v=0

                inv = LabelEncoders[i].inverse_transform([v])[0]
                result[i] = inv
            else:
                result[i] = round(float(v), 2)

    return result




def health_risk(sample_risk):
    sample_risk = np.array([sample_risk])  
    ans = riskmodel.predict(sample_risk)
    return ans
