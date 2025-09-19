from flask import Blueprint, request, jsonify
from extensions import db,logger
from models import User, Transaction
import requests

bp = Blueprint("api", __name__)

@bp.route("/health", methods=["GET"])
def health():
    logger.info("Health check endpoint hit")
    return jsonify({"status": "healthy"}), 200


@bp.route("/run", methods=["POST"])
def run():
    body = request.get_json(force=True)
    invoice_id = body.get("invoice_id", None)
    callback_url = body.get("callback_url", None)

    new_obj = Transaction(invoice_id=invoice_id, callback_url=callback_url)
    db.session.add(new_obj)
    db.session.commit()

    logger.info(f"New Transaction created: {new_obj.to_dict()}")
    return jsonify(new_obj.to_dict()), 201


@bp.route("/data", methods=["POST"])
def get_data():
    """Fetch last received machine data"""
    try:
        body = request.get_json(force=True)
        logger.info(f"Received machine data: {body}")

        transaction: Transaction = Transaction.query.order_by(Transaction.id.desc()).first()
        if not transaction:
            logger.error("No transaction found in database")
            return jsonify({"status": "Error", "message": "No transaction found"}), 404

        logger.info(f"Forwarding data to callback: {transaction.callback_url}")
        body['invoice_id'] = transaction.invoice_id
        api_response = requests.post(transaction.callback_url, json=body)

        if api_response.status_code == 200:
            logger.info("Callback succeeded")
            return jsonify({"status": "success"}), 200
        elif api_response.status_code == 400:
            logger.warning("Callback returned 400 (not found)")
            raise Exception(api_response.text)
        elif api_response.status_code == 500:
            logger.error("Callback returned 500 (server error)")
            raise Exception(api_response.text)
        else:
            logger.error(f"Unexpected callback status: {api_response.status_code}")
            raise Exception("Something Went Wrong in CallBack Url")

    except Exception as e:
        logger.exception("Error handling /data request")  # logs stack trace
        return jsonify({"status": "Error", "message": str(e)}), 500
