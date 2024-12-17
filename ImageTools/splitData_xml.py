import os
import pickle
import random

# Paths
dataset_path = '/home/iplslam/Husha/Dataset/1_3/all/jpg'
xml_path = '/home/iplslam/Husha/Dataset/1_3/all/xml'
train_dataset_path = '/home/iplslam/Husha/Dataset/1_3/train.pkl'
valid_dataset_path = '/home/iplslam/Husha/Dataset/1_3/valid.pkl'

# List of image and annotation files
image_files = sorted([os.path.join(dataset_path, f) for f in os.listdir(dataset_path) if f.endswith('.jpg')])
annotation_files = sorted([os.path.join(xml_path, f) for f in os.listdir(xml_path) if f.endswith('.xml')])

# Shuffle and split
combined = list(zip(image_files, annotation_files))
random.shuffle(combined)
split_idx = int(len(combined) * 0.8)  # 80% train, 20% valid
train_data = combined[:split_idx]
valid_data = combined[split_idx:]

# Save splits
def save_split(data, path):
    image_files, annotation_files = zip(*data)
    with open(path, 'wb') as f:
        pickle.dump((image_files, annotation_files), f)

save_split(train_data, train_dataset_path)
save_split(valid_data, valid_dataset_path)

print(f"Training data saved to {train_dataset_path}")
print(f"Validation data saved to {valid_dataset_path}")
