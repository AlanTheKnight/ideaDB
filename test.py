import ideadb

db = ideadb.DataBase("/home/alantheknight/Repositories/ideaDB/", "db")

t = ideadb.Table(db, "users2")

for i in t:
    print(i)
t()