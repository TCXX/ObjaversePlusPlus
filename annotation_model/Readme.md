# Use the Annotation Network to annotate the 3D models
This annotation work is intended to annotate the 3D models from Objaverse. To annotate other 3D models, some modifications are needed.

1. Download the models to the folder `$pwd$/objaverse_models/`. You can use `download_objaverse.py` to download all the glb's from Objaverse along with the metadata.

2. Prepare a `to_render.txt`, which includes all the uids/filenames of the models to be annotated.

3. Prepare `metadata/model_metadata.csv` for the annotation network. If the 3D models are from Objavese, you can use `download_metadata.py` to generate the csv file. Otherwise, prepare the metadata following the example of `metadata/model_metadata.csv`, and make all fields (vertexCount,faceCount,viewCount,likeCount) 0. 

4. Run `bash batch_render_small_size.sh` to generate the screenshots of all the models in `objaverse/models`. The screenshots will be saved in `$pwd$/views`.

5. Run `python3 transform_annotation_data.py` to generate the lmdb used by the annotation network.

6. Run `python3 annotate_all.py` to annotate all the 3D models. `annotation_network.pth` can be downloaded from [annotation_model_weights](https://huggingface.co/datasets/cindyxl/ObjaversePlusPlus/blob/main/annotation_network.pth). The results will be saved in "annotated_results.csv".
