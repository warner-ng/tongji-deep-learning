import os
from shutil import copy, rmtree
import random


def mk_file(file_path: str):
    if os.path.exists(file_path):
        # if the folder exists, delete it and create a new one
        rmtree(file_path)
    os.makedirs(file_path)

if __name__ == '__main__':
    # ensure reproducibility
    random.seed(0)

    # split 10% of the dataset into the validation set
    split_rate = 0.1

    # point to your unzipped flower_photos folder
    cwd = os.getcwd()
    data_root = os.path.join(cwd, "datasets")
    origin_flower_path = os.path.join(cwd, "dataset_flowers")
    assert os.path.exists(origin_flower_path), "path '{}' does not exist.".format(origin_flower_path)

    flower_class = [cla for cla in os.listdir(origin_flower_path)
                    if os.path.isdir(os.path.join(origin_flower_path, cla))]

    # create folders for train sets
    train_root = os.path.join(data_root, "train")
    mk_file(train_root)
    for cla in flower_class:
        # create folder for each class
        mk_file(os.path.join(train_root, cla))

    # create folders for validation sets
    val_root = os.path.join(data_root, "val")
    mk_file(val_root)
    for cla in flower_class:
        # create folder for each class
        mk_file(os.path.join(val_root, cla))

    for cla in flower_class:
        cla_path = os.path.join(origin_flower_path, cla)
        images = os.listdir(cla_path)
        num = len(images)
        # random sampling
        eval_index = random.sample(images, k=int(num*split_rate))
        for index, image in enumerate(images):
            if image in eval_index:
                # copy files assigned to validation set to corresponding directory
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(val_root, cla)
                copy(image_path, new_path)
            else:
                # copy files assigned to training set to corresponding directory
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(train_root, cla)
                copy(image_path, new_path)
            print("\r[{}] processing [{}/{}]".format(cla, index+1, num), end="")  # processing bar
        print()

    print("processing done!")