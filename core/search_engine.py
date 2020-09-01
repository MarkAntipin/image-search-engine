from uuid import uuid4
from pathlib import Path
from typing import BinaryIO, Union, Dict, List
from shutil import copyfileobj, rmtree
from datetime import datetime as dt

from app.database.engine import Session
from app.database.models import Image as ImageModel
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

    def add(self):
        pass

    def add_bulk(self):
        pass

    def add_data(self):
        pass

    def add_data_bulk(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def put_in_index(
            self,
            db: Session,
            extension: str,
            content_type: str,
            image_obj: BinaryIO,
            image_name: Union[str, Path] = None,
    ) -> int:
        image_dir = Path(self.files_dir, dt.now().strftime("%Y-%m-%d"))
        image_dir.mkdir(exist_ok=True)
        image_path = Path(image_dir, str(uuid4())).with_suffix(f'.{extension}')

        with open(image_path, 'wb') as f:
            copyfileobj(image_obj, f)

        vector = self.image_to_vec.get_vector(image_obj)

        db_image = ImageModel(
            name=image_name,
            content_type=content_type,
            path=image_path.as_posix(),
            vector=vector.tolist(),
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        vector.resize((1, vector.size))
        self.index.add_vector(vector, db_image.id)
        return db_image.id

    def remove_from_index(self, db: Session, idx: int) -> [int, None]:
        # TODO: add atomic
        db_image = db.query(ImageModel).filter(ImageModel.id == idx).first()
        if db_image:
            Path(db_image.path).unlink()
            self.index.delete_vector(idx)
            db.delete(db_image)
            db.commit()
            return db_image.id
        return

    def delete_index(self, db: Session):
        # TODO: add atomic
        num_rows_deleted = db.query(ImageModel).delete()
        db.commit()
        for directory in self.files_dir.iterdir():
            rmtree(directory)
        self.index = Index(
            m=self.m,
            ef_construction=self.ef_construction,
            max_elements=self.max_elements,
            space=self.space,
            ef=self.ef
        )
        return num_rows_deleted

    @staticmethod
    def get_all_images_data(db: Session) -> List[Dict]:
        result = [
            {
                'id': image.id,
                'name': image.name,
                'data': image.data,
            }
            for image in db.query(ImageModel).all()
        ]
        return result

    @staticmethod
    def get_image_data(db: Session, idx: int) -> [Dict, None]:
        image = db.query(ImageModel).filter(ImageModel.id == idx).first()
        if image:
            return {
                'id': image.id,
                'name': image.name,
                'data': image.data,
                'vector': image.vector,
                'path': image.path,
                'content_type': image.content_type
            }
        else:
            return

    def search(
            self,
            db: Session,
            k: int,
            image_obj: BinaryIO
    ) -> [List[Dict], None]:
        pass
