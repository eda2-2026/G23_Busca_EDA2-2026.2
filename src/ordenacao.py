def quicksort(vetor, inicio, fim, chave):
    if inicio >= fim:
        return

    i, j = inicio, fim
    pivo = chave(vetor[(inicio + fim) // 2])

    while i <= j:
        while chave(vetor[i]) < pivo:
            i += 1
        while chave(vetor[j]) > pivo:
            j -= 1
        if i <= j:
            vetor[i], vetor[j] = vetor[j], vetor[i]
            i += 1
            j -= 1

    if inicio < j:
        quicksort(vetor, inicio, j, chave)
    if i < fim:
        quicksort(vetor, i, fim, chave)


def ordenar_por_nome(vetor):
    from busca import normalizar
    quicksort(vetor, 0, len(vetor) - 1, chave=lambda c: normalizar(c.nome_urna))