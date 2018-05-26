import numpy as np
from scipy import misc, ndimage
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def read_image(path = "trees.png"):
    image = ndimage.imread(path, mode="RGB")
    return image


def fit_kmeans(n_clusters):
    """
    fit kmeans
    :param n_clusters:
    :return:
    """
    kme = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    kme.fit(rgb)
    return kme


def predict_kmeans(test, shape):
    """
    predict which center an image point belong to
    :param test: test data
    :param shape: the shape of the image (x,y)
    :return:
    """
    return kme.predict(test).reshape(shape)

# fill in rgb values with
def fill_rgbs(projected, kme, result):
    """
    :param projected: prejected image (x,y,r,g,b)
    :param kme: kme trained model
    :param result: predicted cluster center(stored in result), for every x, y, one center number
            0 - num_cluster
    :return:
    """
    for i in range(projected.shape[0]):
        for j in range(projected.shape[1]):
            for k in range(3):  # RGB
                cluster_center = kme.cluster_centers_[result[i][j], :]
                projected[i][j][k] = cluster_center[k]

def show_image(img):
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    # read image and preprocessing
    image = read_image("trees.png")
    shape = image.shape[0:2]
    rgb = image.reshape((-1, 3)).astype(np.float64)
    # kmeans classifier, here training data and testing data is the same
    # since we do image segmentation
    for num_cluster in [3, 9, 20]:
        kme = fit_kmeans(num_cluster)
        result = predict_kmeans(rgb, shape)
        # fill rgbs
        projected = np.empty_like(image)
        fill_rgbs(projected, kme, result)
        # show image
        show_image(projected)







