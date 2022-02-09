class Docs:

    Greeter = (
        "Welcome to MySQL backend hospital management application"
        "An attempt to simplify hospital database management while also retaining the the integrity of MySQL.\n"
        "The Application is simple fast,responsive and easy to learn and its also feature rich.\n"
        "It lacks a Graphical user interface but at the same time there are no commands to be entered by user.\n"
        "Every operation can be navigated simply by arrow keys and data entered by keyboard.\n"
        "No difficult learning commands of MySQL,but the application requires are pre created MySQL account to work."
    )

    Authentication = (
        "Welcome to Authentication Mode\n" 
        "Users are supposed to enter their MySQL username along with User password to Use the application.\n"
        "NOTE:Please avoid using root account as it contains MySQL required databases that must not be tampered with.\n"
        "Users may choose their own host but by default localhost is selected, if you don't know what you are doing\n"
        "then please leave it unchanged."

    )

    Home = (
        "Welcome to Home\n" 
        "User Home is the Door to every application functions use your arrow keys to navigate.\n"
        "There are three predefined tables which this application with create and manipulate namely:\n\n"
        "Workers --> This table hold the data about staff workers.\n"
        "Patients --> This table holds the data about patients.\n"
        "Dispensary --> This table holds data about Dispensary.\n"
        "There are a few available operations present in Home:\n\n"
        "Select Database --> Before any data manipulation a database has to be selected.\n"
        "Data Entry --> This method is used to enter data in the three tables defined above.\n"
        "Data Read/Update --> This method is used to read or update any existing data.\n"
        "Administration --> This method is used to clear Tables, create/delete Databases and etc\n"
        "Logout --> This method logs out current user.\n"
        "EXIT --> This method terminates the program safely.\n\n"
        "SPECIAL INFORMATION: in order to navigate back in the application you need to press ctrl + C,\n"
        "Certain Operations cannot be cancelled like entering data in a table, if you attempt to cancel them a\n"
        "default value None will be passed in place of data to prevent errors and a Warning message will be printed.\n"
        "You may cancel them later.\n"
        "But other operations can be cancelled\n\n"
        "HOW TO IDENTIFY:"
        "you should see the prompt specially inside []\n"
        "If [C] present then operation can be cancelled\n"
        "If [N] present then operation cannot be cancelled.\n\n"
        "ALL STATEMENTS PRINTED IN RED IS A WARNING."
    )

    Entry = (
        "Welcome to Entry\n" 
        "Data Entry method allows user to add data to predefined tables.\n\n"
        "Note:\n"
        "ID --> This field is present in every table and its value is incremented automatically by MySQL.\n"
        "Time_N_Date --> This field is very important and adds a time and date value of "
        "the moment the operation is performed\n"
        "All other fields require user entered data but some special "
        "fields default entry is 'N/A' i.e. information not available\n"
        "But user can replace N/A and enter their own specific value.\n"
        "While some filed like admission date are entered automatically and can be changed.\n"
        "There also exist certain safeguards to prevent faulty data from being entered,\n"
        "In such an event the entire operation is automatically cancelled."
    )

    Read_Update = (
        "Welcome to Read/Update\n" 
        "Data Read/Update method allows user to update pre existing data, search data and display entire table.\n"
        "There are certain operations you will encounter:\n\n"
        "Display Entire Table --> prints the entire record of a table selected.\n"
        "Sort and Display --> prints the rows which contain a specific value of a particular filed/column.\n"
        "Update Data --> This method updates a row on the basis of row ID.Please be careful while entering ID.\n"
        "Delete Row --> This method deletes a row on the basis of row ID.Please be careful.\n\n"
        "Entered ID value cannot be Zero as ID cannot be Zero"
    )

    Admin = (
        "Welcome to Administration\n" 
        "Administration method allows you to perform massive"
        "database manipulation operation and the operations are:\n\n"
        "Create Database --> This operation allows you to add database and by default also creates default tables.\n"
        "Drop Database --> Extremely dangerous operation to delete all data and database, requires user password.\n"
        "Clear Table --> This operation allows user to wipe out entire data of a table, requires user password."
    )


class Var:
    # start declaring modes and operations  |
    read_functions = [
        "Display Entire Table",
        "Sort and Display",
        "Update Data",
        "Delete Row"
    ]

    admin_functions = [
        "Create Database",
        "Drop Database",
        "Clear Table",
    ]

    modes = [
        "Select Database",
        "Data Entry",
        "Data Read/Update",
        "Administration",
        "Logout",
        "Exit"
    ]
    #   | end declaring modes and methods

    # start declaring tables and related information    |
    pfields = {
        "ID": "int",
        "Name": "str",
        "DOB": "Date",
        "Age": "int",
        "Sex": "sex",
        "Address": "str",
        "UIDAI": "int",
        "Contact": "int",
        "Description": "str",
        "Additional_Information": "str",
        "Date_of_Admission": "Date",
        "Date_of_Discharge": "Date",
        "Illness": "str",
        "Fees": "float",
        "Item": "str",
        "Batch_No": "int",
        "Count": "int",
        "Expiry_Date": "Date",
        "Total_Cost": "float",
        "Cost_Per_Piece": "float"
    }

    tables = [
        "Workers",
        "Patients",
        "Dispensary"
    ]

    QWorkers = {
        "Name": ["Please enter staff member name: ", None],
        "DOB": ["Please enter the date of birth: YYYY-MM-DD", None],
        "Sex": ["Please specify Sex: ", "sex"],
        "Address": ["Please enter the Home Address: ", None],
        "UIDAI": ["Please enter the UIDAI: ", None],
        "Contact": ["Please enter contact number: ", None],
        "Description": ["please enter the job type (eg: ward boy, nurse, etc): ", None],
        "Additional_Information": ["Please enter additional information if any: ", "N/A"]
    }

    QPatients = {
        "Name": ["Please enter patient name: ", None],
        "DOB": ["Please enter Date of Birth: ", None],
        "Sex": ["Please specify Sex: ", "sex"],
        "Age": ["Please enter the age of patient: ", None],
        "Date_of_Admission": ["Date of admission automatically entered: YYYY-MM-DD ", "auto_date"],
        "Date_of_Discharge": ["Date of Discharge automatically left blank: YYYY-MM-DD", "N/A"],
        "Illness": ["Please describe the patient illness: ", None],
        "Address": ["Please enter address of the patient: ", None],
        "Contact": ["please enter the contact number of patient: ", None],
        "Fees": ["Please enter the frees paid: ", "N/A"],
        "Additional_Information": ["please enter additional information if any: ", "N/A"]
    }

    QDispensary = {
        "Item": ["please enter the product name: ", None],
        "Batch_No": ["please enter the batch number: ", None],
        "Count": ["please enter the count: ", None],
        "Expiry_Date": ["Please enter the expiry date: YYYY-MM-DD", "N/A"],
        "Total_Cost": ["please enter the total cost: ", None],
        "Cost_Per_Piece": ["please enter the per piece cost: ", None]
    }
    #   | end declaring tables and related information


