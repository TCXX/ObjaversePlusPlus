import torch
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from dataset import LMDBDataset
from torchvision import transforms

from annotation_dataset import LMDBDatasetAnnotation


def get_all_data(data_path):
    # Define your transform
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    transformed_dataset = LMDBDatasetAnnotation(data_path, transform)
    # Assuming 'transformed_dataset' is an instance of your dataset
    total_size = len(transformed_dataset)
    print("total number of all data: ", total_size)

    all_loader = DataLoader(
        transformed_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=36,
        pin_memory=True,
    )
    return all_loader
