import dateutil.parser
import os
import pandas as pd
import sys
import time
from sqlalchemy.sql import text
from customerupload import db

class ProcessInput:
    UNPROCESSED_PATH = "customerupload/data/unprocessed/"
    COMPLETE_PATH = "customerupload/data/complete/"
    ERROR_PATH = "customerupload/data/error/"

    def __init__(self, tsv_path):
        self._tsv_path = tsv_path

    def _insert_product(self, row):
        sql_insert_product = """
            INSERT IGNORE INTO products
            (id, product_name)
            VALUES (:product_id, :product_name)
        """
        db.engine.execute(text(sql_insert_product),
                          product_id=row['product_id'],
                          product_name=row['product_name'])

    def _insert_user(self, row, start_time):
        sql_insert_user = """
            INSERT IGNORE INTO users
            (
                id, first_name, last_name,
                street_address, state_code, zip_code,
                created_at, updated_at
            ) VALUES (
                :id, :first_name, :last_name,
                :street_address, :state_code, :zip_code,
                :created_at, :updated_at
            ) ON DUPLICATE KEY UPDATE
                first_name = VALUES(first_name),
                last_name = VALUES(last_name),
                street_address = VALUES(street_address),
                state_code = VALUES(state_code),
                zip_code = VALUES(zip_code),
                updated_at = VALUES(updated_at)
        """
        db.engine.execute(text(sql_insert_user),
                          id=row['user_id'],
                          first_name=row['first_name'],
                          last_name=row['last_name'],
                          street_address=row['street_address'],
                          state_code=row['state_code'],
                          zip_code=row['zip_code'],
                          created_at=row['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                          updated_at=start_time.strftime('%Y-%m-%d %H:%M:%S'))

    def _insert_transaction(self, row, start_time):
        sql_insert_transaction = """
            INSERT IGNORE INTO transactions
            (
                user_id,
                product_id,
                purchase_status,
                purchase_amount,
                created_at
            ) VALUES (
                :user_id,
                :product_id,
                :purchase_status,
                :purchase_amount,
                :created_at
            )
        """
        db.engine.execute(text(sql_insert_transaction),
                          user_id=row['user_id'],
                          product_id=row['product_id'],
                          purchase_status=row['purchase_status'],
                          purchase_amount=row['purchase_amount'],
                          created_at=row['datetime'].strftime('%Y-%m-%d %H:%M:%S'))

    def _insert_subscription(self, row, start_time):
        if row['purchase_status'] == 'canceled':
            sql_get_user_subscription = """
                SELECT *
                FROM subscriptions
                WHERE user_id = :user_id AND product_id = :product_id
            """
            user_subscription_result = db.engine.execute(text(sql_get_user_subscription),
                                                         user_id=row['user_id'],
                                                         product_id=row['product_id'])
            user_subscription = pd.DataFrame(user_subscription_result)

            if len(user_subscription) == 0:
                print("ERROR: Non existant subscription attempted to be cancelled: {}, {}".format(user_subscription,
                    row.to_string()), file=sys.stderr)
            else:
                sql_delete_user_subscription = """
                    DELETE FROM subscriptions
                    WHERE user_id = :user_id AND product_id = :product_id
                """
                db.engine.execute(text(sql_get_user_subscription),
                                  user_id=row['user_id'],
                                  product_id=row['product_id'])
        else:
            sql_insert_user_subscription = """
                INSERT IGNORE INTO subscriptions
                (
                    user_id,
                    product_id,
                    purchase_amount,
                    created_at,
                    updated_at
                ) VALUES (
                    :user_id,
                    :product_id,
                    :purchase_amount,
                    :created_at,
                    :updated_at
                ) ON DUPLICATE KEY UPDATE
                    updated_at = VALUES(updated_at)
            """
            db.engine.execute(text(sql_insert_user_subscription),
                              user_id=row['user_id'],
                              product_id=row['product_id'],
                              purchase_amount=row['purchase_amount'],
                              created_at=row['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                              updated_at=start_time.strftime('%Y-%m-%d %H:%M:%S'))

    def _process_row(self, row, start_time):
        # todo: wrap all these functions in a transaction so we can back out
        self._insert_product(row)
        self._insert_user(row, start_time)
        self._insert_transaction(row, start_time)
        self._insert_subscription(row, start_time)
        # todo: return success based on completion of all steps w/o exception
        return True

    def execute(self):
        start_time = time
        
        tsv = pd.read_csv(self._tsv_path, sep='\t',
                                names=["user_id", "first_name", "last_name", "street_address", "state_code", "zip_code", "purchase_status", "product_id", "product_name", "purchase_amount", "dt_ISO8601"])
        tsv['datetime'] = tsv['dt_ISO8601'].apply(lambda ts: dateutil.parser.parse(ts))

        input_rows = len(tsv.index)
        processed_rows = 0
        for index, row in tsv.iterrows():
            processed_success = self._process_row(row, start_time)
            processed_rows += 1 if processed_success else 0

        new_filename = start_time.strftime("%Y%m%d-%H%M%S") + '.tsv'
        # if processed_rows == input_rows:
        #     if not os.path.exists(self.COMPLETE_PATH):
        #         os.makedirs(self.COMPLETE_PATH)
        #     os.rename(self._tsv_path, self.COMPLETE_PATH + new_filename)
        # else:
        #     if not os.path.exists(self.ERROR_PATH):
        #         os.makedirs(self.ERROR_PATH)
        #     os.rename(self._tsv_path, self.ERROR_PATH + new_filename)
        return processed_rows
        
