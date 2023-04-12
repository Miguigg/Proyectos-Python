import requests
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from requests.exceptions import HTTPError


def request(idConcello):
    """Obtiene por parametro el id de algun concello y realiza la pedicion a meteogalicia

    :param idConcello: entero que identifica a donde se realiza la peticion
    :return: el objeto jsonResponse o htt_err en caso de que el id no exista
    """
    try:
        url = 'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredMedioPrazo.action?idConc=' + str(idConcello)
        response = requests.get(url)
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        return jsonResponse

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def requestHistorico(dataIni, dataFin, idEst):
    """Con esta funcion buscamos, en funcion de la fecha de inicio y fecha de fin (que por defecto estan puestas para mostrar un año)
        en meteogalicia el historico de datos de una estacion

    :param dataIni: Fecha de inicio de la busqueda
    :param dataFin: Fecha de finalizacion de la busqueda
    :param idEst: Estacion a buscar
    :return: El objeto JSON que nos devuelve meteogalicia
    """
    try:
        url = 'https://servizos.meteogalicia.gal/mgrss/observacion/datosMensuaisEstacionsMeteo.action?dataIni=' + str(
            dataIni) + '&dataFin=' + str(dataFin) + '&idEst=' + str(idEst)
        response = requests.get(url)
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        return jsonResponse

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def getDatosJsonObligatorio(jsonObj):
    """Recibe el objeto json que se obtiene de meteogaliciai y trata los campos de la variable para obtener sus temperaturas
    y las fechas

    :param jsonObj: objeto con los datos del tiempo

    """
    prediccion = jsonObj['predMPrazo']['listaPredDiaMPrazo']

    tempMin = []
    tempMax = []
    tempMedia = []
    dias = []

    for i in prediccion:
        diaActual = i
        for key, value in diaActual.items():
            if key == 'dataPredicion':
                insert, no = value.split('T')
                dias.append(insert)
            elif key == 'tMax':
                tempMax.append(value)
            elif key == 'tMin':
                tempMin.append(value)

    for i, j in zip(tempMax, tempMin):
        res = (i + j) / 2
        tempMedia.append(res)

    graficoObligatoiro(tempMax, tempMin, dias, tempMedia)


def getDatosJsonOpcional(jsonObj):
    """Funcion para tratar el objeto json recibido y quedarnos con las temperaturas maximas y minimas asi como con las fechas

    :param jsonObj: Objeto recibido en la funcion requestHistorico
    """
    valoresTempMax = []
    valoresTempMin = []
    precipitaciones = []
    fechas = []
    tamanho = len(jsonObj['listDatosMensuais'])
    for i in range(tamanho):
        obj = jsonObj['listDatosMensuais'][i]
        for key, value in obj.items():
            if key == 'data':
                fechas.append(value.split('T')[0])
            if key == 'listaEstacions':
                list = value
                for key, value in list[0].items():
                    if key == 'listaMedidas':
                        tamanho2 = len(value)
                        for i in range(tamanho2):
                            objActual = value[i]
                            if objActual['codigoParametro'] == 'TA_MAX_1.5m':
                                valoresTempMax.append(objActual['valor'])
                            if objActual['codigoParametro'] == 'TA_MIN_1.5m':
                                valoresTempMin.append(objActual['valor'])
                            if objActual['codigoParametro'] == 'PP_SUM_1.5m':
                                precipitaciones.append(objActual['valor'])

    graficoOpcional(valoresTempMax, valoresTempMin, fechas,precipitaciones)


"""
    meses = []
    diccionarioMeses = {
        '01': "ene",
        '02': "feb",
        '03': "mar",
        '04': "abr",
        '05': "may",
        '06': "jun",
        '07': "jul",
        '08': "agos",
        '09': "sept",
        '10': "oct",
        '11': "nov",
        '12': "dic"
    }
    print(fechas)
    for i in fechas:
        meses.append(diccionarioMeses.get(str(i[5:7])))
"""


def graficoObligatoiro(tempMax, tempMin, dias, tempMedia):
    """A partir de los datos obtenidos genera una grafica representando las temperaturas maximas, minimas y medias

    :param tempMax: lista con las temperatuas maximas
    :param tempMin: lista con las temperaturas minimas
    :param dias: lista de las fechas en las que se tomaron los datos
    :param tempMedia: temperatura media
    """
    plt.plot(dias, tempMax)
    plt.plot(dias, tempMin, '-.')
    plt.plot(dias, tempMedia, '--')
    plt.plot(dias, tempMax, label="Maxima")
    plt.plot(dias, tempMin, label="Minima")
    plt.plot(dias, tempMedia, label="Media")

    plt.xlabel("Fechas")
    plt.ylabel("Temperaturas")
    plt.title('Evolución temperaturas')
    plt.legend()
    plt.show()


def graficoOpcional(valoresTemperaturaMax, valoresTemperaturaMin, fechas,precipitaciones):
    """Funcion para generar el grafico a partir de los datos

    :param valoresTemperaturaMax: lista con las temperaturas maximas recibidas
    :param valoresTemperaturaMin: lista con las temperaturas minimas
    :param fechas: Lista de fechas en las que se han mirado las temperaturas
    :param precipitaciones: Lista de precipitacoines en las fechas
    """
    figure(figsize=(10, 15))
    plt.plot(fechas, valoresTemperaturaMax)
    plt.plot(fechas, valoresTemperaturaMin)
    plt.plot(fechas, valoresTemperaturaMax, label="Maximas")
    plt.plot(fechas, valoresTemperaturaMin, label="Minimas")
    plt.xlabel("Meses")
    plt.xticks(rotation=25)
    plt.ylabel("Temperaturas")
    plt.title("Evolucion Temperaturas")
    plt.legend()
    plt.show()


    figure(figsize=(10, 15))
    plt.plot(fechas,precipitaciones,label="precipitaciones")
    plt.ylabel("Precipitaciones")
    plt.title("Evolucion precipitaciones")
    plt.xticks(rotation=25)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    opt = False

    while opt != True:
        print("1: Mostrar predicciones a medios plazo del concello 32054:\n2:Mostrar historico entre fechas "
              "'03/02/2018', '06/05/2019\n")
        entrada = input()
        try:
            if int(entrada) != 1 and int(entrada) != 2:
                opt = False
            else:
                opt = True
        except ValueError:
            print("Debes introducir un numero, 1 o 2")

    if int(entrada) == 1:
        json = request(32054)
        getDatosJsonObligatorio(json)

    if int(entrada) == 2:
        json2 = requestHistorico('03/02/2018', '06/05/2019', 10124)
        getDatosJsonOpcional(json2)
