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

with open("to_render.txt", "r") as file:
     # Read each line, strip whitespace, and add to the list
     uids = [line.strip() for line in file]


# Define the directory to save CSV files, use your Google Drive if needed
output_dir = f"metadata"
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