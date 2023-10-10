import datetime
import hashlib
import json
from flask import Flask, jsonify, request

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Genesis block initialization
        block = {
            'id_block': 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': 1,
            'prev_hash': '0',
            'hash': self.calculate_hash(1, '0', 1, None, None),
            'proof_of_work': None,
            'data': None
        }
        self.chain.append(block)

    def create_block(self, proof, data):
        prev_block = self.get_last_block()
        prev_proof = prev_block['proof']
        prev_hash = prev_block['hash']

        proof_of_work, curr_hash = self.proof_of_work(prev_proof, proof)

        block = {
            'id_block': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'prev_hash': prev_hash,
            'hash': curr_hash,
            'proof_of_work': proof_of_work,
            'data': data
        }

        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof, new_proof):
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof, hash_operation

    def calculate_hash(self, id_block, prev_hash, proof, proof_of_work, data):
        block_data = {
            'id_block': id_block,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'prev_hash': prev_hash,
            'proof_of_work': proof_of_work,
            'data': data
        }
        return hashlib.sha256(json.dumps(block_data).encode()).hexdigest()

    def is_chain_valid(self):
        prev_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):
            current_block = self.chain[current_index]

            if current_block['prev_hash'] != self.calculate_hash(
                    current_block['id_block'] - 1,
                    prev_block['hash'],
                    current_block['proof'],
                    current_block['proof_of_work'],
                    current_block['data']
            ):
                return False

            prev_proof = prev_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            prev_block = current_block
            current_index += 1

        return True


app = Flask(__name__)
blockchain = Blockchain()

@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route("/mine", methods=['GET'])
def mine():
    prev_block = blockchain.get_last_block()
    prev_proof = prev_block['proof']

    # Proof of work
    new_proof = 1
    proof_of_work, curr_hash = blockchain.proof_of_work(prev_proof, new_proof)

    # Create a new block with some data (in this case, "Mined Block")
    block_data = "Mined Block"
    new_block = blockchain.create_block(proof_of_work, block_data)

    response = {
        'message': "New block has been mined!",
        'block': new_block
    }
    return jsonify(response), 200

@app.route("/modify_block", methods=["PUT"])
def modify_block():
    # Simulate modifying the last block in the chain
    if len(blockchain.chain) > 1:
        modified_data = "Modified Data"
        blockchain.chain[-1].data = modified_data
        response = {"message": "Block modified successfully"}
        return jsonify(response), 200
    else:
        response = {"message": "Cannot modify the genesis block"}
        return jsonify(response), 400

def modify_block(self, block_id, new_data):
    if 0 < block_id <= len(self.chain):
        modified_block = self.chain[block_id - 1]  # Index adjustment
        modified_block['data'] = new_data
        modified_block['hash'] = self.calculate_hash(
            modified_block['id_block'],
            modified_block['prev_hash'],
            modified_block['proof'],
            modified_block['proof_of_work'],
            modified_block['data']
        )
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True)
