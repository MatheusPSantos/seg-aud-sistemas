const { mainModule } = require("process");
const Blockchain = require("./Blockchain");

const readline = require("readline-sync");
const Block = require("./Block");

function pergunta(str) {
    return readline.question(str)
}

async function main() {
    let contador = 1;
    let sair = false;
    let dado;
    let nonce;

    console.info("Inicio do programa ...");
    const blockchain = new Blockchain();
    console.info("blockchain inicializada >> ", blockchain);
    // informamos a dificuldade da cadeia
    const dificuldade = pergunta("Qual a dificuldade da blockchain [1 até 254] ? ");
    blockchain.inserirDificuldade(dificuldade);

    console.info("Inserindo o nó zero da cadeia ...");
    blockchain.new();

    while (!sair) {

        dado = pergunta(`Qual dado inserir no bloco? `);
        nonce = pergunta("Qual será o nonce inicial? ");
        
        blockchain.minerar(blockchain, dado, nonce);
        blockchain.validar(blockchain);
        console.info("\n");
        console.info("+------------------ BLOCKCHAIN  ------------------------+")
        blockchain.chain.map((item, index) => console.table(item));
        console.info("+--------------------------------------------------------+");

        console.info("0".repeat(91));
        console.info("  Hash encontrado >> ", blockchain.hashDaSorte, "\t  0");
        console.info("0".repeat(91), "\n");

        sair = pergunta("Deseja continuar [s / N = padrao]?  ");

        sair.toUpperCase() === "S" ? sair = false : sair = true;

    }

}


if (require.main === module) {
    main();
}
