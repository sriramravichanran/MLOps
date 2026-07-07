# Light Gradient Boosting Meachine -> LightGBM developed by Microsoft and It is open source.

from scipy.stats import randint,uniform

LGBM_PARAMS = {
    'n_estimators': randint(100,500),
    'max_depth':randint(5,50),
    'learning':uniform(0.01,0.2),
    'boosting_type': ['gbdt', 'dart', 'goss']
    }

RANDOM_SEARCH_PARAMS = {
    'n_iter': 5,
    'cv':5,
    'n_jobs':-1,
    'verbose':2,
    'random_state':42,
    'scoring':'accuracy'
}