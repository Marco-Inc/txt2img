import os
import sys
import random
import json
import requests
import boto3
import torch
import gc

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
USER_ID = sys.argv[3]
ALBUM_ID = sys.argv[4]
PRODUCT_ID = sys.argv[5]
IS_FIRST_ALBUM = sys.argv[6]

with torch.no_grad():
    torch.cuda.empty_cache()
    gc.collect()

url = "http://localhost:7861"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

photos = 20
if PRODUCT_ID in ["com.marcocorp.cai.standard", "com.marcocorp.cai.express"]:
    if IS_FIRST_ALBUM.lower() == 'true':
        photos += 10
elif PRODUCT_ID in ["com.marcocorp.cai.standardplus", "com.marcocorp.cai.expressplus"]:
    photos += 20
    if IS_FIRST_ALBUM.lower() == 'true':
        photos += 10

prompts = [
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing a ribbon accessory, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, wearing a ribbon accessory, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, wearing a ribbon accessory, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing clothes, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, wearing clothes, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, wearing clothes, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, smiling slightly, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, smiling slightly, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, smiling slightly, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, playing with a toy, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, playing with a toy, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, playing with a toy, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing a necklace, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, wearing a necklace, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, looking at the camera, wearing a necklace, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, sitting down, looking at the camera, wearing a necklace highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, sitting down, looking at the camera, playing with a toy, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, sitting down, looking at the camera, smiling slightly, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, sitting down, looking at the camera, wearing clothes, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, sitting down, looking at the camera, wearing a ribbon accessory, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, holding a ball in mouth, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, wagging tail, smiling, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, sitting down, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, laying down, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full or half body shot, sitting with a teddy bear, looking at the camera, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing a wreath on the head, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing a wreath around the neck, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing glasses, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing a wreath around the neck and head, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, with flower props next to it, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing sunglasses, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing sunglasses, sitting with orange juice and straw next to it, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, full body shot, looking at the camera, wearing sunglasses, sitting, with cocktail next to it, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, with laurel wreath on top of the head, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
    "(jcsla style:1.5), (ONLY ONE light solid background color:1.5, Floor color is same as background one, clear background, not blurry dog), realistic, solo photo, half body shot, looking at the camera, with soccer ball next to it, highly detailed, dslr photo, 8K <lora:ssaemi:1>",
]

selected_prompts = random.sample(prompts, photos)
payload = {
    "prompt": "",
    "negative_prompt": "((stuff:1.5, many background color:1.5, blur:1.5, blurry:1.5), sofa, chair, stuff, table, worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch, various background colors, extra legs, missing legs, accessories, clothes), open mouth, divide photo, grid photo",
    "sampler_name": "Euler a",
    "steps": 20,
    "cfg_scale": 3,
    "width": 1024,
    "height": 1024,
    "denoising_strength": 1.5,
    "hr_scale": 1.5,
    "hr_upscaler": "R-ESRGAN 4x+",
    "send_images": False,
    "save_images": True
}
for prompt in selected_prompts:
    payload["prompt"] = prompt
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', headers=headers, json=payload)

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='ap-northeast-2')
bucket_name = 'cai-data-bucket'
region_name = 'ap-northeast-2'
local_directory_path = "/workspace/stable-diffusion-webui/outputs/txt2img-images"
uploaded_urls = []
for root, dirs, files in os.walk(local_directory_path):
    for file in files:
        local_file_path = os.path.join(root, file)
        s3_key = f'data/${USER_ID}/${ALBUM_ID}/outputs'
        s3.upload_file(local_file_path, bucket_name, s3_key)
        uploaded_url = f'https://{bucket_name}.s3.{region_name}.amazonaws.com/{s3_key}'
        uploaded_urls.append(uploaded_url)

api_url = "https://cai-api.marco-corp.com:8443/v1/finish"
images = json.dumps(uploaded_urls)
data = {
    "userId": USER_ID,
    "albumId": ALBUM_ID,
    "images": images
}
response = requests.post(api_url, json=data)