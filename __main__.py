"""
    Welcome to hospital management software
    install modules by pip
    pip install termcolor colorama questionary prettytable pyfiglet
    and python mysql connector
"""

# IMPORTING MODULES
import questionary as cli
import backend
import functions as Fun
from colorama import init
from termcolor import colored
from variables import Var
init()
# SYSTEM CONTROL VARIABLE
system = {
    "authentication": True,
    "run": True,
    "mode_selector": None,
    "database": None,
    "writing_table": False,
    "status": ["user", "AUTH"],
    "OC": colored("Operation cancelled by user", "yellow", attrs=["bold"]),
    "UOCA": colored(
        "Unsupported Operation Cancel Attempt\n"
        "This may lead to critical error", "red", attrs=["bold"]
    ),
    "style": cli.Style([
        ('qmark', 'fg:#ffff00 bold'),        # token in front of the question
        ('question', 'bold'),                # question text
        ('answer', 'fg:#f44336 bold'),       # submitted answer text behind the question
        ('pointer', 'fg:#673ab7 bold'),      # pointer used in select and checkbox prompts
        ('highlighted', 'fg:#673ab7 bold'),  # pointed-at choice in select and checkbox prompts
        ('selected', 'fg:#cc5454'),          # style for a selected item of a checkbox
        ('separator', 'fg:#cc5454'),         # separator in lists
        ('instruction', ''),                 # user instructions for select, rawselect, checkbox
        ('text', ''),                        # plain text
        ('disabled', 'fg:#858585 italic')    # disabled choices for select and checkbox prompts
    ])
}
Dsystem = system.copy()  # Copy of system dictionary


