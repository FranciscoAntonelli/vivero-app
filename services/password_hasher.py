import hashlib

class PasswordHasher:
    def hash(self, texto):
        return hashlib.sha256(texto.encode()).hexdigest()

    def verificar(self, texto_plano, hash_guardado):
        return self.hash(texto_plano) == hash_guardado