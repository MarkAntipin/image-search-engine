import os
from pathlib import Path

import requests


images_path = Path('/Users/markantipin/Downloads/Images')


def build_payload_dict():
    result = []
    for dog_type in os.listdir(images_path):
        if os.path.isdir(Path(images_path, dog_type)):
            for name in os.listdir(Path(images_path, dog_type)):
                if name.endswith('.jpg'):
                    result.append({
                        'dog_type': dog_type,
                        'path': Path(images_path, dog_type, name).as_posix()
                    })
    return result


def request_se(image_data):
    r = requests.post(
        url='http://127.0.0.1:8000/image',
        files={'image': open(image_data['path'], 'rb')}
    )
    print(r)
    r = requests.post(
        url=f'http://127.0.0.1:8000/data/{r.json()["result"]}',
        json={'dog_type': image_data['dog_type']}
    )
    print(r)


def upload_to_se(payload: list):
    for image_data in payload:
        request_se(image_data)


if __name__ == '__main__':
    payload = build_payload_dict()
    upload_to_se(payload)
