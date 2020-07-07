from uuid import uuid4
from pathlib import Path
from typing import BinaryIO, Union, Dict
from shutil import copyfileobj
from datetime import datetime as dt

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
            m: int = 16,
            ef_construction: int = 200,
            max_elements: int = 100000,
            space: str = 'cosine',
            dim: int = 4096
    ):
        self.image_to_vec = Img2Vec(
            layer=layer, model=model, layer_output_size=dim
        )
        self.index = Index(
            m=m, ef_construction=ef_construction, max_elements=max_elements, space=space, dim=dim
        )
        self.files_dir = Config.FILES_DIR
        self.files_dir.mkdir(exist_ok=True)

    async def put_in_index(
            self,
            image_obj: BinaryIO,
            image_name: Union[str, Path] = None,
            image_data: Dict = None
    ):
        content_type, extension = get_content_type(image_obj, image_name)

        image_dir = Path(self.files_dir, dt.now().strftime("%Y-%m-%d"))
        image_dir.mkdir(exist_ok=True)
        image_path = Path(image_dir, str(uuid4())).with_suffix(f'.{extension}')

        with open(image_path, 'wb') as f:
            copyfileobj(image_obj, f)

        vector = self.image_to_vec.get_vector(image_obj)

        image = await ImageModel.create(
            name=image_name,
            content_type=content_type,
            path=image_path.as_posix(),
            vector=vector.tolist(),
            image_data=image_data
        )

        self.index.add_vector(vector, image.id)
        return image.id

    async def remove_from_index(self, idx):
        image = await ImageModel.get(id=idx)
        await image.delete()
        Path(image.path).unlink()
        self.index.delete_vector(idx)
        return image.id

    @staticmethod
    async def get_all_images_data():
        result = [i for i in await ImageModel.all()]
        return result

    @staticmethod
    async def get_image_data(idx):
        result = await ImageModel.get(id=idx)
        return result

    def search(self, image_obj: BinaryIO):
        vector = self.image_to_vec.get_vector(image_obj)
        labels, distances = self.index.search(vector, k=1)
        return {'labels': labels.tolist(), 'distances': distances.tolist()}
