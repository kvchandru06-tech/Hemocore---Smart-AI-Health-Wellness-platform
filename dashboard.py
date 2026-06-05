def get_dashboard_stats(features):
    # Shows all features neatly
    return [{"name": k, "value": v} for k, v in features.items()]
