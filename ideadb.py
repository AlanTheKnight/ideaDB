import pickle
import os
from shutil import rmtree
from prettytable import PrettyTable


class DataBaseError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    def __str__(self):
        if self.message:
            return "{}".format(self.message)
        else:
            return "DataBase error has been raised."


class DataBase():
    def __init__(self, path: str, name: str):
        if not os.path.isdir(path):
            raise DataBaseError("Invalid database path.")
        self.path = os.path.join(path, "." + name)
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

    def delete(self):
        rmtree(self.path)


class Table():
    """
    A table is a dictionary object connected to a DataBase db with name. 
    """
    def __init__(self, db: DataBase, name: str):
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
    
    def add_column(self, name: str, t=None, default=None):
        """Add a column to a table"""
        self._data[name] = {'type':t, 'default':default}
        for i in self.data:
            self.data[i][name] = default

    def add(self, **kwargs):
        """Add a row to a table."""

        if self.data.keys():
            key = max(list(self.data.keys())) + 1
        else:
            key = 0

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

    def clear(self):
        self.data = {}
        self._data = {}

    def get(self, **kwargs):
        """Get a row from table by given keyword arguments."""
        if 'pk' in kwargs:
            try:
                return Row(self, kwargs['pk'])
            except KeyError:
                return None
        else:
            for i in self.data:
                c = 0
                for x in kwargs:
                    try:
                        if self.data[i][x] == kwargs[x]:
                            c += 1
           
                    except KeyError:
                        return None
                if c == len(kwargs):
                    return Row(self, i)
                else:
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
                            out.append(Row(self, i))
                    else:
                        if self.data[i][x] == kwargs[x]:
                            out.append(Row(self, i))
                except KeyError:
                    pass
        return out

    def all(self):
        """Return all rows of the table implemented in Row object."""
        out = []
        for i in self.data:
            out.append(Row(self, i))
        return out

    def remove_row(self, pk):
        """Removes a row in table by it's primary key."""
        self.data.pop(pk, None)

    def __iter__(self):
        return iter(self.data)

    def remove_column(self, name):
        """Remove column from a table by it's"""
        if not name in self._data:
            return False
        for i in self.data:
            self.data[i].pop(name, None)
        self._data.pop(name, None)
        return True

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
                out.append(Row(self, i))
        return out

        def __len__(self):
            return len(self.data)

    def join(self, table, columns=[]):

        def dict_join(dict1: dict, dict2: dict):
            for i in dict2:
                if not i in dict1:
                    dict1[i] = dict2[i]
                else:
                    if dict1[i] is not None:
                        continue
                    else:
                        dict1[i] = dict2[i]
            return dict1

        ifpk = 'pk' in columns
        columns = list(set(self._data.keys()).intersection(set(table._data.keys())).intersection(set(columns)))
        if ifpk: columns.append("pk")
        for i in table._data:
                if i not in self._data:
                    self.add_column(i)
        if not columns:
            for i in table.data:
                self.add(**table.data[i])
        else:
            if ifpk:
                columns.pop(columns.index('pk'))
                if not columns:
                    for i in table.data:
                        if i not in self.data:
                            self.add(**table.data[i])
                        else:
                            self.data[i] = dict_join(self.data[i], table.data[i])
                else:
                    for i in table.data:
                        search = {}
                        for x in columns:
                            search[x] = table.data[i][x]
                        result = self.get(**search)
                        if i not in self.data or result is None:
                            self.add(**table.data[i])
                        else:
                            self.data[i] = dict_join(self.data[i], table.data[i])
            else:
                for x in table.data:
                    search = {}
                    for i in columns:
                        search[i] = table.data[x][i]
                    result = self.get(**search)
                    if result is None:
                        self.add(**table.data[x])
                    else:
                        i = result.pk
                        self.data[i] = dict_join(self.data[i], table.data[x])


class Row():
    def __init__(self, table, pk):
        self.table = table
        self.pk = pk
    
    def __getattr__(self, attr):
        if attr in self.table._data:
            return self.table.data[self.pk][attr]
    
    def __repr__(self):
        return "Row with pk={}".format(self.pk)

    def data(self):
        return self.table.data[self.pk]

    def change(self, **kwargs):
        for i in kwargs:
            if i in self.table._data:
                self.table.data[self.pk][i] = kwargs[i]
