INSERT INTO users (user_id, username, is_logged_in, email, phno) 
VALUES (1, 'user1', 0, 'uniquesnaha@gmail.com', 8248316112);

INSERT INTO users (user_id, username, is_logged_in, email, phno) 
VALUES (2, 'user2', 0, 'snaha1911@gmail.com', 9677555675);
INSERT INTO budgets (budget_id, user_id, budget_name, available_amt, total_amt) 
VALUES (1, 1, 'Monthly Groceries', 1000.00, 1500.00);

INSERT INTO budgets (budget_id, user_id, budget_name, available_amt, total_amt) 
VALUES (2, 2, 'Travel Fund', 500.00, 700.00);
INSERT INTO alert_preferences (user_id, alert_type) 
VALUES (1, 0);  

INSERT INTO alert_preferences (user_id, alert_type) 
VALUES (2, 1); 
