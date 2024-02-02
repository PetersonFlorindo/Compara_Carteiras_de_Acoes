import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plotter

def main():
    lista_nomes_carteiras = []
    cont = int(input('Quantas carteiras deseja analisar?'))

    #lista carteiras analisadas
    for i in range(cont):
        lista_nomes_carteiras.append(input('Digite o nome do '+str(i+1)+'º arquivo xlsx:'))

    #gera carteira e prepara para exibição
    for i in lista_nomes_carteiras:
        plotter.plot(gera_carteira(i)['Valor_Cota'], label='Rentabilidade da cateira '+i)

    plota_graficos()

def plota_graficos ():
    plotter.axhline(y=1, color='r', linestyle='-')
    plotter.legend()
    plotter.xlabel('Data')
    plotter.ylabel('Rentabilidade acumulada')
    plotter.show()

def rentabilidade_ibova(carteira_df):
    indice = yf.download('^BVSP', start=carteira_df.index[0], end=date.today())['Adj Close']
    indice_df = pd.DataFrame(indice)
    indice_df['Retorno'] = 0

    for i, data in enumerate(indice_df.index):
        if i == 0:
            indice_df.at[data, 'Índice'] = 1
        else:
            indice_df.at[data, 'Índice'] = (indice_df.iloc[i]['Adj Close']/indice_df.iloc[0]['Adj Close'])

    plotter.plot(indice_df['Índice'], label='índice IBOV')


def gera_carteira (nome_carteira):

    #obtendo dados da planilha com os dados de investimento
    carteira_xlsx = pd.read_excel(f'{nome_carteira}.xlsx')

    carteira_df = carteira_xlsx.pivot_table(carteira_xlsx, index=['Data'], columns=['Ativo'], aggfunc=np.sum, fill_value=0)

    #nota: a função pivot table neste caso retorna um data frame multindex onde cada linha contém dois valor (quantidade e ativo)

    #Extrai nome dos ativos do Dataframe Multindex e transforma em uma lista
    ativos = carteira_df.columns.get_level_values('Ativo').to_list()

    #busca os preços ajustados de fechamento dos ativos
    precos = yf.download(ativos, start = carteira_df.index[0], end=date.today())['Adj Close']
    precos = precos.rename_axis('Data', axis='index')


    #reindexa a carteira de investimento com as datas vindas do dataframe de preços
    carteira_data_completa = carteira_df.reindex(index=precos.index)

    #preenche valor vazio com 0
    carteira_data_completa.fillna(value=0, inplace=True)

    #acumula quantidades investidas
    carteira_acumulada = carteira_data_completa.cumsum()

    #transformando precos em multindex
    precos.columns = pd.MultiIndex.from_product([['Preço'], precos.columns])

    #multiplica os dataframes com os preços e as quantidade dos ativos
    carteira_acumulada *= precos.reindex(carteira_acumulada.index.get_level_values('Data'))['Preço'].to_numpy()

    #cria coluna com total investido
    carteira_acumulada['Total'] = carteira_acumulada.sum(axis=1)

    #cria registro dos aportes diários
    aporte = carteira_data_completa*precos.reindex(carteira_acumulada.index.get_level_values('Data'))['Preço'].to_numpy()
    aporte = aporte.sum(axis=1)

    #cotizando carteira de ações

    for i, data in enumerate(aporte.index):
        if i == 0:
            # define valores para a data0
            carteira_acumulada.at[data, 'Valor_Cota'] = 1
            carteira_acumulada.at[data, 'Quantidade_de_Cotas'] = carteira_acumulada.loc[data]['Total'].to_numpy()
        else:
            # se houve aporte
            if aporte[data] != 0:
                # quantidade de cotas atual = quantidade que eu tinha + quantidade de cotas que estou aportando
                carteira_acumulada.at[data, 'Quantidade_de_Cotas'] = carteira_acumulada.iloc[i-1] + aporte[data]/carteira_acumulada.iloc[i - 1]['Valor_Cota']
                # valor da cota = total investido / quantidade de cotas
                carteira_acumulada.at[data, 'Valor_Cota'] = carteira_acumulada.iloc[i]['Total'].to_numpy()/carteira_acumulada.loc[data]['Quantidade_de_Cotas'].to_numpy()
                carteira_acumulada.at[data, 'Retorno'] = (carteira_acumulada.iloc[i]['Valor_Cota'].to_numpy() /carteira_acumulada.iloc[i - 1]['Valor_Cota'].to_numpy()) - 1
            else:
                # quantidade de cotas atual = quantidade que eu tinha + quantidade de cotas que estou aportando
                carteira_acumulada.at[data, 'Quantidade_de_Cotas'] = carteira_acumulada.iloc[i - 1]
                # valor da cota = total investido / quantidade de cotas
                carteira_acumulada.at[data, 'Valor_Cota'] = carteira_acumulada.iloc[i]['Total'].to_numpy() /carteira_acumulada.loc[data]['Quantidade_de_Cotas'].to_numpy()
                carteira_acumulada.at[data, 'Retorno'] = (carteira_acumulada.iloc[i]['Valor_Cota'].to_numpy() /carteira_acumulada.iloc[i - 1]['Valor_Cota'].to_numpy()) - 1
    carteira_acumulada.fillna(value=0, inplace=True)
    return carteira_acumulada


if __name__ == "__main__":
    main()