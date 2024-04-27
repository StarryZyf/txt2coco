import os
import json
import cv2
import random

def convert_to_coco_format(annotation_folder, image_folder, train_json_path, val_json_path, val_split=0.2):
    categories = [{"id": 0, "name": "ant", "supercategory": "animal"},
                  {"id": 1, "name": "boy", "supercategory": "person"},
                  {"id": 18, "name": "cat", "supercategory": "animal"},
                  {"id": 21, "name": "dog", "supercategory": "animal"},
                  {"id": 28, "name": "egg", "supercategory": "animal"}]  # Update with your categories

    coco_train_data = {
        "info": {
            "description": "My Dataset - Training Set",
            "url": "http://mydataset.com",
            "version": "1.0",
            "year": 2024,
            "contributor": "Me",
            "date_created": "2024-04-26"
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": categories
    }

    coco_val_data = {
        "info": {
            "description": "My Dataset - Validation Set",
            "url": "http://mydataset.com",
            "version": "1.0",
            "year": 2024,
            "contributor": "Me",
            "date_created": "2024-04-26"
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": categories
    }

    image_id = 1
    annotation_id = 1

    # Get list of image files
    image_files = [f for f in os.listdir(annotation_folder) if f.endswith('.txt')]

    # Shuffle the image files
    random.shuffle(image_files)

    # Split the dataset into training and validation sets
    val_size = int(len(image_files) * val_split)
    val_images = image_files[:val_size]
    train_images = image_files[val_size:]

    # Process training images
    for filename in train_images:
        image_name = filename.replace(".txt", ".jpg")  # Assuming image extension is jpg
        image_path = os.path.join(image_folder, image_name)
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            if image is not None:
                height, width, _ = image.shape
                image_info = {
                    "id": image_id,
                    "width": width,
                    "height": height,
                    "file_name": image_name,
                    "license": 0,  # Example license, update if needed
                    "flickr_url": "",  # Optional
                    "coco_url": "",  # Optional
                    "date_captured": "2024-04-26"  # Optional
                }
                coco_train_data["images"].append(image_info)

                with open(os.path.join(annotation_folder, filename), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        parts = line.strip().split('\t')
                        label = int(parts[0])
                        x1, y1, x2, y2 = map(float, parts[1:])

                        # Convert corner coordinates to top-left corner and width/height
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)

                        # Convert relative coordinates to absolute coordinates
                        x_abs = int(x * width)
                        y_abs = int(y * height)
                        w_abs = int(w * width)
                        h_abs = int(h * height)

                        bbox = [x_abs, y_abs, w_abs, h_abs]
                        area = w_abs * h_abs

                        annotation_info = {
                            "id": annotation_id,
                            "image_id": image_id,
                            "category_id": label,  # Assuming label corresponds to category ID
                            "bbox": bbox,
                            "area": area,
                            "segmentation": [],  # Optional
                            "iscrowd": 0,
                            "attributes": {}  # Optional
                        }
                        coco_train_data["annotations"].append(annotation_info)
                        annotation_id += 1

                image_id += 1

    # Process validation images
    for filename in val_images:
        image_name = filename.replace(".txt", ".jpg")  # Assuming image extension is jpg
        image_path = os.path.join(image_folder, image_name)
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            if image is not None:
                height, width, _ = image.shape
                image_info = {
                    "id": image_id,
                    "width": width,
                    "height": height,
                    "file_name": image_name,
                    "license": 0,  # Example license, update if needed
                    "flickr_url": "",  # Optional
                    "coco_url": "",  # Optional
                    "date_captured": "2024-04-26"  # Optional
                }
                coco_val_data["images"].append(image_info)

                with open(os.path.join(annotation_folder, filename), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        parts = line.strip().split('\t')
                        label = int(parts[0])
                        x1, y1, x2, y2 = map(float, parts[1:])

                        # Convert corner coordinates to top-left corner and
                        # Convert corner coordinates to top-left corner and width/height
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)

                        # Convert relative coordinates to absolute coordinates
                        x_abs = int(x * width)
                        y_abs = int(y * height)
                        w_abs = int(w * width)
                        h_abs = int(h * height)

                        bbox = [x_abs, y_abs, w_abs, h_abs]
                        area = w_abs * h_abs

                        annotation_info = {
                            "id": annotation_id,
                            "image_id": image_id,
                            "category_id": label,  # Assuming label corresponds to category ID
                            "bbox": bbox,
                            "area": area,
                            "segmentation": [],  # Optional
                            "iscrowd": 0,
                            "attributes": {}  # Optional
                        }
                        coco_val_data["annotations"].append(annotation_info)
                        annotation_id += 1

                image_id += 1

    # Save COCO format training data to a JSON file
    with open(train_json_path, "w") as f:
        json.dump(coco_train_data, f)

    # Save COCO format validation data to a JSON file
    with open(val_json_path, "w") as f:
        json.dump(coco_val_data, f)

# Example usage
convert_to_coco_format("./labels", "./images", "train_annotations1.json", "val_annotations1.json")
