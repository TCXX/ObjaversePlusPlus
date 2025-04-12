# Objaverse++: Curated 3D Object Dataset with Quality Annotations

[![Paper](https://badgen.net/badge/icon/arXiv?icon=awesome&label&color=red)](https://arxiv.org/abs/2504.07334)
[![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/TCXX/ObjaversePlusPlus)
[![Hugging Face](https://img.shields.io/badge/HuggingFace-yellow?logo=huggingface&logoColor=white)](https://huggingface.co/datasets/cindyxl/ObjaversePlusPlus)

[Chendi Lin](https://chendilin.com/), 
[Heshan Liu](), 
[Qunshu Lin](), 
[Zachary Bright](),
[Shitao Tang](),
[Yihui He](),
[Minghao Liu](),
[Ling Zhu](),
[Cindy Le]()

Objaverse++ is a dataset that labels 3D modeling objects in terms of quality score and other important traits for machine learning researchers. We meticulously curated a collection of Objaverse objects and developed an effective classifier capable of scoring the entire Objaverse. Our extensive annotation system considers geometric structure and texture information, enabling researchers to filter training data according to specific requirements.
<p align="center">
<img src="ttps://github.com/user-attachments/files/19720691/rubric.pdff" width="700">
</p>
<!-- [rubric.pdf](https://github.com/user-attachments/files/19720691/rubric.pdf) -->

Less is more. We proved that, with only the high-quality objects in a 3D dataset, you can perform generative AI tasks like text-to-3D and image-to-3D better and faster.



## Overview

To address the prevalence of low-quality models in Objaverse, we:
1. Manually annotated 10,000 3D objects with quality and characteristic attributes;
2. Trained a neural network capable of annotating tags for the rest of the Objaverse dataset;
3. Created a curated subset of approximately 500,000 high-quality 3D models.

Our experiments show that:
- Models trained on our quality-focused subset achieve better performance than those trained on the larger Objaverse dataset in image-to-3D generation tasks;
- Higher data quality leads to faster training loss convergence;
- Careful curation and rich annotation can compensate for raw dataset size.

<p align="center">
<img src="https://github.com/user-attachments/assets/035acd0b-c9b3-4c03-b030-ac84aa570eef" width="700">
  </p>


<p align="center">
<img src="https://github.com/user-attachments/assets/837728c7-4e67-43d3-9b2b-19ecd8a88789" width="700">
</p>

## Quality and Attribute Annotations

### Quality Score
We define quality score as a metric to assess how useful a 3D object is for machine learning training:

- **Low Quality**: No semantic meaning. Objects that annotators cannot identify or are corrupted.
- **Medium Quality**: Identifiable objects missing basic material texture and color information.
- **High Quality**: Acceptable quality with clear object identity, properly textured with material and color details.
- **Superior Quality**: Excellent quality with high semantic clarity and professional texturing with strong aesthetic harmony.

### Binary Traits
In addition to quality scores, we annotate several binary tags:

- **Transparency**: Identifies models with see-through parts.
- **Scene**: Identifies whether the model represents a scenario/environment rather than a standalone object.
- **Single Color**: Tags models that are unintentionally monochromatic.
- **Not a Single Object**: Marks models consisting of multiple separate components.
- **Figure**: Indicates if the model represents a character, person, or figure.

<p align="center">
<img src="https://github.com/user-attachments/assets/3790a57b-10cc-4bee-aa71-9e809953ebde" width="700">
</p>


## Dataset Evaluation

We set up an image-to-3D generation task to evaluate our dataset using OpenLRM. We compared:
- A randomly sampled subset of 100,000 objects from Objaverse (Training Set A)
- A quality-filtered dataset of ~50,000 high-quality objects (Training Set B)

Our key findings:
1. **Better Generation Quality**: User study shows significant preference for models trained on our curated dataset.
2. **Faster Convergence**: Our model demonstrates faster convergence on a carefully curated dataset.

<p align="center">
<img src="https://github.com/user-attachments/assets/a91dbc90-a9da-4d3d-8f3a-e1a884ea7555" width="500">
</p>


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

We gratefully acknowledge Exascale Labs and Zillion Network for providing the computational resources and supporting our training infrastructure that made this research possible. We thank Abaka AI for their valuable assistance with data labeling. Special thanks to Ang Cao and Liam Fang for their technical and artistic insights that significantly enhanced our understanding of 3D model quality assessment. 
