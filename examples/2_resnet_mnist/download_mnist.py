#!/usr/bin/env python3
# -*- encoding utf-8 -*-

'''
@File: save_mnist_to_jpg.py
@Date: 2024-08-23
@Author: KRISNAT
@Version: 0.0.0
@Email: ****
@Copyright: (C)Copyright 2024, KRISNAT
@Desc: 
    1. 通过 torchvision.datasets.MNIST 下载、解压和读取 MNIST 数据集；
    2. 使用 PIL.Image.save 将 MNIST 数据集中的灰度图片以 JPEG 格式保存。
'''

import sys, os
sys.path.insert(0, os.getcwd())
from shutil import copy, rmtree
import random

from torchvision.datasets import MNIST
import PIL
from tqdm import tqdm


def mk_file(file_path: str):
    if os.path.exists(file_path):
        # if the folder exists, delete it and create a new one
        rmtree(file_path)
    os.makedirs(file_path)


if __name__ == "__main__":
    # 图片保存路径
    cwd = os.getcwd()
    data_root = os.path.join(cwd, "datasets")
    if not os.path.exists(data_root):
        os.makedirs(data_root)

    # 从网络上下载或从本地加载MNIST数据集
    # 训练集60K、测试集10K
    # torchvision.datasets.MNIST接口下载的数据一组元组
    # 每个元组的结构是: (PIL.Image.Image image model=L size=28x28, 标签数字 int)
    training_dataset = MNIST(
        root='mnist',
        train=True,
        download=True,
    )
    test_dataset = MNIST(
        root='mnist',
        train=False,
        download=True,
    )

    # create folders for train sets
    train_root = os.path.join(data_root, "train")
    mk_file(train_root)
    for i in range(10):
        mk_file(os.path.join(train_root, str(i)))

    # create folders for validation sets
    val_root = os.path.join(data_root, "val")
    mk_file(val_root)
    for i in range(10):
        mk_file(os.path.join(val_root, str(i)))
        
    # 保存训练集图片
    with tqdm(total=len(training_dataset), ncols=150) as pro_bar:
        for idx, (X, y) in enumerate(training_dataset):
            class_name = str(training_dataset[idx][1])
            file_path = os.path.join(train_root, class_name, str(idx) + ".jpg")  # 文件路径
            training_dataset[idx][0].save(file_path)
            pro_bar.update(n=1)

    # 保存测试集图片
    with tqdm(total=len(test_dataset), ncols=150) as pro_bar:
        for idx, (X, y) in enumerate(test_dataset):
            class_name = str(test_dataset[idx][1])
            file_path = os.path.join(val_root, class_name, str(idx) + ".jpg")  # 文件路径
            test_dataset[idx][0].save(file_path)
            pro_bar.update(n=1)

