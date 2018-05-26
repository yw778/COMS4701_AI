import numpy as np
import pandas as pd
import sys

def PLA(X, y):
    # w: w1, w2, w0(b)
    w_out = []
    w = np.zeros(3)
    convergence = False
    while not convergence:
        w_out.append(w)
        convergence = True
        for i in range(n):
            if X[i].dot(w) * y[i] <= 0:
                w = w + y[i] * X[i]
                convergence = False
    return w_out


if __name__ == "__main__":
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    # load and preprocess the data
    data = pd.read_csv(in_filename, header=None)
    data_np = data.values.astype(np.float)
    X = data_np[:, 0:2]
    y = data_np[:, 2]
    n = len(X)
    X = np.column_stack([X, np.ones(n)])
    # pla
    w_out = PLA(X, y)
    # save the data to csv
    pd_out = pd.DataFrame(w_out)
    pd_out.to_csv(out_filename, header = None, index = None)


