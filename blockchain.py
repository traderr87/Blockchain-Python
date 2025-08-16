import datetime
import json
import hashlib

class Blockchain:
    # group of block
    def __init__(self):
        # list of block 
        self.chain = []
        # genesis block
        self.create_block(nonce=1, previous_hash="0")
        self.create_block(nonce=11, previous_hash="00")

    # build block for keep in blockchain
    def create_block(self, nonce, previous_hash):
        # detail block
        block ={
            "index":len(self.chain)+1, 
            "timestamp":str(datetime.datetime.now()), 
            "nonce":nonce, 
            "previouse_hash":previous_hash,  
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
    
# call to use Blockchain 
blockchain = Blockchain()
print(blockchain.chain)

# print(blockchain.get_previous_block())

# first block encryption
print(blockchain.hash(blockchain.chain[0]))
# second block encryption
print(blockchain.hash(blockchain.chain[1]))