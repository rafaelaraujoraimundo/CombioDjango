# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AlertaSsmaV2(models.Model):
    # Field name made lowercase.
    id = models.IntegerField(db_column='ID', primary_key=True)
    nome_responsavel_sol = models.TextField(blank=True, null=True)
    estabelecimento = models.TextField(blank=True, null=True)
    codigo_estabelecimento = models.TextField(blank=True, null=True)
    data_ocorrencia = models.TextField(blank=True, null=True)
    hora_ocorrencia = models.TextField(blank=True, null=True)
    origem_ocorrencia = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    parteafetada = models.TextField(
        db_column='parteAfetada', blank=True, null=True)
    lateralidade = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    tipolesao = models.TextField(db_column='tipoLesao', blank=True, null=True)
    empresa = models.TextField(blank=True, null=True)
    experiencia = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    tempocombio = models.TextField(
        db_column='tempoCombio', blank=True, null=True)
    periodo = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    diasemana = models.TextField(db_column='diaSemana', blank=True, null=True)
    hora_trabalhada = models.TextField(blank=True, null=True)
    genero = models.TextField(blank=True, null=True)
    idade = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    tipoprocesso = models.TextField(
        db_column='tipoProcesso', blank=True, null=True)
    # Field name made lowercase.
    regravida = models.TextField(db_column='regraVida', blank=True, null=True)
    # Field name made lowercase.
    tipoocorpatr = models.TextField(
        db_column='tipoOcorPatr', blank=True, null=True)
    # Field name made lowercase.
    tipoacidente = models.TextField(
        db_column='tipoAcidente', blank=True, null=True)
    # Field name made lowercase.
    tipodado = models.TextField(db_column='tipoDado', blank=True, null=True)
    descricao_ocorrencia = models.TextField(blank=True, null=True)
    potencial = models.TextField(blank=True, null=True)
    info_relevantes = models.TextField(blank=True, null=True)
    num_atividade = models.TextField(blank=True, null=True)
    usuario_responsavel = models.TextField(blank=True, null=True)
    usuario_solicitante = models.TextField(blank=True, null=True)
    nome_anexo_tabela = models.TextField(blank=True, null=True)
    numero_solicitacao = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alerta_ssma_v2'


