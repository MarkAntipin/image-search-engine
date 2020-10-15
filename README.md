# image-search-engine

### What is it?
It is a search similar engine for images.
![Alt text](https://raw.githubusercontent.com/MarkAntipin/image-search-engine/master/readme_images/dogs_1.png)
![Alt text](https://raw.githubusercontent.com/MarkAntipin/image-search-engine/master/readme_images/dogs_2.png)

This is a web application allows you to search similar images in database.

The basic idea is that you can delete or add images at any time while maintaining data consistency.
A useful feature is also implemented: search for similar images by request
(for example, find similar images, but search only among those who are Labradors)

I am currently using:
* `img2vec_pytorch` - wrapper around Alexnet for image feature extraction (https://github.com/christiansafka/img2vec)
* `postgeSQL` with `CUBE` extension; vectors are very large, so i can't build index, but postgres allows to query data even in json fields 

In last version i have used `hnswlib` it was faster, but not so flexible as postgres
(you can check it out on 'hnsw' branch)


### Deployment
#### Docker
```bash
docker-compose build
docker-compose up
```

#### Without Docker
requirements: postgeSQL;
It will be simpler to run postgres in docker '/postgres/Dockerfile', otherwise you have to recompile CUBE extension (like in Dockerfile) 
also specify `PG_USER`, `PG_DATABASE`, `PG_PASSWORD` params in `settings/env` file


```bash
virtualenv venv --python=python3.6
source venv/bin/activate 
pip install -r requirements.txt
uvicorn run:app --host 0.0.0.0 --port 8001
```

App will be available on 0.0.0.0:8001 in both cases


### Api Description
All handlers are available on 0.0.0.0:8001/docs

#### Add Image
`POST /image` add image to database

Python requests
```python
import requests

r = requests.post(
    url='http://0.0.0.0:8001/image',
    files={'image': open('image_path', 'rb')}
)
```
Curl
```curl
curl -X POST "http://0.0.0.0:8001/image"
 -H "Content-Type: multipart/form-data" -F "image=@{image_path};type=image/jpeg"
```

#### Get Image
`GET /image/{id}` download image by id

Python requests
```python
import requests

r = requests.get(url='http://0.0.0.0:8001/image/{id}')

with open('output_file_name', 'wb') as f:
    f.write(r.content)
```
Curl
```curl
curl -X GET "http://0.0.0.0:8001/image/{id}" --output {output_file_name}
```

#### Delete Image
`DELETE /image/{id}` delete image by id

Python requests
```python
import requests

r = requests.delete(url='http://0.0.0.0:8001/image/{id}')
```
Curl
```curl
curl -X DELETE "http://0.0.0.0:8001/image/{id}"
```

#### Search Image
`POST /image/search?k={k}` search k nearest images

Most complex handler. You can search nearest images n all database
or you can select only specific images (for example only 'Irish terriers')
For such selects you need to add data to images as json fields (see `POST data/{id}`)
Also you can select images by 'name' or 'path' in the same way.
For such queries pass valid dict in params

Python requests
```python
import json

import requests

r = requests.post(
    url='http://0.0.0.0:8001/image/search',
    files={
        'image': open('image_path', 'rb'),
    },
    params={'k': 3, 'query': json.dumps({'dog_type': 'Irish_terrier'})}
)
```
Curl
```curl
curl -X POST "http://0.0.0.0:8001/image/search?k={k}&query=%7B%22dog_type%22%3A%20%22Irish_terrier%22%7D"
 -H  "accept: application/json"" -H "Content-Type: multipart/form-data" -F "image=@{image_path};type=image/jpeg"
```


#### Add Data
`POST /data/{id}` add additional info for image by id

Pass all image data in json field

Python requests
```python
import requests

r = requests.post(
    url='http://0.0.0.0:8001/data/{id}',
    json={'dog_type': 'Irish_terrier'}
)
```
Curl
```curl
curl -X POST "http://0.0.0.0:8001/data/{id}"
 -H "Content-Type: application/json" -d "{\"dog_type\":\"Irish_terrier\"}"
```

#### Get Data
`GET /data/{id}` get data for image by id (vector and some additional info)

Python requests
```python
import requests

r = requests.get(url='http://0.0.0.0:8001/data/{id}')
```
Curl
```curl
curl -X GET "http://0.0.0.0:8001/data/{id}"
```

#### Query Data
`POST /data/query` get data for image by query

You can search for images by querying data (see `POST /image/search`)
But you need to pass query data in json field

Python requests
```python
import requests

r = requests.post(
    url='http://0.0.0.0:8001/data/query',
    json={'dog_type': 'Irish_terrier'}
)
```
Curl
```curl
curl -X POST "http://0.0.0.0:8001/data/query" -H  "accept: application/json"
 -H  "Content-Type: application/json" -d "{\"dog_type\":\"Irish_terrier\"}"
```