# CLASSES
# start local functions class   [[
class LocalFunction:
    """ class Lfun : Local Functions """

    # start miscellaneous functions (
    def Terminate(self):
        """ Function to disconnect and close the application"""
        Dbms.disconnect()
        system["run"] = False

    def Logout(self):
        global system
        system = Dsystem.copy()
        system["status"] = ["user", "AUTH"]
        Dbms.disconnect()
        Dbms.__init__()

    def Entry(self, data, dtype=None):
        """ function to enter values
            for dtype:[None, N/A, sex] data: question statement
            for dtype:[eval] data: list[question statement, pre entered value]"""

        if dtype is None:
            value = cli.text(
                data, qmark=Fun.Qmark(None, "N"), style=system["style"]
            ).ask(kbi_msg=system["UOCA"])
            if value == "":
                value = None
            return value

        if dtype == "auto_date":
            value = cli.text(
                data, default=str(Fun.Date()), qmark=Fun.Qmark(None, "N"), style=system["style"]
            ).ask(kbi_msg=system["UOCA"])
            return value

        if dtype == "N/A":
            value = cli.text(
                data, default="N/A", qmark=Fun.Qmark(None, "N"), style=system["style"]
            ).ask(kbi_msg=system["UOCA"])
            if value == "N/A":
                return None
            else:
                return value

        if dtype == "sex":
            value = cli.select(
                data, choices=["Male", "Female"], qmark=Fun.Qmark(None, "N"), style=system["style"]
            ).ask(kbi_msg=system["UOCA"])
            return value

        if dtype == "update":
            question, pvalue = data
            if pvalue is None:
                nvalue = cli.text(
                    question, default="N/A", qmark=Fun.Qmark(None, "N"), style=system["style"]
                ).ask(kbi_msg=system["UOCA"])
                return nvalue
            else:
                nvalue = cli.text(
                    question, default=str(pvalue), qmark=Fun.Qmark(None, "N"), style=system["style"]
                ).ask(kbi_msg=system["UOCA"])
                return nvalue

    def SelTable(self):
        """ function to fetch and print table"""
        Dbms.table = None
        Dbms.table = cli.select(
            "Please select a table: ", choices=Var.tables,
            qmark=Fun.Qmark(system["status"], "C"), style=system["style"]
        ).ask(kbi_msg="Cancelling Operation")

    #   ) end miscellaneous functions

    # start entry mode functions    (
    def Insert(self):
        """ function for inserting values of fields in a table"""
        questions = getattr(
            Var, "Q{}".format(Dbms.table)
        )
        rdata = {}
        for a in questions.items():
            rdata[a[0]] = Lfun.Entry(a[1][0], a[1][1])
        integrity, data, error = Fun.Check(rdata)
        if integrity is True:
            data["Date_N_Time"] = "{} || {}".format(Fun.Date(), Fun.Time())
            print()
            for a in data.items():
                Fun.Qprint(a[0], a[1])

            if cli.confirm(
                    "Do you want to enroll Data into table {}".format(Dbms.table),
                    default=True, style=system["style"], qmark=Fun.Qmark(system["status"], "C")
            ).ask(kbi_msg="Cancelling Operation") is True:
                Dbms.insert_data(data)
            else:
                Fun.Sprint("Operation Cancelled by user", space_less=True)
        else:
            Fun.Wprint(error)

        if cli.confirm(
                "Would you like to continue adding data ?", default=True,
                qmark=Fun.Qmark(system["status"], "C"), style=system["style"]
        ).ask(kbi_msg="Cancelling Operation") is True:
            Fun.Sprint("Continue Entering Data for Table {}". format(Dbms.table))
            Lfun.Insert()
        else:
            Dbms.table = None
            Fun.Sprint("Done Entering Data for Table {}".format(Dbms.table), space_less=True)

    #   ) end entry mode functions

    # start read/update mode functions  (
    def Dtable(self):
        """ function to fetch and print table"""
        Lfun.SelTable()
        if Dbms.table is not None:
            Dbms.disp_table()
        else:
            Fun.Sprint("Operation Cancelled by User", space_less=True)

    def Utable(self):
        """ function to update table"""
        Lfun.SelTable()
        if Dbms.table is not None:
            try:
                number = int(cli.text(
                    "Please enter the row ID:", qmark=Fun.Qmark(None, "N"), style=system["style"]
                ).ask(kbi_msg=system["UOCA"]))
            except:
                number = 0
            if number != 0:
                old_data, keys = Dbms.old(number)
                new_data = {}
                if old_data is not None:
                    for a in old_data.items():
                        new_data[a[0]] = Lfun.Entry(
                            ["Please Enter New value for: {}".format(a[0]), a[1]], "update"
                        )
                    integrity, data, error = Fun.Check(new_data)

                    if integrity is True:
                        data["Date_N_Time"] = "{} || {}".format(Fun.Date(), Fun.Time())
                        print()
                        for s in keys:
                            Fun.UQprint(s, [old_data[s], data[s]])
                        if cli.confirm(
                            "Would you like to proceed updating data", qmark=Fun.Qmark(system["status"], "C"),
                                style=system["style"]
                        ).ask(kbi_msg="Cancelling Operation") is True:
                            Dbms.update_table(number, data)

                        else:
                            Fun.Sprint("Operation Cancelled by User", space_less=True)

                    else:
                        Fun.Wprint(error)
            else:
                Fun.Wprint("Entered ID Is 0 Or Not An Integer")
        else:
            Fun.Sprint("Operation Cancelled by User", space_less=True)

    def Stable(self):
        """ function to display information sorted"""
        Lfun.SelTable()
        if Dbms.table is not None:
            keys = (
                getattr(Var, "Q{}".format(Dbms.table))
            ).keys()

            field = cli.select(
                "Please select a field to search for:", style=system["style"],
                choices=keys, qmark=Fun.Qmark(system["status"], "C")
            ).ask(kbi_msg=system["OC"])

            if field is not None:
                value = cli.text(
                    "Enter a valid value for {}:".format(field), qmark=Fun.Qmark(None, "C"), style=system["style"]
                ).ask(kbi_msg=system["OC"])

                if value is not None:
                    integrity, data, error = Fun.Check({field: value})

                    if integrity is True:
                        Fun.Cprint(
                            "Searching for field {}".format(field), system["status"]
                        )
                        Dbms.disp_sorted(field=field, value=data)

                    else:
                        Fun.Wprint(error)
        else:
            Fun.Sprint("Operation Cancelled by User", space_less=True)

    def Drow(self):
        """ function to delete a row from table"""
        Lfun.SelTable()
        if Dbms.table is not None:
            try:
                number = int(cli.text(
                    "Enter the ID of row to be deleted", qmark=Fun.Qmark(None, "N"), style=system["style"]
                ).ask(kbi_msg=system["UOCA"]))
            except:
                number = 0

            if number != 0:
                Dbms.delete_row(number)
            else:
                Fun.Wprint("Entered ID is either 0 or not integer")
        else:
            Fun.Sprint("Operation Cancelled by User")

    #   ) end read/update mode functions

    # start administration mode functions    (
    def Ctable(self):
        """ function to clear a table"""
        Lfun.SelTable()
        if Dbms.table is not None:
            if cli.confirm(
                "Are you sure to proceed clearing table", style=system["style"], qmark=Fun.Qmark(None, "C")
            ).ask(kbi_msg="Cancelling Operation") is True:
                Dbms.clear_table()

            else:
                Fun.Sprint("Operation Cancelled by user", space_less=True)
        else:
            Fun.Sprint("Operation Cancelled by User", space_less=True)

    def Cdatabase(self):
        """ function to create a new database"""
        name = cli.text(
            "Please Enter New Database name [white space, numbers, special character not allowed]:",
            qmark=Fun.Qmark(None, "N"), style=system["style"]
        ).ask(kbi_msg=system["OC"])

        if name is not None:
            
            if cli.confirm(
                "Are you sure to proceed creating database",
                qmark=Fun.Qmark(system["status"], "C"), style=system["style"]
            ).ask(kbi_msg="Cancelling Operation") is True:
                Dbms.create_database(name)

            else:
                Fun.Sprint("Operation Cancelled by user", space_less=True)

    def Ddatabse(self):
        """ function to drop a database"""
        name = cli.select(
            "Please select the database to drop:",
            choices=Dbms.databases, qmark=Fun.Qmark(None, "C"), style=system["style"]
        ).ask(kbi_msg=system["OC"])

        if name is not None:

            if cli.confirm(
                "Are you sure to proceed deleting database",
                qmark=Fun.Qmark(system["status"], "C"), style=system["style"]
            ).ask(kbi_msg="Cancelling Operation") is True:
                if system["database"] == name:
                    system["database"] = None
                Dbms.drop_database(name)

            else:
                Fun.Sprint("Operation Cancelled by user", space_less=True)

    #   ) end administration mode functions
