import hnswlib


class Index(hnswlib.Index):
    def __init__(
            self,
            m: int = 16,
            ef_construction: int = 200,
            max_elements: int = 100000,
            space: str = 'l2',
            dim: int = 4096
    ):
        super().__init__(space, dim)
        self.init_index(M=m, ef_construction=ef_construction, max_elements=max_elements)

    def add_image(self):
        pass

    def add_images(self):
        pass
