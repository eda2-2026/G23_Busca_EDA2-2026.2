# G23_Busca_EDA2-2026.2
>Repositorio dedicado ao Trabalho 1 na turma de Estruturas de Dados 2 do 2o semestre de 2026.


## Aluno
| Matricula | Aluno           |
| --------- | --------------- |
| 221007715 | Fernanda Santos |

---

# Buscarcandidato2026
![Demonstração do aplicativo](img\eleiçoes.png)
 

 ---

## Sobre  
Sistema de consulta de candidatos e propostas de governo — Eleições 2026 (Presidente, DF e GO) — construído em cima dos dados reais fornecidos pelo TSE.


## Como executar

Requer apenas Python 3.

```bash
cd buscarcandidato/src
python3 main.py
```
## Estruturas de dados usadas

- **Vetor (`list`)**: armazena os candidatos titulares. Vices e suplentes são mantidos em um índice separado.

- **Tabela Hash**: permite a busca rápida pelo `SQ_CANDIDATO`, utilizando endereçamento aberto e sondagem linear.

- **Lista Encadeada**: armazena as propostas de governo por meio de nós encadeados criados manualmente.

- **Quicksort**: ordena os candidatos por nome, preparando os dados para a busca binária.

- **Busca Binária**: realiza buscas exatas pelo nome de urna.

- **Busca Sequencial**: realiza buscas por partido, cargo, estado e nome parcial.


## Imagens 
## Buscar candidato por nome

##  Buscar candidato por numero

![Texto alternativo da imagem](img\1.png)

## Buscar por partido
![Texto alternativo da imagem](img\2.png)

##  Buscar por cargo
![Texto alternativo da imagem](img\03.png)

## Buscar por estado
![Texto alternativo da imagem](img\4.png)

## Listar candidatos 
![Texto alternativo da imagem](img\5.png)

##  Ver propostas de um candidato
![Texto alternativo da imagem](img\6.png)

## Comparar propostas de candidatos por area
![Texto alternativo da imagem](img/10.png)

## Vídeo demonstrativo
[![Texto alternativo](URL_da_imagem_de_capa)](URL_do_video)



