import torch
import lmdb
import os
import glob
import pickle
from PIL import Image, UnidentifiedImageError
import io
from tqdm import tqdm
import shutil
import csv
from multiprocessing import Pool, cpu_count, Manager


def load_metadata_from_csv(csv_file):
    metadata = {}
    counter = 0
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line, which is the header
        for row in reader:
            uid = row[0]
            # if uid == "e0643d0ee9af4795b699099e17637083":
            metadata[uid] = tuple(row[1:])  # Adjust the slicing if necessary
    return metadata


def process_item(args):
    """This function will be executed by each worker process."""
    uid, metadata, source_folder, lmdb_path, lock = args

    img_folder = os.path.join(source_folder, uid)
    if not os.path.exists(img_folder):
        return  # No images, skip

    images = sorted(glob.glob(f"{img_folder}/*.png"))
    if len(images) != 40:
        return  # Not enough images, skip

    img_list = []
    for img_path in images:
        try:
            img = Image.open(img_path).convert("RGB")
        except UnidentifiedImageError:
            print(f"Error opening image")
            return
        except Exception as e:
            print(f"Error")
            return

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_list.append(img_byte_arr.getvalue())

    metadata_values = [int(m) for m in metadata]
    metadata_tensor = torch.tensor(metadata_values)

    key = uid.encode("ascii")
    value = pickle.dumps((uid, img_list, metadata_tensor))

    # Locking LMDB access to avoid race conditions
    with lock:
        map_size = int(1e12)  # Size of the database
        db = lmdb.open(lmdb_path, map_size=map_size)
        with db.begin(write=True) as txn:
            txn.put(key, value)
        db.close()


def create_lmdb_dataset(source_folder, lmdb_path, all_metadata):
    # print(all_metadata)
    # If the database directory already exists, remove it
    if os.path.exists(lmdb_path):
        shutil.rmtree(lmdb_path)  # Use shutil.rmtree to delete an entire directory tree
    # Use multiprocessing with a Manager to safely handle locks
    num_workers = min(
        cpu_count(), len(all_metadata)
    )  # Limit number of workers to available CPUs
    with Manager() as manager:
        lock = manager.Lock()

        pool = Pool(num_workers)

        # Prepare arguments for each worker
        tasks = [
            (uid, metadata, source_folder, lmdb_path, lock)
            for uid, metadata in all_metadata.items()
        ]

        # Shared progress bar
        pbar = tqdm(total=len(all_metadata), desc="Creating LMDB Dataset", unit="item")

        # Process in parallel
        for _ in pool.imap_unordered(process_item, tasks):
            pbar.update(1)

        pool.close()
        pool.join()
        pbar.close()


# Load metadata
all_metadata = load_metadata_from_csv("metadata/model_metadata.csv")
# Set up paths
cwd = os.getcwd()
lmdb_path = cwd + "/transformed_annotation_data"
source_folder = cwd + "/views"
os.makedirs(lmdb_path, exist_ok=True)

# Instantiate your dataset
create_lmdb_dataset(
    source_folder=source_folder,
    lmdb_path=lmdb_path,
    all_metadata=all_metadata,
)

print("Finished creating LMDB.")