class BiCentroCusto(models.Model):
    # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=22)
    # Field name made lowercase.
    descricaocusto = models.CharField(
        db_column='descricaoCusto', max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_centro_custo'


class BiChamadosServiceUp(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    ticket_number = models.CharField(max_length=50)
    age = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    created_by = models.IntegerField()
    changed = models.DateTimeField()
    changed_by = models.IntegerField()
    closed = models.DateTimeField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    type_name = models.CharField(max_length=50, blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    owner_name = models.CharField(max_length=200, blank=True, null=True)
    responsible_id = models.IntegerField(blank=True, null=True)
    responsible_name = models.CharField(max_length=50, blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    queue_id = models.IntegerField(blank=True, null=True)
    queue_name = models.CharField(max_length=50)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=50, blank=True, null=True)
    state_type = models.CharField(max_length=50, blank=True, null=True)
    priority_id = models.IntegerField(blank=True, null=True)
    priority_name = models.CharField(max_length=50)
    service_id = models.IntegerField(blank=True, null=True)
    service_name = models.CharField(max_length=255, blank=True, null=True)
    sla_id = models.IntegerField(blank=True, null=True)
    sla_name = models.CharField(max_length=50, blank=True, null=True)
    customer_user = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    ticket_lock_id = models.CharField(max_length=11, blank=True, null=True)
    ticket_lock_name = models.CharField(max_length=50, blank=True, null=True)
    time_account = models.IntegerField(blank=True, null=True)
    until_time = models.IntegerField(blank=True, null=True)
    escalation_destination_in = models.CharField(
        max_length=20, blank=True, null=True)
    escalation_destination_date = models.DateTimeField(blank=True, null=True)
    escalation_time_working_time = models.CharField(
        max_length=20, blank=True, null=True)
    escalation_time = models.CharField(max_length=20, blank=True, null=True)
    escalation_response_time = models.IntegerField(blank=True, null=True)
    escalation_update_time = models.IntegerField(blank=True, null=True)
    escalation_solution_time = models.IntegerField(blank=True, null=True)
    first_response_time_escalation = models.CharField(
        max_length=20, blank=True, null=True)
    first_response_time_notification = models.CharField(
        max_length=20, blank=True, null=True)
    first_response_time_destination_time = models.CharField(
        max_length=20, blank=True, null=True)
    first_response_time_destination_date = models.CharField(
        max_length=20, blank=True, null=True)
    first_response_time_working_time = models.CharField(
        max_length=20, blank=True, null=True)
    first_response_time = models.CharField(
        max_length=20, blank=True, null=True)
    update_time_escalation = models.CharField(
        max_length=20, blank=True, null=True)
    update_time_notification = models.CharField(
        max_length=20, blank=True, null=True)
    update_time_destination_time = models.CharField(
        max_length=20, blank=True, null=True)
    update_time_destination_date = models.DateTimeField(blank=True, null=True)
    update_time_working_time = models.CharField(
        max_length=20, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time_escalation = models.CharField(
        max_length=20, blank=True, null=True)
    solution_time_notification = models.CharField(
        max_length=20, blank=True, null=True)
    solution_time_destination_time = models.CharField(
        max_length=20, blank=True, null=True)
    solution_time_destination_date = models.DateTimeField(
        blank=True, null=True)
    solution_time_working_time = models.CharField(
        max_length=20, blank=True, null=True)
    solution_time = models.CharField(max_length=20, blank=True, null=True)
    first_response = models.DateTimeField(blank=True, null=True)
    first_response_in_min = models.CharField(
        max_length=20, blank=True, null=True)
    first_response_diff_min = models.CharField(
        max_length=20, blank=True, null=True)
    solution_in_min = models.CharField(max_length=20, blank=True, null=True)
    solution_diff_in_min = models.CharField(
        max_length=20, blank=True, null=True)
    first_lock = models.DateTimeField(blank=True, null=True)
    unlock_timeout = models.CharField(max_length=50, blank=True, null=True)
    real_till_time_not_used = models.IntegerField(blank=True, null=True)
    number_of_articles = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    change_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bi_chamados_service_up'


class BiContaContabil(models.Model):
    conta = models.CharField(max_length=40)
    descricao = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_conta_contabil'


class BiEfz1005Cep(models.Model):
    conta = models.CharField(max_length=40)
    # Field name made lowercase.
    descricaoconta = models.CharField(
        db_column='descricaoConta', max_length=120, blank=True, null=True)
    # Field name made lowercase.
    datarealizado = models.DateField(
        db_column='dataRealizado', blank=True, null=True)
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    # Field name made lowercase.
    valorrealizado = models.CharField(
        db_column='valorRealizado', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    mediorecebimento = models.CharField(
        db_column='medioRecebimento', max_length=17, blank=True, null=True)
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    # Field name made lowercase.
    historicomodulo = models.CharField(
        db_column='historicoModulo', max_length=500, blank=True, null=True)
    # Field name made lowercase.
    ordemmanutencao = models.IntegerField(
        db_column='ordemManutencao', blank=True, null=True)
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    # Field name made lowercase.
    unidadenegocio = models.CharField(
        db_column='unidadeNegocio', max_length=16, blank=True, null=True)
    # Field name made lowercase.
    centrocusto = models.CharField(
        db_column='centroCusto', max_length=24, blank=True, null=True)
    # Field name made lowercase.
    descricaocusto = models.CharField(
        db_column='descricaoCusto', max_length=60, blank=True, null=True)
    # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    # Field name made lowercase.
    descricaoitem = models.CharField(
        db_column='descricaoItem', max_length=80, blank=True, null=True)
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    # Field name made lowercase.
    observacao = models.CharField(
        db_column='Observacao', max_length=15000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_efz1005_cep'


class BiEfz1005Completo(models.Model):
    conta = models.CharField(max_length=40)
    # Field name made lowercase.
    descricaoconta = models.CharField(
        db_column='descricaoConta', max_length=120, blank=True, null=True)
    # Field name made lowercase.
    datarealizado = models.DateField(
        db_column='dataRealizado', blank=True, null=True)
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    # Field name made lowercase.
    valorrealizado = models.CharField(
        db_column='valorRealizado', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    mediorecebimento = models.CharField(
        db_column='medioRecebimento', max_length=17, blank=True, null=True)
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    # Field name made lowercase.
    historicomodulo = models.CharField(
        db_column='historicoModulo', max_length=500, blank=True, null=True)
    # Field name made lowercase.
    ordemmanutencao = models.IntegerField(
        db_column='ordemManutencao', blank=True, null=True)
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    # Field name made lowercase.
    unidadenegocio = models.CharField(
        db_column='unidadeNegocio', max_length=16, blank=True, null=True)
    # Field name made lowercase.
    centrocusto = models.CharField(
        db_column='centroCusto', max_length=24, blank=True, null=True)
    # Field name made lowercase.
    descricaocusto = models.CharField(
        db_column='descricaoCusto', max_length=60, blank=True, null=True)
    # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    # Field name made lowercase.
    descricaoitem = models.CharField(
        db_column='descricaoItem', max_length=80, blank=True, null=True)
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    # Field name made lowercase.
    observacao = models.CharField(
        db_column='Observacao', max_length=15000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_efz1005_completo'


class BiEfz1005Folha(models.Model):
    conta = models.CharField(max_length=40)
    # Field name made lowercase.
    descricaoconta = models.CharField(
        db_column='descricaoConta', max_length=120, blank=True, null=True)
    # Field name made lowercase.
    datarealizado = models.DateField(
        db_column='dataRealizado', blank=True, null=True)
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    # Field name made lowercase.
    valorrealizado = models.CharField(
        db_column='valorRealizado', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    mediorecebimento = models.CharField(
        db_column='medioRecebimento', max_length=17, blank=True, null=True)
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    # Field name made lowercase.
    historicomodulo = models.CharField(
        db_column='historicoModulo', max_length=500, blank=True, null=True)
    # Field name made lowercase.
    ordemmanutencao = models.IntegerField(
        db_column='ordemManutencao', blank=True, null=True)
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    # Field name made lowercase.
    unidadenegocio = models.CharField(
        db_column='unidadeNegocio', max_length=16, blank=True, null=True)
    # Field name made lowercase.
    centrocusto = models.CharField(
        db_column='centroCusto', max_length=24, blank=True, null=True)
    # Field name made lowercase.
    descricaocusto = models.CharField(
        db_column='descricaoCusto', max_length=60, blank=True, null=True)
    # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    # Field name made lowercase.
    descricaoitem = models.CharField(
        db_column='descricaoItem', max_length=80, blank=True, null=True)
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    # Field name made lowercase.
    observacao = models.CharField(
        db_column='Observacao', max_length=15000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_efz1005_folha'


class BiEfz1005Oi(models.Model):
    conta = models.CharField(max_length=40, blank=True, null=True)
    # Field name made lowercase.
    descricaoconta = models.CharField(
        db_column='descricaoConta', max_length=120, blank=True, null=True)
    # Field name made lowercase.
    datarealizado = models.DateField(
        db_column='dataRealizado', blank=True, null=True)
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    # Field name made lowercase.
    valorrealizado = models.CharField(
        db_column='valorRealizado', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    mediorecebimento = models.CharField(
        db_column='medioRecebimento', max_length=17, blank=True, null=True)
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    # Field name made lowercase.
    historicomodulo = models.CharField(
        db_column='historicoModulo', max_length=500, blank=True, null=True)
    # Field name made lowercase.
    ordemmanutencao = models.IntegerField(
        db_column='ordemManutencao', blank=True, null=True)
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    # Field name made lowercase.
    unidadenegocio = models.CharField(
        db_column='unidadeNegocio', max_length=16, blank=True, null=True)
    # Field name made lowercase.
    centrocusto = models.CharField(
        db_column='centroCusto', max_length=24, blank=True, null=True)
    # Field name made lowercase.
    descricaocusto = models.CharField(
        db_column='descricaoCusto', max_length=60, blank=True, null=True)
    # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    # Field name made lowercase.
    descricaoitem = models.CharField(
        db_column='descricaoItem', max_length=80, blank=True, null=True)
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    # Field name made lowercase.
    observacao = models.CharField(
        db_column='Observacao', max_length=15000, blank=True, null=True)
    ordem_investimento = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_efz1005_oi'


class BiEstabelecimento(models.Model):
    # Field name made lowercase.
    estabelecimento = models.CharField(
        db_column='ESTABELECIMENTO', max_length=10, blank=True, null=True)
    # Field name made lowercase.
    sigla_unidade = models.CharField(
        db_column='SIGLA_UNIDADE', max_length=30, blank=True, null=True)
    # Field name made lowercase.
    nome_unidade = models.CharField(
        db_column='NOME_UNIDADE', max_length=80, blank=True, null=True)
    endereco = models.CharField(max_length=70, blank=True, null=True)
    bairro = models.CharField(max_length=120, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    pais = models.CharField(max_length=40, blank=True, null=True)
    # Field name made lowercase.
    regional = models.CharField(
        db_column='Regional', max_length=4000, blank=True, null=True)
    # Field name made lowercase.
    ie = models.CharField(db_column='IE', max_length=38, blank=True, null=True)
    # Field name made lowercase.
    nome_fantasia = models.CharField(
        db_column='NOME_FANTASIA', max_length=80, blank=True, null=True)
    # Field name made lowercase.
    cnpj = models.CharField(
        db_column='CNPJ', max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_estabelecimento'


class BiEstabelecimentoCcusto(models.Model):
    # The composite primary key (cod_empresa, cod_estab, cod_ccusto) found, that is not supported. The first column is selected.
    cod_empresa = models.CharField(primary_key=True, max_length=6)
    cod_estab = models.CharField(max_length=10)
    nom_abrev = models.CharField(max_length=30, blank=True, null=True)
    cod_ccusto = models.CharField(max_length=22)
    des_tit_ctbl = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_estabelecimento_ccusto'
        unique_together = (('cod_empresa', 'cod_estab', 'cod_ccusto'),)


class BiItensSinc(models.Model):
    codigo = models.CharField(primary_key=True, max_length=32)
    # Field name made lowercase.
    unitem = models.CharField(
        db_column='unItem', max_length=4, blank=True, null=True)
    descricao = models.CharField(max_length=120, blank=True, null=True)
    narrativa = models.CharField(max_length=4000, blank=True, null=True)
    # Field name made lowercase.
    tipocontr = models.IntegerField(
        db_column='tipoContr', blank=True, null=True)
    # Field name made lowercase.
    ctcodigo = models.CharField(
        db_column='ctCodigo', max_length=40, blank=True, null=True)
    ncm = models.CharField(max_length=20, blank=True, null=True)
    # Field name made lowercase.
    codobsoleto = models.IntegerField(
        db_column='codObsoleto', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_itens_sinc'


class BiOrdemInvestimentoCompromissado(models.Model):
    # Field name made lowercase.
    ordem_investimento = models.IntegerField(
        db_column='ORDEM_INVESTIMENTO', blank=True, null=True)
    # Field name made lowercase.
    ordem_compra = models.IntegerField(
        db_column='ORDEM_COMPRA', blank=True, null=True)
    # Field name made lowercase.
    cod_item = models.CharField(
        db_column='COD_ITEM', max_length=32, blank=True, null=True)
    # Field name made lowercase.
    desc_item = models.CharField(
        db_column='DESC_ITEM', max_length=120, blank=True, null=True)
    # Field name made lowercase.
    preco_fornecedor_unitario = models.CharField(
        db_column='PRECO_FORNECEDOR_UNITARIO', max_length=20, blank=True, null=True)
    # Field name made lowercase.
    qtd = models.CharField(
        db_column='QTD', max_length=20, blank=True, null=True)
    # Field name made lowercase.
    centrocusto = models.CharField(
        db_column='centroCusto', max_length=24, blank=True, null=True)
    data_ordem = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_ordem_investimento_compromissado'


class BiOrdemInvestimentoOrcado(models.Model):
    # Field name made lowercase.
    filial = models.CharField(
        db_column='FILIAL', max_length=10, blank=True, null=True)
    # Field name made lowercase.
    ordem_investimento = models.IntegerField(
        db_column='ORDEM_INVESTIMENTO', blank=True, null=True)
    # Field name made lowercase.
    desc_projeto = models.CharField(
        db_column='DESC_PROJETO', max_length=80, blank=True, null=True)
    # Field name made lowercase.
    desc_ordem = models.CharField(
        db_column='DESC_ORDEM', max_length=80, blank=True, null=True)
    sigla = models.CharField(max_length=30, blank=True, null=True)
    # Field name made lowercase.
    situacao_ordem_invest = models.CharField(
        db_column='SITUACAO_ORDEM_INVEST', max_length=25, blank=True, null=True)
    # Field name made lowercase.
    ccusto = models.CharField(
        db_column='CCUSTO', max_length=40, blank=True, null=True)
    # Field name made lowercase.
    desc_centro = models.CharField(
        db_column='DESC_CENTRO', max_length=80, blank=True, null=True)
    # Field name made lowercase.
    verba_original = models.CharField(
        db_column='VERBA_ORIGINAL', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    verba_atual = models.CharField(
        db_column='VERBA_ATUAL', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    valor_compromissado = models.CharField(
        db_column='VALOR_COMPROMISSADO', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    valor_realizado = models.CharField(
        db_column='VALOR_REALIZADO', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    valor_saldo = models.CharField(
        db_column='VALOR_SALDO', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    saldo_compromissado = models.CharField(
        db_column='SALDO_COMPROMISSADO', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    usuario_responsavel = models.CharField(
        db_column='USUARIO_RESPONSAVEL', max_length=24, blank=True, null=True)
    # Field name made lowercase.
    saldo_oi = models.CharField(
        db_column='SALDO_OI', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    ano_emissao = models.IntegerField(
        db_column='ANO_EMISSAO', blank=True, null=True)
    # Field name made lowercase.
    datainivalidade = models.DateField(
        db_column='DataIniValidade', blank=True, null=True)
    # Field name made lowercase.
    datafimvalidade = models.DateField(
        db_column='dataFimValidade', blank=True, null=True)
    # Field name made lowercase.
    dataemissao = models.DateField(
        db_column='DataEmissao', blank=True, null=True)
    # Field name made lowercase.
    dataliberacao = models.DateField(
        db_column='DataLiberacao', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_ordem_investimento_orcado'


class BiTi(models.Model):
    # Field name made lowercase.
    ticket = models.IntegerField(db_column='TICKET', primary_key=True)
    # Field name made lowercase.
    nome_fantasia_do_cliente = models.CharField(
        db_column='NOME_FANTASIA_DO_CLIENTE', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    tipo_do_ticket = models.CharField(
        db_column='TIPO_DO_TICKET', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    status_do_ticket = models.CharField(
        db_column='STATUS_DO_TICKET', max_length=100, blank=True, null=True)
    data_de_criacao_do_ticket = models.DateTimeField(
        db_column='DATA_DE_CRIACAO_DO_TICKET', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_da_solucao = models.CharField(
        db_column='DATA_DA_SOLUCAO', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    nome_do_tecnico = models.CharField(
        db_column='NOME_DO_TECNICO', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    nome_da_categoria_primaria = models.CharField(
        db_column='NOME_DA_CATEGORIA_PRIMARIA', max_length=100, blank=True, null=True)
    nome_da_categoria_secundaria = models.CharField(
        db_column='NOME_DA_CATEGORIA_SECUNDARIA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    contato_do_ticket = models.CharField(
        db_column='CONTATO_DO_TICKET', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    descricao_do_setor = models.CharField(
        db_column='DESCRICAO_DO_SETOR', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    descricao_do_ticket = models.CharField(
        db_column='DESCRICAO_DO_TICKET', max_length=15200, blank=True, null=True)
    data_do_primeiro_atendimento = models.CharField(
        db_column='DATA_DO_PRIMEIRO_ATENDIMENTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_de_saida = models.CharField(
        db_column='DATA_DE_SAIDA', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_ti'


class BiTiAbertos(models.Model):
    # Field name made lowercase.
    ticket = models.IntegerField(db_column='TICKET', primary_key=True)
    # Field name made lowercase.
    nome_fantasia_do_cliente = models.CharField(
        db_column='NOME_FANTASIA_DO_CLIENTE', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    tipo_do_ticket = models.CharField(
        db_column='TIPO_DO_TICKET', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    status_do_ticket = models.CharField(
        db_column='STATUS_DO_TICKET', max_length=100, blank=True, null=True)
    data_de_criacao_do_ticket = models.DateTimeField(
        db_column='DATA_DE_CRIACAO_DO_TICKET', blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_da_solucao = models.CharField(
        db_column='DATA_DA_SOLUCAO', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    nome_do_tecnico = models.CharField(
        db_column='NOME_DO_TECNICO', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    nome_da_categoria_primaria = models.CharField(
        db_column='NOME_DA_CATEGORIA_PRIMARIA', max_length=100, blank=True, null=True)
    nome_da_categoria_secundaria = models.CharField(
        db_column='NOME_DA_CATEGORIA_SECUNDARIA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    contato_do_ticket = models.CharField(
        db_column='CONTATO_DO_TICKET', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    descricao_do_setor = models.CharField(
        db_column='DESCRICAO_DO_SETOR', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    descricao_do_ticket = models.CharField(
        db_column='DESCRICAO_DO_TICKET', max_length=15000, blank=True, null=True)
    data_do_primeiro_atendimento = models.CharField(
        db_column='DATA_DO_PRIMEIRO_ATENDIMENTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # Field name made lowercase.
    data_de_saida = models.CharField(
        db_column='DATA_DE_SAIDA', max_length=100, blank=True, null=True)
    # Field name made lowercase.
    data_atualizacao = models.DateTimeField(
        db_column='DATA_ATUALIZACAO', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_ti_abertos'


class DimItem(models.Model):
    # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)
    # Field renamed to remove unsuitable characters.
    desc_item = models.CharField(
        db_column='desc-item', max_length=120, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    data_ult_ent = models.DateField(
        db_column='data-ult-ent', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_item'


class DimRegiao(models.Model):
    # Field name made lowercase.
    cod_estab = models.IntegerField(
        db_column='COD_ESTAB', blank=True, null=True)
    # Field name made lowercase.
    regiao = models.CharField(
        db_column='REGIAO', max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_regiao'


class DimTipFluxo(models.Model):
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    des_tip_fluxo_financ = models.CharField(max_length=80)
    ind_tip_secao_fluxo_cx = models.CharField(max_length=22)
    ind_fluxo_movto_financ = models.CharField(max_length=14)
    cod_plano_cta_ctbl = models.CharField(max_length=16, blank=True, null=True)
    cod_cta_ctbl = models.CharField(max_length=40, blank=True, null=True)
    dat_inic_valid = models.DateField()
    dat_fim_valid = models.DateField()
    num_niv_tip_fluxo_financ = models.IntegerField()
    num_clas_tip_fluxo_financ = models.IntegerField()
    ind_tip_lancto_livro_cx = models.CharField(
        max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_tip_fluxo'


class Efz1005(models.Model):
    conta = models.CharField(max_length=40)
    # Field name made lowercase.
    descricaoconta = models.CharField(
        db_column='descricaoConta', max_length=120, blank=True, null=True)
    # Field name made lowercase.
    datarealizado = models.DateField(
        db_column='dataRealizado', blank=True, null=True)
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    # Field name made lowercase.
    valorrealizado = models.CharField(
        db_column='valorRealizado', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    mediorecebimento = models.CharField(
        db_column='medioRecebimento', max_length=17, blank=True, null=True)
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    # Field name made lowercase.
    historicomodulo = models.CharField(
        db_column='historicoModulo', max_length=500, blank=True, null=True)
    # Field name made lowercase.
    ordemmanutencao = models.IntegerField(
        db_column='ordemManutencao', blank=True, null=True)
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    # Field name made lowercase.
    unidadenegocio = models.CharField(
        db_column='unidadeNegocio', max_length=16, blank=True, null=True)
    # Field name made lowercase.
    centrocusto = models.CharField(
        db_column='centroCusto', max_length=24, blank=True, null=True)
    # Field name made lowercase.
    descricaocusto = models.CharField(
        db_column='descricaoCusto', max_length=60, blank=True, null=True)
    emitente = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    # Field name made lowercase.
    descricaoitem = models.CharField(
        db_column='descricaoItem', max_length=80, blank=True, null=True)
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    # Field name made lowercase.
    observacao = models.CharField(
        db_column='Observacao', max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'efz1005'


class EpmDif(models.Model):
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epm_dif'


class EpmPart(models.Model):
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epm_part'


class EpmProd(models.Model):
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)
    start_value = models.FloatField(blank=True, null=True)
    end_value = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epm_prod'


class EsAbastecimentoDieselUpv(models.Model):
    numero_solicitacao = models.IntegerField(primary_key=True)
    utilizacao_maquina_d = models.CharField(
        max_length=200, blank=True, null=True)
    horario_abastecimento = models.CharField(
        max_length=16, blank=True, null=True)
    horimetro_abastecimento = models.CharField(
        max_length=50, blank=True, null=True)
    volume_abastecido = models.CharField(max_length=17, blank=True, null=True)
    nf_diesel = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_abastecimento_diesel_upv'


class EsCaldeiraCombioUpv(models.Model):
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    parada_caldeira_redu_consu = models.CharField(
        max_length=10, blank=True, null=True)
    data_interrupcao_vapor = models.DateField(blank=True, null=True)
    hora_interrupcao_vapor = models.CharField(
        max_length=16, blank=True, null=True)
    data_retorno_caldeira = models.DateField(blank=True, null=True)
    hora_liberacao_manutencao = models.CharField(
        max_length=16, blank=True, null=True)
    hora_retorno_vapor = models.CharField(max_length=16, blank=True, null=True)
    comentar_detalhadamente_parada = models.CharField(
        max_length=120, blank=True, null=True)
    raiz_causou_parada = models.CharField(
        max_length=500, blank=True, null=True)
    outros_causa_raiz = models.CharField(max_length=500, blank=True, null=True)
    detalhes_causa_raiz = models.CharField(
        max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_caldeira_combio_upv'


class EsCaldeiraCombioUpvTeste(models.Model):
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    parada_caldeira_redu_consu = models.CharField(
        max_length=10, blank=True, null=True)
    data_interrupcao_vapor = models.DateField(blank=True, null=True)
    hora_interrupcao_vapor = models.CharField(
        max_length=16, blank=True, null=True)
    data_retorno_caldeira = models.DateField(blank=True, null=True)
    hora_liberacao_manutencao = models.CharField(
        max_length=16, blank=True, null=True)
    hora_retorno_vapor = models.CharField(max_length=16, blank=True, null=True)
    comentar_detalhadamente_parada = models.CharField(
        max_length=120, blank=True, null=True)
    raiz_causou_parada = models.CharField(
        max_length=500, blank=True, null=True)
    outros_causa_raiz = models.CharField(max_length=500, blank=True, null=True)
    detalhes_causa_raiz = models.CharField(
        max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_caldeira_combio_upv_teste'


class EsCentroCusto(models.Model):
    cod_ccusto = models.CharField(max_length=120, blank=True, null=True)
    des_tit_ctbl = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_centro_custo'


class EsContaContabil(models.Model):
    cod_cta_ctbl = models.CharField(max_length=120, blank=True, null=True)
    des_tit_ctbl = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_conta_contabil'


class EsFolhaBi(models.Model):
    # The composite primary key (mes, ano, cdn_funcionario, cdn_estab, cdn_empresa, Evento) found, that is not supported. The first column is selected.
    mes = models.IntegerField(primary_key=True)
    ano = models.IntegerField()
    cdn_funcionario = models.IntegerField()
    cdn_estab = models.CharField(max_length=200)
    cdn_empresa = models.CharField(max_length=6)
    # Field name made lowercase.
    evento = models.CharField(db_column='Evento', max_length=16)
    # Field renamed to remove unsuitable characters.
    tipo_movto = models.BigIntegerField(
        db_column='tipo-movto', blank=True, null=True)
    quantidade = models.CharField(max_length=18, blank=True, null=True)
    horas = models.CharField(max_length=18, blank=True, null=True)
    base = models.CharField(max_length=18, blank=True, null=True)
    valor = models.CharField(max_length=18, blank=True, null=True)
    nom_funcionario = models.CharField(max_length=120, blank=True, null=True)
    dat_admis_func = models.DateField(blank=True, null=True)
    dat_desligto_func = models.DateField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    plano_lotacao = models.CharField(
        db_column='plano-lotacao', max_length=16, blank=True, null=True)
    cod_unid_lotac = models.CharField(max_length=16, blank=True, null=True)
    des_unid_lotac = models.CharField(max_length=80, blank=True, null=True)
    sindicato = models.CharField(max_length=16, blank=True, null=True)
    des_sindicato = models.CharField(max_length=80, blank=True, null=True)
    cod_turno = models.CharField(max_length=16, blank=True, null=True)
    cod_turma = models.CharField(max_length=16, blank=True, null=True)
    desc_turno = models.CharField(max_length=80, blank=True, null=True)
    unid_negoc = models.CharField(max_length=16, blank=True, null=True)
    des_unid_negoc = models.CharField(max_length=80, blank=True, null=True)
    cod_pais = models.CharField(max_length=16, blank=True, null=True)
    localidade = models.CharField(max_length=16, blank=True, null=True)
    des_localidade = models.CharField(max_length=80, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    mao_de_obra = models.CharField(
        db_column='mao-de-obra', max_length=16, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    desc_mao_de_obra = models.CharField(
        db_column='desc_mao-de-obra', max_length=80, blank=True, null=True)
    desc_categ_sal = models.CharField(max_length=80, blank=True, null=True)
    cod_cargo = models.CharField(max_length=16, blank=True, null=True)
    cod_nivel = models.CharField(max_length=16, blank=True, null=True)
    des_nivel = models.CharField(max_length=80, blank=True, null=True)
    fpas = models.CharField(max_length=24, blank=True, null=True)
    tomador = models.CharField(max_length=16, blank=True, null=True)
    desc_tomador = models.CharField(max_length=80, blank=True, null=True)
    sat = models.CharField(max_length=17, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    desc_evento = models.CharField(
        db_column='desc-evento', max_length=80, blank=True, null=True)
    usuario = models.CharField(max_length=24, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    hora = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_folha_bi'
        unique_together = (('mes', 'ano', 'cdn_funcionario',
                           'cdn_estab', 'cdn_empresa', 'evento'),)


class EsFuncionario(models.Model):
    nome_funcionario = models.CharField(max_length=200, blank=True, null=True)
    # The composite primary key (cpf_funcionario, cpf_superior) found, that is not supported. The first column is selected.
    cpf_funcionario = models.CharField(primary_key=True, max_length=16)
    cpf_superior = models.CharField(max_length=38)
    nome_superior = models.CharField(max_length=200, blank=True, null=True)
    codigo_cargo = models.IntegerField(blank=True, null=True)
    descricao_cargo = models.CharField(max_length=200, blank=True, null=True)
    nivel_hierarquico = models.CharField(max_length=200, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    diretoria = models.CharField(max_length=200, blank=True, null=True)
    filial = models.CharField(max_length=6, blank=True, null=True)
    email_funcionario = models.CharField(max_length=200, blank=True, null=True)
    sexo = models.CharField(max_length=40, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_admissao = models.DateField(blank=True, null=True)
    data_demissao = models.DateField(blank=True, null=True)
    data_transferencia = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_funcionario'
        unique_together = (('cpf_funcionario', 'cpf_superior'),)


class EsInssBi(models.Model):
    # The composite primary key (cdn_estab, mes, ano) found, that is not supported. The first column is selected.
    cdn_estab = models.CharField(primary_key=True, max_length=10)
    mes = models.IntegerField()
    ano = models.IntegerField()
    # Field name made lowercase.
    empregadosnormal = models.CharField(
        db_column='empregadosNormal', max_length=17, blank=True, null=True)
    segurados = models.CharField(max_length=17, blank=True, null=True)
    autonomos = models.CharField(max_length=17, blank=True, null=True)
    recisao = models.CharField(max_length=17, blank=True, null=True)
    # Field name made lowercase.
    vlrecolhesegurados = models.CharField(
        db_column='vlRecolheSegurados', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    vlrecolhefamilia = models.CharField(
        db_column='vlRecolheFamilia', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    baserecolhimentogeral = models.CharField(
        db_column='baseRecolhimentoGeral', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    vlrecolheautonomos = models.CharField(
        db_column='vlRecolheAutonomos', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    vlrecolheempresa = models.CharField(
        db_column='vlRecolheEmpresa', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    vlrecolhesat = models.CharField(
        db_column='vlRecolheSAT', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    vlrecolheterceiros = models.CharField(
        db_column='vlRecolheTerceiros', max_length=17, blank=True, null=True)
    # Field name made lowercase.
    totalliquido = models.CharField(
        db_column='totalLiquido', max_length=17, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_inss_bi'
        unique_together = (('cdn_estab', 'mes', 'ano'),)


class EsLinhaAmarelaUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    selecionar_maquina = models.CharField(max_length=70, blank=True, null=True)
    informar_horimetro_maquina = models.CharField(
        max_length=100, blank=True, null=True)
    houve_ocorrencia_maquina = models.CharField(
        max_length=5, blank=True, null=True)
    hora_inicio_indisponibilidade = models.CharField(
        max_length=16, blank=True, null=True)
    hora_termino_indisponibilidade = models.CharField(
        max_length=16, blank=True, null=True)
    comentarios_relacao_maquina = models.CharField(
        max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_linha_amarela_upv'


class EsMudancaMixUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    horario_mudanca_mix = models.CharField(
        max_length=16, blank=True, null=True)
    mix_utilizado_volumetrica = models.CharField(
        max_length=30, blank=True, null=True)
    outros_mix_utili_propor = models.CharField(
        max_length=150, blank=True, null=True)
    comentario_relacao_caldeira = models.CharField(
        max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_mudanca_mix_upv'


class EsOcorrenciasCaldeiraUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    informe_ocorrencia = models.CharField(max_length=70, blank=True, null=True)
    outros_ocorrencia_caldeira = models.CharField(
        max_length=500, blank=True, null=True)
    descreva_detalha_ocorrencia = models.CharField(
        max_length=1000, blank=True, null=True)
    inicio_ocorrencia = models.CharField(max_length=16, blank=True, null=True)
    termino_ocorrencia = models.CharField(max_length=16, blank=True, null=True)
    ocorrencia_afetou = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_ocorrencias_caldeira_upv'


class EsPedidoEmergencial(models.Model):
    # The composite primary key (numero_solicitacao, pedido) found, that is not supported. The first column is selected.
    numero_solicitacao = models.IntegerField(primary_key=True)
    processo = models.CharField(max_length=40, blank=True, null=True)
    tipo_recebimento = models.CharField(max_length=40, blank=True, null=True)
    pedido = models.IntegerField()
    num_nf = models.CharField(max_length=20, blank=True, null=True)
    serie_nf = models.CharField(max_length=10, blank=True, null=True)
    cod_estabelecimento = models.CharField(
        max_length=16, blank=True, null=True)
    estabelecimento = models.CharField(max_length=60, blank=True, null=True)
    cod_emitente = models.IntegerField(blank=True, null=True)
    emitente = models.CharField(max_length=40, blank=True, null=True)
    emitente_nome = models.CharField(max_length=80, blank=True, null=True)
    chave_acesso = models.CharField(max_length=130, blank=True, null=True)
    data_emissao = models.DateField(blank=True, null=True)
    data_entrada = models.DateField(blank=True, null=True)
    data_vencimento = models.DateField(blank=True, null=True)
    comprado_por = models.CharField(max_length=100, blank=True, null=True)
    cod_condicao_pagamento = models.IntegerField(blank=True, null=True)
    condicao_pagamento = models.CharField(max_length=80, blank=True, null=True)
    valor_total_ipi = models.FloatField(blank=True, null=True)
    valor_total_nf = models.FloatField(blank=True, null=True)
    valor_total_produtos = models.FloatField(blank=True, null=True)
    aprovacao = models.CharField(max_length=24, blank=True, null=True)
    aprovador_nivel_1 = models.CharField(max_length=24, blank=True, null=True)
    aprovador_nivel_2 = models.CharField(max_length=24, blank=True, null=True)
    motivo_compra = models.CharField(max_length=120, blank=True, null=True)
    justificativa = models.CharField(max_length=500, blank=True, null=True)
    status_aprovacao = models.CharField(max_length=36, blank=True, null=True)
    status_recebimento = models.CharField(max_length=36, blank=True, null=True)
    data_abertura = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_pedido_emergencial'
        unique_together = (('numero_solicitacao', 'pedido'),)


class EsRelatorioProducaoUpv(models.Model):
    acionar_caldeira_cliente = models.CharField(
        max_length=100, blank=True, null=True)
    comentarios_sobre_cascas = models.TextField(blank=True, null=True)
    comentarios_sobre_cinzas = models.TextField(blank=True, null=True)
    comentarios_sobre_finos = models.TextField(blank=True, null=True)
    comentario_consumo_biomassa = models.TextField(blank=True, null=True)
    comentario_mix = models.TextField(blank=True, null=True)
    comentar_detalhadamente_parada = models.TextField(blank=True, null=True)
    detalhes_causa_raiz = models.TextField(blank=True, null=True)
    equipe_aprov = models.TextField(blank=True, null=True)
    equipe_coments = models.TextField(blank=True, null=True)
    esta_chovendo = models.CharField(max_length=100, blank=True, null=True)
    foi_necessario_abastecer = models.CharField(
        max_length=100, blank=True, null=True)
    gestor_aprov = models.CharField(max_length=100, blank=True, null=True)
    gestor_coments = models.TextField(blank=True, null=True)
    houve_mudanca_mix = models.CharField(max_length=100, blank=True, null=True)
    houve_ocorrencia_caldeira = models.CharField(
        max_length=100, blank=True, null=True)
    houve_remocao_cascas = models.CharField(
        max_length=100, blank=True, null=True)
    houve_remocao_finos = models.CharField(
        max_length=100, blank=True, null=True)
    localizacao = models.CharField(max_length=500, blank=True, null=True)
    mix_utilizado_proporcao = models.CharField(
        max_length=100, blank=True, null=True)
    nf_cascas = models.CharField(max_length=100, blank=True, null=True)
    nf_finos = models.CharField(max_length=100, blank=True, null=True)
    nf_residuos = models.CharField(max_length=100, blank=True, null=True)
    outros_causa_raiz = models.TextField(blank=True, null=True)
    outros_mix_utilizado = models.TextField(blank=True, null=True)
    parada_caldeira_combio = models.CharField(
        max_length=100, blank=True, null=True)
    parada_caldeira_redu_consu = models.CharField(
        max_length=500, blank=True, null=True)
    possui_maquina = models.CharField(max_length=100, blank=True, null=True)
    raiz_causou_parada = models.CharField(
        max_length=500, blank=True, null=True)
    remocao_cacamba_turno = models.CharField(
        max_length=100, blank=True, null=True)
    responsavel_conferencia = models.CharField(
        max_length=500, blank=True, null=True)
    responsavel_preenchimento = models.CharField(
        max_length=500, blank=True, null=True)
    unidade = models.CharField(max_length=500, blank=True, null=True)
    data_interrupcao_vapor = models.DateField(blank=True, null=True)
    data_preenchimento = models.DateField(blank=True, null=True)
    consumo_biomassa_tonelada = models.CharField(
        max_length=17, blank=True, null=True)
    consumo_tonelada = models.CharField(max_length=17, blank=True, null=True)
    conversao = models.CharField(max_length=17, blank=True, null=True)
    eficiencia_anterior = models.CharField(
        max_length=17, blank=True, null=True)
    estoque_total_tonelada = models.CharField(
        max_length=17, blank=True, null=True)
    pressao_vapor_turno = models.CharField(
        max_length=17, blank=True, null=True)
    qtd_cascas = models.CharField(max_length=17, blank=True, null=True)
    qtd_cinzas_geradas = models.CharField(max_length=17, blank=True, null=True)
    qtd_finos = models.CharField(max_length=17, blank=True, null=True)
    total_final_agua = models.CharField(max_length=17, blank=True, null=True)
    total_final_balanca = models.CharField(
        max_length=17, blank=True, null=True)
    total_final_vapor = models.CharField(max_length=17, blank=True, null=True)
    total_inicial_vapor = models.CharField(
        max_length=17, blank=True, null=True)
    total_inicio_agua = models.CharField(max_length=17, blank=True, null=True)
    total_inici_balanca = models.CharField(
        max_length=17, blank=True, null=True)
    total_vapor_vendido = models.CharField(
        max_length=17, blank=True, null=True)
    codigo_formulario = models.IntegerField(blank=True, null=True)
    numero_solicitacao = models.IntegerField(primary_key=True)
    comentario_geral = models.TextField(blank=True, null=True)
    hora_interrupcao_vapor = models.CharField(
        max_length=16, blank=True, null=True)
    hora_liberacao_manutencao = models.CharField(
        max_length=16, blank=True, null=True)
    hora_retorno_vapor = models.CharField(max_length=16, blank=True, null=True)
    inicio_caldeira_cliente = models.CharField(
        max_length=16, blank=True, null=True)
    termino_caldeira_cliente = models.CharField(
        max_length=16, blank=True, null=True)
    total_combio = models.CharField(max_length=17, blank=True, null=True)
    total_levedura = models.CharField(max_length=17, blank=True, null=True)
    data_retorno_caldeira = models.DateField(blank=True, null=True)
    hora_entrada = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_relatorio_producao_upv'


class EsRemocaoCascasUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_cascas = models.CharField(max_length=17, blank=True, null=True)
    nf_cascas = models.CharField(max_length=20, blank=True, null=True)
    comentarios_sobre_cascas = models.CharField(
        max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_cascas_upv'


class EsRemocaoCinzasUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_cinzas_geradas = models.CharField(
        max_length=100, blank=True, null=True)
    nf_residuos = models.CharField(max_length=20, blank=True, null=True)
    comentarios_sobre_cinzas = models.CharField(
        max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_cinzas_upv'


class EsRemocaoFinosUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_finos = models.DecimalField(
        max_digits=17, decimal_places=5, blank=True, null=True)
    nf_finos = models.CharField(max_length=100, blank=True, null=True)
    comentarios_sobre_finos = models.CharField(
        max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_finos_upv'


class EsRemocaoRedlerUpv(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_cinzas_redler = models.DecimalField(
        max_digits=17, decimal_places=2, blank=True, null=True)
    comentarios_cinzas_redler = models.CharField(
        max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_redler_upv'


class EstrutTipFinanc(models.Model):
    cod_tip_fluxo_financ_pai = models.CharField(max_length=24)
    cod_tip_fluxo_financ_filho = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'estrut_tip_financ'


class FatMovtoFluxoCx(models.Model):
    cod_estab = models.IntegerField()
    dat_movto_fluxo_cx = models.DateField()
    ind_fluxo_movto_cx = models.CharField(max_length=6)
    # Field name made lowercase.
    cod_cenario = models.IntegerField(
        db_column='Cod_cenario', blank=True, null=True)
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    des_tip_fluxo_financ = models.CharField(max_length=80)
    val_movto_fluxo_cx = models.CharField(max_length=100)
    # Field name made lowercase.
    regiao = models.CharField(
        db_column='REGIAO', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fat_movto_fluxo_cx'


class FatSaldo(models.Model):
    # Field renamed to remove unsuitable characters.
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)
    # Field renamed to remove unsuitable characters.
    cod_depos = models.CharField(db_column='cod-depos', max_length=6)
    # Field renamed to remove unsuitable characters.
    qtidade_atu = models.DecimalField(
        db_column='qtidade-atu', max_digits=19, decimal_places=4)
    # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)

    class Meta:
        managed = False
        db_table = 'fat_saldo'


class Item(models.Model):
    # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(
        db_column='it-codigo', primary_key=True, max_length=32)
    # Field renamed to remove unsuitable characters.
    desc_item = models.CharField(
        db_column='desc-item', max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class OrdemCompra(models.Model):
    # Field renamed to remove unsuitable characters.
    numero_ordem = models.IntegerField(
        db_column='numero-ordem', primary_key=True)
    # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)
    natureza = models.IntegerField()
    situacao = models.IntegerField()
    origem = models.IntegerField()
    # Field renamed to remove unsuitable characters.
    op_codigo = models.IntegerField(db_column='op-codigo')
    # Field renamed to remove unsuitable characters.
    data_emissao = models.DateField(db_column='data-emissao')
    # Field renamed to remove unsuitable characters.
    ct_codigo = models.CharField(db_column='ct-codigo', max_length=40)
    # Field renamed to remove unsuitable characters.
    sc_codigo = models.CharField(db_column='sc-codigo', max_length=40)
    requisitante = models.CharField(max_length=24)
    # Field renamed to remove unsuitable characters.
    dep_almoxar = models.CharField(db_column='dep-almoxar', max_length=6)
    # Field renamed to remove unsuitable characters.
    ordem_servic = models.IntegerField(db_column='ordem-servic')
    # Field renamed to remove unsuitable characters.
    cod_comprado = models.CharField(db_column='cod-comprado', max_length=24)
    narrativa = models.CharField(max_length=4000)
    # Field renamed to remove unsuitable characters.
    num_pedido = models.IntegerField(db_column='num-pedido')
    # Field renamed to remove unsuitable characters.
    data_pedido = models.DateField(
        db_column='data-pedido', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_emitente = models.IntegerField(db_column='cod-emitente')
    # Field renamed to remove unsuitable characters.
    data_cotacao = models.DateField(
        db_column='data-cotacao', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    preco_orig = models.CharField(db_column='preco-orig', max_length=20)
    # Field renamed to remove unsuitable characters.
    preco_unit = models.CharField(db_column='preco-unit', max_length=20)
    # Field renamed to remove unsuitable characters.
    pre_unit_for = models.CharField(db_column='pre-unit-for', max_length=20)
    # Field renamed to remove unsuitable characters.
    preco_fornec = models.CharField(db_column='preco-fornec', max_length=20)
    # Field renamed to remove unsuitable characters.
    nr_alt_preco = models.IntegerField(db_column='nr-alt-preco')
    # Field renamed to remove unsuitable characters.
    mo_codigo = models.IntegerField(db_column='mo-codigo')
    # Field renamed to remove unsuitable characters. This field type is a guess.
    codigo_ipi = models.TextField(db_column='codigo-ipi')
    # Field renamed to remove unsuitable characters.
    aliquota_ipi = models.CharField(db_column='aliquota-ipi', max_length=17)
    # Field renamed to remove unsuitable characters.
    codigo_icm = models.IntegerField(db_column='codigo-icm')
    # Field renamed to remove unsuitable characters.
    aliquota_icm = models.CharField(db_column='aliquota-icm', max_length=17)
    # Field renamed to remove unsuitable characters.
    aliquota_iss = models.CharField(db_column='aliquota-iss', max_length=17)
    frete = models.TextField()  # This field type is a guess.
    # Field renamed to remove unsuitable characters.
    valor_frete = models.CharField(db_column='valor-frete', max_length=19)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    taxa_financ = models.TextField(db_column='taxa-financ')
    # Field renamed to remove unsuitable characters.
    valor_taxa = models.CharField(db_column='valor-taxa', max_length=19)
    # Field renamed to remove unsuitable characters.
    saldo_emb = models.CharField(
        db_column='saldo-emb', max_length=17, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    perc_descto = models.CharField(db_column='perc-descto', max_length=20)
    # Field renamed to remove unsuitable characters.
    saldo_gi = models.CharField(
        db_column='saldo-gi', max_length=17, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_cond_pag = models.IntegerField(db_column='cod-cond-pag')
    # Field renamed to remove unsuitable characters.
    prazo_entreg = models.IntegerField(db_column='prazo-entreg')
    contato = models.CharField(max_length=80)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    impr_ficha = models.TextField(db_column='impr-ficha')
    comentarios = models.CharField(max_length=4000)
    usuario = models.CharField(max_length=24)
    # Field renamed to remove unsuitable characters.
    data_atualiz = models.DateField(db_column='data-atualiz')
    # Field renamed to remove unsuitable characters.
    hora_atualiz = models.CharField(db_column='hora-atualiz', max_length=16)
    # Field renamed to remove unsuitable characters.
    nr_ord_orig = models.IntegerField(db_column='nr-ord-orig')
    # Field renamed to remove unsuitable characters.
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)
    # Field renamed to remove unsuitable characters.
    ind_reajuste = models.CharField(db_column='ind-reajuste', max_length=17)
    linha = models.IntegerField()
    # Field renamed to remove unsuitable characters.
    cod_refer = models.CharField(db_column='cod-refer', max_length=16)
    # Field renamed to remove unsuitable characters.
    nr_processo = models.IntegerField(db_column='nr-processo')
    # Field renamed to remove unsuitable characters.
    valor_descto = models.CharField(
        db_column='valor-descto', max_length=19, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_dias_taxa = models.IntegerField(db_column='nr-dias-taxa')
    # Field renamed to remove unsuitable characters.
    tp_despesa = models.IntegerField(
        db_column='tp-despesa', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    qt_acum_nec = models.CharField(
        db_column='qt-acum-nec', max_length=19, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    qt_acum_rec = models.CharField(
        db_column='qt-acum-rec', max_length=19, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    qt_acum_dev = models.CharField(
        db_column='qt-acum-dev', max_length=19, blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    ind_extrac = models.TextField(
        db_column='ind-extrac', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    cons_mrp = models.TextField(db_column='cons-mrp', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    cons_pmp = models.TextField(db_column='cons-pmp', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    item_pai = models.CharField(db_column='item-pai', max_length=32)
    # Field renamed to remove unsuitable characters.
    cod_roteiro = models.CharField(db_column='cod-roteiro', max_length=32)
    # Field renamed to remove unsuitable characters.
    op_seq = models.IntegerField(db_column='op-seq')
    # Field renamed to remove unsuitable characters.
    num_ord_inv = models.IntegerField(
        db_column='num-ord-inv', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_requisicao = models.IntegerField(db_column='nr-requisicao')
    sequencia = models.IntegerField()
    # Field renamed to remove unsuitable characters. This field type is a guess.
    reaj_tabela = models.TextField(
        db_column='reaj-tabela', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_tab = models.CharField(db_column='nr-tab', max_length=20)
    # Field renamed to remove unsuitable characters.
    ep_codigo = models.CharField(
        db_column='ep-codigo', max_length=6, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    conta_contabil = models.CharField(
        db_column='conta-contabil', max_length=34, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_seq_contr = models.IntegerField(
        db_column='nr-seq-contr', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    ordem_emitida = models.TextField(
        db_column='ordem-emitida', blank=True, null=True)
    # This field type is a guess.
    expectativa = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    qt_solic = models.CharField(
        db_column='qt-solic', max_length=19, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cota_ordem = models.IntegerField(
        db_column='cota-ordem', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    seq_evento = models.IntegerField(
        db_column='seq-evento', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    pend_aprov = models.IntegerField(
        db_column='pend-aprov', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    perc_vat = models.CharField(
        db_column='perc-vat', max_length=17, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    perc_sales_tax = models.CharField(
        db_column='perc-sales-tax', max_length=17, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_maq_origem = models.IntegerField(
        db_column='cod-maq-origem', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    num_processo_mp = models.IntegerField(
        db_column='num-processo-mp', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    char_1 = models.CharField(
        db_column='char-1', max_length=1000, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    char_2 = models.CharField(
        db_column='char-2', max_length=200, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dec_1 = models.CharField(
        db_column='dec-1', max_length=23, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dec_2 = models.CharField(
        db_column='dec-2', max_length=23, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    int_1 = models.IntegerField(db_column='int-1', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    int_2 = models.IntegerField(db_column='int-2', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    log_1 = models.TextField(db_column='log-1', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    log_2 = models.TextField(db_column='log-2', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    data_1 = models.DateField(db_column='data-1', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    data_2 = models.DateField(db_column='data-2', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_transp = models.IntegerField(
        db_column='cod-transp', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    num_id_documento = models.IntegerField(
        db_column='num-id-documento', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_contrato = models.IntegerField(db_column='nr-contrato')
    # Field renamed to remove unsuitable characters.
    num_seq_item = models.IntegerField(db_column='num-seq-item')
    # Field renamed to remove unsuitable characters.
    sit_ordem_contrat = models.IntegerField(
        db_column='sit-ordem-contrat', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dat_ordem = models.DateField(db_column='dat-ordem', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    check_sum = models.CharField(
        db_column='check-sum', max_length=40, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    prioridade_aprov = models.IntegerField(
        db_column='prioridade-aprov', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    origem_aprov = models.IntegerField(
        db_column='origem-aprov', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    gera_edi = models.TextField(db_column='gera-edi')
    # Field renamed to remove unsuitable characters.
    cod_estab_gestor = models.CharField(
        db_column='cod-estab-gestor', max_length=10)
    # Field renamed to remove unsuitable characters.
    licenca_import = models.CharField(
        db_column='licenca-import', max_length=40, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    loc_entrega = models.CharField(
        db_column='loc-entrega', max_length=60, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_entrega = models.CharField(
        db_column='cod-entrega', max_length=24, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    estab_entrega = models.CharField(
        db_column='estab-entrega', max_length=10, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_pedcli = models.CharField(
        db_column='nr-pedcli', max_length=24, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    seq_ped_venda = models.IntegerField(
        db_column='seq-ped-venda', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    local_entrega = models.IntegerField(
        db_column='local-entrega', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_estab_ctr = models.CharField(
        db_column='cod-estab-ctr', max_length=10, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_seq_contr_it = models.IntegerField(
        db_column='nr-seq-contr-it', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_contrato_venda = models.IntegerField(
        db_column='nr-contrato-venda', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_refer_b2b = models.CharField(
        db_column='cod-refer-b2b', max_length=100, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dat_inicio_leilao_rfq = models.DateField(
        db_column='dat-inicio-leilao-rfq', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dat_fim_leilao_rfq = models.DateField(
        db_column='dat-fim-leilao-rfq', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    hra_inicio_leilao_rfq = models.CharField(
        db_column='hra-inicio-leilao-rfq', max_length=16, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    hra_fim_leilao_rfq = models.CharField(
        db_column='hra-fim-leilao-rfq', max_length=16, blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    log_cot_aberta = models.TextField(
        db_column='log-cot-aberta', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    log_leilao = models.TextField(
        db_column='log-leilao', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_grp_compra = models.CharField(
        db_column='cod-grp-compra', max_length=24, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cdn_fabrican = models.IntegerField(db_column='cdn-fabrican')
    # Field renamed to remove unsuitable characters.
    des_referencia = models.CharField(
        db_column='des-referencia', max_length=30, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_unid_negoc = models.CharField(
        db_column='cod-unid-negoc', max_length=6, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cdn_tip_lote_pregao = models.IntegerField(
        db_column='cdn-tip-lote-pregao', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    qtd_recbda_fut = models.CharField(
        db_column='qtd-recbda-fut', max_length=19, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ordem_compra'


class PedidoCompr(models.Model):
    # Field renamed to remove unsuitable characters.
    num_pedido = models.IntegerField(db_column='num-pedido', primary_key=True)
    # Field renamed to remove unsuitable characters.
    num_ped_benef = models.IntegerField(db_column='num-ped-benef')
    natureza = models.IntegerField()
    # Field renamed to remove unsuitable characters.
    data_pedido = models.DateField(db_column='data-pedido')
    situacao = models.IntegerField()
    # Field renamed to remove unsuitable characters.
    cod_emitente = models.IntegerField(db_column='cod-emitente')
    # Field renamed to remove unsuitable characters.
    end_entrega = models.CharField(db_column='end-entrega', max_length=10)
    # Field renamed to remove unsuitable characters.
    end_cobranca = models.CharField(db_column='end-cobranca', max_length=10)
    frete = models.IntegerField()
    # Field renamed to remove unsuitable characters.
    cod_transp = models.IntegerField(db_column='cod-transp')
    # Field renamed to remove unsuitable characters.
    via_transp = models.IntegerField(db_column='via-transp')
    # Field renamed to remove unsuitable characters.
    cod_cond_pag = models.IntegerField(db_column='cod-cond-pag')
    responsavel = models.CharField(max_length=24)
    # Field renamed to remove unsuitable characters.
    cod_mensagem = models.IntegerField(db_column='cod-mensagem')
    # Field renamed to remove unsuitable characters. This field type is a guess.
    impr_pedido = models.TextField(db_column='impr-pedido')
    comentarios = models.CharField(max_length=1000)
    # Field renamed to remove unsuitable characters.
    mot_elimina = models.CharField(db_column='mot-elimina', max_length=1000)
    # Field renamed to remove unsuitable characters.
    nome_ass = models.CharField(
        db_column='nome-ass', max_length=186, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cargo_ass = models.CharField(
        db_column='cargo-ass', max_length=186, blank=True, null=True)
    emergencial = models.TextField()  # This field type is a guess.
    # Field renamed to remove unsuitable characters.
    nr_prox_ped = models.IntegerField(db_column='nr-prox-ped')
    # Field renamed to remove unsuitable characters. This field type is a guess.
    contr_forn = models.TextField(db_column='contr-forn')
    # Field renamed to remove unsuitable characters.
    nr_processo = models.IntegerField(db_column='nr-processo')
    # Field renamed to remove unsuitable characters.
    compl_entrega = models.CharField(
        db_column='compl-entrega', max_length=14, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    l_tipo_ped = models.IntegerField(
        db_column='l-tipo-ped', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    l_classificacao = models.IntegerField(
        db_column='l-classificacao', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    l_ind_prof = models.TextField(
        db_column='l-ind-prof', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    i_importador = models.IntegerField(db_column='i-importador')
    # Field renamed to remove unsuitable characters.
    i_situacao = models.IntegerField(
        db_column='i-situacao', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    c_cod_tabela = models.CharField(
        db_column='c-cod-tabela', max_length=20, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    i_moeda = models.IntegerField(db_column='i-moeda')
    # Field renamed to remove unsuitable characters.
    i_cod_forma = models.IntegerField(db_column='i-cod-forma')
    # Field renamed to remove unsuitable characters.
    i_cod_via = models.IntegerField(db_column='i-cod-via')
    # Field renamed to remove unsuitable characters.
    c_prazo = models.CharField(
        db_column='c-prazo', max_length=40, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    c_descr_merc = models.CharField(
        db_column='c-descr-merc', max_length=324, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    i_cod_porto = models.IntegerField(db_column='i-cod-porto')
    # Field renamed to remove unsuitable characters.
    de_vl_fob = models.CharField(db_column='de-vl-fob', max_length=19)
    # Field renamed to remove unsuitable characters.
    c_embalagem = models.CharField(
        db_column='c-embalagem', max_length=186, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    c_observacao = models.CharField(
        db_column='c-observacao', max_length=760, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    i_exportador = models.IntegerField(db_column='i-exportador')
    # Field renamed to remove unsuitable characters.
    desc_forma = models.CharField(
        db_column='desc-forma', max_length=72, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    desc_via = models.CharField(
        db_column='desc-via', max_length=40, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    de_vl_frete_i = models.CharField(
        db_column='de-vl-frete-i', max_length=17, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    ind_orig_entrada = models.IntegerField(
        db_column='ind-orig-entrada', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    ind_via_envio = models.IntegerField(
        db_column='ind-via-envio', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nro_proc_entrada = models.IntegerField(
        db_column='nro-proc-entrada', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nro_proc_saida = models.IntegerField(
        db_column='nro-proc-saida', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nro_proc_alteracao = models.IntegerField(
        db_column='nro-proc-alteracao', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_maq_origem = models.IntegerField(
        db_column='cod-maq-origem', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    num_processo_mp = models.IntegerField(
        db_column='num-processo-mp', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    char_1 = models.CharField(
        db_column='char-1', max_length=200, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    char_2 = models.CharField(
        db_column='char-2', max_length=200, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dec_1 = models.CharField(
        db_column='dec-1', max_length=23, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dec_2 = models.CharField(
        db_column='dec-2', max_length=23, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    int_1 = models.IntegerField(db_column='int-1', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    int_2 = models.IntegerField(db_column='int-2', blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    log_2 = models.TextField(db_column='log-2', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    data_1 = models.DateField(db_column='data-1', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    data_2 = models.DateField(db_column='data-2', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    num_id_documento = models.IntegerField(
        db_column='num-id-documento', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_contrato = models.IntegerField(db_column='nr-contrato')
    # Field renamed to remove unsuitable characters.
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)
    # Field renamed to remove unsuitable characters.
    check_sum = models.CharField(
        db_column='check-sum', max_length=40, blank=True, null=True)
    # Field renamed to remove unsuitable characters. This field type is a guess.
    gera_edi = models.TextField(db_column='gera-edi')
    # Field renamed to remove unsuitable characters.
    cod_estab_gestor = models.CharField(
        db_column='cod-estab-gestor', max_length=10)
    # Field renamed to remove unsuitable characters.
    cod_emit_terc = models.IntegerField(
        db_column='cod-emit-terc', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    nr_ped_venda = models.IntegerField(
        db_column='nr-ped-venda', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_entrega = models.CharField(
        db_column='cod-entrega', max_length=24, blank=True, null=True)
    endereco_text = models.CharField(max_length=1000, blank=True, null=True)
    endereco = models.CharField(max_length=80, blank=True, null=True)
    bairro = models.CharField(max_length=60, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    pais = models.CharField(max_length=40, blank=True, null=True)
    cep = models.CharField(max_length=24, blank=True, null=True)
    jurisdicao = models.CharField(max_length=40, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    local_entrega = models.IntegerField(
        db_column='local-entrega', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_usuar_criac = models.CharField(
        db_column='cod-usuar-criac', max_length=24, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    dat_criac = models.DateField(db_column='dat-criac', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cod_usuar_alter = models.CharField(
        db_column='cod-usuar-alter', max_length=24, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    hra_criac = models.CharField(
        db_column='hra-criac', max_length=16, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    hra_alter = models.CharField(
        db_column='hra-alter', max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedido_compr'


class StgEpm(models.Model):
    # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100)
    # Field name made lowercase.
    timestamp = models.DateTimeField(
        db_column='TIMESTAMP', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    doubleval_value_field = models.FloatField(
        db_column='DOUBLEVAL(VALUE)', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_epm'


class StgItem(models.Model):
    # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)
    # Field renamed to remove unsuitable characters.
    desc_item = models.CharField(
        db_column='desc-item', max_length=120, blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    data_ult_ent = models.DateField(
        db_column='data-ult-ent', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_item'


class StgMovtoFluxoCx(models.Model):
    dat_movto_fluxo_cx = models.DateField()
    cod_estab = models.CharField(max_length=10)
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    val_movto_fluxo_cx = models.DecimalField(max_digits=17, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'stg_movto_fluxo_cx'


class StgRegiao(models.Model):
    # Field name made lowercase.
    cod_estab = models.IntegerField(
        db_column='COD_ESTAB', blank=True, null=True)
    # Field name made lowercase.
    regiao = models.CharField(
        db_column='REGIAO', max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_regiao'


class StgSaldo(models.Model):
    # Field renamed to remove unsuitable characters.
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)
    # Field renamed to remove unsuitable characters.
    cod_depos = models.CharField(db_column='cod-depos', max_length=6)
    # Field renamed to remove unsuitable characters.
    qtidade_atu = models.DecimalField(
        db_column='qtidade-atu', max_digits=19, decimal_places=4)
    # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)

    class Meta:
        managed = False
        db_table = 'stg_saldo'


class StgTipFluxo(models.Model):
    cod_tip_fluxo_financ = models.CharField(primary_key=True, max_length=24)
    des_tip_fluxo_financ = models.CharField(max_length=80)
    ind_tip_secao_fluxo_cx = models.CharField(max_length=22)
    ind_fluxo_movto_financ = models.CharField(max_length=14)
    cod_plano_cta_ctbl = models.CharField(max_length=16, blank=True, null=True)
    cod_cta_ctbl = models.CharField(max_length=40, blank=True, null=True)
    dat_inic_valid = models.DateField()
    dat_fim_valid = models.DateField()
    num_niv_tip_fluxo_financ = models.IntegerField()
    num_clas_tip_fluxo_financ = models.IntegerField()
    ind_tip_lancto_livro_cx = models.CharField(
        max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_tip_fluxo'


class TipFluxoFinanc(models.Model):
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    des_tip_fluxo_financ = models.CharField(max_length=80)
    ind_fluxo_movto_financ = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'tip_fluxo_financ'


class UmidadeBiomassa(models.Model):
    id = models.IntegerField(primary_key=True)
    identificador = models.TextField(blank=True, null=True)
    solicitacao = models.TextField(blank=True, null=True)
    email_usuario = models.TextField(blank=True, null=True)
    unidade = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    cnpj_unidade = models.TextField(
        db_column='CNPJ_UNIDADE', blank=True, null=True)
    # Field name made lowercase.
    natureza = models.TextField(db_column='Natureza', blank=True, null=True)
    # Field name made lowercase.
    fornecedor = models.TextField(
        db_column='Fornecedor', blank=True, null=True)
    # Field name made lowercase.
    numero_nf = models.TextField(db_column='Numero_NF', blank=True, null=True)
    # Field name made lowercase.
    emissao = models.DateField(db_column='Emissao', blank=True, null=True)
    # Field name made lowercase.
    entrada = models.DateField(db_column='Entrada', blank=True, null=True)
    # Field name made lowercase.
    codigo_item = models.TextField(
        db_column='Codigo_item', blank=True, null=True)
    desc_item = models.TextField(blank=True, null=True)
    tipo_biomassa = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    unidade_medida = models.TextField(
        db_column='Unidade_medida', blank=True, null=True)
    valor_unitario = models.TextField(blank=True, null=True)
    quantidade_recebida = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    valor_frete = models.TextField(
        db_column='Valor_frete', blank=True, null=True)
    # Field name made lowercase.
    valor_total = models.TextField(
        db_column='VALOR_TOTAL', blank=True, null=True)
    # Field name made lowercase.
    frete = models.TextField(db_column='Frete', blank=True, null=True)
    transportadora = models.TextField(blank=True, null=True)
    placa = models.TextField(blank=True, null=True)
    metragem = models.TextField(blank=True, null=True)
    motorista = models.TextField(blank=True, null=True)
    peso_bruto = models.TextField(blank=True, null=True)
    tara = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    peso_liquido = models.TextField(
        db_column='Peso_liquido', blank=True, null=True)
    peso_excedente = models.TextField(blank=True, null=True)
    resultado_umidade_01 = models.TextField(blank=True, null=True)
    resultado_umidade_02 = models.TextField(blank=True, null=True)
    resultado_umidade_03 = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    utiliza_balde = models.TextField(
        db_column='Utiliza_balde', blank=True, null=True)
    # Field name made lowercase.
    peso_amostra_massa_01 = models.TextField(
        db_column='Peso_amostra_massa_01', blank=True, null=True)
    # Field name made lowercase.
    peso_amostra_massa_02 = models.TextField(
        db_column='Peso_amostra_massa_02', blank=True, null=True)
    # Field name made lowercase.
    observacoes = models.TextField(
        db_column='Observacoes', blank=True, null=True)
    umidade = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'umidade_biomassa'
