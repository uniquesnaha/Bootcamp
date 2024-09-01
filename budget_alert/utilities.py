import smtplib
from twilio.rest import Client
import tkinter as tk
from tkinter import messagebox
from budget_alert.constants import *
import oracledb




def connect_db():
    try:
        connection = oracledb.connect(user=oracle_username, password=oracle_password, dsn=dsn)
        print("Connected as new_orac successfully!")
        return connection

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Oracle Database error: {error.message}")




def execute_sql_file(file_path,connection):
    try:
        with open(file_path, 'r') as file:
            sql_script = file.read()

        cursor = connection.cursor()
        sql_commands = sql_script.split(';')  
        for command in sql_commands:
            if command.strip():  
                print(command)
                cursor.execute(command)
        
        connection.commit()
        print("SQL script executed successfully.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Oracle Database error: {error.message}")
    finally:
        cursor.close()
        connection.close()
def execute_triggers_from_file(file_path, connection):
    try:
        with open(file_path, 'r') as file:
            sql_script = file.read()
        
        cursor = connection.cursor()
        # Split the script into individual statements using the delimiter '/'. 
        # This is specific to Oracle PL/SQL where '/' is used to terminate PL/SQL blocks.
        sql_commands = sql_script.split('/')

        for command in sql_commands:
            command = command.strip()
            if command.upper().startswith("CREATE OR REPLACE TRIGGER"):
                if command:  # Ensure that the command is not empty
                    print(f"Executing Trigger: {command[:50]}...")  # Print the beginning of the command for readability
                    cursor.execute(command)
                    print("Trigger executed successfully.")
        
        connection.commit()
        print("All triggers executed successfully.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Oracle Database error: {error.message}")
    finally:
        cursor.close()
        connection.close()



def send_email(reciever_email,budget_name,exceeded_amt):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("budgetalert007@gmail.com", "lqgw fmfw lvko juyx")
        # message to be sent
        message = "Alert! Your Budget named {budget_name} is exceeded by Rs.{exceeded_amt}".format(budget_name=budget_name,exceeded_amt=exceeded_amt)
        # sending the mail
        s.sendmail("budgetalert007@gmail.com", reciever_email, message)
        # terminating the session
        s.quit()
    except smtplib.SMTPConnectError:
        print("Error in establishing connection with Gmail")
    except smtplib.SMTPAuthenticationError:
        print("Incorrect Username or Password")


def send_sms(reciever_phno,budget_name,exceeded_amt):
    # Twilio credentials
    account_sid = 'AC75312d4fea64730cc46d98a0b92e9c12'
    auth_token = 'c5a8042c701593c4107a6f791e26bb09'
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        body="Alert! Your Budget named {budget_name} is exceeded by Rs.{exceeded_amt}".format(budget_name=budget_name,exceeded_amt=exceeded_amt),
        from_='+14136505320',  # Twilio number
        to="+91"+ str(reciever_phno)  # Replace with receivers number
    )

def send_inapp(budget_name,exceeded_amt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Format the alert message
    message = f"Alert! Your budget named {budget_name} has been exceeded by Rs.{exceeded_amt}".format(budget_name=budget_name,exceeded_amt=exceeded_amt) 

    # Show the alert pop-up
    messagebox.showwarning("Budget Exceeded Alert", message)

    # Optional: Close the root window after the alert is closed
    root.destroy()

