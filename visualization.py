import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_value_plot(features):
    labels = list(features.keys())
    values = [features[k] for k in labels]
    plt.figure(figsize=(8,3))
    bars = plt.bar(labels, values, color='#b30000')
    plt.title("Your Blood Report - Key Values")
    plt.ylabel("Measured Value")
    plt.xticks(rotation=15)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(round(bar.get_height(),2)), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plot_path = "static/barplot.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path
