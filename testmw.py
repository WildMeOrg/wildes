import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import AutoModel

model_tag = f"conservationxlabs/miewid-msv3"
model = AutoModel.from_pretrained(model_tag, trust_remote_code=True)

def generate_random_image(height=440, width=440, channels=3):
    random_image = np.random.randint(0, 256, (height, width, channels), dtype=np.uint8)
    return Image.fromarray(random_image)

random_image = generate_random_image()

preprocess = transforms.Compose([
    transforms.Resize((440, 440)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_tensor = preprocess(random_image)
input_batch = input_tensor.unsqueeze(0) 

with torch.no_grad():
    output = model(input_batch)

print(output)
print(output.shape)
