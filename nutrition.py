def get_nutrition_recommendations(features):
    recs = []
    if features.get('Hemoglobin', 99) < 13:
        recs.append("Increase iron: spinach, lentils, eggs, lean meat.")
    if features.get('Vitamin_D', 99) < 30:
        recs.append("Get more sunlight, consider Vitamin D supplement.")
    if features.get('LDL', 0) > 130:
        recs.append("Eat low-fat foods, reduce fried food.")
    if features.get('Fasting_Blood_Sugar', 0) > 100:
        recs.append("Reduce sugar/carbs, eat whole grains.")
    if not recs:
        recs.append("Maintain a balanced, nutritious diet.")
    return recs
