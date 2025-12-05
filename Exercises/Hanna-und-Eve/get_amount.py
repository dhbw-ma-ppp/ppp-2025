import torch
from dataset import *
from transformers import pipeline
from PIL import Image

pipeline = pipeline(
    task="document-question-answering",
    model="naver-clova-ix/donut-base-finetuned-docvqa",
    device=-1,
    dtype=None
)
question = "Was ist die Summe?"
print("hey")

def get_amount(image):
    image_rgb = image.convert("RGB")
    result = pipeline(image=image_rgb, question= question)

    print("Predicted  :", result)
    print("-"*50)
    return result