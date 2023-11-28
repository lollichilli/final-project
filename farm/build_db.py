#!/usr/bin/env python3
"""Build the database"""

import csv
import pathlib

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Product

def init_db(filename: str):
    """Initialize the database"""
    this_dir = pathlib.Path(__file__).parent
    if pathlib.Path(f"{this_dir}/{filename}.sqlite3").exists():
        pathlib.Path(f"{this_dir}/{filename}.sqlite3").unlink()
    engine = sa.create_engine(f"sqlite:///{this_dir}/{filename}.sqlite3")
    session = scoped_session(sessionmaker(bind=engine))

    Product.metadata.create_all(engine)

    with open(f"{this_dir}/{filename}.csv", "r", encoding="utf8") as f:
        content = csv.DictReader(f)
        headers = content.fieldnames
        print("CSV Headers:", headers)

        for item in content:
            try:
                p_id = item["id"]
            except KeyError as e:
                print(f"KeyError: {e} not found in item: {item}")
                continue

            a_product = Product(
                p_id=p_id,
                name=item["name"],
                description=item["description"],
                price=item["price"],
                available=bool(item["available"].lower()),
                image=item["image"],
            )
            session.add(a_product)

        session.commit()

def main():
    """This is the main function"""
    init_db("farmtotable")

if __name__ == "__main__":
    main()
