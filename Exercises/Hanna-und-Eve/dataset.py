from datasets import load_dataset
from PIL import Image
from sklearn.model_selection import train_test_split
import numpy as np

def format(ds, indizes):
    batch = []
    for i in indizes:
        sample = ds[i]
        image = sample["image"].convert("RGB")  # PIL Image
        text = sample.get("text", "")
        batch.append({"image": image, "text": text})
    return batch


ds_dic = load_dataset("mychen76/ds_receipts_v2_train")

ds = ds_dic["train"]

ds_split = ds.train_test_split(test_size=0.2, seed=42) #seed sorgt dafür, dass bei jeder Wiederholung die Test splits gleich aufgeteil ist (ist besser fürs vergleichen)
train_ds = ds_split["train"]
test_ds = ds_split["test"]

#Das erwartet unser Model:
#{
#    "image": PIL.Image.Image,  -RGB
#    "text": "Label-Text"       -für den Vergleich
#}

train_batch = format(train_ds, range(20))
test_batch = format(test_ds, range(20))

#Sprache!!