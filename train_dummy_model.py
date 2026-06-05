import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

print("Script started!")  # debugging step

X = np.array([
    [13.2, 85, 120, 50, 145, 40],   # normal
    [12.0, 120, 170, 38, 250, 22],  # high risk
    [14.0, 90, 110, 45, 140, 35],   # normal
    [11.5, 125, 190, 37, 180, 15],  # high risk
    [13.8, 80, 125, 60, 130, 42],   # normal
    [12.5, 115, 160, 42, 160, 25],  # normal
    [12.9, 99, 125, 53, 140, 35],   # normal
    [11.7, 110, 150, 36, 170, 18],  # high risk
    [13.5, 85, 120, 47, 150, 38],   # normal
    [12.1, 130, 200, 35, 190, 12],  # high risk
])
y = np.array([0,1,0,1,0,0,0,1,0,1])  # 0=Normal, 1=High Risk

clf = RandomForestClassifier()
clf.fit(X, y)
joblib.dump(clf, "blood_risk_model.pkl")
print("Dummy model saved!")
