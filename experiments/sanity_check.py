import numpy as np

from torch.distributions.log_normal import LogNormal
from sklearn.tree import DecisionTreeRegressor
from ngboost import SurvNGBoost
from experiments.evaluation import calculate_concordance_naive

from ngboost.scores import MLE_surv, CRPS_surv


def main():
    m, n = 100, 50
    X = np.random.rand(m, n).astype(np.float32)
    # Y = np.random.rand(m).astype(np.float32) * 2 + 1
    Y = np.sum(X, axis=1)
    Y = (Y - np.mean(Y)) / np.std(Y)
    Y = Y - np.min(Y) + 1e-2
    C = (np.random.rand(m) > 0.5).astype(np.float32)
    # C = np.zeros_like(Y)

    sb = SurvNGBoost(Base = lambda : DecisionTreeRegressor(criterion='mse'),
                     Dist = LogNormal,
                     Score = MLE_surv,
                     n_estimators = 12,
                     learning_rate = 0.1,
                     natural_gradient = True,
                     second_order = True,
                     quadrant_search = False,
                     nu_penalty=1e-5)

    train, test = sb.fit(X[:70], Y[:70], C[:70], X[70:], Y[70:], C[70:])
    preds = sb.pred_mean(X)

    print("Train/DecTree:", calculate_concordance_naive(preds, Y, C))
    print('Pred_mean: %f, True_mean: %f' % (np.mean(preds), np.mean(Y)))


if __name__ == '__main__':
    main()