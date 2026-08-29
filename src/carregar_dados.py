import csv
import os
import re

from modelos import Candidato, ListaPropostas
from tabela_hash import TabelaHash


PADRAO_SQ_NO_PDF = re.compile(r"\d{4}[A-Z]{2}(\d+)_\d+\.pdf")

ARQUIVOS_CANDIDATOS = [
    "consulta_cand_2026_BR_presidente.csv",
    "consulta_cand_2026_DF.csv",
    "consulta_cand_2026_GO.csv",
]

ARQUIVOS_PLANOS = [
    "planos_de_governo-presidente.csv",
    "planos_de_governo_df_2026.csv",
    "planos_governo_goias_2026.csv",
]

AREAS_PLANO = ["Visao Geral", "Saude", "Educacao", "Seguranca", "Mobilidade e Transportes"]


def _ler_candidatos_arquivo(caminho):
    candidatos = []
    with open(caminho, encoding="latin-1", newline="") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            candidatos.append(Candidato(
                sq_candidato=linha["SQ_CANDIDATO"].strip(),
                numero=linha["NR_CANDIDATO"].strip(),
                nome_urna=linha["NM_URNA_CANDIDATO"].strip(),
                nome_completo=linha["NM_CANDIDATO"].strip(),
                partido_sigla=linha["SG_PARTIDO"].strip(),
                partido_nome=linha["NM_PARTIDO"].strip(),
                cargo=linha["DS_CARGO"].strip(),
                estado=linha["SG_UF"].strip(),
                coligacao=linha["NM_COLIGACAO"].strip(),
                situacao=linha["DS_SIT_TOT_TURNO"].strip(),
                genero=linha["DS_GENERO"].strip(),
            ))
    return candidatos


def _ler_planos_arquivo(caminho, lista_propostas):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        leitor = csv.reader(f, delimiter=";")
        cabecalho = next(leitor)  
        for linha in leitor:
            if not linha or not linha[0].strip():
                continue
            achado = PADRAO_SQ_NO_PDF.findall(linha[0])
            if not achado:
                continue
            sq_candidato = achado[0]

            for area, valor in zip(AREAS_PLANO, linha[2:7]):
                valor = valor.strip()
                if valor:
                    lista_propostas.inserir(sq_candidato, area, valor)


def carregar_tudo(diretorio_dados):
    vetor_candidatos = []
    for nome_arquivo in ARQUIVOS_CANDIDATOS:
        caminho = os.path.join(diretorio_dados, nome_arquivo)
        vetor_candidatos.extend(_ler_candidatos_arquivo(caminho))

    lista_propostas = ListaPropostas()
    for nome_arquivo in ARQUIVOS_PLANOS:
        caminho = os.path.join(diretorio_dados, nome_arquivo)
        _ler_planos_arquivo(caminho, lista_propostas)

    tabela_hash = TabelaHash(tamanho=max(3001, len(vetor_candidatos) * 3))
    for candidato in vetor_candidatos:
        tabela_hash.inserir(candidato.sq_candidato, candidato)

    return vetor_candidatos, lista_propostas, tabela_hash
