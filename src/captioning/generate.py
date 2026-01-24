from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
import torch
import argparse
import os

def load_model(device):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.to(device)
    model.eval()
    return processor, model


def caption_image(processor, model, image_path, device, max_length=30):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model.generate(**inputs, max_length=max_length)
        caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='Path to input image')
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print('Using device:', device)

    processor, model = load_model(device)
    caption = caption_image(processor, model, args.image, device)
    print('\nCaption:')
    print(caption)


if __name__ == '__main__':
    main()