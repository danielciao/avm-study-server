from modules.data_reader import S3DataReader
from modules.school_finder import SchoolFinder


class LocationAttributeFinder:
    def __init__(self):
        # Load and prepare all the necessary data
        self.reader = S3DataReader(
            bucket_name='avm-area-data',
            region_name='eu-west-2',
            aws_access_key_id='AKIAWJUUQTPWZZXZRLE6',
            aws_secret_access_key='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',
        )

        self.uprn_df = self.reader.load_file('london_uprn', 'parquet')
        self.onsud_df = self.reader.load_file(
            'onsud_london_feb_2023-geodetic', 'parquet')

        self.school_finder = SchoolFinder(
            reader=self.reader, uprn_df=self.uprn_df)

    def get_load_status(self):
        return {'schools': len(self.school_finder.df)}

    def find_schools(self, lat, lon, radius):
        return self.school_finder.get_schools_within_radius(central_point=(lat, lon), radius=radius).to_json(orient='records')