#   ]] end local Function class


# start class Modes ((
class Modes:
    """ This class consists of parts of main application programs. """
    def Authentication(self=None):

        # start sql authentication  {{
        while system["status"][1] == "AUTH":
            # start acquiring credentials and connecting  {
            Dbms.sql_username = cli.text(
                "Please enter your username: ",
                qmark=Fun.Qmark(None, "N"), style=system["style"]
            ).ask(kbi_msg=system["OC"])
            Dbms.status[0] = system["status"][0] = Dbms.sql_username
            
            Dbms.sql_password = cli.password(
                "Please enter your Password: ",
                qmark=Fun.Qmark(None, "N"), style=system["style"]
            ).ask(kbi_msg=system["UOCA"])

            Dbms.host = cli.text(
                "Please enter your host: ",
                qmark=Fun.Qmark(None, "N"), default="localhost", style=system["style"]
            ).ask(kbi_msg=system["UOCA"])

            Dbms.connect()
            #   } done acquiring credentials and connected

            # setting parameters and handling login error   {
            if Dbms.connected is True:  # connection successfully established
                system["authentication"] = False
                Dbms.status[1] = system["status"][1] = "HOME"

            else:  # connection not established

                if cli.confirm(
                    "Would you like to try again", qmark=Fun.Qmark(None, "C"), style=system["style"]
                ).ask(kbi_msg="Cancelling Operation") is True:
                    Fun.Sprint("Reattempting Authentication")
                    continue

                else:
                    Fun.Sprint("Terminating Application", space_less=True)
                    system["run"] = False
                    break
            #   } done setting parameter and handling login error
        #   }} end sql authentication

    def Home(self=None):
        # start sql home    {{
        while system["status"][1] == "HOME" and Dbms.connected is True:
            Fun.Cprint(
                "Database in use is: " + str(system["database"]), system["status"]
            )
            Fun.Cprint(
                "Please Choose Appropriate Command:", system["status"]
            )
            # start mode selection  {
            system["mode_selector"] = cli.select(
                "All the available Modes are",
                choices=Var.modes, qmark=Fun.Qmark(system["status"], "N"), style=system["style"]
            ).ask(kbi_msg=system["UOCA"])
            #   } end mode selection

            # start mode change {
            Dbms.list_databases()

            if system["mode_selector"] is not None:
                if system["mode_selector"] == "Select Database":
                    Fun.Sprint("Running Operation Select Database")
                    Fun.Cprint(
                        "Please Choose From Available Databases", system["status"]
                    )
                    name = cli.select(
                        "Please select a database to use:", qmark=Fun.Qmark(None, "C"),
                        choices=Dbms.databases, style=system["style"]
                    ).ask(kbi_msg=system["OC"])

                    if name is not None:
                        system["database"] = name
                        Dbms.use_database(system["database"])

                        # start creating tables {
                        Dbms.list_tables()
                        for a in Var.tables:
                            if a.lower() not in Dbms.tables:
                                Dbms.table = a
                                Dbms.create_table()
                                Fun.Cprint(
                                    "created Table:" + a, system["status"]
                                )
                            else:
                                Fun.Cprint("Table {} already exist, skipping generation". format(a), system["status"])
                        #   } end creating tables
                        Fun.Sprint("Successfully Ran Operation Select Database")
                        continue

                elif system["mode_selector"] == "Data Entry" and system["database"] is not None:
                    Dbms.status[1] = system["status"][1] = "ENTRY"
                    continue

                elif system["mode_selector"] == "Data Read/Update" and system["database"] is not None:
                    Dbms.status[1] = system["status"][1] = "READ"
                    continue

                elif system["mode_selector"] == "Administration":
                    Dbms.status[1] = system["status"][1] = "ADMIN"
                    continue

                elif system["mode_selector"] == "Logout":
                    Lfun.Logout()
                    break

                elif system["mode_selector"] == "Exit":
                    Dbms.status[1] = system["status"][1] = "EXIT"
                    break

                else:
                    Fun.Sprint("Please Select A Database First")
            #   } end mode change
        #   }} end sql home

    def Entry(self=None):
        Fun.Cprint(
            "Database in use is: " + str(system["database"]), system["status"]
        )
        # start database entry mode {{
        while system["status"][1] == "ENTRY" and Dbms.connected is True:
            # start entering data   {
            system["writing_table"] = True

            while system["writing_table"] is True:
                Lfun.SelTable()

                if Dbms.table is not None:
                    Lfun.Insert()

                else:
                    Fun.Sprint("Operation Cancelled by User", space_less=True)
                    system["writing_table"] = False
                    Dbms.status[1] = system["status"][1] = "HOME"
                    continue

            #   } end entering data
        #   }} end database entry mode

    def Read(self=None):
        Fun.Cprint(
            "Database in use is: " + str(system["database"]), system["status"]
        )
        # start read mode {{
        while system["status"][1] == "READ" and Dbms.connected is True:

            operation = cli.select(
                "Please select the operation:", qmark=Fun.Qmark(system["status"], "C"), style=system["style"],
                choices=Var.read_functions
            ).ask(kbi_msg=system["OC"])

            if operation == "Display Entire Table":
                Fun.Sprint("Running Read/Update Operation Display Entire Table")
                Lfun.Dtable()

            if operation == "Sort and Display":
                Fun.Sprint("Running Read/Update Operation Sort and Display")
                Lfun.Stable()

            if operation == "Update Data":
                Fun.Sprint("Running Read/Update Operation Update Data")
                Lfun.Utable()

            if operation == "Delete Row":
                Fun.Sprint("Running Read/Update Operation Delete Row")
                Lfun.Drow()

            if operation is None:
                system["status"][1] = "HOME"
                continue
        #   }} end read mode

    def Admin(self=None):
        Fun.Cprint(
            "Database in use is: " + str(system["database"]), system["status"]
        )
        info = True  # Special Variable to Print table information only once everytime the mode runs
        # start administration mode {{
        while system["status"][1] == "ADMIN" and Dbms.connected is True:

            if system["database"] is not None and info is True:
                Fun.Cprint(
                    "All the available information about Tables is: ", system["status"]
                )
                Dbms.disp_table_info(Var.tables)
                info = False

            operation = cli.select(
                "Please select the operation:", qmark=Fun.Qmark(system["status"], "C"), style=system["style"],
                choices=Var.admin_functions
            ).ask(kbi_msg=system["OC"])

            if operation == "Create Database":
                Fun.Sprint("Running Administration Operation Create Database")
                Lfun.Cdatabase()

            if operation == "Drop Database":
                Fun.Sprint("Running Administration Operation Drop Database")
                Lfun.Ddatabse()

            if operation == "Clear Table":

                if system["database"] is not None:
                    Fun.Sprint("Running Administration Operation Clear Table")
                    Lfun.Ctable()

                else:
                    Fun.Cprint(
                        "Please Select a database first before this operation", system["status"]
                    )

            if operation is None:
                Dbms.status[1] = system["status"][1] = "HOME"
                continue

        #   }} end administration mode
