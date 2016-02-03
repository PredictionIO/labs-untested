#!/usr/bin/python

import argparse
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFECV, SelectKBest, \
        SelectFromModel, f_regression
from sklearn.pipeline import Pipeline

# import problems
import o_5000_class
import fw_e_fm_class
import fm_reg

parser = argparse.ArgumentParser(
        prog="evaluate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
Evaluate models for the following problems
--------------------------------------------------------------------------------
fm_reg        - predict revenue for every user after first month of registration
fw_e_fm_class - classify if user is going to spend anything during first
                month after first week (first month != first week)
o_5000_class  - classify if user is going to spend over 5000 dollars
                during the first month after the registration''')

parser.add_argument(
        'X',
        help='features array *.npy')
parser.add_argument(
        'y',
        help='results array *.npy')
parser.add_argument(
        '--o_5000_class',
        help='models to test',
        nargs='*',
        default=[],
        choices=['ALL'] + [name for (name, m) in o_5000_class.models])
parser.add_argument(
        '--fm_reg',
        help='models to test',
        nargs='*',
        default=[],
        choices=['ALL'] + [name for (name, m) in fm_reg.models])
parser.add_argument(
        '--fw_e_fm_class',
        help='models to test',
        nargs='*',
        default=[],
        choices=['ALL'] + [name for (name, m) in fw_e_fm_class.models])
parser.add_argument(
        '--PCA',
        type=int,
        default=7,
        help='number of dimensions to reduce data to')
parser.add_argument(
        '--KBest',
        type=int,
        default=7,
        help='Select K Best features')
parser.add_argument(
        '--chain',
        nargs='*',
        choices=['KBest', 'PCA', 'Poly'],
        help='Modify input features in provided order')

class EvaluationContext:

    # @param problem_name is the name of the ML problem considered
    # @param metrics is an iterable of (name, metrics) to evaluate models
    # @param models is an iterable of (name, model)
    # @param preparer is a callable(X, y) returning X, y, folds_iterator
    def __init__(self, problem_name, metrics, models, preparer):
        self.problem_name = problem_name
        self.metrics = metrics
        self.models = models
        self.prepare_data = preparer


# --------- Pipeline --------------------------------------------------------------

def create_pipeline(chain, name, model):
    p = Pipeline(chain + [(name, model)])
    return p

def get_models_for_names(names, models):
    return [(name, model) for (name, model) in models if name in names]

# --------- Evaluation ------------------------------------------------------------

def run_model(model, X_train, y_train, X_test, y_test, metrics):

    model.fit(X_train, y_train)
    y_res = model.predict(X_test)

    scores = {}
    for name, metric in metrics:
        scores[name] = metric(y_test, y_res)

    return scores


def evaluate(X, y, chain, ctx):
    print("=== Evaluating models for the problem: {0} ===".format(ctx.problem_name))

    print("--- Preparing data... ---")
    X, y, folds = ctx.prepare_data(X, y)

    if any(chain):
        ctx.models = list(map(
            lambda mt: (mt[0], create_pipeline(chain, mt[0], mt[1])),
            ctx.models))

    for name, m in ctx.models:
        print("--- Evaluating: {0}... ---".format(name))
        scores = { name:[] for (name, metric) in ctx.metrics }

        for train_index, test_index in folds:
            results = run_model(
                    m, X[train_index], y[train_index],
                    X[test_index], y[test_index],
                    ctx.metrics)

            for metric_name, score in results.items():
                print("{0} score: {1:.3f}".format(metric_name, score))
                scores[metric_name].append(score)
        print()

        print("--- Overall scores: ---")
        for metric_name, scores in scores.items():
            sc_arr = np.array(scores)
            print("{0}: {1:.3f} (+/-) {2:.3f}".format(
                metric_name, sc_arr.mean(), sc_arr.std(), name))
            print("Min: {0:.3f} Max {1:.3f}".format(sc_arr.min(), sc_arr.max()))
        print()


# --------- Main-------------------------------------------------------------------

if __name__ == "__main__":
    args = parser.parse_args()
    os.environ["OMP_NUM_THREADS"] = "4"

    print("=== Reading data... ===")
    X = np.load(args.X)
    y = np.load(args.y)

    chain = []
    if args.chain:
        for modifier in args.chain:
            if modifier == "PCA":
                chain.append(("PCA", PCA(args.PCA)))
            elif modifier == "KBest":
                chain.append(("SelectKBest", SelectKBest(f_regression, k=args.KBest)))
            elif modifier == "Poly":
                chain.append(("PolynomialFeatures", PolynomialFeatures(2)))

    contexts = []
    if any(args.o_5000_class):
        models = []
        if args.o_5000_class[0] == 'ALL':
            models = o_5000_class.models
        else:
            models = get_models_for_names(args.o_5000_class, o_5000_class.models)

        contexts.append(EvaluationContext(
            "Over 5000 in the first month",
            o_5000_class.metrics,
            models,
            o_5000_class.prepare_data))

    if any(args.fw_e_fm_class):
        models = []
        if args.fw_e_fm_class[0] == 'ALL':
            models = fw_e_fm_class.models
        else:
            models = get_models_for_names(args.fw_e_fm_class, fw_e_fm_class.models)

        contexts.append(EvaluationContext(
            "Is the first week spending not equal to the first month spending for every user",
            fw_e_fm_class.metrics,
            models,
            fw_e_fm_class.prepare_data))

    if any(args.fm_reg):
        models = []
        if args.fm_reg[0] == 'ALL':
            models = fm_reg.models
        else:
            models = get_models_for_names(args.fm_reg, fm_reg.models)

        contexts.append(EvaluationContext(
            "Predictions of user spendings during the first month after registration",
            fm_reg.metrics,
            models,
            fm_reg.prepare_data))

    for ctx in contexts:
        evaluate(X, y, chain, ctx)
