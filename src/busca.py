import unicodedata


def normalizar(texto):
    if texto is None:
        return ""
    forma = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in forma if not unicodedata.combining(c))
    return sem_acento.strip().upper()


def busca_binaria(vetor, nome_busca, chave, contar=False):

    alvo = normalizar(nome_busca)
    inicio, fim = 0, len(vetor) - 1
    comparacoes = 0

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        valor_meio = normalizar(chave(vetor[meio]))

        if valor_meio == alvo:
            while meio > 0 and normalizar(chave(vetor[meio - 1])) == alvo:
                meio -= 1
                comparacoes += 1
            if contar:
                return meio, comparacoes
            return meio
        elif valor_meio < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1

    if contar:
        return -1, comparacoes
    return -1


def busca_sequencial(vetor, condicao, contar=False):
    resultado = []
    comparacoes = 0
    for i, elemento in enumerate(vetor):
        comparacoes += 1
        if condicao(elemento):
            resultado.append(i)

    if contar:
        return resultado, comparacoes
    return resultado


def busca_sequencial_nome(vetor, nome_busca, chave, contar=False):
    alvo = normalizar(nome_busca)
    comparacoes = 0
    for i, elemento in enumerate(vetor):
        comparacoes += 1
        if normalizar(chave(elemento)) == alvo:
            if contar:
                return i, comparacoes
            return i
    if contar:
        return -1, comparacoes
    return -1
