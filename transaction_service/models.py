from db import get_connection

def add_transaction(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (customer, timestamp, status, vendor_id, amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['customer'], data['timestamp'], data['status'], data['vendor_id'], data['amount']))
    conn.commit()
    transaction_id = cursor.lastrowid
    conn.close()
    return {"message": "Transaction created", "transaction_id": transaction_id}

def update_transaction(transaction_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions SET status = ?, vendor_id = ?, amount = ?
        WHERE id = ?
    ''', (data['status'], data['vendor_id'], data['amount'], transaction_id))
    conn.commit()
    conn.close()
    return {"message": "Transaction updated"}

def get_prediction_result(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM results WHERE transaction_id = ?
    ''', (transaction_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "transaction_id": row[1],
            "timestamp": row[2],
            "is_fraudulent": bool(row[3]),
            "confidence": row[4]
        }
    return {"error": "No result found"}, 404
