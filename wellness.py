def get_wellness_guidance(features):
    recs = []
    if features.get('Hemoglobin', 0) < 12:
        recs.append("Eat more iron-rich foods such as spinach, lentils, red meat. Consider supplements.")
    if features.get('Fasting_Blood_Sugar', 0) > 110:
        recs.append("Maintain regular exercise and reduce consumption of sweets/carbohydrates.")
    if features.get('LDL', 0) > 130:
        recs.append("Reduce fried/processed foods and increase intake of fruits and vegetables.")
    if features.get('Vitamin_D', 99) < 30:
        recs.append("Increase exposure to sunlight, consume fortified foods or supplements.")
    if not recs:
        recs.append("Your results are generally healthy! Keep up your wellness routine.")
    return recs
