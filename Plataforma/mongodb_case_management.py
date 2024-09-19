from pymongo import errors
from datetime import datetime
from utils import get_mongo_connection  # Import the MongoDB connection function
import json
from decimal import Decimal
from datetime import datetime
from bson.objectid import ObjectId
import streamlit as st 


# Get MongoDB connection
db = get_mongo_connection()
if db is None:
    st.error("Failed to connect to MongoDB.")
else:
    cases = db.cases  # Access the cases collection
def create_case(alert_id, transaction_data, client_data):
    cases = db.cases  # Use the initialized db object

class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder to handle Decimal objects.
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomEncoder, self).default(obj)

def convert_decimals(obj):
    """
    Recursively convert Decimal objects to float within the data structure.
    """
    if isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def create_case(alert_id, transaction_data, client_data):
    cases = db.cases  # Use the initialized db object

    # Build transaction_details
    transaction_details = {
        "timestamp": transaction_data[1] if len(transaction_data) > 1 else None,
        "from_bank": transaction_data[2] if len(transaction_data) > 2 else None,
        "from_account": transaction_data[3] if len(transaction_data) > 3 else None,
        "to_bank": transaction_data[4] if len(transaction_data) > 4 else None,
        "to_account": transaction_data[5] if len(transaction_data) > 5 else None,
        "amount_received": {
            "value": float(transaction_data[6]) if len(transaction_data) > 6 and isinstance(transaction_data[6], (Decimal, float, int)) else None,
            "currency": transaction_data[7] if len(transaction_data) > 7 else None
        },
        "amount_paid": {
            "value": float(transaction_data[8]) if len(transaction_data) > 8 and isinstance(transaction_data[8], (Decimal, float, int)) else None,
            "currency": transaction_data[9] if len(transaction_data) > 9 else None
        },
        "payment_format": transaction_data[10] if len(transaction_data) > 10 else None,
        "is_laundering": "Yes" if len(transaction_data) > 11 and transaction_data[11] else "No"
    }

    # Safely get client details
    client_details = {
        "name": client_data[5] if client_data and len(client_data) > 5 else None,
        "age": client_data[1] if client_data and len(client_data) > 1 else None,
        "job": client_data[2] if client_data and len(client_data) > 2 else None,
        "marital_status": client_data[3] if client_data and len(client_data) > 3 else None,
        "education": client_data[4] if client_data and len(client_data) > 4 else None
    }

    # Case data
    case_data = {
        "alert_id": alert_id,
        "created_at": datetime.now(),
        "last_updated": datetime.now(),
        "status": "open",
        "transaction_details": transaction_details,
        "entities": {
            "PrincipalEntity": client_details
        },
        "narrative": "",
        "documents": []
    }

    # Convert Decimal objects to float
    case_data = convert_decimals(case_data)

    # Insert the case data into MongoDB
    try:
        result = cases.insert_one(case_data)
        return str(result.inserted_id)
    except errors.PyMongoError as e:
        st.error(f"Error creating case: {e}")
        return None


def update_case(case_id, update_data):
    cases = db.cases  # Use the initialized db object

    update_data = convert_decimals(update_data)
    update_data["last_updated"] = datetime.now()

    try:
        result = cases.update_one({"_id": ObjectId(case_id)}, {"$set": update_data})
        return result.modified_count > 0
    except errors.PyMongoError as e:
        st.error(f"Error updating case: {e}")
        return False


def get_case(case_id):
    cases = db.cases  # Use the initialized db object

    try:
        case = cases.find_one({"_id": ObjectId(case_id)})
        return case
    except errors.PyMongoError as e:
        st.error(f"Error retrieving case: {e}")
        return None

def add_entity_to_case(case_id, entity_name, entity_data):
    cases = db.cases  # Use the initialized db object

    update_data = {
        f"entities.{entity_name}": entity_data,
        "last_updated": datetime.now()
    }

    try:
        result = cases.update_one(
            {"_id": ObjectId(case_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except errors.PyMongoError as e:
        st.error(f"Error adding entity to case: {e}")
        return False

def update_entity_info(case_id, entity_name, entity_data):
    db = get_mongo_connection()
    cases = db.cases

    # Corrected the update operation to use '$set' only once
    update_data = {
        f"entities.{entity_name}": entity_data,
        "last_updated": datetime.now()
    }

    result = cases.update_one(
        {"_id": ObjectId(case_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0

def update_narrative(case_id, narrative):
    db = get_mongo_connection()
    cases = db.cases

    result = cases.update_one(
        {"_id": ObjectId(case_id)},
        {
            "$set": {
                "narrative": narrative,
                "last_updated": datetime.now()
            }
        }
    )
    return result.modified_count > 0

def add_document_to_case(case_id, document_data):
    cases = db.cases  # Use the initialized db object

    document_data = convert_decimals(document_data)
    document_data["added_at"] = datetime.now()

    try:
        result = cases.update_one(
            {"_id": ObjectId(case_id)},
            {
                "$push": {"documents": document_data},
                "$set": {"last_updated": datetime.now()}
            }
        )
        return result.modified_count > 0
    except errors.PyMongoError as e:
        st.error(f"Error adding document to case: {e}")
        return False


def get_all_cases():
    db = get_mongo_connection()
    cases = db.cases

    return list(cases.find())

def close_case(case_id, closure_type):
    return update_case(case_id, {
        "status": "closed",
        "closure_type": closure_type,
        "closed_at": datetime.now()
    })

def add_osint_result_to_case(case_id, osint_data):
    cases = db.cases  # Use the initialized db object

    osint_data = convert_decimals(osint_data)
    osint_data["added_at"] = datetime.now()

    try:
        result = cases.update_one(
            {"_id": ObjectId(case_id)},
            {
                "$push": {"osint_results": osint_data},
                "$set": {"last_updated": datetime.now()}
            }
        )
        return result.modified_count > 0
    except errors.PyMongoError as e:
        st.error(f"Error adding OSINT result to case: {e}")
        return False

def update_entity_to_case(case_id, entity_name, entity_data):
    db = get_mongo_connection()
    cases = db.cases

    # Corrected the update operation to use '$set' only once
    update_data = {
        f"entities.{entity_name}": entity_data,
        "last_updated": datetime.now()
    }

    result = cases.update_one(
        {"_id": ObjectId(case_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0
