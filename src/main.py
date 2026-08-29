import os
import sys

from sistema import SistemaBusca, AREAS_PLANO

DIR_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")


def linha(char="=", n=46):
    print(char * n)


def texto_vice(sistema, candidato):
    vices = sistema.vices_do_candidato(candidato)
    if not vices:
        return ""
    if len(vices) == 1:
        return f" (Vice: {vices[0].nome_urna})"
    nomes = ", ".join(v.nome_urna for v in vices)
    return f" (Suplentes: {nomes})"


def mostrar_candidato_resumo(sistema, c):
    nome_com_vice = f"{c.nome_urna}{texto_vice(sistema, c)}"
    print(f"{c.numero:<8} {nome_com_vice:<45} {c.partido_sigla:<10} {c.cargo:<20} {c.estado}")


def mostrar_lista(sistema, candidatos, titulo):
    linha()
    print(titulo)
    linha()
    if not candidatos:
        print("Nenhum candidato encontrado.")
        return
    print(f"{'Numero':<8} {'Nome de urna (e vice/suplente)':<45} {'Partido':<10} {'Cargo':<20} UF")
    print("-" * 100)
    for c in candidatos:
        mostrar_candidato_resumo(sistema, c)
    print(f"\nTotal: {len(candidatos)} candidato(s)")


def escolher_candidato(sistema, candidatos):
    if not candidatos:
        print("Nenhum candidato encontrado.")
        return None
    if len(candidatos) == 1:
        return candidatos[0]

    mostrar_lista(sistema, candidatos, "VARIOS CANDIDATOS ENCONTRADOS")
    try:
        idx = int(input("\nDigite o indice (1 a {}) do candidato desejado: ".format(len(candidatos))))
        if 1 <= idx <= len(candidatos):
            return candidatos[idx - 1]
    except ValueError:
        pass
    print("Selecao invalida.")
    return None


def mostrar_ficha_com_propostas(sistema, candidato):
    print()
    print(candidato.ficha())
    vices = sistema.vices_do_candidato(candidato)
    if vices:
        rotulo = "Vice" if len(vices) == 1 else "Suplentes"
        print(f"{rotulo}       : {', '.join(v.nome_urna for v in vices)}")

    propostas = sistema.propostas_do_candidato(candidato.sq_candidato)
    print()
    print("PROPOSTAS DE GOVERNO")
    print("-" * 46)
    if not propostas:
        print("Nenhum plano de governo cadastrado para este candidato.")
    else:
        for p in propostas:
            print(f"\n[{p.area}]\n{p.descricao}")


def resolver_candidato_por_nome(sistema, nome):
    resultados = sistema.buscar_por_nome(nome)
    if not resultados:
        resultados = sistema.buscar_por_nome_parcial(nome)
    return escolher_candidato(sistema, resultados)


def opcao_buscar_por_nome(sistema):
    nome = input("Digite o nome (busca binaria, exata): ").strip()
    candidato = resolver_candidato_por_nome(sistema, nome)
    if candidato:
        mostrar_ficha_com_propostas(sistema, candidato)


def opcao_buscar_por_numero(sistema):
    numero = input("Digite o numero do candidato: ").strip()
    resultados = sistema.buscar_por_numero(numero)
    candidato = escolher_candidato(sistema, resultados)
    if candidato:
        mostrar_ficha_com_propostas(sistema, candidato)


def opcao_buscar_por_partido(sistema):
    sigla = input("Digite a sigla do partido (ex.: PT, PL, PSOL): ").strip()
    resultados = sistema.buscar_por_partido(sigla)
    mostrar_lista(sistema, resultados, f"CANDIDATOS DO PARTIDO {sigla.upper()}")


def opcao_buscar_por_cargo(sistema):
    print("Ex.: PRESIDENTE, GOVERNADOR, SENADOR, DEPUTADO FEDERAL,")
    print("     DEPUTADO DISTRITAL (DF), DEPUTADO ESTADUAL (GO)")
    cargo = input("Digite o cargo: ").strip()
    resultados = sistema.buscar_por_cargo(cargo)
    mostrar_lista(sistema, resultados, f"CANDIDATOS AO CARGO: {cargo.upper()}")


