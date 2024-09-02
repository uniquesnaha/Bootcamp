# USER STORY: RECEIVE BUDGET EXCEEDANCE ALERT

## 

**Actors :** User 

**Description:** As a user, I want to receive an alert when I exceed my budget limit so that I can take corrective actions. 

**Pre-conditions:** User must have set budget alert preferences. 

**Post-conditions:** User receives an alert when spending exceeds the budget limit. 

**Normal Course:** 
1. User's spending data is monitored. 
2. System detects when spending exceeds the budget limit based on user preferences. 
3. System sends an alert to the user. 
4. User receives and reviews the alert. 

**Alternative Courses:**
 1. User has multiple budgets set. 
 2. System sends alerts for each budget individually. Frequency of Use Daily, as transactions occur. Assumptions The system can accurately detect when spending exceeds budget limits. Notes and Issues Ensuring timely alerts to enable users to take corrective actions promptly is critical. 


 ## MODULES 

 ## **alerts.py** 
**check_exceedance(user_id,budget_id):** Checks is the budget is exceeded and triggers an alert for the user_id depending on their alert preferences.

**add_transaction(user_id,budget_id,transaction_amount):** To process a transaction for the budget_id and user_id , and update the available amount in budgets table. Invokes alert trigger when budget is exceeded

**check_available_budget(user_id, budget_id):** Allows the user to check available_amt in the budget referencing budget_id

 ## **utilities.py** 

 **connect_db():** Utility to Connect to oracle database and return the connection

 **execute_sql_file(file_path,connection):** Utility to run an SQL file

 **execute_triggers_from_file(file_path, connection):** Utility to execute a PL/SQL file

 **send_email(reciever_email,budget_name,exceeded_amt):**
 Utility to send email alert to an email address

 **send_sms(reciever_phno,budget_name,exceeded_amt):** Utility to send sms alert to a phone number

 **send_inapp(budget_name,exceeded_amt):** Utility to raise in app alert message 

 ## **spark_utils.py** 

 **get_spark_session():** Utility to create and return a spark session

 **spark_db_to_df(spark,table_name):** Utility to convert and return an oracle database table to a dataframe


## **main.py** 

**main_menu():** Menu driven code to add a transaction, check budget availability and exit

