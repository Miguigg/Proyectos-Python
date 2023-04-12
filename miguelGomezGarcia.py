import doctest

from multipledispatch import dispatch


class NotRomanException(TypeError):
    def __init__(self, info, mensaje="Error, el numero debe estar en la lista de los romanos"):
        self.mensaje = mensaje
        self.info = info
        super().__init__(self.mensaje)

        def __str__():
            return f'{self.info}->{self.mensaje}'


class NumerosRomanos:
    """Esta clase recibe como parametros en el constructor un numero romanos, El cual será verificado,
    luego permitirá realizar operaciones con el. Ademas implementa metodos para poder transformar numeros de romano a
     integer y viceversa"""

    def __init__(self, numero1):
        self.validarNumeroRomano(numero1)

        self.__numero1 = numero1

    def getNumero(self):
        return self.__numero1

    def setNumero1(self, numero):
        self.validarNumeroRomano(numero)
        self.__numero1 = numero

    @dispatch(int)
    @staticmethod
    def deIntegerARomano(num):
        """permite transformar un numero de integer a romano. Este se utiliza en las operaciones de esta clase pero
        tambien se puede utilizar fuera.

        :param num: numero para traducir
        :return: un numero romano
        """

        toret = ""
        equivalencias = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]
        for entero, romano in equivalencias:
            cociente, resto = divmod(num, entero)
            toret += romano * cociente
            num = resto
        return toret

    def deRomanoAInteger(self, num=None):
        """Recibe un numero romano, el cual se valida antes de operar, y lo transforma a integer, si no se le pasa un
        parametro, transforma el numero con el que se ha instanciado la clase, si se le pasa, transforma los que se le pasa

        :param num: es un numero romano
        :return: un integer con el valor
        Example:
        -------
        >>> NumerosRomanos.validarNumeroRomano(NumerosRomanos, 'XI')
        True
        >>> NumerosRomanos.validarNumeroRomano(NumerosRomanos, 'AAAA')
        Traceback (most recent call last):
        ...
        NotRomanException: Error, el numero debe estar en la lista de los romanos
        """
        equivalencias = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        toret = 0
        if num is not None:
            num = num.upper()
            if self.validarNumeroRomano(num):
                for i in range(len(num)):
                    if i + 1 < len(num) and equivalencias[num[i]] < equivalencias[
                        num[i + 1]]:  # miramos que no queden mas
                        # numeros para ver si hay que sumar o restar
                        toret = toret - equivalencias[num[i]]
                    else:
                        toret = toret + equivalencias[num[i]]
                return toret
        else:
            num = self.getNumero()
            for i in range(len(num)):
                if i + 1 < len(num) and equivalencias[num[i]] < equivalencias[
                    num[i + 1]]:  # miramos que no queden mas
                    # numeros para ver si hay que sumar o restar
                    toret = toret - equivalencias[num[i]]
                else:
                    toret = toret + equivalencias[num[i]]
            return toret

    def validarNumeroRomano(self, num):
        """comprueba que el numero introducido esta formado en su totalidad por numeros romanos. Tambien valida que no
        tenga mas de tres cifras romanas iguales y que no presente varias V , L o D

        :param num: numero romano entrante
        :return: True si el numero es romano y lanza la excepcion si no lo es
        :raises NotRomanException cuando se introduce un numero que no es romano o una letra
        Examples:
        ---------
        >>> NumerosRomanos.validarNumeroRomano(NumerosRomanos,'VV')
        Traceback (most recent call last):
        ...
        NotRomanException: Error, el numero debe estar en la lista de los romanos

        >>> NumerosRomanos.validarNumeroRomano(NumerosRomanos,'V')
        True
        >>> NumerosRomanos.validarNumeroRomano(NumerosRomanos,'A')
        Traceback (most recent call last):
        ...
        NotRomanException: Error, el numero debe estar en la lista de los romanos
        """
        param = str(num)
        numerosRomanos = ["I", "V", "X", "L", "C", "D", "M"]

        # comprobamos que las letras sean de numero romanos

        for i in range(0, len(param)):
            if not param[i].upper() in numerosRomanos:
                raise NotRomanException("El numero introducido no es un numero romano")

        # Ahora miramos si se repite mas de 3 veces cada numero

        for i in range(0, len(param)):
            numeroActual = param[i].upper()
            if i + 3 < len(param) and numeroActual == param[i + 1].upper() and numeroActual == param[
                i + 2].upper() and numeroActual == param[i + 3]:
                raise NotRomanException("El numero introducido no es un numero romano")

        # Ahora validamos que no se metan elementos como VV, LL o DD seguidas o en distintas posiciones en el numero

        for i in range(0, len(param)):
            if param[i].upper() == 'V' or param[i].upper() == 'L' or param[i].upper() == 'D':
                for j in range(i + 1, len(param)):
                    if param[j].upper() == param[i].upper():
                        raise NotRomanException("El numero introducido no es un numero romano")
        return True;

    # Sobreescribimos operaciones

    def __add__(self, v):
        """Metodo que sobreescribe la accion de sumar y que permite operar con romanos

        :param v: el numero romano a sumar, su no es un objeto de tipo NumerosRomanos saltará una excepcion
        :return: retorna un objeto de tipo NumerosRomanos
        Examples:
        --------
        >>> numero1 = NumerosRomanos('V')
        >>> numero2 = NumerosRomanos('V')
        >>> numerRes = numero1 + numero2
        >>> numerRes.getNumero()
        'X'
        """
        if not isinstance(v, NumerosRomanos):
            raise NotRomanException("Ambos nunmeros deben ser romanos")
        else:
            value1 = self.deRomanoAInteger(self.getNumero())
            value2 = self.deRomanoAInteger(v.getNumero())
            suma = value1 + value2
            toret = NumerosRomanos(self.deIntegerARomano(suma))
            return toret

    def __mul__(self, v):
        """Sobrecarga la multiplicacion para permitir que se relize con numero romanos

        :param v: Numero a multiplicar
        :return: Un objeto de tipo NumerosRomanos
                Examples:
        --------
        >>> numero1 = NumerosRomanos('V')
        >>> numero2 = NumerosRomanos('II')
        >>> numerRes = numero1 * numero2
        >>> numerRes.getNumero()
        'X'
        """
        if not isinstance(v, NumerosRomanos):
            raise NotRomanException("Los numeros deben ser romanos")
        else:
            value1 = self.deRomanoAInteger(self.getNumero())
            value2 = self.deRomanoAInteger(v.getNumero())
            mult = value1 * value2
            toret = NumerosRomanos(self.deIntegerARomano(mult))
            return toret

    def __sub__(self, v):
        """Operacion que permite realizar la resta entre dos objetos de numero romano, obligatriamente se deben de
        usar valores cuyo resultado sea positivo

        :param v: Numero romano a restar
        :return: Objeto de tipo numero romano
        xamples:
        --------
        >>> numero1 = NumerosRomanos('VI')
        >>> numero2 = NumerosRomanos('V')
        >>> numerRes = numero1 - numero2
        >>> numerRes.getNumero()
        'I'
        """
        if not isinstance(v, NumerosRomanos):
            raise NotRomanException("Los numeros deben ser romanos")
        else:
            value1 = self.deRomanoAInteger(self.getNumero())
            value2 = self.deRomanoAInteger(v.getNumero())
            res = value1 - value2
            if res < 1:
                raise NotRomanException("El resultado no se puede representar, es 0 o inferior")
            else:
                toret = NumerosRomanos(self.deIntegerARomano(res))
                return toret

    def __floordiv__(self, v):
        """Operacion que permite realizar divisiones enteras, nunca con decimales ya que no se pueden motrar con
        numero romanos, siempre obteniendo un resultado mayor que 0

        :param v: Numero entre el que dividir
        :return: cociente
                Examples:
        --------
        >>> numero1 = NumerosRomanos('V')
        >>> numero2 = NumerosRomanos('V')
        >>> numerRes = numero1 // numero2
        >>> numerRes.getNumero()
        'I'
        """
        if not isinstance(v, NumerosRomanos):
            raise NotRomanException("El operando 2 debe ser romano")
        else:
            value1 = self.deRomanoAInteger(self.getNumero())
            value2 = self.deRomanoAInteger(v.getNumero())
            floorDiv = value1 // value2
            if floorDiv < 1:
                raise NotRomanException("El resultado no se puede representar, es 0 o inferior")
            else:
                toret = NumerosRomanos(self.deIntegerARomano(floorDiv))
                return toret


if __name__ == '__main__':
    num1 = NumerosRomanos('CMXIX')
    print(num1.deRomanoAInteger())

    # inicializacion de numeros
    num2 = NumerosRomanos('XI')
    num3 = NumerosRomanos('X')

    # operaciones
    suma = num2 + num3
    resta = num2 - num3
    mult = num2 * num3
    floorDiv = num2 // num3

    # resultados
    print(mult.getNumero())
    print(resta.getNumero())
    print(suma.getNumero())
    print(floorDiv.getNumero())
    print("-----------------------------")


    #doctest.testmod(verbose=True)
