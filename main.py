import requests
import boto3
import os
import sys
import io
import base64
from PIL import Image
from datetime import datetime

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
USER_ID = sys.argv[3]
ALBUM_ID = sys.argv[4]


def upload_folder_to_s3(local_folder):
    bucket_name = 'cai-data-bucket'
    path = USER_ID + "/" + ALBUM_ID + '/outputs'

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_file_key = os.path.join(path, file)
            s3.upload_file(local_file_path, bucket_name, s3_file_key)


url = "http://localhost:3001"
payload = {
    "prompt": "jcsla style, light solid background color, realistic, solo photo, full or half body shot, looking at the camera, sharp focus, highly detailed <lora:ssaemi:1>",
    "negative_prompt": "(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch, various background colors, extra legs, missing legs, accessories, clothes), open mouth, divide photo, grid photo",
    "cfg_scale": 3,
    "width": 1024,
    "height": 1024,
    "denoising_strength": 1.5
}

output_directory = 'outputs'
os.makedirs(output_directory, exist_ok=True)
for i in range(10):
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    print(response.status_code)
    print(response.text)
    print(response.content)
    r = response.json()

    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image.save('outputs/' + timestamp + '.jpg')

upload_folder_to_s3('outputs/')
