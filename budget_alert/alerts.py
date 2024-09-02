import oracledb
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import logging
from utilities import *
from constants import*
from spark_utils import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("alert_system.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

# Logger instance
logger = logging.getLogger(__name__)

#Check budget exceedance of a particular user
def check_exceedance(user_id,budget_id):
      try:
        spark=get_spark_session()
        conn=connect_db()
        budgets_df=spark_db_to_df(spark,"budgets").collect()
        
        logger.info("Checking budget exceedance")
        for row in budgets_df:
                if row['AVAILABLE_AMT']<0 and row['USER_ID']==user_id and row['BUDGET_ID']==budget_id:
                    logger.info(f"Budget exceeded by {abs(row['AVAILABLE_AMT'])}")
                    exceeded_amt=abs(row['AVAILABLE_AMT'])
                    alert_type=get_alert_type(user_id,conn)
                    user_df = spark_db_to_df(spark,"users")
                    # Register the DataFrame as a temporary view
                    user_df.createOrReplaceTempView("user_view")

                    # Execute an SQL query to fetch user details
                    query = f"SELECT * FROM user_view WHERE user_id = {user_id}"
                    result_df = spark.sql(query)
                    user=result_df.collect()[0]
                    print(user)
                    logger.info(f"Sending alert to {user['USERNAME']}")
                    if alert_type == 0:
                        receiver_email = user['EMAIL']
                        send_email(receiver_email, row['BUDGET_NAME'], exceeded_amt)
                    elif alert_type == 1:
                        receiver_phno = user['PHNO']
                        send_sms(receiver_phno, row['BUDGET_NAME'], exceeded_amt)
                    elif alert_type == 2:
                        send_inapp(row['BUDGET_NAME'], exceeded_amt)
                    else:
                        print(f"Unknown alert type {alert_type} for user {user_id}.")

                    
        conn.close()
      except Exception as e:
           logger.error(f"An error occured while checking budget exceedance : {e}",exc_info=True)
           
                  


#Process a transaction of a particular user
def add_transaction(user_id,budget_id,transaction_amount):
        try:
            conn=connect_db()
            cursor = conn.cursor()

        
            insert_transaction_query = f"""
            INSERT INTO transactions (transaction_id, budget_id, user_id, amount, transaction_date) 
            VALUES (transaction_seq.NEXTVAL, {budget_id}, {user_id}, {transaction_amount}, SYSDATE)
            """
            cursor.execute(insert_transaction_query)
            conn.commit()
            logger.info(f"Transaction of {transaction_amount} processed successfully for user {user_id}")
            check_exceedance(user_id,budget_id)
            
        except Exception as e:
           logger.error(f"An error occured while processing transaction : {e}",exc_info=True)
        finally:
            conn.close() 

#Get alert preference of a user
def get_alert_type(user_id, conn):
    try:
        """Fetch the alert type for the given user from OracleDB."""
        query = f"""
        SELECT alert_type 
        FROM alert_preferences 
        WHERE user_id = {user_id}
        """
        
        cursor = conn.cursor()
        cursor.execute(query)
        
        alert_type = cursor.fetchone()[0]
        cursor.close()
        logger.info(f"Fetched alert type for user {user_id}")
        return alert_type
    except Exception as e:
        logger.error(f"An error occured while fetching alert type: {e}",exc_info=True)
    

#Check available limit until budget is reached
def check_available_budget(user_id, budget_id):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Query to fetch the available amount for the specified user_id and budget_id
        query = """
        SELECT AVAILABLE_AMT
        FROM BUDGETS
        WHERE USER_ID = :user_id AND BUDGET_ID = :budget_id
        """
        
        cursor.execute(query, {'user_id': user_id, 'budget_id': budget_id})
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            available_amt = result[0]
            print(f"Available amount for budget ID {budget_id} and user ID {user_id}: {available_amt}")

            return available_amt
        else:
            print("No budget found for the specified user and budget ID.")
            return None

    except oracledb.DatabaseError as e:
        print(f"Database query error: {e}")
        raise

    finally:
        if conn:
            conn.close()




     
