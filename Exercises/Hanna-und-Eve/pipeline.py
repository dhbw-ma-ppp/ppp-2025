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

question = "Which items were bought?"
answers = []

for i, sample in enumerate(train_batch):
    image = sample["image"]
    result = pipeline(image=image, question= question)
    answers.append(result)

    print(f"Bild {i+1}:")
    print("Ground truth:", sample["text"])
    print("Predicted  :", result)
    print("-"*50)