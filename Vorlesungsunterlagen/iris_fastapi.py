# uvicorn iris_fastapi:app --port 3334 --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


data = pd.read_csv('../data/iris.csv')


@app.get("/iris")
async def get_iris(
            min_sepal_length: float = 4, max_sepal_length: float = 8,
            min_sepal_width: float = 2, max_sepal_width: float = 5,
            min_petal_length: float = 1, max_petal_length: float = 7,
            min_petal_width: float = 0, max_petal_width: float = 3,
        ):
    filtered_data = data.query(
        'sepal_length > @min_sepal_length and sepal_length <= @max_sepal_length and '
        'sepal_width > @min_sepal_width and sepal_width <= @max_sepal_width and '
        'petal_length > @min_petal_length and petal_length <= @max_petal_length and '
        'petal_width > @min_petal_width and petal_width <= @max_petal_width'
    )
    return filtered_data.to_dict(orient='list')
