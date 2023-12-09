import requests
import boto3
import os
import sys

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


url = "http://localhost:7861"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
payload = {
    "prompt": "jcsla style, light solid background color, realistic, solo photo, full or half body shot, looking at the camera, sharp focus, highly detailed <lora:ssaemi:1>",
    "negative_prompt": "(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch, various background colors, extra legs, missing legs, accessories, clothes), open mouth, divide photo, grid photo",
    "steps": 20,
    "cfg_scale": 3,
    "width": 512,
    "height": 512,
    "restore_faces": False,
    "denoising_strength": 1.5,
    "hr_scale": 1,
    "send_images": False,
    "save_images": True
}

for i in range(1):
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', headers=headers, json=payload)

upload_folder_to_s3('../outputs/')