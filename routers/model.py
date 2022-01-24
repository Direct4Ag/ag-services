from ..config import settings

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from torchvision import transforms
from PIL import Image

import pickle
import torch
import io
import os

router = APIRouter(
    prefix="/model",
    tags=["classification"],
    dependencies=[],
    responses={},
)

alex_net_model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained=True)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])
imagenet_classes_path = os.path.join(settings.models_path, "imagenet_classes.txt")
with open(imagenet_classes_path) as f:
    labels = [line.strip() for line in f.readlines()]

yolov3_model = torch.hub.load('ultralytics/yolov3', 'yolov3', pretrained=True)


@router.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    if "image" not in file.content_type:
        raise HTTPException(status_code=400, detail="File must be an image")
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    alex_net_model.eval()
    out = alex_net_model(batch_t)
    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

    _, indices = torch.sort(out, descending=True)
    o = [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]

    return {"Classification": o}


@router.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    if "image" not in file.content_type:
        raise HTTPException(status_code=400, detail="File must be an image")
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    results = yolov3_model(img)
    script_path = os.path.abspath(os.path.dirname(__file__))
    results.save(f"{script_path}/")
    return FileResponse(f"{script_path}/image0.jpg")
