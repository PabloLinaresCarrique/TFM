import pymysql

def check_aml_rules():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Banana22!',
        database='aml_system'
    )

    try:
        with connection.cursor() as cursor:
            # Fetch transactions that are not yet reviewed
            cursor.execute("SELECT id, amount_paid, payment_currency, payment_format FROM transactions WHERE review_status = 'clear'")
            transactions = cursor.fetchall()

            for trans in transactions:
                trans_id, amount_paid, currency, payment_format = trans
                # Example rule: non-USD transactions over $10,000 or cash transactions
                if (payment_format == 'Cash' and amount_paid > 10000):
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))
            
            connection.commit()
            print("AML rules applied and transactions updated.")
    
    finally:
        connection.close()

# Run the AML rule checks
check_aml_rules()
