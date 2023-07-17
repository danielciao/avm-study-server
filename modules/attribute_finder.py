from modules.data_reader import S3DataReader


class LocationAttributeFinder:
    def __init__(self):
        # Load and prepare all the necessary data
        self.reader = S3DataReader(
            bucket_name='avm-area-data',
            region_name='eu-west-2',
            aws_access_key_id='AKIAWJUUQTPWZZXZRLE6',
            aws_secret_access_key='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',
        )

        self.school_df = self.reader.load_file(
            'national_school_edubasealldata20230402', 'csv')

    def get_load_status(self):
        return {'schools': len(self.school_df)}
