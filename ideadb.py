import pickle
import os
import pathlib


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
        if not os.path.isdir(self.path):
            os.mkdir(self.path)


class Table():
    """
        A table is a dictionary object connected to a DataBase db with name. 
    """
    class Query():
        def __init__(self, data={}):
            self.data = data
        def __str__(self):
            return self.data
        def __len__(self):
            return len(self.data)

    def __init__(self, db, name: str):
        try:
            self.path = os.path.join(db.path, name)
            self.dir = db.path
        except:
            raise ValueError("You must provide the DataBase class to create a table.")
        if not os.path.isfile(self.path):
            with open(self.path, "wb") as file:
                self.data = {}
                pickle.dump(self.data, file)
        else:
            if os.path.getsize(self.path) > 0:
                with open(self.path, "rb") as file:
                    self.data = pickle.load(file)
            else:
                self.data = {}
    
    def _atomic(func):
        def wrapper(self, *args, **kwargs):
            self._synch()
            func(self, *args, **kwargs)
            self._synch()
        return wrapper

    def __str__(self):
        return self.path

    def _synch(self):
        with open(self.path, "wb") as file:
            pickle.dump(self.data, file)
    
    def get(self, key):
        """
        Gets value from table by it's key.
        """
        self._synch()
        if key in self.data:
            return self.data[key]
        else:
            return None

    @_atomic
    def load(self, key, value):
        """
        Loads key with value to a table.
        """
        self.data[str(key)] = value
        return key

    def __len__(self):
        self._synch()
        return len(self.data)

    def filter(self, expression, mode=True):
        """
        Returns data from table that matches the expression.
        Expression needs to be a function that returns either True or False.
        If mode is set to False, not matching results are included.
        """
        self._synch()
        out = {}
        for i in self.data.keys():
            if mode and expression(i):
                out[i] = self.data[i]
        return Query(out)

    def delete(self):
        """
        Deletes the table and terminates all data.
        """
        os.remove(self.path)

    def rename(self, name):
        """
        Renames the table file to new name.
        """
        os.rename(self.path, os.path.join(self.dir, name))
        self.path = os.path.join(self.dir, name)
        return self.path

    @_atomic
    def remove(self, key):
        """
        Removes a key from table.
        """
        return self.data.pop(key, None)

    def __call__(self):
        return self.path
