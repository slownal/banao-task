from flask import Flask, request, jsonify
from handler import send_email as send_email_handler
import json

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def webhook():
    event = {
        'body': json.dumps(request.json)
    }
    context = {}
    
    response = send_email_handler(event, context)
    
    return jsonify(json.loads(response['body'])), response['statusCode']

if __name__ == "__main__":
    app.run(port=5001) 