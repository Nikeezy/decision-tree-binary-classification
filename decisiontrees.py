# -*- coding: utf-8 -*-
"""DecisionTrees.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1crvPM3cm_nNAWMkgEz4DjC4SOW3MBxj7
"""

from numpy.lib.utils import info
import numpy as np
import matplotlib.pyplot as plt


def compute_entropy(y):

    entropy = 0.

    if len(y) != 0:
        p1 = len(y[y == 1]) / len(y)
        if p1 != 0 and p1 != 1:
            entropy = -p1 * np.log2(p1) - (1 - p1) * np.log2(1 - p1)
        else:
            entropy = 0.

    return entropy


def split_dataset(X, node_indices, feature):

    left_indices = []
    right_indices = []

    for i in node_indices:
        if X[i][feature] == 1:
            left_indices.append(i)
        else:
            right_indices.append(i)

    return left_indices, right_indices


def compute_information_gain(X, y, node_indices, feature):

    left_indices, right_indices = split_dataset(X, node_indices, feature)

    X_node, y_node = X[node_indices], y[node_indices]
    X_left, y_left = X[left_indices], y[left_indices]
    X_right, y_right = X[right_indices], y[right_indices]

    node_entropy = compute_entropy(y_node)

    left_entropy = compute_entropy(y_left)

    right_entropy = compute_entropy(y_right)

    w_left = len(X_left) / len(X_node)
    w_right = len(X_right) / len(X_node)

    w_entropy = w_left * left_entropy + w_right * right_entropy

    informational_gain = node_entropy - w_entropy

    return informational_gain


def get_best_split(X, y, node_indices):

    num_features = X.shape[1]

    best_feature = -1

    max_info_gain = 0

    for feature in range(num_features):
        info_gain = compute_information_gain(X, y, node_indices, feature)
        if info_gain > max_info_gain:
            max_info_gain = info_gain
            best_feature = feature

    return best_feature


def build_tree_recursive(X, y, node_indices, branch_name, max_depth, cur_depth, tree):

    tree = []

    if cur_depth == max_depth:
        formatting = " " * cur_depth + "-" * cur_depth
        print(formatting +
              f"{branch_name} leaf node with indices {node_indices}")
        return


    best_feature = get_best_split(X, y, node_indices)
    tree.append((cur_depth, branch_name, best_feature, node_indices))

    formatting = "-"*cur_depth
    print(f"{formatting} Depth {cur_depth}, \
    {branch_name}: Split on feature: {best_feature}")

    left_indices, right_indices = split_dataset(X, node_indices, best_feature)

    build_tree_recursive(X, y, left_indices, "Left", max_depth, cur_depth + 1, tree)
    build_tree_recursive(X, y, right_indices, "Right", max_depth, cur_depth + 1, tree)

    return tree

"""# Новый раздел"""

X_train = np.array([[1,1,1],[1,0,1],[1,0,0],[1,0,0],[1,1,1],[0,1,1],[0,0,0],[1,0,1],[0,1,0],[1,0,0]])
y_train = np.array([1,1,0,0,1,0,0,1,1,0])

root_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

compute_information_gain(X_train, y_train, root_indices, 0)
get_best_split(X_train, y_train, root_indices)
build_tree_recursive(X_train, y_train, root_indices, "Root", 2, 0, [])