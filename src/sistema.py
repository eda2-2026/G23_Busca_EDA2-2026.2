from carregar_dados import carregar_tudo
from ordenacao import ordenar_por_nome
from busca import busca_binaria, busca_sequencial, normalizar

CARGOS_VICE = {"VICE-PRESIDENTE", "VICE-GOVERNADOR", "1º SUPLENTE", "2º SUPLENTE"}

AREAS_PLANO = ["Visao Geral", "Saude", "Educacao", "Seguranca", "Mobilidade e Transportes"]


class SistemaBusca:
    def __init__(self, diretorio_dados):
        vetor_completo, self.propostas, self.hash = carregar_tudo(diretorio_dados)

        self.vetor = [c for c in vetor_completo if c.cargo not in CARGOS_VICE]

        self._vices_por_chave = {}
        for c in vetor_completo:
            if c.cargo in CARGOS_VICE:
                chave = (c.estado, c.numero, c.coligacao)
                self._vices_por_chave.setdefault(chave, []).append(c)
                
        ordem_cargo = {"VICE-PRESIDENTE": 0, "VICE-GOVERNADOR": 0, "1º SUPLENTE": 1, "2º SUPLENTE": 2}
        for lista in self._vices_por_chave.values():
            lista.sort(key=lambda c: ordem_cargo.get(c.cargo, 9))

        self.vetor_ordenado = list(self.vetor)
        ordenar_por_nome(self.vetor_ordenado)

        self._por_numero = {}
        for c in self.vetor:
            self._por_numero.setdefault(c.numero, []).append(c)

    def vices_do_candidato(self, candidato):
        chave = (candidato.estado, candidato.numero, candidato.coligacao)
        return self._vices_por_chave.get(chave, [])

    def buscar_por_nome(self, nome):
        indice = busca_binaria(self.vetor_ordenado, nome, chave=lambda c: c.nome_urna)
        if indice == -1:
            return []
        alvo = normalizar(nome)
        resultado = []
        i = indice
        while i < len(self.vetor_ordenado) and normalizar(self.vetor_ordenado[i].nome_urna) == alvo:
            resultado.append(self.vetor_ordenado[i])
            i += 1
        return resultado

    def buscar_por_nome_parcial(self, trecho):
        alvo = normalizar(trecho)
        return [c for c in self.vetor if alvo in normalizar(c.nome_urna)]

    def buscar_por_numero(self, numero):
        return self._por_numero.get(str(numero).strip(), [])

    def buscar_por_partido(self, sigla):
        alvo = normalizar(sigla)
        indices = busca_sequencial(self.vetor, lambda c: normalizar(c.partido_sigla) == alvo)
        return [self.vetor[i] for i in indices]

    def buscar_por_cargo(self, cargo):
        alvo = normalizar(cargo)
        indices = busca_sequencial(self.vetor, lambda c: alvo in normalizar(c.cargo))
        return [self.vetor[i] for i in indices]

    def buscar_por_estado(self, estado):
        alvo = normalizar(estado)
        indices = busca_sequencial(self.vetor, lambda c: normalizar(c.estado) == alvo)
        return [self.vetor[i] for i in indices]

    def listar_presidenciaveis(self):
        return self.buscar_por_estado("BR")

    def propostas_do_candidato(self, sq_candidato):
        return self.propostas.buscar_por_candidato(sq_candidato)

    def proposta_do_candidato_na_area(self, sq_candidato, area):
        alvo = normalizar(area)
        for p in self.propostas.buscar_por_candidato(sq_candidato):
            if normalizar(p.area) == alvo:
                return p.descricao
        return None

    def comparar_propostas(self, candidatos, area):
        resultado = []
        for candidato in candidatos:
            texto = self.proposta_do_candidato_na_area(candidato.sq_candidato, area)
            resultado.append((candidato, texto))
        return resultado

    def listar_todos(self):
        return self.vetor

