import sqlparse
import re

sql_scripts = """
CREATE TABLE Customers (
    CustomerID int PRIMARY KEY,
    CustomerName nvarchar(255) UNIQUE,
    ContactName nvarchar(255) UNIQUE,
    Country nvarchar(255),
    City nvarchar(255),
    PostalCode nvarchar(255)
);
CREATE TABLE Orders (
    OrderID int PRIMARY KEY,
    CustomerID int,
    OrderDate date,
    UNIQUE (CustomerID)
);
CREATE TABLE Orders2 (
    OrderID int PRIMARY KEY,
    CustomerID int,
    OrderDate date,
    test int UNIQUE,
    UNIQUE (CustomerID, OrderDate)
);
CREATE TABLE Orders3 (
    OrderID int,
    productID int,
    OrderDate date,
    PRIMARY KEY (OrderID, productID)
);
CREATE TABLE Orders4 (
    OrderID int,
    productID int,
    OrderDate date UNIQUE,
    PRIMARY KEY (OrderID, productID)
);
CREATE TABLE Orders5 (
    OrderID int,
    productID int,
    PRIMARY KEY (OrderID, productID)
);
CREATE TABLE Orders6 (
    OrderID int PRIMARY KEY,
    productID int FOREIGN KEY REFERENCES Orders5(productID),
    PlaceID int FOREIGN KEY REFERENCES Places(PlaceID)
)
"""

parsed = sqlparse.parse(sql_scripts)

tables = {}
for statement in parsed:
    if statement.get_type() == 'CREATE':
        table_name = None
        column_names = []
        primary_keys = []
        unique_keys = []
        foreign_keys = []

        for token in statement.tokens:
            # Getting table name
            if token.ttype is None and isinstance(token, sqlparse.sql.Identifier):
                table_name = token.get_real_name()

            # Getting column names, primary keys, unique keys
            elif token.ttype is None and isinstance(token, sqlparse.sql.Parenthesis):
                columns = token.value.replace('(', '').replace(')', '').replace(',', '').split('\n')
                while '' in columns:
                    columns.remove('')
                for col in columns:
                    col_parts = col.strip().split()
                    column_name = col_parts[0]

                    # Exclude UNIQUE keyword from columns list
                    if column_name.upper() != 'UNIQUE' and column_name.upper() != 'PRIMARY' and column_name.upper() != 'FOREIGN':
                        column_names.append(column_name)
                    
                    if 'FOREIGN' in col_parts:
                        if column_name.upper() != 'FOREIGN':
                            foreign_keys.append(column_name)
                        else:
                            combination = []
                            print(len(col_parts))
                            if len(col_parts) > 3:
                                for i in range(2, len(col_parts)):
                                    combination.append(col_parts[i])
                                foreign_keys.append(combination)
                            else:
                                foreign_keys.append(col_parts[1])

                    if 'PRIMARY' in col_parts:
                        if column_name.upper() != 'PRIMARY':
                            primary_keys.append(column_name)
                        else:
                            combination = []
                            print(len(col_parts))
                            if len(col_parts) > 3:
                                for i in range(2, len(col_parts)):
                                    combination.append(col_parts[i])
                                primary_keys.append(combination)
                            else:
                                primary_keys.append(col_parts[1])
                    if 'UNIQUE' in col_parts:
                        if column_name.upper() != 'UNIQUE':
                            unique_keys.append(column_name)
                        else:
                            combination = []
                            print(len(col_parts))
                            if len(col_parts) > 2:
                                for i in range(1, len(col_parts)):
                                    combination.append(col_parts[i])
                                unique_keys.append(combination)
                            else:
                                unique_keys.append(col_parts[1])


        # Storing table information in dictionary
        if table_name:
            tables[table_name] = {
                "columns": column_names,
                "primary keys": primary_keys,
                "unique keys": unique_keys,
                "foreign keys": foreign_keys
            }

print(tables)
