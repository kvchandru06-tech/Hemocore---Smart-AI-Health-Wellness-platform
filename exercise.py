def get_exercise_plan(features):
    plan = []
    plan.append("Daily 30 min brisk walking or cycling.")
    if features.get("Triglycerides", 0) > 150:
        plan.append("Add 20 min yoga or stretching daily.")
    if features.get("Vitamin_D", 99) < 30:
        plan.append("Exercise outdoors in morning sunlight.")
    plan.append("Include 3x/week strength training.")
    return plan
