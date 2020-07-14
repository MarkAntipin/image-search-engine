import hnswlib
import numpy as np

from app.database.models import Image as ImageModel
from app.database.engine import Session


class Index(hnswlib.Index):
    def __init__(
            self,
            m: int = 16,
            ef_construction: int = 100,
            max_elements: int = 100000,
            space: str = 'cosine',
            dim: int = 4096
    ):
        super().__init__(space, dim)
        self.init_index(M=m, ef_construction=ef_construction, max_elements=max_elements)
        self.__restore_index()
        self.set_ef(300)

    def add_vector(self, vector, idx):
        self.add_items(vector, ids=[idx])

    def add_vectors(self, vectors, indexes):
        self.add_items(vectors, indexes)

    def delete_vector(self, idx):
        self.mark_deleted(idx)

    def search(self, vector, k: int = 1):
        labels, distances = self.knn_query(vector, k=k)
        return labels, distances

    def __restore_index(self):
        db = Session()
        db_images = db.query(ImageModel.id, ImageModel.vector).all()
        db.close()
        if db_images:
            indexes, vectors = zip(*[(idx, vector) for idx, vector in db_images])
            vectors = np.array(vectors)
            indexes = np.array(indexes)
            self.add_vectors(vectors=vectors, indexes=indexes)
