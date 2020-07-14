from typing import BinaryIO, List

from PIL import Image
from img2vec_pytorch import Img2Vec as Img2VecPytorch


class Img2Vec(Img2VecPytorch):
    def __init__(
            self,
            layer: str = 'default',
            model: str = 'alexnet',
            layer_output_size: int = 4096
    ):
        super().__init__(
            model=model, layer=layer, layer_output_size=layer_output_size
        )

    @staticmethod
    def _create_pill(img_obj: BinaryIO):
        return Image.open(img_obj).convert('RGB')

    def get_vector(self, img_obj: BinaryIO):
        image = self._create_pill(img_obj)
        return self.get_vec(image)

    def get_vectors(self, img_objects: List[BinaryIO]):
        images = [self._create_pill(img) for img in img_objects]
        return self.get_vec(images)
