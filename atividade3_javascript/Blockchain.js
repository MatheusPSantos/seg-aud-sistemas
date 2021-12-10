'use strict'

const Block = require("./Block");
const Crypto = require("./Crypto");
const Mining = require("./Mining");


class Blockchain {
    constructor() {
        this.chain = [];
        this.Mining = new Mining();
        this.dificuldade = 0;
        this.hashDoNoZero = null;
        this.hashDaSorte = null;
    }

    //informar dificuldade da blockchain
    inserirDificuldade(d) {
        this.Mining.informarDificuldade(parseInt(d));
        this.dificuldade = this.Mining.obterDificuldade();
    }

    // cria a blockchain
    new() {
        this.chain.push(new Crypto().adicionaHash(new Block().zero()));
        return this.chain;
    }

    // minera um novo bloco
    minerar(blockchain, data, nonce) {
        console.info("Criando novo bloco ...");
        let blocoValido = false;
        let novoBloco;
        let contadorNonce = nonce;
        
        const blocoAnterior = blockchain.chain[blockchain.chain.length - 1];
        novoBloco = new Block().new(data, blocoAnterior.hash, contadorNonce);

        while (!blocoValido) {
            novoBloco.nonce = contadorNonce;
            novoBloco.hash = new Crypto().sha256(JSON.stringify(novoBloco));
            let novoBlocoString = JSON.stringify(novoBloco);
            let hashDoNovoBloco = new Crypto().sha256(novoBlocoString);
            console.info("\thash calculado << ", hashDoNovoBloco);
            if (this.Mining.validarBloco(hashDoNovoBloco)) {
                this.chain.push(novoBloco)
                this.hashDaSorte = hashDoNovoBloco;
                blocoValido = true;
            } else {
                console.info("Bloco inválido: ", novoBloco);
                contadorNonce++;
            }
        }

        return this.chain;
    }
    // função para validar a blockchain
    validar(blockchain) {
        const chain = JSON.parse(JSON.stringify(blockchain.chain));

        chain.reverse().map((block, index) => {
            if (index != 0 && block.hash !== chain[index - 1].hash_anterior) {
                throw new Error("Blockchain inválida. Há uma inconsistência entre os blocos ", index, " e ", index - 1);
            }
        });
        console.log("0".repeat(49));
        console.info("0 \tBlockchain válida! Congratulations! \t0");
        console.log("0".repeat(49),"\n");
        return;
    }
}

module.exports = Blockchain;