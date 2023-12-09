import requests
import sys

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
USER_ID = sys.argv[3]
ALBUM_ID = sys.argv[4]

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