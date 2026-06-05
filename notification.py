def get_health_alerts(features):
    alerts = []
    # Example alerts
    hb = features.get('Hemoglobin')
    wbc = features.get('WBC_COUNT')
    if hb is not None and hb < 13:
        alerts.append("Alert: Hemoglobin is low, risk of anemia.")
    if wbc is not None and wbc > 11000:
        alerts.append("Alert: High WBC count, possible infection.")
    if not alerts:
        alerts.append("No critical health alerts for this blood report.")
    return alerts
