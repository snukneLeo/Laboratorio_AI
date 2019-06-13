"""
Utility functions
"""

import numpy as np
import matplotlib.pyplot as plt


def build_path(node):
    """
    Builds a path going backward from a node

    Args:
        node: node to start from

    Returns:
        path from root to ``node``
    """
    path = []
    while node.parent is not None:
        path.append(node.state)
        node = node.parent
    return tuple(reversed(path))


def run_episode(environment, policy, limit):
    """
    Executes an episode within ``env`` following ``policy``

    Args:
        environment: problem
        policy: policy to follow
        limit: maximum number of steps

    Returns:
        reward
    """
    obs = environment.reset()
    done = False
    reward = 0
    s = 0
    while not done and s < limit:
        obs, r, done, _ = environment.step(policy[obs])
        reward += r
        s += 1
    return reward


def plot(series, title, xlabel, ylabel):
    """
    Plots data

    Args:
        series: data series
        title: plot title
        xlabel: x labels
        ylabel: y labels
        ylabel: y labels
    """
    plt.figure(figsize=(13, 6))
    for s in series:
        plt.plot(s["x"], s["y"], label=s["label"])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()


def rolling(a, window):
    """
    Running mean

    Args:
        a: input array
        window: sliding window size

    Returns:
         Running mean
    """
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.mean(np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides), -1)