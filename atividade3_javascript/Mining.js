'use strict'

class Mining{

    constructor() {
        this.dificuldade = 0; //A dificuldade inicial é zero
    }
    // informa o número de zeros iniciais no hash
    informarDificuldade(dificuldade) {
        this.dificuldade = dificuldade;
    }
    // retorna a dificuldade informada
    obterDificuldade() {
        return this.dificuldade;
    }
    // pega em forma de strin a dificuldade, por exemplo: "000"
    pegarInicioDoHash() {
        const zero = "0";
        return this.dificuldade < 256 ? zero.repeat(this.dificuldade) : zero.repeat(254);
    }
    // valida o novo bloco de acordo com a
    // string de dificuldade
    validarBloco(hashBlock) {
        let hashString = new String(hashBlock);
        return hashString.startsWith(this.pegarInicioDoHash());
    }
}

module.exports = Mining;