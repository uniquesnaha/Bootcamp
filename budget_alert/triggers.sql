
CREATE OR REPLACE TRIGGER trg_update_available_amt_after_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    -- Update the available amount for the specific budget and user
    UPDATE budgets
    SET available_amt = available_amt - :NEW.amount
    WHERE budget_id = :NEW.budget_id
      AND EXISTS (
          SELECT 1
          FROM users
          WHERE user_id = :NEW.user_id
            AND EXISTS (
                SELECT 1
                FROM budgets
                WHERE budget_id = :NEW.budget_id
                  AND user_id = :NEW.user_id
            )
      );
END;
/
CREATE OR REPLACE TRIGGER trg_update_available_amt_after_update
AFTER UPDATE ON transactions
FOR EACH ROW
BEGIN
    -- Reverse the effect of the old transaction amount
    UPDATE budgets
    SET available_amt = available_amt + :OLD.amount
    WHERE budget_id = :OLD.budget_id
      AND EXISTS (
          SELECT 1
          FROM users
          WHERE user_id = :OLD.user_id
            AND EXISTS (
                SELECT 1
                FROM budgets
                WHERE budget_id = :OLD.budget_id
                  AND user_id = :OLD.user_id
            )
      );

    -- Apply the new transaction amount
    UPDATE budgets
    SET available_amt = available_amt - :NEW.amount
    WHERE budget_id = :NEW.budget_id
      AND EXISTS (
          SELECT 1
          FROM users
          WHERE user_id = :NEW.user_id
            AND EXISTS (
                SELECT 1
                FROM budgets
                WHERE budget_id = :NEW.budget_id
                  AND user_id = :NEW.user_id
            )
      );
END;
/
CREATE OR REPLACE TRIGGER trg_update_available_amt_after_delete
AFTER DELETE ON transactions
FOR EACH ROW
BEGIN
    -- Revert the available amount in the budget table after deletion
    UPDATE budgets
    SET available_amt = available_amt + :OLD.amount
    WHERE budget_id = :OLD.budget_id
      AND EXISTS (
          SELECT 1
          FROM users
          WHERE user_id = :OLD.user_id
            AND EXISTS (
                SELECT 1
                FROM budgets
                WHERE budget_id = :OLD.budget_id
                  AND user_id = :OLD.user_id
            )
      );
END;
/
CREATE OR REPLACE TRIGGER trg_alert_negative_budget
AFTER UPDATE OF available_amt ON budgets
FOR EACH ROW
BEGIN
    IF :NEW.available_amt < 0 THEN
        INSERT INTO alerts (alert_id, user_id, budget_id, alert_type, alert_message)
        VALUES (
            alerts_seq.NEXTVAL,  -- Assuming you have a sequence named alerts_seq
            :NEW.user_id,
            :NEW.budget_id,
            (SELECT alert_type FROM alert_preferences WHERE user_id = :NEW.user_id),
            'Alert: Budget has been exceeded. Available amount is negative.'
        );
    END IF;
END;
/

