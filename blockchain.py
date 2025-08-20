import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    # group of block
    def __init__(self):
        # list of block 
        self.chain = []
        # genesis block
        self.create_block(nonce=1, previous_hash="0")

    # build block for keep in blockchain
    def create_block(self, nonce, previous_hash):
        # detail block
        block ={
            "index":len(self.chain)+1, 
            "timestamp":str(datetime.datetime.now()), 
            "nonce":nonce, 
            "previous_hash":previous_hash,  
        }
        self.chain.append(block)
        return block
    
    # service for previous block
    def get_previous_block(self):
        return self.chain[-1]
    
    # block encryption
    def hash(self, block):
        # python object(dict) => json object
        encode_block = json.dumps(block, sort_keys=True).encode()
        # sha-256
        return hashlib.sha256(encode_block).hexdigest() # hex = 16 number base
    
    def proof_of_work(self, previous_nonce):
        # get nonce that result target hash => 0000xxxxxxxxxxxxx
        new_nonce = 1
        check_proof = False

        # mathematical problems
        while check_proof is False:
            # get 16 number base
            hashOperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashOperation[:4] == "0000":
                check_proof=True
            else:
                new_nonce+=1
        return new_nonce

    def get_previous_block(self):
        return self.chain[-1]
    
    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False

        while check_proof is False:
            hashOperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashOperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce+=1
        return new_nonce
    
# web server
app = Flask(__name__)

# call to use Blockchain 
blockchain = Blockchain()

# routing
@app.route('/')
def hello():
    return "<p>Hello Blockchain</p>"

@app.route('/get_chain', methods = ["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,  
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/mining', methods = ["GET"])
def mining_block():
    # pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    # nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    
    # previous hash block
    previous_hash = blockchain.hash(previous_block)

    # update new block
    block = blockchain.create_block(nonce, previous_hash)
    response = {
        "message": "Mining Block Compeleted", 
        "index": block["index"], 
        "timestamp": block["timestamp"], 
        "nonce": block["nonce"], 
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200

# run server
if __name__ == "__main__":
    app.run()