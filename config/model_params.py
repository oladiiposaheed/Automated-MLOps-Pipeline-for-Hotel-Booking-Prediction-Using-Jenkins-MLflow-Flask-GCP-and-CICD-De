from scipy.stats import randint, uniform

# Create parametrs for the LightBM model
LIGHTGM_PARAMS = {
    'n_estimators': randint(10, 500),
    'max_depth': randint(10, 500),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5),
    'bootstrap': [True, False]
}

# Random Search Parameters
RANDOM_SEARCH_PARAMS = {
    'n_iter': 5,
    'n_jobs': 2,
    'cv': 5,
    'verbose': 2,
    'random_state': 43,
    'scoring': 'accuracy'
}


