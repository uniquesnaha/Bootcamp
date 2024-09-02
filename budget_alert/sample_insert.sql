INSERT INTO users (user_id, username, is_logged_in, email, phno) 
VALUES (1, 'user1', 0, 'uniquesnaha@gmail.com', 8248316112);

INSERT INTO users (user_id, username, is_logged_in, email, phno) 
VALUES (2, 'user2', 0, 'snaha1911@gmail.com', 9677555675);
INSERT INTO budgets (budget_id, user_id, budget_name, available_amt, total_amt) 
VALUES (1, 1, 'Monthly Groceries', 10000.00, 10000.00);
INSERT INTO budgets (budget_id, user_id, budget_name, available_amt, total_amt) 
VALUES (2, 1, 'Online Retail Spends', 7000.00, 7000.00);


INSERT INTO budgets (budget_id, user_id, budget_name, available_amt, total_amt) 
VALUES (3, 2, 'Travel Fund', 5000.00, 5000.00);
--Alert preferences: 0 for email, 1 for sms and 2 for in_app
INSERT INTO alert_preferences (user_id, alert_type) 
VALUES (1, 0); 

INSERT INTO alert_preferences (user_id, alert_type) 
VALUES (2, 1); 

INSERT INTO users (user_id, username, is_logged_in, email, phno) 
VALUES (3, 'user3', 0, 'budgetalert007@gmail.com', 8248318103);

INSERT INTO alert_preferences (user_id, alert_type) 
VALUES (3, 2); 
INSERT INTO budgets (budget_id, user_id, budget_name, available_amt, total_amt) 
VALUES (4, 3, 'Clothing spends', 5000.00, 5000.00);