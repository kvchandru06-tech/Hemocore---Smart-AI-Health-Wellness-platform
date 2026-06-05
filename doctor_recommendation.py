def recommend_doctors(features):
    doctors = []
    # Example logic matching to risks above
    hb = features.get('Hemoglobin', None)
    wbc = features.get('WBC_COUNT', None)
    platelets = features.get('Platelet_Count', None)

    if hb is not None and hb < 13:
        doctors.append("Consult a Hematologist for anemia")
    if wbc is not None and wbc > 11000:
        doctors.append("Visit a General Physician for possible infection check")
    if platelets is not None and platelets < 150000:
        doctors.append("Meet a Hematologist for low platelets")
    if not doctors:
        doctors.append("No specific specialist required based on report")
    return doctors
