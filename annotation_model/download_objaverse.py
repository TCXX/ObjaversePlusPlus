# -*- coding: utf-8 -*-
import objaverse
import shutil
import os
import csv
import multiprocessing

objaverse.__version__

"""# Loading UIDs

Each object has a unique corresponding UID (universal identifier). Let's get all the object UIDs:
"""

uids = objaverse.load_uids()
len(uids), type(uids)

"""Here, `uids` is a list of strings. Let's look at a few of them:

# Loading Annotations

We can get the object annotations for each of object using the
```python
objaverse.load_annotations(
    uids: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]
```

function. The function optionally takes in a list of the `uids` and returns a map of each specified uid to its corresponding annotations. If `uids` is not specified, the annotations for every object is returned.

Here, we see properties like the "name", "license", "description", "tags", and other metadata.

### Filtering

We can use the annotations to filter for particular properties of objects. For example, we can filter for objects that are distributed with the CC-BY license:
"""

annotations = objaverse.load_annotations()

uids = objaverse.load_uids()

# Define the directory to save CSV files, use your Google Drive if needed
output_dir = f"metadata_{job_id}"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "model_metadata.csv")

# Add headers
headers = ["uid", "vertexCount", "faceCount", "viewCount", "likeCount"]

# Open the CSV file and write headers and data
with open(csv_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    # Add data and images
    for uid in uids:
        annotation = annotations[uid]
        vertex_count = annotation["vertexCount"]
        face_count = annotation["faceCount"]
        view_count = annotation["viewCount"]
        like_count = annotation["likeCount"]

        writer.writerow([uid, vertex_count, face_count, view_count, like_count])

# files.download(csv_path)

"""# Downloading Objects

We're going to use multiprocessing to download the objects. First, let's check our CPU count to get the number of processes we'll use:
"""


processes = multiprocessing.cpu_count()
# processes

"""**For** ease of demonstration, let's randomly sample 100 objects that we'll want to download:

And now, let's download them with `objaverse.load_objects` with all of our processes. The function

```python
objaverse.load_objects(
    uids: List[str],
    download_processes: int = 1
) -> Dict[str, str]
```

takes in a list of object UIDs and optionally the number of download processes, and returns a map from each object UID to its `.glb` file location on disk:
"""

objects = objaverse.load_objects(uids=random_object_uids, download_processes=1)
# objects

"""**Once** objects are downloaded locally for the first time, subsequent calls to `load_objects` are cached, and thus much faster:"""


"""> **NOTE: I highly recommend using Blender for rendering. It will texture the meshes much better than trimesh. I just wanted to show a quick visualization.**"""

cwd = os.getcwd()
new_dir = cwd + f"/objaverse_{job_id}"
home_dir = os.path.expanduser("~")
objaverse_dir = home_dir + "/.objaverse"
shutil.move(objaverse_dir, new_dir)
