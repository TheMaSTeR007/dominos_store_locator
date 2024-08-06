# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Connecting to Database
client = pymysql.Connect(
    database='dominos_db',
    user='root',
    password='actowiz',
    autocommit=True,
)
cursor = client.cursor()


class DominosStoreLocatorPipeline:
    def process_item(self, item, spider):
        insert_query = '''INSERT INTO `dominos_db`.`dominos_stores`
                        (`address`, `area`, `landmark`, `phone`, `open_until`, `map_url`, `site_url`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        print('Inserting Data into DB Table...')
        try:
            cursor.execute(query=insert_query, args=tuple(item.values()))
        except Exception as e:
            print(e)
        print('Inserted Data...')
