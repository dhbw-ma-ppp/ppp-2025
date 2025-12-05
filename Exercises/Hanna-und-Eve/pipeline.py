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

question1 = "What ist the total amount?"
question2 = "company"

# for i, sample in enumerate(train_batch):
#    image = sample["image"]
#    result1 = pipeline(image=image, question= question1)
#    result2 = pipeline(image=image, question= question2)

def get_amount(image):
    image_rgb = image.convert("RGB")
    result1 = pipeline(image=image, question= question1)
    result2 = pipeline(image=image, question= question2)

    print("Predicted Total :", result1)
    print("Predicetd Store  :", result2)
    print("-"*50)
    return result1, result2
