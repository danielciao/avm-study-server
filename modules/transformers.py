import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


def encode_month_to_cyclic(month):
    return -np.cos(0.52359 * month)


class BooleanToInteger(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.astype(int)

    def get_feature_names_out(self, input_features=None):
        return input_features if input_features is not None else []


class DateTimeExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.datetime_cols = X.columns.tolist()
        return self

    def transform(self, X, y=None):
        for col in self.datetime_cols:
            X[col + '_Year'] = X[col].dt.year
            X[col + '_Month'] = encode_month_to_cyclic(X[col].dt.month)
        return X.drop(columns=self.datetime_cols)

    def get_feature_names_out(self, input_features=None):
        feature_names = []
        for col in self.datetime_cols:
            feature_names.extend([col + '_Year', col + '_Month'])
        return np.array(feature_names)


class InvalidValueCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, values_to_replace=None):
        self.values_to_replace = values_to_replace if values_to_replace is not None else [
            'NO DATA!', 'INVALID!', 'unknown', 'Not defined - use in the case of a new dwelling for which the intended tenure in not known. It is no']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        replaced = X.fillna(np.nan)

        # Replace invalid values with np.nan
        for value in self.values_to_replace:
            replaced.replace(value, np.nan, inplace=True)

        return replaced

    def get_feature_names_out(self, input_features=None):
        return input_features


class StringCleaner(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        for col in X_copy.select_dtypes(include=['object']).columns:
            X_copy[col] = X_copy[col].str.upper().str.strip()

        return X_copy

    def get_feature_names_out(self, input_features=None):
        return input_features
