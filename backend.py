from __future__ import print_function
import mysql.connector as mysql
import questionary as cli
from prettytable import from_db_cursor
import functions as Fun
from variables import Queries, Var


class Backend(object):
    """ Class Functions is a mysql object for communicating with mysql server and executing user commands"""
    def __init__(self):
        """ initializing the object """
        self.sql_username = None
        self.sql_password = None
        self.host = "localhost"
        self.connection = None
        self.Ncursor = None
        self.databases = None
        self.connected = False
        self.tables = None
        self.table = None
        self.status = ["user", "AUTH"]

    #   //* Start Connection /Disconnection Functions
    def connect(self):
        """ Function connect trying to authenticate to user """
        Fun.Cprint(
            "Attempting to connect", self.status
        )
        try:
            self.connection = mysql.connect(
                host=self.host, user=self.sql_username, password=self.sql_password
            )
            self.Ncursor = self.connection.cursor()
            self.connected = True
            Fun.Sprint("Successfully Connected to user {}".format(self.sql_username))

        except mysql.Error as error:
            Fun.Wprint(
                "Authentication Failed:"
            )
            Fun.Wprint(error)

    def disconnect(self):
        """ Function disconnect signing out user """
        try:
            self.Ncursor.close()
            self.connection.close()
            self.connected = False
            Fun.Sprint(
                "Successfully Disconnected user {}".format(self.sql_username)
            )
        except mysql.Error as error:
            Fun.Wprint("Disconnection Failed for user {}".format(self.sql_username))
            Fun.Wprint(error)
    #   *\\ End Connection/Disconnection Functions

    #   //* Start Listing and Display Functions
    def row_check(self, number):
        """ function to check if a row exists"""
        try:
            self.Ncursor.execute("select ID from {} where ID = {}".format(self.table, number))
            row = self.Ncursor.fetchall()
            if len(row) == 1:
                if row[0][0] == number:
                    return True
                else:
                    return False
            else:
                return False
        except mysql.Error as error:
            Fun.Wprint("Cannot Check If ID = {} Exists".format(number))
            Fun.Wprint(error)
            return None

    def list_databases(self):
        """ Function list_databases to list all the available databases present in user account """
        try:
            self.Ncursor.execute("show databases")
            x = self.Ncursor.fetchall()
            y = []
            for a in x:
                y.append(a[0])
            self.databases = y

        except mysql.Error as error:
            Fun.Wprint("Database Listing Failed:")
            Fun.Wprint(error)

    def list_tables(self):
        """ Function to return list of all available tables """
        try:
            self.Ncursor.execute("show tables")
            x = self.Ncursor.fetchall()
            y = []
            for a in x:
                y.append(a[0].lower())
            self.tables = y
        except mysql.Error as error:
            Fun.Wprint("Table Listing Failed:")
            Fun.Wprint(error)

    def disp_table(self):
        """ Function to display the table whose name is entered"""
        try:
            self.Ncursor.execute("select * from {}".format(self.table))
            y = from_db_cursor(self.Ncursor)
            Fun.Tprint(
                y.get_string()
            )
            Fun.Sprint("Successfully Printed Table {}".format(self.table))
        except mysql.Error as error:
            Fun.Wprint("Table Display Failed for Table {}".format(self.table))
            Fun.Wprint(error)

    def disp_sorted(self, field, value):
        """ function to sort and display table"""
        command = "select * from {} where {} = %({})s".format(self.table, field, field)
        try:
            self.Ncursor.execute(command, value)
            y = from_db_cursor(self.Ncursor)
            Fun.Tprint(
                y.get_string()
            )
            Fun.Sprint("Successfully Printed Sorted Table {}".format(self.table))
        except mysql.Error as error:
            Fun.Wprint("Sorting Failed for Table {}".format(self.table))
            Fun.Wprint(error)

    def disp_table_info(self, tables):
        """ function to display information about tables"""
        for a in tables:
            try:
                self.Ncursor.execute('describe {}'.format(a))
                y = from_db_cursor(self.Ncursor)
                Fun.Sprint("Complete Information about Table: {}".format(a))
                Fun.Tprint(
                    y.get_string()
                )

            except mysql.Error as error:
                Fun.Wprint("Table Display Failed for Table {}".format(self.table))
                Fun.Wprint(error)

    def old(self, number):
        """ function to return dictionary of one row"""
        keys = (
            getattr(Var, "Q{}".format(self.table))
        ).keys()
        row_check = self.row_check(number)
        if row_check is True:
            data = {}
            try:
                for a in keys:
                    self.Ncursor.execute("select {} from {} where ID = {}".format(a, self.table, number))
                    data[a] = (self.Ncursor.fetchone())[0]
                return data, keys
            except mysql.Error as error:
                Fun.Wprint("Read Current Data in Table {} where ID is {} Failed".format(self.table, number))
                Fun.Wprint(error)
                return None, keys
        elif row_check is False:
            Fun.Wprint("Entered ID = {} Does Not Exist".format(number))
            return None, keys

        else:
            Fun.Wprint("I don't know if ID = {} exists or not sorry".format(number))
            return None, keys
    #   *\\ End Listing and Display Functions

    #   //* Start Data Manipulation Functions
    def delete_row(self, number):
        """ function to delete a row"""
        command = "delete from {} where ID = {}".format(self.table, number)
        row_check = self.row_check(number)
        if row_check is True:
            try:
                self.Ncursor.execute(command)
                self.connection.commit()
                Fun.Sprint("Operation Successfully Completed")
            except mysql.Error as error:
                Fun.Wprint("Row deletion failed for Table {} where ID is {}".format(self.table, number))
                Fun.Wprint(error)
        elif row_check is False:
            Fun.Wprint("Entered ID = {} Does Not Exist".format(number))
        else:
            Fun.Wprint("I don't know if ID = {} exists or not sorry".format(number))

    def use_database(self, name):
        """ Function use_database to change to user selected database """
        try:
            self.Ncursor.execute("use {}".format(name))
            Fun.Sprint("database successfully changes to {}".format(name))
        except mysql.Error as error:
            Fun.Wprint("Database Change Failed")
            Fun.Wprint(error)

    def insert_data(self, data):
        """ Function insert_data to insert data into table """
        command = getattr(
            Queries, "E{}".format(str(self.table))
        )
        try:
            self.Ncursor.execute(command, data)
            self.connection.commit()
            Fun.Sprint("Data Successfully Entered into Table {}".format(self.table))

        except mysql.Error as error:
            Fun.Wprint("Data Entry Failed for Table {}".format(self.table))
            Fun.Wprint(error)

    def update_table(self, number, value):
        """ function to update table"""
        command = (
            getattr(Queries, "U{}".format(str(self.table)))
        ).format(number)
        try:
            self.Ncursor.execute(command, value)
            self.connection.commit()
            Fun.Sprint("Data Successfully Updated into Table {} where ID is {}".format(self.table, number))
        except mysql.Error as error:
            Fun.Wprint("Data Update Failed for Table {} where ID is {}".format(self.table, number))
            Fun.Wprint(error)

    #   *\\ End Data Manipulation Functions

    #   //* Start Creation/Deletion Functions
    def create_database(self, name):
        """ function to create table"""
        try:
            self.Ncursor.execute("create database {}".format(name))
            self.connection.commit()
            Fun.Sprint("Successfully Created Database {}".format(name))
        except mysql.Error as error:
            Fun.Wprint("Database Creation Failed")
            Fun.Wprint(error)

    def clear_table(self):
        """ function to clear table"""
        if cli.password(
                "Please Enter the password to continue: ", qmark="AUTHENTICATION:"
        ).ask() == self.sql_password:
            try:
                self.Ncursor.execute("delete from {}".format(self.table))
                self.connection.commit()
                Fun.Sprint("Successfully Cleared Data for Table {}".format(self.table))
            except mysql.Error as error:
                Fun.Wprint("Data Deletion Failed")
                Fun.Wprint(error)

    def create_table(self):
        """ Function to create_table """
        command = getattr(
            Queries, "C{}".format(self.table)
        )
        try:
            self.Ncursor.execute(command)
            self.connection.commit()
        except mysql.Error as error:
            Fun.Wprint("Table Creation Failed")
            Fun.Wprint(error)

    def drop_database(self, name):
        """ Function to delete a database """
        Fun.Cprint(
            "password required for user: {}".format(self.sql_username), self.status
        )
        if cli.password(
            "Please Enter the password to continue: ", qmark="AUTHENTICATION:"
        ).ask() == self.sql_password:
            try:
                self.Ncursor.execute("drop database {}".format(str(name)))
                self.connection.commit()
                Fun.Sprint("Successfully Dropped Database {}".format(name))
            except mysql.Error as error:
                Fun.Wprint("Database Deletion Failed:")
                Fun.Wprint(error)

    #   *// End Creation/Deletion Functions
