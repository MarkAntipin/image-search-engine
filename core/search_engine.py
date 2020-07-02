from uuid import uuid4
from pathlib import Path
from typing import BinaryIO, Union, Dict
from shutil import copyfileobj
from datetime import datetime as dt

from app.database.models import Image
from core.utils import get_content_type
from settings.config import Config
from .image_to_vector import Img2Vec
from .index import Index


class SearchEngine:
    def __init__(
            self,
            layer: str = 'default',
            model: str = 'alexnet',
            layer_output_size: int = 4096,
            m: int = 16,
            ef_construction: int = 200,
            max_elements: int = 100000,
            space: str = 'l2',
            dim: int = 4096
    ):
        self.image_to_vec = Img2Vec(
            layer=layer, model=model, layer_output_size=layer_output_size
        )
        self.index = Index(
            m=m, ef_construction=ef_construction, max_elements=max_elements, space=space, dim=dim
        )

    def put_in_index(
            self,
            image_obj: BinaryIO,
            image_name: Union[str, Path] = None,
            image_data: Dict = None
    ):
        image_uuid = uuid4()

        content_type, extension = get_content_type(image_obj, image_name)

        image_dir = Path(Config.FILES_DIR, dt.now().strftime("%Y-%m-%d"))
        image_dir.mkdir(exist_ok=True)

        with open(Path(image_dir, str(image_uuid)).with_suffix(f'.{extension}'), 'wb') as buff:
            copyfileobj(image_obj, buff)

        vector = self.image_to_vec.get_vector(image_obj)

        image = await Image.add(
            name=image_name,
            content_type=content_type,
            image_uuid=image_uuid,
            image_data=image_data,
            vector=vector
        )

        self.index

    def remove_from_index(self):
        pass

    def search(self):
        pass
