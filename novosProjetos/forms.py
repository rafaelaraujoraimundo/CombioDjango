from django import forms
from novosProjetos.models import Consultoria, Sistemas, Projeto


class ConsultoriaForm(forms.ModelForm):

    class Meta:
        model = Consultoria
        fields = ['nome','valor_hora','total_horas_projetos_pagos','horas_restantes_pagas']


class SistemasForm(forms.ModelForm):

    class Meta:
        model = Sistemas
        fields = ['nome',]


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome_projeto', 'data_entrega', 'horas_utilizadas', 'consultoria', 'sistemas', 'descricao_solucao', 'anexo_escopo', 'anexo_documentacao', 'anexo_fontes','utilizou_horas_pagas']
        widgets = {
            'nome_projeto': forms.TextInput(attrs={'class': 'form-control'}),
            'data_entrega': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'horas_utilizadas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descricao_solucao': forms.Textarea(attrs={'class': 'form-control'}),
            'anexo_escopo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'anexo_documentacao': forms.FileInput(attrs={'class': 'form-control-file'}),
            'anexo_fontes': forms.FileInput(attrs={'class': 'form-control-file'}),
            'utilizou_horas_pagas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

        labels = {
            'nome_projeto': 'Nome do Projeto',
            'data_entrega': 'Data de Entrega',
            'horas_utilizadas': 'Horas Utilizadas',
            'descricao_solucao': 'Descrição da Solução',
            'anexo_escopo': 'Anexo do Escopo',
            'anexo_documentacao': 'Anexo da Documentação',
            'anexo_fontes': 'Anexo dos Fontes',
            'utilizou_horas_pagas': 'Utilizou Horas Já pagas'
        }