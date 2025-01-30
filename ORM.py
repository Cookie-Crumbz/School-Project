from typing import Type, List, Tuple, Any
from abc import ABC

class AbstractRecord(ABC):
    def __init__(self, **kwargs):
        """
        Initialize the record with attributes representing each column.

        Parameters:
        - kwargs (Dict[str, Any]): A dictionary of column-value pairs.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


    @classmethod
    def get_primary_key(cls):
        """
        Get the name of the primary key attribute. This is assumed to be the first attribute of the class.

        Returns:
        - str: The name of the primary key attribute.
        """
        if hasattr(cls, '__annotations__'):
            return list(cls.__annotations__.keys())[0]
        else:
            raise AttributeError("Class has no attributes defined with type annotations.")
   


class RecordHandler:
    def __init__(self, sql_helper):
        self.sql_helper = sql_helper

    def save_record(self, record: AbstractRecord) -> int:
        """
        Save the record to the database.

        Parameters:
        - record (AbstractRecord): An instance of AbstractRecord or its subclass.

        Returns:
        - int: Error or success code.
        """
        table_name = record.__class__.__name__
        columns = record.__dict__
        
        print(table_name, columns)
        return self.sql_helper.insert_data(table_name, columns)

    def fetch_records(self, record_cls: Type[AbstractRecord], value: Any, column: str = None) -> Tuple[List[AbstractRecord], int]:
        """
        Fetch all records from the database based on a specified column and value.

        Parameters:
        - record_cls (Type[AbstractRecord]): The type of the record class (subclass of AbstractRecord).
        - value (Any): The value to search for.
        - column (str, optional): The column to search by. If not specified, the primary key is used.

        Returns:
        - Tuple[List[AbstractRecord], int]: A tuple containing a list of instances of the record class fetched from the database and an error code.
        """
        table_name = record_cls.__name__  # Get table name from class name
        if column is None:
            column = record_cls.get_primary_key()
        query = f"SELECT * FROM {table_name} WHERE {column} = %s"
        params = (value,)
        results, error_code = self.sql_helper.fetch_all(query, params)
        records = [record_cls(**result) for result in results] if results else []
        return records, error_code

    def fetch_all_records(self, record_cls: Type[AbstractRecord]) -> Tuple[List[AbstractRecord], int]:
        """
        Fetch all records from the database.

        Parameters:
        - record_cls (Type[AbstractRecord]): The type of the record class (subclass of AbstractRecord).

        Returns:
        - Tuple[List[AbstractRecord], int]: A tuple containing a list of instances of the record class fetched from the database and an error code.
        """
        table_name = record_cls.__name__
        query = f"SELECT * FROM {table_name}"
        results, error_code = self.sql_helper.fetch_all(query)
        records = [record_cls(**result) for result in results] if results else []
        return records, error_code

    def update_record(self, record: AbstractRecord) -> int:
        """
        Update the record in the database.

        Parameters:
        - record (AbstractRecord): An instance of AbstractRecord or its subclass.

        Returns:
        - int: Error or success code.
        """
        table_name = record.__class__.__name__  # Get table name from class name
        columns = record.__dict__  # Get columns from instance attributes
        return self.sql_helper.update_data(table_name, columns)

    def delete_record(self, record: AbstractRecord) -> int:
        """
        Delete the record from the database.

        Parameters:
        - record (AbstractRecord): An instance of AbstractRecord or its subclass.

        Returns:
        - int: Error or success code.
        """
        table_name = record.__class__.__name__  # Get table name from class name
        primary_key = record.__class__.get_primary_key()
        pk_value = getattr(record, primary_key)
        condition = f"{primary_key} = {pk_value}"
        return self.sql_helper.delete_data(table_name, condition)