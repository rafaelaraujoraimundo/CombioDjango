from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from administration.models import User
import os
import pandas as pd

def pasta_upload(instance, filename):
    # Gera o caminho para a pasta de upload com base no ID do modelo e no nome do arquivo
    nome_arquivo = os.path.basename(filename)
    return f'uploads/finalizados/{instance.id}/{nome_arquivo}'


class Arquivo(models.Model):
    arquivo_original = models.FileField(upload_to='uploads/')
    data_processamento = models.DateTimeField(default=timezone.now)
    arquivo_final = models.FileField(upload_to=pasta_upload)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return os.path.basename(self.arquivo_original.name)

    def processar_arquivo(self):
        # Realize aqui o processamento necessário no arquivo original
        # Neste exemplo, vou apenas adicionar um prefixo ao nome do arquivo final
        nome_arquivo_final = 'processado_' + \
            os.path.basename(self.arquivo_original.name)

        # Crie o conteúdo do arquivo final (neste exemplo, será o mesmo do arquivo original)
        conteudo_arquivo_final = self.arquivo_original.read()

        # Salve o arquivo final
        self.arquivo_final.save(
            nome_arquivo_final, ContentFile(conteudo_arquivo_final))




def pasta_upload_ativo(instance, filename):
    nome_arquivo = os.path.basename(filename)
    return f'uploads/finalizados/ativos/{instance.id}/{nome_arquivo}'

class ArquivoAtivo(models.Model):
    arquivo_original = models.FileField(upload_to='uploads/')
    data_processamento = models.DateTimeField(default=timezone.now)
    arquivo_final = models.FileField(upload_to=pasta_upload_ativo)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return os.path.basename(self.arquivo_original.name)

    def processar_arquivo(self):
        import pandas as pd
        # Lendo dados da planilha
        data = pd.read_excel(self.arquivo_original.file)
        column_config = {
            'Nro Sequencial Bem': '9(08)',
            'Empresa': 'x(3)',
            'Conta Patrimonial': 'x(18)',
            'Bem Patrimonial': '9(09)',
            'Sequência Bem': '9(05)',
            'Descrição Bem Pat': 'x(40)',
            'Número Plaqueta': 'x(20)',
            'Quantidade Bens Representados': '9(08)',
            'Periodicidade': 'x(14)',
            'Data Aquisição': '99/99/9999',
            'Estabelecimento': 'x(5)',
            'Espécie Bem Patrimonial': 'x(6)',
            'Marca': 'x(6)',
            'Modelo': 'x(8)',
            'Licença Uso': 'x(12)',
            'Especificação Técnica': 'x(8)',
            'Estado Físico': 'x(8)',
            'Arrendador': 'x(6)',
            'Contrato Leasing': 'x(12)',
            'Fornecedor': '9(06)',
            'Localização': 'x(12)',
            'Responsável': 'x(12)',
            'Último Inventário': '99/99/9999',
            'Narrativa Bem': 'x(2000)',
            'Seguradora': 'x(8)',
            'Apólice Seguro': 'x(12)',
            'Início Valid Apólice': '99/99/9999',
            'Fim Validade Apólice': '99/99/9999',
            'Prêmio Seguro': '9(12),99',
            'Docto Entrada': 'x(16)',
            'Numero Item': '9(06)',
            'Pessoa Garantia': '9(09)',
            'Inicio Garantia': '99/99/9999',
            'Fim Garantia': '99/99/9999',
            'Termo Garantia': 'x(2000)',
            'Grupo Cálculo': 'x(6)',
            'Data Movimento': '99/99/9999',
            'Perc Baixado': '9(3),99',
            'Início Cálculo Dpr': '99/99/9999',
            'Data Cálculo': '99/99/9999',
            'Série Nota': 'x(5)',
            'Envia PIMS Detalhado': 'yes/no',
            'Bem Importado': 'yes/no',
            'Credita PIS': 'yes/no',
            'Credita COFINS': 'yes/no',
            'Nro Parcelas Crédito PIS/COFINS': '9(03)',
            'Parcelas Descontadas': '9(03)',
            'Valor Crédito PIS': '9(9),99',
            'Valor Crédito COFINS': '9(9),99',
            'Credita CSLL': 'yes/no',
            'Exercícios Crédito CSLL': '9(02)',
            'Valor Base PIS': '9(9),99',
            'Valor Base COFINS': '9(9),99'
        }

        formatted_data = []
        for index, row in data.iterrows():
            formatted_row = []
            for col, value in row.items():
                format_type = column_config.get(col, 'x')
                if 'x' in format_type:
                    max_length = int(format_type.split('(')[-1].strip(')'))
                    formatted_value = f'"{str(value)[:max_length]}"' if pd.notna(value) else '""'
                elif format_type == '99/99/9999':
                    if pd.notna(value):
                        formatted_value = value.strftime('%d/%m/%Y')  # Formatação de data correta
                    else:
                        formatted_value = '""'
                elif '9' in format_type or '9(12),99' in format_type:
                    formatted_value = str(value) if pd.notna(value) else '0'
               
                elif format_type == 'yes/no':
                    formatted_value = value if pd.notna(value) and value.strip() != '' else '?'
                formatted_row.append(formatted_value)
            formatted_data.append(' '.join(formatted_row))
  
        
        # Criando o arquivo final
        final_content = '\n'.join(formatted_data)
        nome_arquivo_final = 'processado_' + os.path.basename(self.arquivo_original.name) + '.txt'
        self.arquivo_final.save(nome_arquivo_final, ContentFile(final_content.encode('utf-8')))

