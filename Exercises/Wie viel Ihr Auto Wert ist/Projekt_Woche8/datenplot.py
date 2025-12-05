from flask import Flask, render_template
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/")
def index():
    # Plot erstellen
    x = [1, 2, 3, 4, 5]
    y = [10, 14, 18, 22, 27]
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))

    # HTML-Code für den Plot
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Übergabe an Template
    return render_template("index.html", plot_html=plot_html)

if __name__ == "__main__":
    app.run(debug=True)
