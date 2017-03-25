import numpy as np
import matplotlib.pyplot as plt


filename_train = "a9a/a9a"
filename_test = "a9a/a9a.t"
iter_num = 15


def read_data(filename):
    target = []
    mat = []
    dim = 123
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            words = line.split()
            target.append(int(words[0]))
            data_line = [0] * dim
            for num in words[1:]:
                ind = num.split(":")
                ind_num = int(ind[0])
                data_line[ind_num-1] = 1.0
            mat.append(data_line)
            line = f.readline()
    y = np.array(target)
    y = y.reshape([1, -1])
    y = (y+1)/2
    X = np.array(mat)
    X = X.T
    return y, X


def sigmoid(X):
    return 1.0 / (1 + np.exp(-X))


def forward(X, W):
    return sigmoid(np.dot(W, X))


def construct_R(y):
    diag = y * (1 - y)
    diag = diag.reshape(-1)
    return np.diag(diag)


def update(y_hat, y, X, R, W, lambda_val):
    H = np.dot(np.dot(X, R), X.T)
    H += lambda_val * np.eye(H.shape[0])
    H_inv = np.linalg.pinv(np.mat(H))
    return (np.mat(y_hat - y) * np.mat(X).T + lambda_val * W) * np.mat(H_inv)


def loss(y, y_hat):
    mu = y_hat > 0.5
    return np.sum(np.abs(y-mu))


def norm2(w):
    return np.sum(w ** 2)

if __name__ == "__main__":
    y, X = read_data(filename_train)
    y_t, X_t = read_data(filename_test)

    embed_dim, sample_num = X.shape
    _, sample_num_t = X_t.shape

    l = []
    l_t = []
    w_norm2 = []

    lambda_list = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]

    for lambda_val in lambda_list:
        l_row = []
        l_row_t = []
        w_norm2_row = []
        # This one is unstable
        # W = np.random.rand(1, embed_dim) - 0.5
        # use this one
        W = 0.001 * np.ones([1, embed_dim])
        for i in range(iter_num):
            y_hat = forward(X, W)
            y_hat_t = forward(X_t, W)
            # (N, N)
            R = construct_R(y_hat)
            delta_W = update(y_hat, y, X, R, W, lambda_val)
            W -= delta_W
            l_row.append(loss(y, y_hat) / float(sample_num))
            l_row_t.append(loss(y_t, y_hat_t) / float(sample_num_t))
            w_norm2_row.append(norm2(W))
            print("In iteration=%d, loss=%f" % (i, l_row[-1]))
        w_norm2.append(w_norm2_row)
        l.append(l_row)
        l_t.append(l_row_t)

    # plot 1: error vs. iteration
    x = np.linspace(1, iter_num, iter_num)
    plt.figure(figsize=(8, 6))
    plt_train, = plt.plot(x, l[0])
    plt_test, = plt.plot(x, l_t[0])
    plt.legend([plt_train, plt_test], ['training set', 'testing set'])
    plt.xlabel('iteration')
    plt.ylabel('error rate')
    plt.title('IRLS')
    plt.savefig('IRLS_1.png')

    # plot 2: error vs. lambda
    x_tick = lambda_list
    plt.figure(figsize=(8, 6))
    plt_train, = plt.semilogx(x_tick, [l[i][-1] for i in range(len(l))])
    plt_test, = plt.semilogx(x_tick, [l_t[i][-1] for i in range(len(l_t))])
    plt.legend([plt_train, plt_test], ['training set', 'testing set'])
    plt.xlabel('lambda')
    plt.ylabel('error rate')
    plt.title('IRLS')
    plt.savefig('IRLS_2.png')

    # plot 3: w_norm2 vs. lambda
    plt.figure(figsize=(8, 6))
    plt_handle = []
    for i in range(len(lambda_list)):
        plt_handle_tmp = plt.plot(x, w_norm2[i], label="lambda="+str(lambda_list[i]))
        plt_handle.append(plt_handle_tmp[0])
    plt.xlabel('iteration')
    plt.ylabel('||w||^2')
    plt.title('IRLS')
    plt.legend()
    plt.savefig('IRLS_3.png')
