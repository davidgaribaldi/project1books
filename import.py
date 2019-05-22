import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

try:
    with open('books.csv', 'r') as fin:
        csv_in = csv.reader(fin)
        for row in csv_in:
            db.execute("INSERT INTO books (isbn, title, author, pub_year) VALUES (:isbn, :title, :author, :pub_year)",
                           {'isbn': row[0], 'title': row[1], 'author':row[2], 'pub_year':row[3]})
            print(row)
        db.commit()
        count = db.rowcount
        print(count, 'Rows inserted')
except Exception as error:
    print('Failed to insert data', error)


