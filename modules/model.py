import pickle

from modules.data_reader import S3DataReader


class Model:
    def __init__(self):
        self.reader = S3DataReader()

        self.model = self.reader.load_file(
            name='model', type='pkl', load=lambda buffer: pickle.load(buffer))

    def predict(self, df):
        return self.model.predict(df)  # type: ignore
