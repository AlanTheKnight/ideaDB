# IdeaDB

## Usage

Install needed library:

    python -m pip install prettytable

Copy ideadb.py to your project and import it as a module.

    import ideadb
    
## API

### Creating a new database

    db = DataBase(r"C:\users\ideasoft\Desktop\myproject\", "db")

First argument is a string containing the absolute path to the database.
Second argument is a name of the database.
    
### Creating a new table

    t = Table(db, "users")

First argument is a DataBase object.
Second argument is a name of a table.

### Adding a column to a table

    t.add_column("name")
    t.add_column("email")
    t.add_column("age")
    
The only argument is a column's name.
    
### Adding a row to a table

    t.add(0, name="Max", email="max@gmail.com", age=14)
    t.add(1, name="Alex", email="alex@gmail.com", age=15)
    t.add(2, name="Alan", email="alan@gmail.com", age=16)

First argument is a primary key - main id of a row.
I recommend to provide an integer primary key.

### Getting data out of table

1. Print it out

        t()
        
   Will give you something like that:
   
        +----+----------------+------+-----+
        | pk |     email      | name | age |
        +----+----------------+------+-----+
        | 0  | max@gmail.com  | Max  |  14 |
        | 1  | alex@gmail.com | Alex |  15 |
        | 2  | alan@gmail.com | Alan |  16 |
        +----+----------------+------+-----+
        
2. Get as a list

        a = t.all()
        for i in a:
            print(a.name)
            
3. Get elements by some keywords

        t.get(pk=0) # Row with id=0
        t.get(name="Alex", age=15) # Row with id=1
        t.get(name="Max", age=0) # None
        
4. Filter elements by some keywords
        
        t.add(0, name="Max", email="max@mail.com", age=15)
        for i in t.filter(age=15):
            print(i.name)
        # Max
        # Alex
        
5. Get elements as a dictionary
        
        print(t.data)
        # {0: {'email': 'max@gmail.com', 'name': 'Max', 'age': 15}, 1: {'email': 'alex@gmail.com', 'name': 'Alex', 'age': 15}, 2: {'email': 'alan@gmail.com', 'name': 'Alan', 'age': 16}}
        print(t.data[0]['name'])
        # Max
6. Use custom function to filter elements

        def myfunc(id, data):
            if data['name'].startswith("A"): return True
            return False
            
        for i in t.filter_func(myfunc):
            print(i.name)
        # Alex
        # Alan
        
    Or use lambda instead:

        for i in t.filter_func(lambda id, data: id < 2):
            print(i.id)
        # 0
        # 1
    
