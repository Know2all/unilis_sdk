from flask import Flask, jsonify,request
from socket_server import SocketServer

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/data", methods=["POST"])
def get_data():
    body = request.get_json(force=True)
    print(body)
    """Fetch last received machine data"""
    print("Received in flask app")
    return jsonify({"status": "Success"}), 200


if __name__ == "__main__":
    # Start socket server in background
    server = SocketServer(host="0.0.0.0", port=9001, callback_url="http://127.0.0.1:5000/data")
    server.start()
    # Start Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
