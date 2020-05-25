from flask import Flask, request
import requests
from datetime import datetime
import json

app = Flask(__name__)

block_index = 0
previous_block_hash = 0
nodes = []
max_no_of_tx_in_block = 1
transactions_in_current_block = []
total_transaction_in_current_block = 0

def broadcast_block():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    global block_index
    global previous_block_hash
    global nodes
    global transactions_in_current_block
    global total_transaction_in_current_block
    global max_no_of_tx_in_block
    payload = {"index": block_index, "transactions": transactions_in_current_block, "timestamp": timestamp, "previous_hash": previous_block_hash}
    s = json.dumps(payload)
    previous_block_hash = hash(s)
    block_index = block_index + 1
    for node in nodes:
        url = node
        r = requests.post(url, data = payload)
    return "Broadcasting"

@app.route('/')
def hello():
    return "Hello"

@app.route('/register_node', methods = ['POST', 'GET'])
def node_found():
    global block_index
    global previous_block_hash
    global nodes
    global transactions_in_current_block
    global total_transaction_in_current_block
    global max_no_of_tx_in_block
    print(request.method)
    if request.method == 'POST':
        node_addr = request.form.get('node_address')
        port = request.form.get('port')
        url = "" + node_addr + ":" + port
        nodes.append(url)

    if request.method == 'GET':
        f = open("file.txt", "a")
        f.write("IN GET")
        f.close()
        node_addr = request.args.get('node_address')
        port = request.args.get('port')
        url = "https://" + node_addr + ":" + port
        nodes.append(url)

    return "Node Registered"
        

@app.route("/transaction", methods = ['POST', 'GET'])
def transaction_received():
    global block_index
    global previous_block_hash
    global nodes
    global transactions_in_current_block
    global total_transaction_in_current_block
    global max_no_of_tx_in_block
    if request.method == 'POST':
        total_transaction_in_current_block = total_transaction_in_current_block + 1
        sender = request.form.get('sender')
        receiver = request.form.get('receiver')
        amount = request.form.get('amount')

    if request.method == 'GET':
        total_transaction_in_current_block = total_transaction_in_current_block + 1
        sender = request.args.get('sender')
        receiver = request.args.get('receiver')
        amount = request.args.get('amount')
        
    current_tx = []
    current_tx.append(sender)
    current_tx.append(receiver)
    current_tx.append(amount)
        
    transactions_in_current_block.append(current_tx)

    if total_transaction_in_current_block == max_no_of_tx_in_block:
        return broadcast_block()

    return "Transaction Received"

if __name__ == '__main__':
    app.run(debug=True, port=5000)