#   )) end class Modes


# BEGIN APPLICATION {{{
if __name__ == "__main__":
    # PRE APPLICATION STATEMENT
    Fun.Greeter("Welcome Hospital Management")
    Fun.docs_printer(1)
    print()
    Dbms = backend.Backend()  # setting to Authentication mode
    Lfun = LocalFunction()
    cli.confirm(
        "press ENTER to continue", default=True, qmark=Fun.Qmark(None, "N"), style=system["style"]
    ).ask(kbi_msg=system["OC"])

    while system["run"] is True:
        
        if system["status"][1] == "AUTH":
            Fun.Cscreen()
            Fun.Greeter("Authenticate User")
            Fun.docs_printer(2)
            Fun.Sprint("Running Method Authentication")
            Modes.Authentication()

        if system["status"][1] == "HOME" and Dbms.connected is True:
            Fun.Cscreen()
            Fun.Greeter("User Home")
            Fun.docs_printer(3)
            Fun.Sprint("Running Method Home")
            Modes.Home()

        if system["status"][1] == "ENTRY" and Dbms.connected is True:
            Fun.Cscreen()
            Fun.Greeter("ENTRY MODE")
            Fun.docs_printer(4)
            Fun.Sprint("Running Method Entry")
            Modes.Entry()

        if system["status"][1] == "READ" and Dbms.connected is True:
            Fun.Cscreen()
            Fun.Greeter("RETRIEVAL MODE")
            Fun.docs_printer(5)
            Fun.Sprint("Running Method Read/Update")
            Modes.Read()

        if system["status"][1] == "ADMIN" and Dbms.connected is True:
            Fun.Cscreen()
            Fun.Greeter("ADMIN MODE")
            Fun.docs_printer(6)
            Fun.Sprint("Running Method Administration")
            Modes.Admin()

        if system["status"][1] == "EXIT" and Dbms.connected is True:
            Lfun.Terminate()

    Fun.Greeter("BYE")
#   }}} END APPLICATION
