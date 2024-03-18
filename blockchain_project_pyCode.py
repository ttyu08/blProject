import datetime  
import hashlib  
import json  
from flask import Flask, jsonify  
from flask import render_template 
 
   
class Blockchain:  
    def __init__(self):  
        self.chain = []  
        self.create_block(proof=1, previous_hash='0', body='')  
 
    def create_block(self, proof, previous_hash, body):  
        block = {'index': len(self.chain) + 1,  
                 'timestamp': str(datetime.datetime.now()),  
                 'proof': proof,  
                 'previous_hash': previous_hash, 
                 'body': body}  
        self.chain.append(block)  
        return block  
 
    def print_previous_block(self):  
        return self.chain[-1] 
     
    def proof_of_work(self, previous_proof):  
        new_proof = 1  
        check_proof = False  
   
        while check_proof is False:  
            hash_operation = hashlib.sha256(  
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()  
            if hash_operation[:5] == '00000':  
                check_proof = True  
            else:  
                new_proof += 1  
   
        return new_proof  
   
    def hash(self, block):  
        encoded_block = json.dumps(block, sort_keys=True).encode()  
        return hashlib.sha256(encoded_block).hexdigest()  
   
    def chain_valid(self, chain):  
        previous_block = chain[0]  
        block_index = 1  
   
        while block_index < len(chain):  
            block = chain[block_index]  
            if block['previous_hash'] != self.hash(previous_block):  
                return False  
   
            previous_proof = previous_block['proof']  
            proof = block['proof']  
            hash_operation = hashlib.sha256(  
                str(proof**2 - previous_proof**2).encode()).hexdigest()  
   
            if hash_operation[:5] != '00000':  
                return False  
            previous_block = block  
            block_index += 1  
   
        return True  
   
app = Flask(__name__)  
   
blockchain = Blockchain()    
   
@app.route('/mine_block', methods=['GET'])  
def mine_block(body):  
    previous_block = blockchain.print_previous_block()  
    previous_proof = previous_block['proof']  
    proof = blockchain.proof_of_work(previous_proof)  
    previous_hash = blockchain.hash(previous_block)  
    block = blockchain.create_block(proof, previous_hash, body)  
   
    response = {'message': 'A block is MINED',  
                'index': block['index'],  
                'timestamp': block['timestamp'],  
                'proof': block['proof'],  
                'previous_hash': block['previous_hash'], 
                'body': block['body']}  
   
    return jsonify(response), 200  
 
   
   
@app.route('/get_chain', methods=['GET'])  
def display_chain():  
    response = {'chain': blockchain.chain,  
                'length': len(blockchain.chain)}  
    return jsonify(response), 200  
 
   
@app.route('/valid', methods=['GET'])  
def valid():  
    valid = blockchain.chain_valid(blockchain.chain)  
   
    if valid:  
        response = {'message': 'The Blockchain is valid.'}  
    else:  
        response = {'message': 'The Blockchain is not valid.'}  
    return jsonify(response), 200  
 
 
 
 
 
 
def test_init(body):  
    previous_block = blockchain.print_previous_block()  
    previous_proof = previous_block['proof']  
    proof = blockchain.proof_of_work(previous_proof)  
    previous_hash = blockchain.hash(previous_block) 
    block = blockchain.create_block(proof, previous_hash, body) 
 
test_init('<h1>Блокчейн</h1><p> - выстроенная по определённым правилам непрерывная последовательная цепочка блоков (связный список), содержащих какую-либо информацию. Связь между блоками обеспечивается не только нумерацией, но и тем, что каждый блок содержит свою собственную хеш-сумму и хеш-сумму предыдущего блока. Изменение любой информации в блоке изменит его хеш-сумму.
</p>') 
 
 
@app.route('/index', methods=['GET']) 
def index(): 
    list_of_articles = [] 
    for i in blockchain.chain: 
        list_of_articles.append(i['body'][:50]) 
    return render_template('index.html', articles=list_of_articles) 
 
@app.route('/articles/<int:article_id>') 
def get_article(article_id): 
    for i in blockchain.chain: 
        if i['index'] == article_id: 
            return i['body'] 
 
 
 
 
app.run(host='127.0.0.1', port=5000)
