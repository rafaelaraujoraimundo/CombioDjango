from django import forms
from .models import AcoesProntuario, Celular, ControleFones, Controlekit, Estoque, Status, TipoItem
from dashboard.models import BiFuncionariosCombio
from django.utils.timezone import now

class TipoItemForm(forms.ModelForm):
    class Meta:
        model = TipoItem
        fields = ['nome']
        labels = {
            'nome': 'Nome do Tipo de Item',
        }
        help_texts = {
            'nome': 'Insira o nome do tipo de item (deve ser único).',
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['nome_status']
        labels = {
            'nome_status': 'Nome do Status',
        }
        help_texts = {
            'nome_status': 'Insira o nome do status (deve ser único).',
        }


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['tipo_item', 'modelo', 'fabricante', 'status', 'observacao', 'local']
        labels = {
            'tipo_item': 'Tipo de Item',
            'modelo': 'Modelo',
            'fabricante': 'Fabricante',
            'status': 'Status',
            'observacao': 'Observação',
            'local': 'Local',
        }
        help_texts = {
            'tipo_item': 'Selecione o tipo de item relacionado.',
            'status': 'Escolha o status atual do item.',
        }

class ControlekitForm(forms.ModelForm):
    class Meta:
        model = Controlekit
        fields = ['matricula', 'usuario', 'data_entrega', 'modelo', 'estabelecimento', 'centro_custo', 'serie', 'data_final']
        labels = {
            'matricula': 'Matrícula',
            'usuario': 'Nome do Usuário',
            'data_entrega': 'Data de Entrega',
            'modelo': 'Modelo',
            'estabelecimento': 'Estabelecimento',
            'centro_custo': 'Centro de Custo',
            'serie': 'Série',
            'data_final': 'Data Final',
        }

    def __init__(self, *args, **kwargs):
        super(ControlekitForm, self).__init__(*args, **kwargs)
        self.fields['data_final'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        data_entrega = cleaned_data.get('data_entrega')

        # Verificar se o mesmo usuário já tem um registro com data_final maior ou igual à nova data de entrega
        if Controlekit.objects.filter(usuario=usuario, data_final__gte=data_entrega).exists():
            raise forms.ValidationError("Esse usuário já possui um kit com uma data final que se sobrepõe à nova data de entrega.")
        
        return cleaned_data


class ControleFonesForm(forms.ModelForm):
    class Meta:
        model = ControleFones
        fields = ['matricula', 'usuario', 'data_entrega', 'modelo', 'estabelecimento', 'centro_custo', 'serie', 'data_final']
        labels = {
            'matricula': 'Matrícula',
            'usuario': 'Nome do Usuário',
            'data_entrega': 'Data de Entrega',
            'modelo': 'Modelo',
            'estabelecimento': 'Estabelecimento',
            'centro_custo': 'Centro de Custo',
            'serie': 'Série',
            'data_final': 'Data Final',
        }

    def __init__(self, *args, **kwargs):
        super(ControleFonesForm, self).__init__(*args, **kwargs)
        self.fields['data_final'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        data_entrega = cleaned_data.get('data_entrega')

        # Verificar se o mesmo usuário já tem um registro com data_final futura
        if ControleFones.objects.filter(usuario=usuario, data_final__gte=data_entrega).exists():
            raise forms.ValidationError("Esse usuário já possui um fone com data de entrega dentro do período de validade.")

        return cleaned_data
    
class CelularForm(forms.ModelForm):
    class Meta:
        model = Celular
        fields = [
            'modelo', 'fabricante', 'numero_serie', 'imei', 'numero_linha',
            'usuario', 'status', 'estabelecimento', 'centro_custo'
        ]
        labels = {
            'modelo': 'Modelo',
            'fabricante': 'Fabricante',
            'numero_serie': 'Número de Série',
            'imei': 'IMEI',
            'numero_linha': 'Número da Linha',
            'usuario': 'Nome do Usuário',
            'status': 'Status',
            'estabelecimento': 'Estabelecimento',
            'centro_custo': 'Centro de Custo'
        }

    def __init__(self, *args, **kwargs):
        super(CelularForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].widget.attrs.update({'list': 'usuarios'})
        self.fields['estabelecimento'].widget.attrs.update({'list': 'estabelecimentos'})
        self.fields['centro_custo'].widget.attrs.update({'list': 'centros_custo'})



class AcoesProntuarioForm(forms.ModelForm):
    class Meta:
        model = AcoesProntuario
        fields = ['acao', 'tipo']
        labels = {
            'acao': 'Ação',
            'tipo': 'Tipo de Ação',
        }