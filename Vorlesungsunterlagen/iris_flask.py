# flask --app iris_flask run --reload

from flask import Flask, request
from jinja2 import Template
import pandas as pd


app = Flask(__name__)

data = pd.read_csv('../data/iris.csv')


@app.route("/", methods=['GET', 'POST'])
def main():
    filters = dict(
        min_sepal_length=4.,
        max_sepal_length=8.,
        min_sepal_width=1.,
        max_sepal_width=5.,
        min_petal_length=0.,
        max_petal_length=7.,
        min_petal_width=0.,
        max_petal_width=3.,
    )

    if request.method == 'POST':
        filters = {k: float(v) for k, v in request.form.items()}
        filters['min_sepal_length'] = min(filters['min_sepal_length'], filters['max_sepal_length'])
        filters['min_sepal_width'] = min(filters['min_sepal_width'], filters['max_sepal_width'])
        filters['min_petal_length'] = min(filters['min_petal_length'], filters['max_petal_length'])
        filters['min_petal_width'] = min(filters['min_petal_width'], filters['max_petal_width'])

    filtered_data = data
    for key, value in filters.items():
        minmax, column = key.split('_', 1)
        sign = '>' if minmax == 'min' else '<='
        filtered_data = filtered_data.query(f'{column} {sign} {value}')

    html_table = filtered_data.to_html()
    # Jinja2 Template
    template = Template(
        '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Iris in Flask</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <style>
            table {
                text-align: center;
                table-layout: auto;
            }
            tr {
                text-align: center;
                padding: 1rem;
                border-bottom-width: 1px;
            }
            th {
                border-color: rgb(219 234 254);
                background-color: rgb(239 246 255);
                text-align: center;
            }
            td {
                border-color: rgb(239 246 255);
            }
        </style>
        <body>

            <div class="text-4xl p-4 text-center">
            Explore Iris Data
            </div>
            <div class="flex w-full h-full p-4 items-center">
                <div class="w-1/3 h-full">
                    <form method=post enctype=multipart/form-data>
                    <div class="flex flex-col items-center">
                        <div class="w-40 p-2 m-2 border-2 rounded-md">
                        <label for="sepal_length_min_range" class="block mb-2 text-sm font-medium text-gray-900">Sepal Length</label>
                        <input id="sepal_length_min_range" type="range" value={{ min_sepal_length }} min=4 max=8 step=0.1 name="min_sepal_length" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        <input id="sepal_length_max_range" type="range" value={{ max_sepal_length }} min=4 max=8 step=0.1 name="max_sepal_length" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        </div>
                        <div class="w-40 p-2 m-2 border-2 rounded-md">
                        <label for="sepal_width_min_range" class="block mb-2 text-sm font-medium text-gray-900">Sepal Width</label>
                        <input id="sepal_width_min_range" type="range" value={{ min_sepal_width}} min=1 max=5 step=0.1 name="min_sepal_width" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        <input id="sepal_width_max_range" type="range" value={{ max_sepal_width }} min=1 max=5 step=0.1 name="max_sepal_width" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        </div>
                        <div class="w-40 p-2 m-2 border-2 rounded-md">
                        <label for="petal_length_min_range" class="block mb-2 text-sm font-medium text-gray-900">Petal Length</label>
                        <input id="petal_length_min_range" type="range" value={{ min_petal_length }} min=0 max=7 step=0.1 name="min_petal_length" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        <input id="petal_length_max_range" type="range" value={{ max_petal_length }} min=0 max=7 step=0.1 name="max_petal_length" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        </div>
                        <div class="w-40 p-2 m-2 border-2 rounded-md">
                        <label for="petal_width_min_range" class="block mb-2 text-sm font-medium text-gray-900">Petal Width</label>
                        <input id="petal_width_min_range" type="range" value={{ min_petal_width }} min=0 max=3 step=0.1 name="min_petal_width" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        <input id="petal_width_max_range" type="range" value={{ max_petal_width }} min=0 max=3 step=0.1 name="max_petal_width" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"/>
                        </div>

                        <input class="bg-slate-600 hover:bg-slate-500 text-white font-semibold py-2 px-4 border rounded-lg" type=submit value="Apply" />
                    </div>
                    </form>
                </div>
                <div class="
                        w-2/3 h-80 overflow-y-scroll px-auto
                        relative flex flex-col text-gray-700 bg-white shadow-md rounded-xl bg-clip-border
                        [&::-webkit-scrollbar]:w-2
                        [&::-webkit-scrollbar-track]:bg-gray-100
                        [&::-webkit-scrollbar-thumb]:bg-gray-300
                        ">
                    {{ html_table|safe }}
                </div>
            </div>
        </body>
        </html>
        '''
    )
    return template.render(html_table=html_table, **filters)
