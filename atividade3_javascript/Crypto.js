'use strict'

const { createHash } = require("crypto");

class Crypto {

    // define a função usada para hash dos blocos
    sha256(block) {
        const hash = createHash("sha256");
        return hash.update(block).digest("hex");
    }

    adicionaHash(block) {
        block.hash = this.sha256(JSON.stringify(block));
        return block;
    }

}

module.exports = Crypto