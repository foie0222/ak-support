import base64
import json
import requests
import config


# png画像を解析する
def save_png(url):
    file_name = "./image/source.png"

    response = requests.get(url)
    image = response.content

    with open(file_name, "wb") as f:
        f.write(image)


GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='


# APIを呼び、認識結果をjson型で返す
def request_cloud_vison_api(image_base64):
    api_url = GOOGLE_CLOUD_VISION_API_URL + config.GOOGLE_API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                # jsonに変換するためにstring型に変換する
                'content': image_base64.decode('utf-8')
            },
            'features': [{
                'type': 'TEXT_DETECTION',  # ここを変更することで分析内容を変更できる
                'maxResults': 10,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()


# 画像読み込み
def img_to_base64(filepath):
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    return base64.b64encode(img_byte)
