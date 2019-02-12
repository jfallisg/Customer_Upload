import os
import pandas as pd
import time

class ProcessInput:
    UNPROCESSED_PATH = "customerupload/data/unprocessed/"
    COMPLETE_PATH = "customerupload/data/complete/"
    ERROR_PATH = "customerupload/data/error/"

    def __init__(self, tsv_path):
        self._tsv_path = tsv_path

    def _insert_user(self, row):
        print('_insert_user: ', row)

    def _insert_product(self, row):
        print('_insert_product: ', row)

    def _insert_address(self, row):
        print('_insert_address: ', row)

    def _insert_transaction(self, row):
        print('_insert_transaction: ', row)

    def _update_subscription(self, row):
        print('_update_subscription: ', row)

    def _process_row(self, row):
        print('_process_row: ', row)
        # todo: wrap all these functions in a transaction so we can back out

        self._insert_user(row)
        # self._insert_product(row)
        # self._insert_address(row)
        # self._insert_transaction(row)
        # self._update_subscription(row)
        
        # todo: return success based on completion of all steps w/o exception
        return True

    def execute(self):
        # start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_time = time
        
        tsv = pd.read_csv(self._tsv_path, sep='\t',
                                names=["user_id", "first_name", "last_name", "street_address", "state_code", "zip_code", "purchase_status", "product_id", "product_name", "purchase_amount", "dt_ISO8601"])
        
        input_rows = len(tsv.index)
        processed_rows = 0
        for index, row in tsv.iterrows():
            processed_success = self._process_row(row)
            processed_rows += 1 if processed_success else 0

        new_filename = start_time.strftime("%Y%m%d-%H%M%S") + '.tsv'
        if processed_rows == input_rows:
            if not os.path.exists(self.COMPLETE_PATH):
                os.makedirs(self.COMPLETE_PATH)
            os.rename(self._tsv_path, self.COMPLETE_PATH + new_filename)
        else:
            if not os.path.exists(self.ERROR_PATH):
                os.makedirs(self.ERROR_PATH)
            os.rename(self._tsv_path, self.ERROR_PATH + new_filename)
        
