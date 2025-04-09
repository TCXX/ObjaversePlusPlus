from torch.utils.data import Dataset
import lmdb
import pickle
from PIL import Image
import io
import torch


class LMDBDatasetAnnotation(Dataset):
    def __init__(self, lmdb_path, transform=None):
        self.lmdb_path = lmdb_path
        self.transform = transform
        self.uids = self._load_uids()

    def _load_uids(self):
        uids = []
        with lmdb.open(self.lmdb_path, readonly=True, lock=False) as env:
            with env.begin(write=False) as txn:
                cursor = txn.cursor()
                for key, _ in cursor:
                    uids.append(
                        key.decode("utf-8")
                    )  # assuming keys are bytes, decode as needed
        return uids

    def __len__(self):
        with lmdb.open(self.lmdb_path, readonly=True, lock=False) as env:
            with env.begin(write=False) as txn:
                return txn.stat()["entries"]

    def __getitem__(self, index):
        uid = self.uids[index] 
        with lmdb.open(self.lmdb_path, readonly=True, lock=False) as env:
            with env.begin(write=False) as txn:
                key = f"{uid}".encode("ascii")
                value = txn.get(key)
        if not value:
            raise ValueError("Could not retrieve data - key not found in LMDB.")

        uid2, image_data_list, metadata = pickle.loads(value)
        assert uid==uid2
        images = [
            Image.open(io.BytesIO(img_data)).convert("RGB")
            for img_data in image_data_list
        ]
        if self.transform:
            images = [self.transform(img) for img in images]
        imgs_tensor = torch.stack(images)
        
        return imgs_tensor, metadata, uid

    def __del__(self):
        if hasattr(self, "env") and self.env is not None:
            self.env.close()
