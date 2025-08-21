import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    # group of block
    def __init__(self):
        # list of block 
        self.chain = []
        self.transaction = 0 # amount
        # genesis block
        self.create_block(nonce=1, previous_hash="0")

    # build block for keep in blockchain
    def create_block(self, nonce, previous_hash):
        # detail block
        block ={
            "index": len(self.chain)+1, 
            "timestamp": str(datetime.datetime.now()), 
            "nonce": nonce, 
            "data": self.transaction, 
            "previous_hash": previous_hash,  
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
            hashOperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest() # must same number

            if hashOperation[:4] == "0000":
                check_proof=True
            else:
                new_nonce+=1

        return new_nonce
    
    # validate block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index] # checked block
            
            if block["previous_hash"] != self.hash(previous_block):
                return False
            
            previous_nonce = previous_block["nonce"] # nonce of previous block
            nonce = block["nonce"] # nonce of validate block
            hashOperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest() # must same number
            
            if hashOperation[:4] != "0000":
                return False

            previous_block = block
            block_index+=1
        
        return True

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
    amount = 1000000
    blockchain.transaction = blockchain.transaction+amount
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
        "data": block["data"], 
        "nonce": block["nonce"], 
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200

@app.route('/is_valid', methods = ["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={"message": "Blockchain Valid"}
    else:
        response={"message": "Have a Problem, Blockchain Is Not Valid"}
    return jsonify(response), 200

# run server
if __name__ == "__main__":
    app.run()