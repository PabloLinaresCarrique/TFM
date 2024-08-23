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
            cursor.execute("SELECT id, amount_paid, payment_currency, payment_format, country, account_age, beneficiary_account FROM transactions WHERE review_status = 'clear'")
            transactions = cursor.fetchall()

            for trans in transactions:
                trans_id, amount_paid, currency, payment_format, country, account_age, beneficiary_account = trans

                # Regla 1: Transacciones en efectivo superiores a $10,000
                if payment_format == 'Cash' and amount_paid > 10000:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 2: Transacciones no en USD superiores a $10,000
                elif currency != 'USD' and amount_paid > 10000:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 3: Transacciones en criptomonedas superiores a $5,000
                elif payment_format == 'Cryptocurrency' and amount_paid > 5000:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 4: Transacciones en países de alto riesgo superiores a $1,000
                cursor.execute("SELECT COUNT(*) FROM high_risk_countries WHERE country = %s", (country,))
                if cursor.fetchone()[0] > 0 and amount_paid > 1000:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 5: Transacciones realizadas en cuentas con menos de 30 días de antigüedad y montos superiores a $5,000
                if account_age < 30 and amount_paid > 5000:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 6: Transacciones en países sancionados (por ejemplo, Corea del Norte, Irán)
                cursor.execute("SELECT COUNT(*) FROM sanctioned_countries WHERE country = %s", (country,))
                if cursor.fetchone()[0] > 0:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 7: Múltiples transacciones pequeñas (menos de $1,000) en un corto período de tiempo (ej. 24 horas)
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE beneficiary_account = %s AND amount_paid < 1000 AND TIMESTAMPDIFF(HOUR, transaction_date, NOW()) < 24", (beneficiary_account,))
                if cursor.fetchone()[0] > 5:  # Si hay más de 5 transacciones pequeñas en 24 horas
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 8: Transacciones redondeadas a montos exactos ($10,000, $20,000, etc.)
                if amount_paid % 10000 == 0:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 9: Beneficiarios que reciben múltiples transacciones grandes ($50,000+) de diferentes remitentes en un corto período
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE beneficiary_account = %s AND amount_paid > 50000 AND TIMESTAMPDIFF(DAY, transaction_date, NOW()) < 7", (beneficiary_account,))
                if cursor.fetchone()[0] > 2:  # Si el beneficiario recibe más de 2 transacciones grandes en 7 días
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 10: Transacciones hacia cuentas en jurisdicciones offshore conocidas (ej. Islas Caimán, Suiza)
                cursor.execute("SELECT COUNT(*) FROM offshore_jurisdictions WHERE country = %s", (country,))
                if cursor.fetchone()[0] > 0:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 11: Transferencias internacionales realizadas por individuos sin historial de transacciones internacionales previas
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE id = %s AND international_transfer = TRUE", (trans_id,))
                if cursor.fetchone()[0] == 0 and country != 'USA':  # Suponiendo que el sistema está basado en USA
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

                # Regla 12: Transacciones de más de $5,000 en cuentas de beneficiarios sin actividad en los últimos 6 meses
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE beneficiary_account = %s AND TIMESTAMPDIFF(MONTH, transaction_date, NOW()) > 6", (beneficiary_account,))
                if cursor.fetchone()[0] == 0 and amount_paid > 5000:
                    cursor.execute("UPDATE transactions SET review_status = 'to_be_reviewed' WHERE id = %s", (trans_id,))

            connection.commit()
            print("AML rules applied and transactions updated.")
    
    finally:
        connection.close()

# Run the AML rule checks
check_aml_rules()