def pasta_upload_ativo_valores(instance, filename):
    return f'uploads/finalizados/ativos/{instance.id}/{os.path.basename(filename)}'

class AtivoValores(models.Model):
    arquivo_original = models.FileField(upload_to='uploads/')
    data_processamento = models.DateTimeField(default=timezone.now)
    arquivo_final = models.FileField(upload_to=pasta_upload_ativo_valores)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return os.path.basename(self.arquivo_original.name)

    def processar_arquivo(self):
        data = pd.read_excel(self.arquivo_original.file)
        
        column_config = {
            'Nro Sequencial Bem': '9(08)',
            'Sequência Incorp': '9(08)',
            'Cenário Contábil': 'x(8)',
            'Finalidade': 'x(10)',
            'Valor Original': '9(12),99',
            'Correção Monetária': '9(12),99',
            'Dpr Valor Original': '9(12),99',
            'Dpr Correção Monet': '9(12),99',
            'Correção Monet Dpr': '9(12),99',
            'Depreciação Incentiv': '9(12),99',
            'Dpr Incentiv CM': '9(12),99',
            'CM Dpr Incentivada': '9(12),99',
            'Amortização VO': '9(12),99',
            #'Amortização CM': '9(12),99',
            #'CM Amortização': '9(12),99',
            #'Amortizacao Incentiv': '9(12),99',
            #'Amort Incentiv CM': '9(12),99',
            ##'CM Amort Incentvda': '9(12),99',
            #'Percentual Dpr': '9(5),9999',
            #'Perc Dpr Incentivada': '9(5),9999',
            #'Perc Dpr Redução Saldo': '9(5),9999',
            #'Quantidade Vida Útil': '9(10),99',
        }

        formatted_data = []
        for index, row in data.iterrows():
            formatted_row = []
            for col, value in row.items():
                format_type = column_config.get(col, 'x')
                if 'x' in format_type:
                    max_length = int(format_type.split('(')[-1].strip(')'))
                    formatted_value = f'"{str(value)[:max_length]}"' if pd.notna(value) else '""'
                elif format_type == '99/99/9999':
                    if pd.notna(value):
                        formatted_value = value.strftime('%d/%m/%Y')  # Formatação de data correta
                    else:
                        formatted_value = '""'
                elif '9' in format_type or '9(12),99' in format_type:
                    formatted_value = str(value) if pd.notna(value) else '0'
               
                elif format_type == 'yes/no':
                    formatted_value = value if pd.notna(value) and value.strip() != '' else '?'
                formatted_row.append(formatted_value)
            formatted_data.append(' '.join(formatted_row))

        
        final_content = '\n'.join(formatted_data)
        nome_arquivo_final = 'processado_valores_' + os.path.basename(self.arquivo_original.name) + '.txt'
        self.arquivo_final.save(nome_arquivo_final, ContentFile(final_content.encode('utf-8')))