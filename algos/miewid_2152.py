import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import AutoModel
import base64
from io import BytesIO

# os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
# os.environ['TORCH_USE_CUDA_DSA'] = "1"

# Global variables to hold model and device


class miewid_2152:
#    @staticmethod
#    def get_embedding(image_url: str) -> list:
        # Placeholder embedding logic
#        return [0.1] * 2048

    model = None
    device = None

    def __init__(self) -> None:
        model_tag= f"conservationxlabs/miewid-msv2"
        self.model = AutoModel.from_pretrained(model_tag, trust_remote_code=True)

    def load_model(model_tag= f"conservationxlabs/miewid-msv2" ):
        #global model, device
        model = AutoModel.from_pretrained(model_tag, trust_remote_code=True)
        return model

    def load_image_from_file(file_path: str):
        image = Image.open(file_path).convert("RGB")  # Ensure it's RGB format
        return image

    def preprocess(img):
        prepr = transforms.Compose([
        transforms.Resize((440, 440)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        return prepr(img)

    def load_image_from_base64(base64_str: str):
        image_data = base64.b64decode(base64_str)  # Decode base64
        image = Image.open(BytesIO(image_data)).convert("RGB")  # Open as RGB
        return image

    def extract_embeddings_from_path(self, one_image):
         global model, device
         with torch.no_grad():
            #for batch in batch_images:
            print("batchhhhhhhhhhhhhhhh:", one_image)
            image = self.load_image_from_file(one_image)
            input_tensor = self.preprocess(image)
            input_batch = input_tensor.unsqueeze(0) 
            model_tag= f"conservationxlabs/miewid-msv2"
            model = self.load_model(model_tag)
            output = model(input_batch)
            #out_embed.append(output.cpu().detach().numpy())
            print("out emb:" , output.cpu().detach().numpy())
            return output.cpu().detach().numpy()[0].tolist()


