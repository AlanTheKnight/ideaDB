# IdeaDB

## Usage

Copy ideadb.py to your project and import it as a module.

    import ideadb
    
## API

### Creating a new database

    db = DataBase(r"C:\users\ideasoft\Desktop\myproject\", "db")
    # DataBase(<Path to DB>, <DB name>)
    
### Creating a new table

    t = Table(db, "users")
    # Table(<DB>, <Table name>)
    
