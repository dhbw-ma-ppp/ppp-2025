from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.express as px

from .data.data import df as car_price_prediction_data


app = Flask(__name__)

@app.route("/")
def index():
    print (car_price_prediction_data)
    # Plot erstellen
    x = 1
    y = 1

    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))


    # plot template
    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )


    # HTML-Code für den Plot
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Übergabe an Template
    return render_template("index.html", plot_html=plot_html)

if __name__ == "__main__":
    # app.run(debug=True)
    pass