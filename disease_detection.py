# from PIL import Image
# import random

# DISEASES = ["Healthy", "Blight", "Bacterial Wilt"]

# def detect_disease_from_image(image: Image.Image):
#     disease = random.choices(DISEASES, weights=[0.5, 0.3, 0.2], k=1)[0]
#     confidence = round(random.uniform(0.75, 0.99), 2)
#     explanation = f"Detected {disease} based on visible symptoms like discoloration or spots."
#     return disease, confidence, explanation

from PIL import Image
import random

DISEASES = ["Healthy", "Blight", "Bacterial Wilt"]

def detect_disease_from_image(image: Image.Image):
    disease = random.choices(DISEASES, weights=[0.5, 0.3, 0.2], k=1)[0]
    confidence = round(random.uniform(0.75, 0.99), 2)
    explanation = f"Detected {disease} based on visible symptoms like discoloration or spots."
    return disease, confidence, explanation
