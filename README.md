# Objaverse++: Curated 3D Object Dataset with Quality Annotations

[![Paper](https://badgen.net/badge/icon/arXiv?icon=awesome&label&color=red)](https://arxiv.org/abs/2504.07334)
[![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/TCXX/ObjaversePlusPlus)
[![Hugging Face](https://img.shields.io/badge/HuggingFace-yellow?logo=huggingface&logoColor=white)](https://huggingface.co/datasets/cindyxl/ObjaversePlusPlus)

[Chendi Lin](https://chendilin.com/), 
[Heshan Liu](https://www.linkedin.com/in/heshan-liu/), 
[Qunshu Lin](https://www.linkedin.com/in/jack-d-lin/), 
Zachary Bright,
[Shitao Tang](https://scholar.google.com/citations?user=JKVeJSwAAAAJ&hl=en),
[Yihui He](https://scholar.google.com/citations?user=2yAMJ1YAAAAJ&hl=en),
Minghao Liu,
Ling Zhu,
[Cindy Le](https://scholar.google.com/citations?hl=en&user=Y5aF5QgAAAAJ)

Objaverse++ is a dataset that labels 3D modeling objects in terms of quality score and other important traits for machine learning researchers. We meticulously curated a collection of Objaverse objects and developed an effective classifier capable of scoring the entire [Objaverse](https://huggingface.co/datasets/allenai/objaverse). Our extensive annotation system considers geometric structure and texture information, enabling researchers to filter training data according to specific requirements.
<p align="center">
<img src="https://github.com/user-attachments/assets/cc886ae2-1a06-42d2-8db7-93d6353d2ff0" width="700">
</p>

Less is more. We proved that, with only the high-quality objects in a 3D dataset, you can perform generative AI tasks like text-to-3D and image-to-3D better and faster.



## Overview

To address the prevalence of low-quality models in Objaverse, we:
1. Manually annotated 10,000 3D objects with quality and characteristic attributes;
2. Trained a neural network capable of annotating tags for the rest of the Objaverse dataset;
3. Annotated the Objaverse (~790k data) with quality and characteristic tags.


Our experiments show that:
- Models trained on our quality-focused subset achieve better performance than those trained on the larger Objaverse dataset in image-to-3D generation tasks;
- Higher data quality leads to faster training loss convergence;
- Careful curation and rich annotation can compensate for raw dataset size.

## Quality and Attribute Annotations

### Quality Score
We define quality score as a metric to assess how useful a 3D object is for machine learning training:

- **Low Quality**: No semantic meaning. Objects that annotators cannot identify or are corrupted.
- **Medium Quality**: Identifiable objects missing basic material texture and color information.
- **High Quality**: Acceptable quality with clear object identity, properly textured with material and color details.
- **Superior Quality**: Excellent quality with high semantic clarity and professional texturing with strong aesthetic harmony.

### Binary Traits

- **Transparency**: Identifies models with see-through parts.
- **Scene**: Identifies whether the model represents a scenario/environment rather than a standalone object.
- **Single Color**: Tags models that are unintentionally monochromatic.
- **Not a Single Object**: Marks models consisting of multiple separate components.
- **Figure**: Indicates if the model represents a character, person, or figure.

<p align="center">
<img src="https://github.com/user-attachments/assets/fb802ae1-23d2-4040-be50-67bf2cdfb9d1" width="700">
</p>

<p align="center">
<img src="https://github.com/user-attachments/assets/3790a57b-10cc-4bee-aa71-9e809953ebde" width="700">
</p>

### Art style (Experimental)
- **Scanned**: With little pieces from real-world camera, usually super high poly.
- **Arcade**: Includes distinct patterns as if in the old games, sometimes has repeating patterns.
- **Sci-Fi**: Dark color with lighting, usually metallic.
- **Cartoon**: Colorful Western cartoon style.
- **Anime**: Color Japanese anime style.
- **Realistic**: With non-repeating textural details, but still handcrafted by artists.
- **Other**: Unable to be categorized or of awful quality.

<p align="center">
<img src="https://github.com/user-attachments/assets/e25f2761-538d-4351-a3d7-6abf31b92455" width="700">
</p>

### Density (Experimental)
Different levels of polygon counts are adopted in different use cases in the 3D modeling and gaming industries. 

## Dataset Evaluation

We set up an image-to-3D generation task to evaluate our dataset using OpenLRM. We compared:
- A randomly sampled subset of 100,000 objects from Objaverse (Training Set A)
- A quality-filtered dataset of ~50,000 high-quality objects (Training Set B)

<p align="center">
<img src="https://github.com/user-attachments/assets/a91dbc90-a9da-4d3d-8f3a-e1a884ea7555" width="500">
</p>

Our key findings:
1. **Better Generation Quality**: User study shows significant preference for models trained on our curated dataset.
2. **Faster Convergence**: Our model demonstrates faster convergence on a carefully curated dataset.

<p align="center">
<img src="https://github.com/user-attachments/assets/035acd0b-c9b3-4c03-b030-ac84aa570eef" width="700">
</p>


<p align="center">
<img src="https://github.com/user-attachments/assets/837728c7-4e67-43d3-9b2b-19ecd8a88789" width="700">
</p>

For more details, please read our [paper](https://arxiv.org/abs/2504.07334), which was peer reviewed at CVPR workshop (2025).

Note: Art style and density data are experimental and not included in the paper.

## Usage

You can view and download the dataset here: [Hugging Face link](https://huggingface.co/datasets/cindyxl/ObjaversePlusPlus).

## Citation

If you find this work useful for your research, please cite our paper:

```
@misc{lin2025objaversecurated3dobject,
      title={Objaverse++: Curated 3D Object Dataset with Quality Annotations}, 
      author={Chendi Lin and Heshan Liu and Qunshu Lin and Zachary Bright and Shitao Tang and Yihui He and Minghao Liu and Ling Zhu and Cindy Le},
      year={2025},
      eprint={2504.07334},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.07334}, 
}
```

## Acknowledgments

We gratefully acknowledge [Exascale Labs](https://www.exascalelabs.ai/) and [Zillion Network](https://zillion.network/) for providing the computational resources and supporting our training infrastructure that made this research possible. We thank [Abaka AI](https://www.abaka.ai/) for their valuable assistance with data labeling. Special thanks to Ang Cao and Liam Fang for their technical and artistic insights that significantly enhanced our understanding of 3D model quality assessment. 

## License

This dataset is licensed under the [Open Data Commons Attribution License (ODC-By) v1.0](http://opendatacommons.org/licenses/by/1.0/).
