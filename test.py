import ideadb

db = ideadb.DataBase("/home/alantheknight/Repositories/ideaDB/", "db")

t = ideadb.Table(db, "users1")
t2 = ideadb.Table(db, "users2")
t.clear()
t2.clear()
t.add_column("name")
t.add_column("age")
t.add_column("sex")
t2.add_column("name")
t2.add_column("age")
t2.add_column("sex")

t.add(name="Max", age=14, sex="M")
t.add(name="Alex", age=15, sex="M")
t.add(name="Alan", age=16, sex="M")
t2.add(name="Max", age=14, sex="M")
t2.add(name="Alex", age=15, sex="F")
t2.add(name="Alan", age=17, sex="M")
t2.add(name="Alec", age=18, sex="M")
t.save()
t2.save()

t()
t2()

t.join(t2, columns=['pk'])
t()