from flask import Flask, render_template
import plotly.express as px
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "data"))
from data import df as car_price_data

app = Flask(__name__)

@app.route("/")
def index():
    df = car_price_data

    # Preisverteilung
    fig = px.histogram(df, x="Price", nbins=50, title="Preisverteilung")
    fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"))
    price_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Preis vs Laufleistung
    fig = px.scatter(df, x="Mileage", y="Price", color="Fuel type_Petrol",
                     title="Preis vs. Laufleistung (Beispiel: Petrol)")
    fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"))
    mileage_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Preis nach Baujahr
    fig = px.box(df, x="Prod. year", y="Price", title="Preis nach Baujahr")
    fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"))
    box_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Anzahl an Autos nach Kategorie
    category_cols = [c for c in df.columns if c.startswith("Category_")]
    category_counts = df[category_cols].sum()
    fig = px.bar(x=category_counts.index, y=category_counts.values, title="Fahrzeuganzahl pro Kategorie")
    fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"))
    category_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Kraftstoffverteilung
    fuel_cols = [c for c in df.columns if c.startswith("Fuel type_")]
    fuel_counts = df[fuel_cols].sum()
    fig = px.pie(names=fuel_counts.index, values=fuel_counts.values, title="Kraftstoffverteilung")
    fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"))
    fuel_plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Übergabe an Template
    return render_template("index.html",
                           price_plot=price_plot_html,
                           mileage_plot=mileage_plot_html,
                           box_plot=box_plot_html,
                           category_plot=category_plot_html,
                           fuel_plot=fuel_plot_html)

if __name__ == "__main__":
    app.run(debug=True)
