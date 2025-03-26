from django import forms
from .models import (AcoesProntuario, Celular, Computador, ControleFones, Controlekit, Estoque,
    Linha, Monitor, ProntuarioCelular, ProntuarioComputador, ProntuarioLinha, ProntuarioMonitor,
    Status, TipoItem, EstoqueMovimentacao)
from dashboard.models import BiFuncionariosCombio
from django.utils.timezone import now
from administration.models import User

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
        widgets = {
            'data_entrega': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_final': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ControlekitForm, self).__init__(*args, **kwargs)
        self.fields['data_final'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        data_entrega = cleaned_data.get('data_entrega')
    
        if usuario and data_entrega:
            # Obtenha o ID da instância atual, se houver (isto é, se estiver sendo editada)
            current_id = self.instance.id if self.instance.id else None
    
            # Verificar se existe outra instância com o mesmo usuário e data_final futura, excluindo a instância atual
            query = Controlekit.objects.filter(usuario=usuario, data_final__gte=data_entrega)
            if current_id:
                query = query.exclude(id=current_id)
            
            if query.exists():
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
        widgets = {
            'data_entrega': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_final': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ControleFonesForm, self).__init__(*args, **kwargs)
        self.fields['data_final'].widget.attrs['readonly'] = True
    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        data_entrega = cleaned_data.get('data_entrega')

        if usuario and data_entrega:
            # Obtenha o ID da instância atual, se houver (isto é, se estiver sendo editada)
            current_id = self.instance.id if self.instance.id else None

            # Verificar se existe outra instância com o mesmo usuário e data_final futura, excluindo a instância atual
            if ControleFones.objects.filter(usuario=usuario, data_final__gte=data_entrega).exclude(id=current_id).exists():
                raise forms.ValidationError("Esse usuário já possui um fone com data de entrega dentro do período de validade.")

        return cleaned_data
    
class CelularForm(forms.ModelForm):
    class Meta:
        model = Celular
        fields = [
            'modelo', 'fabricante', 'numero_serie', 'imei', 'numero_linha',
            'usuario', 'status', 'estabelecimento', 'centro_custo', 'arquivo_celular'
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
            'centro_custo': 'Centro de Custo',
            'arquivo_celular': 'Upload de Arquivo'
        }
        widgets = {
            'arquivo_celular': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = [
            'numero_serie', 'fabricante', 'modelo', 'patrimonio', 
            'estabelecimento', 'local', 'status', 'localizacao'
        ]
        labels = {
            'numero_serie': 'Número de Série',
            'fabricante': 'Fabricante',
            'modelo': 'Modelo',
            'patrimonio': 'Patrimônio',
            'estabelecimento': 'Estabelecimento',
            'local': 'Local',
            'status': 'Status',
            'localizacao': "Localização"
        }

    def __init__(self, *args, **kwargs):
        super(MonitorForm, self).__init__(*args, **kwargs)
        # Aplicando a classe 'form-control' para estilizar com Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
class AcoesProntuarioForm(forms.ModelForm):
    class Meta:
        model = AcoesProntuario
        fields = ['acao', 'tipo']
        labels = {
            'acao': 'Ação',
            'tipo': 'Tipo de Ação',
        }


class ProntuarioCelularForm(forms.ModelForm):
    class Meta:
        model = ProntuarioCelular
        fields = ['usuario', 'data', 'motivo_ocorrencia', 'acao', 'unidade_destino', 'local']
        labels = {
            'usuario': 'Usuário',
            'data': 'Data',
            'motivo_ocorrencia': 'Motivo da Ocorrência',
            'acao': 'Ação',
            'unidade_destino': 'Unidade de Destino',
            'local': 'Local',
        }

    def __init__(self, *args, **kwargs):
        super(ProntuarioCelularForm, self).__init__(*args, **kwargs)
        # Configurações adicionais, se necessário
        self.fields['usuario'].widget.attrs['class'] = 'form-control'
        self.fields['data'].widget.attrs['class'] = 'form-control'
        self.fields['motivo_ocorrencia'].widget.attrs['class'] = 'form-control'
        self.fields['acao'].widget.attrs['class'] = 'form-control'
        self.fields['unidade_destino'].widget.attrs['class'] = 'form-control'
        self.fields['local'].widget.attrs['class'] = 'form-control'


class ProntuarioMonitorForm(forms.ModelForm):
    class Meta:
        model = ProntuarioMonitor
        fields = ['usuario', 'data', 'motivo_ocorrencia', 'acao', 'unidade_destino', 'local', 'localizacao_destino']
        labels = {
            'usuario': 'Usuário',
            'data': 'Data',
            'motivo_ocorrencia': 'Motivo da Ocorrência',
            'acao': 'Ação',
            'unidade_destino': 'Unidade de Destino (Estabelecimento)',
            'local': 'Centro de Custo (Local)',
            'localizacao_destino': 'Localização de Destino'
        }

    def __init__(self, *args, **kwargs):
        super(ProntuarioMonitorForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].widget.attrs['class'] = 'form-control'
        self.fields['data'].widget.attrs['class'] = 'form-control'
        self.fields['motivo_ocorrencia'].widget.attrs['class'] = 'form-control'
        self.fields['acao'].widget.attrs['class'] = 'form-control'
        self.fields['unidade_destino'].widget.attrs['class'] = 'form-control'
        self.fields['local'].widget.attrs['class'] = 'form-control'
        self.fields['localizacao_destino'].widget.attrs['class'] = 'form-control'


class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = [
            'patrimonio', 'hostname', 'numero_serie', 'fabricante', 'modelo', 
            'processador', 'memoria', 'hd', 'usuario', 'centro_custo', 'estabelecimento', 
            'cargo', 'numero_nota_fiscal', 'fornecedor', 'sistema_operacional', 'status', 'hardware', 'arquivo_computador', 'tipo', 
        ]
        labels = {
            'patrimonio': 'Patrimônio',
            'hostname': 'Hostname',
            'numero_serie': 'Número de Série',
            'fabricante': 'Fabricante',
            'modelo': 'Modelo',
            'processador': 'Processador',
            'memoria': 'Memória',
            'hd': 'HD',
            'usuario': 'Usuário',
            'centro_custo': 'Centro de Custo',
            'estabelecimento': 'Estabelecimento',
            'cargo': 'Cargo',
            'numero_nota_fiscal': 'Número da Nota Fiscal',
            'fornecedor': 'Fornecedor',
            'sistema_operacional': 'Sistema Operacional',
            'status': 'Status',
            'hardware': 'Hardware',
            'arquivo_computador': 'Upload de Arquivos',
            'tipo': 'Tipo',
        }

class ProntuarioComputadorForm(forms.ModelForm):
    class Meta:
        model = ProntuarioComputador
        fields = ['usuario', 'data', 'motivo_ocorrencia', 'acao', 'unidade_destino', 'local']
        labels = {
            'usuario': 'Usuário',
            'data': 'Data',
            'motivo_ocorrencia': 'Motivo da Ocorrência',
            'acao': 'Ação',
            'unidade_destino': 'Unidade de Destino',
            'local': 'Local',
        }


class LinhaForm(forms.ModelForm):
    class Meta:
        model = Linha
        fields = ['numero_linha', 'usuario', 'status', 'estabelecimento', 'centro_custo', 'arquivo_linha']
        labels = {
            'numero_linha': 'Número da Linha',
            'usuario': 'Usuário',
            'status': 'Status',
            'estabelecimento': 'Estabelecimento',
            'centro_custo': 'Centro de Custo',
            'arquivo_linha': 'Upload de Arquivo'
        }
        widgets = {
            'arquivo_linha': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class ProntuarioLinhaForm(forms.ModelForm):
    class Meta:
        model = ProntuarioLinha
        fields = ['usuario', 'data', 'motivo_ocorrencia', 'acao', 'unidade_destino', 'local']
        labels = {
            'usuario': 'Usuário',
            'data': 'Data',
            'motivo_ocorrencia': 'Motivo da Ocorrência',
            'acao': 'Ação',
            'unidade_destino': 'Unidade de Destino',
            'local': 'Local',
        }
        widgets = {
            'data': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
        }

class EstoqueMovimentacaoForm(forms.ModelForm):
    MOTIVO_CHOICES = [
        ('Monday', 'Monday'),
        ('Chamado', 'Chamado'),
        ('Inventário', 'Inventário'),
    ]

    class Meta:
        model = EstoqueMovimentacao
        fields = ['data_movimentacao', 'tipo_movimentacao', 'quantidade', 'motivo', 'nova_contratacao', 'hostname', 'patrimonio', 'observacao']
        labels = {
            'data_movimentacao': 'Data da Movimentação',
            'tipo_movimentacao': 'Tipo de Movimentação',
            'quantidade': 'Quantidade',
            'motivo': 'Motivo',
            'nova_contratacao': 'Nova Contratação (Opcional)',
            'hostname': 'Hostname (Opcional)',
            'patrimonio': 'Patrimônio (Opcional)',
            'observacao': 'Observação (Opcional)',
        }
        widgets = {
            'data_movimentacao': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'tipo_movimentacao': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nova_contratacao': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'hostname': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'patrimonio': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        self.estoque = kwargs.pop('estoque', None) # Captura o usuário logado
        super().__init__(*args, **kwargs)

        # Define a data padrão para hoje caso seja um novo registro
        if not self.instance.pk:
            self.fields['data_movimentacao'].initial = now().date()
            self.fields['quantidade'].initial = 1
        # Tornar os campos opcionais
        self.fields['hostname'].required = False
        self.fields['patrimonio'].required = False

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        tipo_movimentacao = self.cleaned_data.get('tipo_movimentacao') 
        estoque = self.estoque
        print(tipo_movimentacao)
        if quantidade is None:
            raise forms.ValidationError("")

        if quantidade < 1:
            raise forms.ValidationError("A quantidade deve ser maior que 0.")
        
        if tipo_movimentacao == 'saida':  # Se for uma saída, verifica a quantidade em estoque
            if not estoque:
                raise forms.ValidationError("Erro ao verificar o estoque.")
            
            if estoque.quantidade < quantidade:
                raise forms.ValidationError("Quantidade insuficiente em estoque.")

        return quantidade

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.usuario = self.user  # Define automaticamente o usuário logado
        if commit:
            instance.save()
        return instance


class RelatorioMovimentacoesForm(forms.Form):
    data_inicio = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    data_fim = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    tipo_movimentacao = forms.ChoiceField(
        choices=[('', 'Todos')] + EstoqueMovimentacao.TIPO_MOVIMENTACAO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    motivo = forms.ChoiceField(
        choices=[('', 'Todos')] + EstoqueMovimentacao.MOTIVO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nova_contratacao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    estoque = forms.ModelChoiceField(
        queryset=Estoque.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Estoque"
    )