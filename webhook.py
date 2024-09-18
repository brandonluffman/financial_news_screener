from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Extract data from the incoming request
    data = request.json

    # Log or process the data
    print("Received data:", data)
    
    # Respond to acknowledge receipt
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(port=5000)
