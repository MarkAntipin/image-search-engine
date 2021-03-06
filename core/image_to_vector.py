from typing import BinaryIO

import numpy as np
from PIL import Image
from img2vec_pytorch import Img2Vec as Img2VecPytorch


class Img2Vec(Img2VecPytorch):
    def __init__(
            self,
            layer: str,
            model: str,
            layer_output_size: int
    ):
        super().__init__(
            model=model, layer=layer, layer_output_size=layer_output_size
        )

    @staticmethod
    def __normalize(vector):
        return vector / np.linalg.norm(vector)

    @staticmethod
    def _create_pill(img_obj: BinaryIO) -> Image:
        image_pill = Image.open(img_obj).convert('RGB')
        img_obj.seek(0)
        return image_pill

    def get_vector(self, img_obj: BinaryIO):
        image = self._create_pill(img_obj)
        vector = self.get_vec(image)
        return self.__normalize(vector)
