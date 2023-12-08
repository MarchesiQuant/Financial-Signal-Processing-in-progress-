# FUNCIONES:

# 1) FUNCION DE INDEXACION

# A partir de un df maestro, indexa los datos correspondientes a cada epoca 

def index_epoch(df, epochs, ratio, i):
    """""
    Indexa los datos de la epoca correspondiente 

    df: dataframe maestro
    epochs: numero de epocas
    ratio: proporcion optimizacion-test (test/opt)
    i: epoca actual (de 0 a epochs-1)

    Autor: Pablo Marchesi 2023
    """
    epochs = epochs-1
    D = round(len(df)/epochs)
    current_epoch = df.iloc[i*D:(i+1)*D-1,:]
    Dopt = round(len(current_epoch)*(1-ratio))
    opt_df = current_epoch.iloc[0:Dopt-1,:]
    test_df = current_epoch.iloc[Dopt:,:]
    
    return test_df, opt_df 
 

# 2) FUNCION DE OPTIMIZACION:

def opt(df, strategy, cons, method = 'grid', goal = 'Return (Ann.) [%]', com = 0):

    """"
    Optimiza una estrategia para una accion (df) dada, devuelve los mejores parametros (wc)
    Se puede elegir el metodo de optimizacion ("grid o "skopt")
    Se puede elegir el objetivo de optimizacion
    Se puede añadir un parametro de comisiones 
    Ejemplo cons: cons = list(np.arange(0.01,0.25,0.01))

    NOTA: no admite mas de un parametro de optimizacion, hay que mejorarlo 
    NOTA2: lo ideal sería indexar el periodo que toca desde el df maestro en lugar de descargar cada vez 
    NOTA3: necesario un try-except por si acaso

    Autor: Pablo Marchesi 2023
    """
    from backtesting import Backtest

    # Llamada al backtesting
    iCash = 100000
    bt = Backtest(df, strategy, cash = iCash, commission = com, exclusive_orders = True)

    # Llamada al proceso de optimizacion 
    stats, heatmap = bt.optimize(wc = cons, return_heatmap = True, maximize = goal, method = method)
    results = heatmap.sort_values(ascending=False)
    best_params = results.keys()[0][0]
    return best_params


# 3) FUNCION TEST:

def test(df, strategy, com = 0):

    """
    Testea una estrategia en el periodo y en la accion dados por el df

    Autor: Pablo Marchesi 2023
    """

    from backtesting import Backtest

    iCash = 100000
    bt = Backtest(df, strategy, cash = iCash, commission = com, exclusive_orders = True)
    output = bt.run()

    mu = output['Return (Ann.) [%]']
    sigma = output['Volatility (Ann.) [%]']
    ntrades = output['# Trades']
    equity = output['_equity_curve']

    return equity, mu, sigma, ntrades 
