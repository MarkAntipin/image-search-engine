from uuid import uuid4
from pathlib import Path
from typing import BinaryIO, Union, Dict, List
from shutil import copyfileobj
from datetime import datetime as dt

from app.database.engine import Session
from app.database.models import Image as ImageModel
from core.utils import get_content_type
from settings.config import Config
from .image_to_vector import Img2Vec
from .index import Index


class SearchEngine:
    def __init__(
            self,
            layer: str = 'default',
            model: str = 'alexnet',
            dim: int = 4096,
            m: int = 16,
            ef_construction: int = 200,
            max_elements: int = 100000,
            space: str = 'cosine',
    ):
        self.image_to_vec = Img2Vec(
            layer=layer,
            model=model,
            layer_output_size=dim
        )
        self.index = Index(
            m=m,
            ef_construction=ef_construction,
            max_elements=max_elements,
            space=space
        )
        self.files_dir = Config.FILES_DIR
        self.files_dir.mkdir(exist_ok=True)

    def put_in_index(
            self,
            db: Session,
            image_obj: BinaryIO,
            image_name: Union[str, Path] = None,
            image_data: Dict = None
    ) -> int:
        # TODO: add atomic
        content_type, extension = get_content_type(image_obj, image_name)
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
            data=image_data
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        vector.resize((1, vector.size))
        self.index.add_vector(vector, db_image.id)
        return db_image.id

    def remove_from_index(self, db: Session, idx: int):
        # TODO: add atomic
        db_image = db.query(ImageModel).filter(ImageModel.id == idx).first()
        if db_image:
            Path(db_image.path).unlink()
            self.index.delete_vector(idx)
            db.delete(db_image)
            db.commit()
            return db_image.id
        return

    @staticmethod
    def get_all_images_data(db: Session) -> List[dict]:
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

    def search(self, db: Session, k: int, image_obj: BinaryIO):
        vector = self.image_to_vec.get_vector(image_obj)
        vector.resize((1, vector.size))
        try:
            labels, distances = self.index.search(vector, k=k)
        except RuntimeError:
            return
        labels_and_distances = {idx: dist for idx, dist in zip(labels[0], distances[0])}

        result = [
            {
                'id': image.id,
                'dist': float(labels_and_distances[image.id]),
                'name': image.name,
                'data': image.data,
            }
            for image in db.query(ImageModel).filter(ImageModel.id.in_(labels[0].tolist())).all()
        ]

        return result

    def reindex(self):
        # TODO: implement it
        pass

    def check_health(self):
        # TODO: implement it
        pass
