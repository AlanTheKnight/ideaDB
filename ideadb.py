import pickle
import os
from prettytable import PrettyTable


class CreationError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    def __str__(self):
        if self.message:
            return "{}".format(self.message)
        else:
            return "CreationError has been raised."


class DataBase():
    def __init__(self, path: str, name: str):
        if not os.path.isdir(path):
            raise CreationError("Invalid database path.")
        self.path = os.path.join(path, name)
        self.name = name
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def tables(self):
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f)) and not f.startswith(".")]
    
    def __call__(self):
        t = PrettyTable()
        t.field_names = ["DataBase \"{}\"".format(self.name)]
        for i in self.tables():
            t.add_row([i])
        print(t)


class Table():
    """
    A table is a dictionary object connected to a DataBase db with name. 
    """
    def __init__(self, db, name: str):
        try:
            self.path = os.path.join(db.path, name)
            self._path = os.path.join(db.path, "." + name)
            self.dir = db.path
        except:
            raise ValueError("You must provide the DataBase class to create a table.")
        if not os.path.isfile(self.path) or not os.path.isfile(self._path):
            with open(self.path, "wb") as file:
                self.data = {}
                pickle.dump(self.data, file)
            with open(self._path, "wb") as file:
                self._data = {}
                pickle.dump(self._data, file)
        try:
            with open(self.path, "rb") as file:
                self.data = pickle.load(file)
            with open(self._path, "rb") as file:
                self._data = pickle.load(file)
        except:
            self.data = {}
            self._data = {}

    def save(self):
        """
        Save all changes made to a table.
        """
        with open(self.path, "wb") as file:
            pickle.dump(self.data, file)
        with open(self._path, "wb") as file:
            pickle.dump(self._data, file)
    
    def add_column(self, name: str, t=None):
        """Add a column to a table"""
        self._data[name] = t

    def add(self, **kwargs):
        """Add a row to a table."""
        key = len(self.data)
        self.data[key] = {}
        for i in self._data:
            if i not in kwargs:
                self.data[key][i] = None
            else:
                self.data[key][i] = kwargs[i]

    def __call__(self):
        t = PrettyTable()
        l = ["{}".format(x) for x in self._data]
        l.insert(0, "pk")
        t.field_names = l
        for i in self.data:
            l2 = [self.data[i][x] for x in l[1:]]
            l2.insert(0, i)
            t.add_row(l2)
        print(t)

    def get(self, **kwargs):
        """Get a row from table by given keyword arguments."""
        if 'pk' in kwargs:
            try:
                return Row(self._data, kwargs['pk'],  self.data[kwargs['pk']])
            except KeyError:
                return None
        else:
            for i in self.data:
                for x in kwargs:
                    try:
                        if self.data[i][x] == kwargs[x]:
                            return self.data[i]
                    except KeyError:
                        return None
            return None

    def filter(self, **kwargs):
        """Return a list of Row objects filtered by given keyword arguments."""
        out = []
        for i in self.data:
            for x in kwargs:
                try:
                    if x == "pk":
                        if i == kwargs["pk"]:
                            out.append(Row(self._data, i, self.data[i]))
                    else:
                        if self.data[i][x] == kwargs[x]:
                            out.append(Row(self._data, i, self.data[i]))
                except KeyError:
                    pass
        return out

    def all(self):
        """Return all rows of the table implemented in Row object."""
        out = []
        for i in self.data:
            out.append(Row(self._data, i, self.data[i]))
        return out

    def remove(self, pk):
        """Removes a row in table by it's primary key."""
        self.data.pop(pk, None)

    def remove_column(self, name):
        """Remove column from a table by it's"""
        for i in self.data:
            self.data[i].pop(name, None)
        self._data.pop(name, None)

    def delete(self):
        """Delete a table from the database."""
        os.remove(self.path)
        os.remove(self._path)

    def filter_func(self, function):
        """
        Return a list of Row objects filtered by given function,
        which needs to return either True or False. The function also
        needs to take 2 positional parameters:
        - Pk of a row
        - Dictionary containing data of a row
        """
        out = []
        for i in self.data:
            if function(i, self.data[i]):
                out.append(Row(self._data, i, self.data[i]))
        return out
        


class Row():
    def __init__(self, h_data, id, data):
        self._data = h_data
        self.id = id
        self.data = data
    def __getattr__(self, attr):
        if attr in self._data:
            return self.data[attr]
        elif attr == "pk":
            return self.id
    def __repr__(self):
        return "Row with pk={}".format(self.id)


if __name__ == '__main__':
    db = DataBase('/home/pashs/PycharmProjects/ideaDB/ideaDB', 'db')
    a = Table(db, 'users')
    a.add_column('email')
    a.add_column('name')
    a.add(email='pashs@gmail.com', name='Паша')
    a.add(email='test@test.com', name='Test')
    print(a.all())