import os
from tempfile import NamedTemporaryFile

import boto3
import joblib as jl
import modules.utils as utils
import numpy as np


class Model:
    def __init__(self):
        bucket_name = 'avm-area-data'
        model_name = 'model.joblib'

        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get(
                              "AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.environ.get(
                              "AWS_SECRET_ACCESS_KEY"),
                          region_name='eu-west-2')

        with utils.Timer() as t:
            t.log(f'Loading model {model_name} from S3')

            with NamedTemporaryFile(delete=False) as temp_file:
                file_path = temp_file.name
                t.log(f'Temporary file created at {file_path}')

                s3.download_fileobj(bucket_name, model_name, temp_file)

                try:
                    with open(file_path, 'rb') as file_buffer:
                        self.model = jl.load(file_buffer)
                        t.log(f'Loaded model {model_name}')

                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)

    def predict(self, df):
        try:
            processed_df = df.copy()
            pipeline = self.model.named_steps['pipeline']

            processed_df = pipeline.named_steps['invalidvaluecleaner'].transform(
                processed_df)
            processed_df = pipeline.named_steps['stringcleaner'].transform(
                processed_df)
            processed_df = pipeline.named_steps['columntransformer'].transform(
                processed_df)

            best_fit = self.model.named_steps['extratreesregressor']

            predictions = np.array([tree.predict(processed_df)
                                   for tree in best_fit.estimators_])

            return {
                'lower_bound': np.percentile(predictions, 10),
                'upper_bound': np.percentile(predictions, 90),
                'prediction': self.model.predict(df).tolist()[0]
            }
        except Exception as e:
            return print(e)
