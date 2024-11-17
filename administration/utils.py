from administration.models import Parametro

def buscar_parametro(modulo, codigo):
    """
    Busca o parâmetro pelo módulo e código e retorna o valor convertido conforme o tipo de dado.

    :param modulo: Nome do módulo (string)
    :param codigo: Código do parâmetro (string)
    :return: Valor do parâmetro convertido conforme o tipo, ou None se não encontrado
    """
    try:
        # Busca o parâmetro no banco de dados
        parametro = Parametro.objects.get(modulo=modulo, codigo=codigo)
        
        # Converte o valor conforme o tipo_dado
        if parametro.tipo_dado == 'inteiro':
            return int(parametro.valor)
        elif parametro.tipo_dado == 'booleano':
            return parametro.valor.lower() in ['true', '1', 'yes']
        elif parametro.tipo_dado in ['string', 'secret']:
            return str(parametro.valor)
        else:
            raise ValueError(f"Tipo de dado desconhecido: {parametro.tipo_dado}")
    except Parametro.DoesNotExist:
        raise ValueError(f"Parâmetro com módulo '{modulo}' e código '{codigo}' não encontrado.")