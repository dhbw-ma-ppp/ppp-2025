from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")
import torch 

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")

def predict_email(email_text):
    # Preprocess and tokenize
    inputs = tokenizer(
        email_text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # Get probabilities for each class
    probs = predictions[0].tolist()
    
    # Create labels dictionary
    labels = {
        "legitimate_email": probs[0],
        "phishing_url": probs[1],
        "legitimate_url": probs[2],
        "phishing_url_alt": probs[3]
    }
    
    # Determine the most likely classification
    max_label = max(labels.items(), key=lambda x: x[1])
    
    return {
        "prediction": max_label[0],
        "confidence": max_label[1],
        "all_probabilities": labels
    }


# Example usage
email = """
Dear User,
Your account security needs immediate attention. Please verify your credentials.
Click here: http://suspicious-link.com
"""

result = predict_email(email)
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
print("\nAll probabilities:")
for label, prob in result['all_probabilities'].items():
    print(f"{label}: {prob:.2%}")
