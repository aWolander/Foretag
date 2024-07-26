import sqlalchemy as sqlal
# from sqlalchemy.orm import Session
import Excel_Reader_Legacy as xlr
from SQL_ORM import *
from itertools import zip_longest
import xlwings as xl
class SQL_Writer:
    def __init__(self) -> None:
        self.xlr = xlr.Book_Reader_Legacy(3, r"C:\Users\Gustav\Desktop\Företag\Foretag\data_files\review_data2.xlsx")
        self.engine = sqlal.create_engine("postgresql+psycopg2://postgres:Manifold_GHJ_69@localhost:5432/manifold")

    def from_excel_to_sql(self):
        with sqlal.orm.Session(self.engine) as session:
            
            source = session.execute(sqlal.select(Source).where(Source.name == "Webhallen")).first()
            if source is None:
                source = Source(name="Webhallen")

            for review_sheet in self.xlr:
                category_name = review_sheet.get_name()
                temp_category = session.execute(sqlal.select(Category).where(Category.name == category_name)).first()
                print(temp_category)
                if temp_category is None:
                    temp_category = Category(name=category_name, source=source)
                # print(review_sheet.get_name())
                # self.xlr.set_sheet(review_sheet.get_name())
                temp_products = []
                for [leftmost_entries, data_lists] in review_sheet:
                    product_name = leftmost_entries[0]
                    product_link = leftmost_entries[-1]
                    reviews = data_lists[0]
                    user_ratings = data_lists[1]
                    dates = data_lists[2]

                    temp_reviews = []
                    for review_text, rating, date in zip_longest(reviews, user_ratings, dates, fillvalue=""):
                        if review_text is not None:
                            review_text = review_text.strip()
                        temp_review = Review(text = review_text, rating = rating, date = date)
                        temp_reviews.append(temp_review)
                    temp_product = Product(name = product_name, reviews = temp_reviews, category = temp_category)
                    temp_products.append(temp_product)
                session.add(source)
                session.add(temp_category)
                session.add_all(temp_reviews)
                session.add_all(temp_products)
                session.commit()


def main():
    for app in xl.apps:
        app.kill()

    sqlw = SQL_Writer()
    with sqlal.orm.Session(sqlw.engine) as session:
        die  = session.execute(sqlal.select(Category).where(Category.name == "Surfplatta")).scalar()
        print(die)
        # session.delete(die)
        # session.commit()
    #     products = session.execute(sqlal.select(Product))
    #     for product in products.scalars():
    #         print(product)
    #         session.delete(product)
    #         session.commit()

    # sqlw.from_excel_to_sql()


main()