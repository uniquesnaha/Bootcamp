-- Create Tables
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    is_logged_in NUMBER(1) DEFAULT 0 NOT NULL,
    email VARCHAR2(100) NOT NULL UNIQUE,
    phno NUMBER(10) NOT NULL UNIQUE
);

CREATE TABLE budgets (
    budget_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    budget_name VARCHAR2(50) NOT NULL UNIQUE,
    available_amt NUMBER(10, 2),
    total_amt NUMBER(10, 2) NOT NULL
);

CREATE TABLE transactions (
    transaction_id NUMBER PRIMARY KEY,
    budget_id NUMBER REFERENCES budgets(budget_id),
    user_id NUMBER REFERENCES users(user_id),
    amount NUMBER(10, 2) NOT NULL,
    transaction_date DATE NOT NULL
);

CREATE TABLE alert_preferences (
    user_id NUMBER PRIMARY KEY REFERENCES users(user_id),
    alert_type NUMBER(1) CHECK (alert_type IN (0, 1, 2))  -- 0 for email, 1 for SMS, 2 for in-app
);

CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    budget_id NUMBER REFERENCES budgets(budget_id),
    alert_type NUMBER(1) CHECK (alert_type IN (0, 1, 2)),  -- 0 for email, 1 for SMS, 2 for in-app
    alert_message VARCHAR2(255),
    alert_date DATE DEFAULT SYSDATE
);

-- Create Sequence
CREATE SEQUENCE alerts_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

CREATE SEQUENCE transaction_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;


