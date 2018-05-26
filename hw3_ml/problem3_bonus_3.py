import time
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler


def make_toy_dataset(n_samples=1500):
    """
    return: data = [data, config]
    """
    # circle_dot
    radius = [0,1,2]
    noise = 0.05
    res = []
    for rad in radius:
        tmp = []
        for i in range(n_samples):
            true_rad = rad + random.gauss(0, noise)
            theta = 2 * math.pi * random.random()
            tmp.append([true_rad * math.cos(theta), true_rad * math.sin(theta)])
        res.append(tmp)
    circle_dot = np.array(res).reshape(-1,2), None
    # circles
    circles = datasets.make_circles(n_samples=n_samples, noise=0.05, factor=.5)
    # moons
    moons = datasets.make_moons(n_samples=n_samples, noise=.05)
    # blobs
    blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
    # spirals
    res = []
    for i in range(2):
        tmp = []
        for j in range(int(n_samples/10)):
            theta = 2 * 4 * np.random.random()
            tmp.append([(-1) ** i * theta * np.cos(theta) - i + 0.5, (-1) ** i * theta * np.sin(theta)])
        res.append(tmp)
    spirals = np.array(res).reshape(-1, 2), None
    # linear blobs
    X, y = datasets.make_blobs(n_samples=n_samples, random_state=170)
    X_transformation = [[0.60834549, -0.63667341], [-0.40887718, 0.85253229]]
    X_aniso = np.dot(X, X_transformation)
    linear_blobs = (X_aniso, y)
    # random
    _randoms = np.random.rand(n_samples, 2), None

    data = [
        (circle_dot, {"n_clusters": 3, "name": "circle_dot"}),
        (circles, {"n_clusters": 2, "name": "circle"}),
        (moons, {"n_clusters": 2, "name": "moons"}),
        (blobs, {"n_clusters": 3, "name": "blobs"}),
        (spirals, {"n_clusters": 2, "name": "spiral"}),
        (linear_blobs, {"n_clusters": 3, "name": "linear_blobs"}),
        (_randoms, {"n_clusters": 3, "name": "_randoms"})]

    return data


def get_cluster_model(config):
    # spectral
    # spectral_rbf = cluster.SpectralClustering(
    #     n_clusters=config['n_clusters'], eigen_solver='arpack',
    #     affinity="rbf")
    # spectral
    spectral_nn = cluster.SpectralClustering(
        n_clusters=config['n_clusters'], eigen_solver='arpack',
        affinity="nearest_neighbors")
    # kmeans
    kmeans = cluster.KMeans(init='k-means++', n_clusters=config['n_clusters'], n_init=10)

    cluster_model = (
        # ('SpectralClustering_rbf', spectral_rbf),
        ('SpectralClustering_nn', spectral_nn),
        ('kmeans', kmeans)
    )

    return cluster_model


if __name__ == "__main__":
    count = 1
    data_config = make_toy_dataset()
    plt.figure(figsize=(18, 12))
    for dataset, config in data_config:
        X, y = dataset
        # normalize dataset
        X = StandardScaler().fit_transform(X)
        # get model
        model_config = get_cluster_model(config)
        for model_label, model in model_config:
            t0 = time.time()
            # fit
            model.fit(X)
            # calculate time
            t_delta = time.time() - t0
            # predict
            y_pred = model.labels_.astype(np.int)
            # plot
            plt.subplot(len(data_config), len(model_config), count)
            plt.title(model_label + "-" + config["name"], size=12)
            colors = np.array(['b', 'c', 'y'])
            plt.scatter(X[:, 0], X[:, 1], color=colors[y_pred])

            plt.xlim(-2.5, 2.5)
            plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(.99, .01, ('%.2fs' % t_delta),
                     transform=plt.gca().transAxes, size=15,
                     horizontalalignment='right')
            count += 1
    plt.show()

