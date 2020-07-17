# image-search-engine

### What is it?
It is a search engine for images.



### Used technologies

* `hnswlib` - 
* `postgeSQL` - 
* `FastApi` - 


### Deployment
```bash
docker-compose build
docker-compose up
```

or without docker
```bash
virtualenv venv --python=python3.6
source venv/bin/activate 
pip install -r requirements.txt
uvicorn run:app --host 0.0.0.0 --port 8001
```

App will be available on 0.0.0.0:8001 in both cases


### Api Description
* `GET /image/{id}` download image by id
```curl
curl -X GET "http://0.0.0.0:8001/image/{id}" --output {output_file_name}
```

* `DELETE /image/{id}` delete image by id
```curl
curl -X DELETE "http://0.0.0.0:8001/image/{id}"
```

* `POST /image/add` add image n index
```curl

```