class Queries:
    # start declaring Table creation Queries    [
    CWorkers = (
        'create table Workers ('
        'ID bigint unique auto_increment,'
        'Name char(100),'
        'DOB date,'
        'Sex char(25),' 
        'Address varchar(1000),'
        'UIDAI bigint,'
        'Contact bigint,'
        'Description varchar(1000),'
        'Additional_Information varchar(1000),'
        'Date_N_Time varchar(100),'
        'primary key (ID))'
    )

    CPatients = (
        'create table Patients ('
        'ID bigint unique auto_increment,'
        'Name char(100),'
        'DOB date,'
        'Sex char(25),'
        'Age integer,'
        'Date_of_Admission date,'
        'Date_of_Discharge date,'
        'Illness varchar(1000),'
        'Address varchar(1000),'
        'Contact bigint,'
        'Fees decimal,'
        'Additional_Information varchar(1000),'
        'Date_N_Time varchar(100),'
        'primary key (ID))'
    )

    CDispensary = (
        'create table Dispensary ('
        'ID bigint unique auto_increment,'
        'Item varchar(100),'
        'Batch_No bigint,'
        'Count bigint,'
        'Expiry_Date date,'
        'Total_Cost float,'
        'Cost_Per_Piece decimal,'
        'Date_N_Time varchar(100),'
        'primary key (ID))'
    )
    #   ] end declaring table creation queries

    # start declaring table entry queries   [
    EWorkers = (
        'insert into Workers '
        '(Name, DOB, Sex, Address, UIDAI, Contact,'
        'Description, Additional_Information, Date_N_Time) '
        'values (%(Name)s, %(DOB)s, %(Sex)s, %(Address)s, %(UIDAI)s,'
        '%(Contact)s, %(Description)s, %(Additional_Information)s, %(Date_N_Time)s)'
    )

    EPatients = (
        'insert into Patients '
        '(Name, DOB, Sex, Age, Date_of_Admission, Date_of_Discharge, Illness, Address, Contact,'
        'Fees, Additional_Information, Date_N_Time) '
        'values (%(Name)s, %(DOB)s, %(Sex)s, %(Age)s, %(Date_of_Admission)s,'
        '%(Date_of_Discharge)s, %(Illness)s, %(Address)s, %(Contact)s, %(Fees)s,'
        '%(Additional_Information)s, %(Date_N_Time)s)'
    )

    EDispensary = (
        'insert into Dispensary '
        '(Item, Batch_No, Count, Expiry_Date, Total_Cost, Cost_Per_Piece) '
        'values (%(Item)s, %(Batch_No)s, %(Count)s, %(Expiry_Date)s, %(Total_Cost)s,'
        '%(Cost_Per_Piece)s)'
    )
    #   ] end declaring Table Entry queries

    # start declaring table update queries  [
    UWorkers = (
        'update Workers set '
        'Name = %(Name)s,'
        'DOB = %(DOB)s,'
        'Sex = %(Sex)s,'
        'Address = %(Address)s,'
        'UIDAI = %(UIDAI)s,'
        'Contact = %(Contact)s,'
        'Description = %(Description)s,'
        'Additional_Information = %(Additional_Information)s,'
        'Date_N_Time = %(Date_N_Time)s '
        'where ID = {}'
    )

    UPatients = (
        'update Patients set '
        'Name = %(Name)s,'
        'DOB = %(DOB)s,'
        'Sex = %(Sex)s,'
        'Age = %(Age)s,'
        'Date_of_Admission = %(Date_of_Admission)s,'
        'Date_of_Discharge = %(Date_of_Discharge)s,'
        'Illness = %(Illness)s,'
        'Address = %(Address)s,'
        'Contact = %(Contact)s,'
        'Fees = %(Fees)s,'
        'Additional_Information = %(Additional_Information)s,'
        'Date_N_Time = %(Date_N_Time)s '
        'where ID = {}'
    )

    UDispensary = (
        'update Dispensary set '
        'Item = %(Item)s,'
        'Batch_No = %(Batch_No)s,'
        'Count = %(Count)s,'
        'Expiry_Date = %(Expiry_Date)s,'
        'Total_Cost = %(Total_Cost)s,'
        'Cost_Per_Piece = %(Cost_Per_Piece)s '
        'where ID = {}'
    )
    #   ]end declaring table update queries
