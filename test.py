from misingval import modelPred


sample_data = {
    "age": 28,
    "pre_pregnancy_bmi": None,
    "gestational_age_weeks": 20,
    "blood_pressure_systolic": 118,
    "blood_pressure_diastolic": 76,
    "hemoglobin_level": 12.8,
    "number_of_prenatal_visits": 5,
    "has_diabetes": 0,           # 0 = No, 1 = Yes
    "has_hypertension": 0,       # 0 = No, 1 = Yes
    "smoking_status": 0,          # 0 = Non-smoker, 1 = Smoker
    "alcohol_consumption": 0      # 0 = None, 1 = Occasional/Yes
}


print(modelPred(sample_data))





sample_data = {
        "age": 28,
        "pre_pregnancy_bmi": None,
        "gestational_age_weeks": 20,
        "blood_pressure_systolic": 118,
        "blood_pressure_diastolic": 76,
        "hemoglobin_level": 12.8,
        "number_of_prenatal_visits": 5,
        "has_diabetes": 0,
        "has_hypertension": 0,
        "smoking_status": 0,
        "alcohol_consumption": 0
    }
    sample_risk = [25, 130, 80, 15.0, 98.0, 86]


