'use strict'

class Block {
    constructor(data, hash_anterior, nonce) {
        this.data = data;
        this.hash = "";
        this.hash_anterior = hash_anterior;
        this.timestamp = new Date().toUTCString();
        this.nonce = nonce;
    }
    // cria um nó zero para a blockchain
    zero() {
        return new Block("bloco zero", "primeiro hash", 0);
    }
    // cria um bloco com valores informados
    new(data, hash_anterior, nonce) {
        return new Block(data, hash_anterior, nonce)
    }

    validar() {}
}

module.exports = Block;