def opcao_buscar_por_estado(sistema):
    estado = input("Digite o estado (BR, DF ou GO): ").strip()
    resultados = sistema.buscar_por_estado(estado)
    mostrar_lista(sistema, resultados, f"CANDIDATOS DO ESTADO: {estado.upper()}")


def opcao_propostas_candidato(sistema):
    numero = input("Digite o numero do candidato: ").strip()
    candidato = escolher_candidato(sistema, sistema.buscar_por_numero(numero))
    if candidato:
        mostrar_ficha_com_propostas(sistema, candidato)


def opcao_comparar_propostas(sistema):
    print("Areas disponiveis:")
    for i, a in enumerate(AREAS_PLANO, 1):
        print(f"{i} - {a}")
    escolha = input("Escolha o numero da area: ").strip()
    try:
        area = AREAS_PLANO[int(escolha) - 1]
    except (ValueError, IndexError):
        print("Opcao invalida.")
        return

    nomes_texto = input(
        "Digite os nomes dos candidatos separados por virgula (ex.: LULA, FLAVIO BOLSONARO): "
    ).strip()
    nomes = [n.strip() for n in nomes_texto.split(",") if n.strip()]
    if len(nomes) < 2:
        print("Digite pelo menos dois nomes para comparar.")
        return

    candidatos = []
    for nome in nomes:
        candidato = resolver_candidato_por_nome(sistema, nome)
        if candidato:
            candidatos.append(candidato)

    if len(candidatos) < 2:
        print("Nao foi possivel localizar candidatos suficientes para comparar.")
        return

    comparacao = sistema.comparar_propostas(candidatos, area)

    linha()
    print(f"COMPARATIVO DE PROPOSTAS - {area.upper()}")
    linha()
    for candidato, texto in comparacao:
        print(f"\n{candidato.nome_urna} ({candidato.partido_sigla} - {candidato.cargo}/{candidato.estado})")
        print("-" * 46)
        print(texto if texto else "Sem proposta cadastrada para esta area.")


def exibir_menu():
    linha()
    print("           BUSCACANDIDATO DF-GO (2026)")
    linha()
    print("1  - Buscar candidato por nome ")
    print("2  - Buscar candidato por numero")
    print("3  - Buscar por partido")
    print("4  - Buscar por cargo")
    print("5  - Buscar por estado")
    print("6  - Listar candidatos do DF")
    print("7  - Listar candidatos de GO")
    print("8  - Listar candidatos a Presidente")
    print("9  - Ver propostas de um candidato")
    print("10 - Comparar propostas de candidatos por area")
    print("0  - Sair")
    linha()


def main():
    print("Carregando dados (candidatos e planos de governo)...")
    sistema = SistemaBusca(DIR_DADOS)
    print(f"Dados carregados: {len(sistema.vetor)} candidatos (titulares), "
          f"{len(sistema.propostas)} propostas cadastradas.\n")

    acoes = {
        "1": opcao_buscar_por_nome,
        "2": opcao_buscar_por_numero,
        "3": opcao_buscar_por_partido,
        "4": opcao_buscar_por_cargo,
        "5": opcao_buscar_por_estado,
        "6": lambda s: mostrar_lista(s, s.buscar_por_estado("DF"), "CANDIDATOS DO DF"),
        "7": lambda s: mostrar_lista(s, s.buscar_por_estado("GO"), "CANDIDATOS DE GO"),
        "8": lambda s: mostrar_lista(s, s.listar_presidenciaveis(), "CANDIDATOS A PRESIDENTE"),
        "9": opcao_propostas_candidato,
        "10": opcao_comparar_propostas,
    }

    while True:
        exibir_menu()
        escolha = input("Escolha: ").strip()
        print()

        if escolha == "0":
            print("Fim!")
            sys.exit(0)

        acao = acoes.get(escolha)
        if acao is None:
            print("Opcao invalida.\n")
            continue

        try:
            acao(sistema)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        print()


if __name__ == "__main__":
    main()
