import numpy as np
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression, SGDClassifier, \
        PassiveAggressiveClassifier, RidgeClassifier
from sklearn.preprocessing import scale
from sklearn.utils import shuffle
from sklearn.metrics import roc_auc_score, recall_score, precision_score, f1_score, \
        fbeta_score, make_scorer
from sklearn.ensemble import RandomForestRegressor, AdaBoostClassifier, \
        GradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from estimators import XGBClassifierWrapper, InterestingUsersClassifier, \
        prepare_bayes

xgb_params = {
        'eval_metric': 'auc',
        'nthread': 4,
        "alpha": 0.04,
        'gamma': 0.005,
        'max_delta_step': 1,
        'max_depth': 8,
        'subsample': 0.99,
        'eta': 0.1,
        'silent': 1,
        }


models = [
        ("Two LogisticRegressions", InterestingUsersClassifier()),
        ("Simple Logistic regression", LogisticRegression(class_weight='balanced')),
        ("AdaBoostClassifier", AdaBoostClassifier()),
        ("GradientBoostingClassifier", GradientBoostingClassifier()),
        ("ExtraTreesClassifier", ExtraTreesClassifier(class_weight='balanced')),
        ("GaussianNB", GaussianNB()),
        ("MultinomialNB", prepare_bayes(MultinomialNB(class_prior=[0.3, 0.7]))),
        ("SGDClassifier1",
            SGDClassifier(
                loss='log', penalty='elasticnet', l1_ratio=0.2, class_weight='balanced')),
        ("SGDClassifier2",
            SGDClassifier(
                loss='log', alpha=0.01, penalty='elasticnet', l1_ratio=0.2, class_weight='balanced')),
        ("BaggingLogisticClassifier",
            BaggingClassifier(base_estimator=LogisticRegression(class_weight='balanced'))),
        ("BaggingLogisticSGDC",
            BaggingClassifier(base_estimator=SGDClassifier(
                loss='log', penalty='elasticnet', l1_ratio=0.2, class_weight='balanced'))),
        ('XGBoost', XGBClassifierWrapper(n_rounds=80, **xgb_params)),
        ('BaggedXGBoost', BaggingClassifier(
            XGBClassifierWrapper(n_rounds=80, **xgb_params),
            15, max_samples=0.9, n_jobs=1)),
        ]

def my_fbeta_score(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=10)

metrics = [
        ("ROC_AUC", roc_auc_score),
        ("Recall", recall_score),
        ("F-beta", my_fbeta_score),
        ("Precision", precision_score)
        ]

def prepare_data(X, y):
    X, y = shuffle(X, y)
    X = scale(X)
    y = np.where(y > 5000, 1, 0)

    return X, y, StratifiedKFold(y, n_folds=5)
