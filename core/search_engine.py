import os
from uuid import uuid4
from pathlib import Path
from typing import BinaryIO, Union, Dict, List
from shutil import copyfileobj, rmtree
from datetime import datetime as dt

from playhouse.shortcuts import model_to_dict

from app.database.models import Image as ImageModel, db
from settings.config import Config
from .image_to_vector import Img2Vec


class SearchEngine:
    def __init__(
            self,
            layer: str = 'default',
            model: str = 'resnet-18',
            dim: int = 512,
    ):
        self.image_to_vec = Img2Vec(
            layer=layer,
            model=model,
            layer_output_size=dim
        )
        self.files_dir = Config.FILES_DIR
        self.files_dir.mkdir(exist_ok=True)
        self.index = None

    def __make_image_dir(self):
        image_dir = Path(self.files_dir, dt.now().strftime("%Y-%m-%d"))
        image_dir.mkdir(exist_ok=True)
        return image_dir

    @staticmethod
    def get(idx: int) -> [dict, None]:
        image = ImageModel.get_or_none(id=idx)
        if image:
            return model_to_dict(image)
        return

    @db.atomic()
    def add(
            self,
            extension: str,
            content_type: str,
            image_obj: BinaryIO,
            image_name: Union[str, Path] = None,
    ) -> int:
        image_dir = self.__make_image_dir()
        image_path = Path(image_dir, str(uuid4())).with_suffix(f'.{extension}')

        # get vector from image
        vector = self.image_to_vec.get_vector(image_obj)

        # save in db
        image = ImageModel.create(
            name=image_name,
            content_type=content_type,
            path=image_path.as_posix(),
            vector=vector.tolist(),
        )
        image.save()

        # save in fs
        with open(image_path, 'wb') as f:
            copyfileobj(image_obj, f)

        return image.id

    def add_bulk(self, images_data: dict) -> List[int]:
        pass

    @staticmethod
    def get_data(idx) -> [dict, None]:
        image = ImageModel.get_or_none(id=idx)
        if image is None:
            return
        return model_to_dict(image)

    @staticmethod
    def get_data_query(query):
        res = ImageModel.get_by_query(query)
        return res

    @staticmethod
    def add_data(idx: int, data: dict) -> [int, None]:
        image = ImageModel.get_or_none(id=idx)
        if image is None:
            return
        image.data = data
        image.save()
        return image.id

    def add_data_bulk(self):
        pass

    @db.atomic()
    def delete(self, idx: int) -> [int, None]:
        image = ImageModel.get_or_none(id=idx)
        if image is None:
            return
        ImageModel.delete().where(ImageModel.id == idx).execute()
        os.remove(image.path)
        return image.id

    def delete_query(self):
        pass

    def search(
            self,
            image_obj: BinaryIO,
            k: int = 10,
            query: dict = None
    ) -> [List[Dict], None]:
        vector = self.image_to_vec.get_vector(image_obj)
        res = ImageModel.search(
            vector=vector.tolist(),
            query=query,
            k=k
        )
        return res
