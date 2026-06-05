def predict_diseases(features):
    diseases = []
    scores = []
    # Example risk logic based on typical values
    hb = features.get('Hemoglobin', None)
    rbc = features.get('RBC_COUNT', None)
    wbc = features.get('WBC_COUNT', None)
    platelets = features.get('Platelet_Count', None)

    if hb is not None and hb < 13:
        diseases.append("Anemia risk")
        scores.append("High")
    if wbc is not None and wbc > 11000:
        diseases.append("Possible Infection")
        scores.append("Moderate")
    if platelets is not None and platelets < 150000:
        diseases.append("Thrombocytopenia risk")
        scores.append("Moderate")
    if not diseases:
        diseases.append("No major risks detected")
        scores.append("Low")
    return diseases, scores
