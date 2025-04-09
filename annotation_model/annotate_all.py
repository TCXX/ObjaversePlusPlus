from model import MultiView3DModelClassifierWithAttention
from data_loader import get_all_data
import torch
from tqdm import tqdm  # Import the tqdm function
from sklearn.metrics import accuracy_score
import csv

# import boto3


def write_results_to_csv(results, output_csv_path):
    with open(output_csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UID", "Tags"])
        for uid, tags in results.items():
            writer.writerow([uid, ",".join(map(str, tags))])


if __name__ == "__main__":

    # Setup model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MultiView3DModelClassifierWithAttention(num_layers=1)
    # modify the following
    model.load_state_dict(
        torch.load("annotation_network.pth", map_location=torch.device("cpu"))
    )
    model.to(device)

    # Setup labels
    # style,score, is_multi_object, is_scene, is_figure, is_transparent,is_single_color, density
    output_labels = [
        "style",
        "score",
        "is_multi_object",
        "is_scene",
        "is_figure",
        "is_transparent",
        "is_single_color",
        "density",
    ]
    categorical_labels = ["style", "score", "density"]
    binary_labels = [
        "is_multi_object",
        "is_scene",
        "is_figure",
        "is_transparent",
        "is_single_color",
    ]

    # Assuming the get_loaders function can also be used here to get test_loader
    print("start loading data")
    data_loader = get_all_data("/transformed_annotation_data")

    output_csv_path = "annotated_results.csv"

    # Setup CSV to write all results
    with open(output_csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header based on the labels
        writer.writerow(["UID"] + output_labels)

        # No gradient calculation is needed
        progress_bar = tqdm(data_loader, desc="Annotating progress", leave=False)
        with torch.no_grad():
            for images, metadata, uid in progress_bar:
                images, metadata = images.to(device), metadata.to(device)
                outputs = model(images, metadata)
                uid_clean = uid[0] if isinstance(uid, tuple) else uid
                # Assuming uid is the first element of a tuple

                # Collect predictions for all labels
                predictions = []
                for i, label_name in enumerate(output_labels):
                    output = outputs[i]
                    if label_name in categorical_labels:  # Categorical labels
                        _, predicted = torch.max(output.data, 1)
                        predictions.append(
                            predicted.cpu().numpy()[0]
                        )  # Assuming batch size is 1
                    else:  # Binary labels
                        predicted = (torch.sigmoid(output.data) > 0.5).int()
                        predictions.append(predicted.view(-1).cpu().numpy()[0])

                # Write predictions to CSV
                writer.writerow([uid_clean] + predictions)
