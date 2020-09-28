import pandas as pd
import PySimpleGUIQt as psg

uri_dados = "https://raw.githubusercontent.com/alura-cursos/introducao-a-data-science/master/aula4.3/ratings.csv"
uri_nomes = "https://raw.githubusercontent.com/alura-cursos/introducao-a-data-science/master/aula4.3/movies.csv"

# Lê csv
nomes_filmes = pd.read_csv(uri_nomes)
dados_filmes = pd.read_csv(uri_dados)

# Exclui coluna
dados_filmes = dados_filmes.drop(columns=["userId"])

# Renomeia colunas
dados_filmes.columns = ["filmeId","nota","momento"]
nomes_filmes.columns = ["filmeId","titulo","genêro"]

# Mescla dois dataframes
filmes_famosos = pd.merge(dados_filmes, nomes_filmes, on=["filmeId"], how="inner")

def filtrar(ano=''):   
    is_filmes_ano = filmes_famosos["titulo"].str.contains(ano,regex=False)
    dt = filmes_famosos[is_filmes_ano]

    dt_avaliacoes = pd.DataFrame({})
    
    for titulo in dt["titulo"].unique():
        is_titulo_atual = dt["titulo"].str.contains(titulo,regex=False)
        titulo_atual = dt[is_titulo_atual]
        n_avaliacoes = len(titulo_atual)
        nova_linha = {"Filme":titulo,"N° avaliações":n_avaliacoes}
        dt_avaliacoes = dt_avaliacoes.append(nova_linha,ignore_index=True)

    dt_avaliacoes = dt_avaliacoes.sort_values(by=["N° avaliações"],ascending=False)
    dt_avaliacoes = dt_avaliacoes.set_index("Filme")
    return dt_avaliacoes.head(20)

psg.theme('DarkAmber')

layout = [
    [
        psg.Text("Filmes famoso do ano: ")
    ],
    [
        psg.Input(size=(10,1), key='-ano-', focus = True),
        psg.Button(size=(10,1), button_text='Filtrar'),
    ]
]

window = psg.Window("Fitro de filmes famosos",layout)

while True:
    event, values = window.read()
    if event == "OK" or event == psg.WIN_CLOSED:
        break
    if event == "Filtrar":
        dados = filtrar(values['-ano-'])
        psg.Print(dados)

window.close()