from fastapi import FastAPI, Path, Query
from pydantic import BaseModel  as BM
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import uvicorn
import select
from treelib import Tree

app = FastAPI(title="Users_Registration")

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",metadata,
                        sqlalchemy.Column("user_id",sqlalchemy.Integer),
                        sqlalchemy.Column("user_name",sqlalchemy.Text),
                         sqlalchemy.Column("user_surname",sqlalchemy.Text),
                         sqlalchemy.Column("user_age",sqlalchemy.Integer),
                         sqlalchemy.Column("user_height",sqlalchemy.Integer),
                         sqlalchemy.Column("user_city",sqlalchemy.Text)
                         )

engine = sqlalchemy.create_engine("sqlite:///users-sqlalchemy.db")
connection = engine.connect()
metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


#Заносим в базу полную инфу о пользователе
@app.get("/{user_id}/{user_name}/{user_surname}/{user_age}/{user_height}/{user_city}")
def user_into_db(user_id: int,
                 user_name: str = Path(),
                 user_surname:str = Path(),
                 user_age:int = Path(),
                 user_height:int = Path(),
                 user_city:str = Path()
                ):
    
    insertion_query = users.insert().values(
        {"user_id": user_id,
         "user_name":user_name,
         "user_surname":user_surname,
         "user_age":user_age,
         "user_height": user_height,
         "user_city":user_city
         }
    )
    connection.execute(insertion_query)
    connection.commit()

    return "User has been added"

#Добавление по частям. Создание айди пользователя.
@app.get("/add_id/{user_id}")
def user_id_into_db(user_id: int = Path()):
    insertion_id_query = users.insert().values(
        {"user_id": user_id,
         "user_name": "Default",
         "user_surname": "Default",
         "user_height": 0,
         "user_age": 0,
         "user_city": "Default"
         }
    )
    connection.execute(insertion_id_query)
    connection.commit()

    return "User id has been added"

@app.get("/add_name/{user_id}/{user_name}")
def user_first_name_into_db(user_id: int, user_name: str):
    update_query = users.update().where(users.columns.user_id == user_id ).values(user_name = user_name)
    cur = connection.execute(update_query)
    connection.commit()

    return "User name has been added"

@app.get("/add_surname/{user_id}/{user_surname}")
def user_last_name_into_db(user_id:int,user_surname: str):
    update_query = users.update().where(users.columns.user_id == user_id).values(user_surname=user_surname)
    cur = connection.execute(update_query)
    connection.commit()

    return "User surname has been added"


@app.get("/add_height/{user_id}/{user_height}")
def user_height_into_db(user_id: int, user_height: int):
    update_query = users.update().where(users.columns.user_id == user_id).values(user_height=user_height)
    cur = connection.execute(update_query)
    connection.commit()

    return "User height has been added"


@app.get("/add_age/{user_id}/{user_age}")
def user_age_into_db(user_id: int,user_age: int):
    update_query = users.update().where(users.columns.user_id == user_id).values(user_age=user_age)
    cur = connection.execute(update_query)
    connection.commit()
    return "User age has been added"


@app.get("/add_city/{user_id}/{user_city}")
def user_city_into_db(user_id: int,user_city: str):
    update_query = users.update().where(users.columns.user_id == user_id).values(user_city=user_city)
    cur = connection.execute(update_query)
    connection.commit()
    return "User city has been added"
"""""
def get_users(session):
    return session.query(users).order_by("user_id").all()

def output_useres(useres):
    useres_tree = Tree()
    useres_tree.create_node("Users", "users")
    for useres in useres:
        useres_id = f"{users.columns.user_id} {users.columns.user_name}{users.columns.user_surname}{users.columns.user_age}{users.columns.user_height}{users.columns.user_city}"
        useres_tree.create_node(useres_id, useres_id, parent="users")
        for user_name in users.columns.user_name:
            name_id = f"{useres_id}:{user_name}"
            useres_tree.create_node(users.columns.user_id, name_id, parent=useres_id)
            for surname in users.columns.user_surname:
                useres_tree.create_node(users.columns.user_surname, parent=name_id) 
    useres_tree.show()
"""""

@app.get("/")
def user_output():
    """""
    Users = get_users(session)
    output_useres(Users)
    """""

    # results = session.query(users.columns).all()
    # return   results

    select_all_query = sqlalchemy.select(sqlalchemy.Column(users))
    select_all_results = connection.execute(select_all_query)
    connection.commit()
    return(select_all_results)


    #
    #
    # select_all_query = sqlalchemy.select([users])
    # select_all_results = connection.execute(select_all_query)
    # connection.commit()
    # return(select_all_results)


if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)