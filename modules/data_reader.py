from io import BytesIO

import boto3
import modules.utils as utils
import pandas as pd


class S3DataReader:
    def __init__(self, bucket_name, region_name, aws_access_key_id, aws_secret_access_key):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.s3 = session.client('s3')
        self.bucket_name = bucket_name

    def load_file(self, name, type, load=None):
        with utils.Timer() as t:
            t.log(f'Loading {name}.{type} from S3')

            file_obj = self.s3.get_object(
                Bucket=self.bucket_name, Key=f'{name}.{type}'
            )
            file_data = file_obj['Body'].read()
            file_buffer = BytesIO(file_data)

            if load:
                df = load(file_buffer)
            else:
                if type == 'csv':
                    df = pd.read_csv(
                        file_buffer, encoding='ISO-8859-1', low_memory=False
                    )
                elif type == 'parquet':
                    df = pd.read_parquet(file_buffer)
                else:
                    raise ValueError(f"Unsupported file type: {type}")

            t.log(f'Loaded {len(df)} rows')

        return df
