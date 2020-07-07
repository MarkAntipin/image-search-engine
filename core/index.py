import hnswlib
# from nptyping import NDArray


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
        self.set_ef(300)

    def add_vector(self, vector, idx):
        self.add_items(vector, ids=[idx])

    def add_vectors(self):
        pass

    def delete_vector(self, idx):
        self.mark_deleted(idx)

    def search(self, vector, k: int = 1):
        labels, distances = self.knn_query(vector, k=k)
        return labels, distances
