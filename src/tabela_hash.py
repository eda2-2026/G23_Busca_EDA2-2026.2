TAM_HASH = 3001


class _Entrada:
    __slots__ = ("ocupado", "chave", "valor", "removido")

    def __init__(self):
        self.ocupado = False
        self.removido = False
        self.chave = None
        self.valor = None


class TabelaHash:
    def __init__(self, tamanho=TAM_HASH):
        self.tamanho = tamanho
        self.tabela = [_Entrada() for _ in range(tamanho)]
        self.qtd = 0
        self.comparacoes = 0

    def _funcao_hash(self, chave):
        return int(chave) % self.tamanho

    def inserir(self, chave, valor):
        if self.qtd >= self.tamanho * 0.7:
            raise RuntimeError("Tabela hash proxima da capacidade maxima.")

        indice = self._funcao_hash(chave)
        inicial = indice
        while self.tabela[indice].ocupado:
            if self.tabela[indice].chave == chave:
                self.tabela[indice].valor = valor
                return
            indice = (indice + 1) % self.tamanho
            if indice == inicial:
                raise RuntimeError("Tabela hash cheia.")

        self.tabela[indice].ocupado = True
        self.tabela[indice].chave = chave
        self.tabela[indice].valor = valor
        self.qtd += 1

    def buscar(self, chave, contar=False):
        """Busca pelo SQ_CANDIDATO. Complexidade media O(1)."""
        indice = self._funcao_hash(chave)
        inicial = indice
        comparacoes = 0

        while self.tabela[indice].ocupado:
            comparacoes += 1
            if self.tabela[indice].chave == chave:
                if contar:
                    return self.tabela[indice].valor, comparacoes
                return self.tabela[indice].valor

            indice = (indice + 1) % self.tamanho
            if indice == inicial:
                break

        if contar:
            return None, comparacoes
        return None

    def __len__(self):
        return self.qtd
