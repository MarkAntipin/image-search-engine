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
            model: str = 'alexnet',
            dim: int = 4096,
    ):
        self.image_to_vec = Img2Vec(
            layer=layer,
            model=model,
            layer_output_size=dim
        )
        self.files_dir = Config.FILES_DIR
        self.files_dir.mkdir(exist_ok=True)
        self.index = None

    def get(self, idx: int) -> [dict, None]:
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
        image_dir = Path(self.files_dir, dt.now().strftime("%Y-%m-%d"))
        image_dir.mkdir(exist_ok=True)
        image_path = Path(image_dir, str(uuid4())).with_suffix(f'.{extension}')

        # get vector from image
        vector = self.image_to_vec.get_vector(image_obj)
        image_obj.seek(0)

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

    def add_bulk(self):
        pass

    def get_data(self, idx) -> [dict, None]:
        image = ImageModel.get_or_none(id=idx)
        if image is None:
            return
        return model_to_dict(image)

    def get_data_query(self, query):

        ImageModel.select().where(ImageModel.data[''])

    def add_data(self, idx: int, data: dict) -> [int, None]:
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
            k: int,
            image_obj: BinaryIO
    ) -> [List[Dict], None]:
        pass
