# image-search-engine

### What is it?
It is a search similar engine for images.
![Alt text](https://raw.githubusercontent.com/MarkAntipin/image-search-engine/master/readme_images/dogs_1.png)
![Alt text](https://raw.githubusercontent.com/MarkAntipin/image-search-engine/master/readme_images/dogs_2.png)

This web application allows you to add and remove images from the index while maintaining data consistency.
 When the application starts again, the entire previous index is saved.This web application allows you to add and remove images from the index while maintaining data consistency. When the application starts again, the entire previous index is saved.

### Used technologies

* `hnswlib` - index engine for quick similarity search (https://github.com/nmslib/hnswlib)
* `postgeSQL` - to store all additional information about the image
* `img2vec_pytorch` - wrapper around Alexnet for image feature extraction (https://github.com/christiansafka/img2vec)


### Deployment
#### Docker
```bash
docker-compose build
docker-compose up
```

#### Without Docker
requirements: gcc and postgeSQL, also specify `PG_USER`, `PG_DATABASE`, `PG_PASSWORD` params in `settings/env` file


```bash
virtualenv venv --python=python3.6
source venv/bin/activate 
pip install -r requirements.txt
uvicorn run:app --host 0.0.0.0 --port 8001
```

App will be available on 0.0.0.0:8001 in both cases


### Api Description
All handlers are available on 0.0.0.0:8001/docs

#### Image
* `GET /image/{id}` download image by id
```curl
curl -X GET "http://0.0.0.0:8001/image/{id}" --output {output_file_name}
```

* `DELETE /image/{id}` delete image by id
```curl
curl -X DELETE "http://0.0.0.0:8001/image/{id}"
```

* `POST /image/add` add image to index
```curl
curl -X POST "http://0.0.0.0:8001/image/add" -H "Content-Type: multipart/form-data" -F "image=@{image_path};type=image/jpeg"
```

* `POST /image/search?k={k}` search k nearest images
```curl
curl -X POST "http://0.0.0.0:8001/image/search?k={k}" -H "Content-Type: multipart/form-data" -F "image=@{image_path};type=image/jpeg"
```

* `DELETE /image/all/records` delete all images from search-engine
```curl
curl -X DELETE "http://0.0.0.0:8001/image/all/records"
```

#### Index
* `GET /index/reindex` rebuild index (only use if it is broken)
```curl
curl -X GET "http://0.0.0.0:8001/index/reindex"
```

* `GET /index/health` check if index is broken
```curl
curl -X GET "http://0.0.0.0:8001/index/health"
```

#### Data
* `GET /data/{id}` get data for image by id (vector and some additional info)
```curl
curl -X GET "http://0.0.0.0:8001/data/{id}"
```

* `POST /data/{id}` add additional info for image by id
```curl
curl -X POST "http://0.0.0.0:8001/data/12345" -H "Content-Type: application/json" -d "{\"image_data\":{some data in json}}"
```
