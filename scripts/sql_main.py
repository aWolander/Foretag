from SQL_ORM import *
import sqlalchemy as sqlal


def main():
    engine = sqlal.create_engine("postgresql+psycopg2://postgres:Manifold_GHJ_69@localhost:5432/manifold")
    # with sqlal.orm.Session(engine) as session:
        # result  = session.execute(sqlal.select(Category)).scalar()
        # print(result)
        # for res in result:
        #     print(res)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # Base.metadata.commit


main()
