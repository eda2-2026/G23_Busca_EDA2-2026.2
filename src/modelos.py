class Candidato:
    """Representa um candidato. Equivalente a struct Candidato do C."""

    __slots__ = (
        "sq_candidato", "numero", "nome_urna", "nome_completo",
        "partido_sigla", "partido_nome", "cargo", "estado",
        "coligacao", "situacao", "genero",
    )

    def __init__(self, sq_candidato, numero, nome_urna, nome_completo,
                 partido_sigla, partido_nome, cargo, estado,
                 coligacao, situacao, genero):
        self.sq_candidato = sq_candidato
        self.numero = numero
        self.nome_urna = nome_urna
        self.nome_completo = nome_completo
        self.partido_sigla = partido_sigla
        self.partido_nome = partido_nome
        self.cargo = cargo
        self.estado = estado
        self.coligacao = coligacao
        self.situacao = situacao
        self.genero = genero

    def __repr__(self):
        return (f"Candidato({self.numero} - {self.nome_urna} / "
                f"{self.partido_sigla} - {self.cargo}/{self.estado})")

    def ficha(self):
        """Retorna uma string formatada com os dados do candidato."""
        linhas = [
            "=" * 46,
            "CANDIDATO",
            "=" * 46,
            f"Nome de urna : {self.nome_urna}",
            f"Nome completo: {self.nome_completo}",
            f"Numero       : {self.numero}",
            f"Partido      : {self.partido_sigla} - {self.partido_nome}",
            f"Coligacao    : {self.coligacao}",
            f"Cargo        : {self.cargo}",
            f"Estado (UF)  : {self.estado}",
            f"Situacao     : {self.situacao}",
        ]
        return "\n".join(linhas)


class NoProposta:
    __slots__ = ("id", "sq_candidato", "area", "descricao", "prox")

    def __init__(self, id_, sq_candidato, area, descricao):
        self.id = id_
        self.sq_candidato = sq_candidato
        self.area = area
        self.descricao = descricao
        self.prox = None


class ListaPropostas:
    
    def __init__(self):
        self._cabeca = None
        self._contador_id = 0
        self._tamanho = 0

    def inserir(self, sq_candidato, area, descricao):
        self._contador_id += 1
        novo = NoProposta(self._contador_id, sq_candidato, area, descricao)
        novo.prox = self._cabeca
        self._cabeca = novo
        self._tamanho += 1
        return novo

    def buscar_por_candidato(self, sq_candidato):
        atual = self._cabeca
        encontrados = []
        while atual is not None:
            if atual.sq_candidato == sq_candidato:
                encontrados.append(atual)
            atual = atual.prox
        return encontrados

    def buscar_por_area(self, area):
        """Retorna os sq_candidato distintos que tem proposta numa area. O(n)."""
        atual = self._cabeca
        vistos = set()
        resultado = []
        area_norm = area.strip().lower()
        while atual is not None:
            if atual.area.strip().lower() == area_norm and atual.sq_candidato not in vistos:
                vistos.add(atual.sq_candidato)
                resultado.append(atual.sq_candidato)
            atual = atual.prox
        return resultado

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self._cabeca
        while atual is not None:
            yield atual
            atual = atual.prox
