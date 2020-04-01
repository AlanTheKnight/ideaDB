import ideadb

db = ideadb.DataBase("/home/alantheknight/Repositories/ideaDB/", "db")

t = ideadb.Table(db, "users")
t.clear()
t.add_column("age")
t.add_column("name")

t.add(name="Max", age=14)
t.add(name="Alex", age=16)

t.save()



t()