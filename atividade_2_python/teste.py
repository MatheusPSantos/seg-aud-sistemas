from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

mensagem = b"eu sou uma mensagem"

chave_privada = rsa.generate_private_key(
    public_exponent=65537, key_size=2048
)
chave_publica = chave_privada.public_key()
texto_cifrado = chave_publica.encrypt(
    mensagem,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("mensagem  ", mensagem)
print("texto cifrado  ", texto_cifrado)

texto_pleno = chave_privada.decrypt(
    texto_cifrado,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("texto pleno >> ",texto_pleno)