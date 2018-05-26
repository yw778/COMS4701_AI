import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

def gradient_descent(X, y, alpha, max_iter = 100):
    # w0(b), w1, w2, I include bias in w
    n = len(X)
    w = np.zeros(3)
    for i in range(int(max_iter)):
        fX = X.dot(w)
        dw = X.T.dot(fX - y) * alpha / n
        w -= dw
    loss = np.sum((X.dot(w) - y)**2) / (2*n)
    return w, loss


if __name__ == "__main__":
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]

    data = pd.read_csv(in_filename, header=None)
    # print (data)
    data_np = data.values.astype(np.float)
    X = data_np[:, :-1]
    y = data_np[:, -1]

    mu = np.mean(X, axis=0)
    stddev = np.std(X, axis=0)
    X = (X - mu) / stddev
    X = np.column_stack([np.ones(len(X)), X])
    result = []
    # losses = []
    for alpha in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]:
        w, loss = gradient_descent(X, y, alpha, max_iter=100)
        # losses.append(loss)
        result.append([alpha, 100, w[0], w[1], w[2]])

    # plt.plot([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],losses)
    # plt.xlabel("alpha")
    # plt.ylabel("losses")
    # print(losses)
    # plt.show()


    # grid search to find the best parameter
    best_alpha = None
    best_iter = None
    best_out = None
    best_loss = float("inf")
    for alpha in np.linspace(0.05, 2, 20):
        for max_iter in np.linspace(50, 1001, 100):
            max_iter = int(max_iter)
            w, loss = gradient_descent(X, y, alpha, max_iter)
            if loss < best_loss:
                best_iter = max_iter
                best_alpha = alpha
                best_out = [alpha, max_iter, w[0], w[1], w[2]]
                best_loss = loss

    result.append(best_out)
    result_out = pd.DataFrame(result)
    result_out.to_csv(out_filename, header=None, index=None)





