# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Base(models.Model):
    class Meta:
        abstract = True
        managed = False

class AlertaSsmaV2(Base):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_responsavel_sol = models.TextField(blank=True, null=True)
    estabelecimento = models.TextField(blank=True, null=True)
    codigo_estabelecimento = models.TextField(blank=True, null=True)
    data_ocorrencia = models.TextField(blank=True, null=True)
    hora_ocorrencia = models.TextField(blank=True, null=True)
    origem_ocorrencia = models.TextField(blank=True, null=True)
    parteafetada = models.TextField(db_column='parteAfetada', blank=True, null=True)  # Field name made lowercase.
    lateralidade = models.TextField(blank=True, null=True)
    tipolesao = models.TextField(db_column='tipoLesao', blank=True, null=True)  # Field name made lowercase.
    empresa = models.TextField(blank=True, null=True)
    experiencia = models.TextField(blank=True, null=True)
    tempocombio = models.TextField(db_column='tempoCombio', blank=True, null=True)  # Field name made lowercase.
    periodo = models.TextField(blank=True, null=True)
    diasemana = models.TextField(db_column='diaSemana', blank=True, null=True)  # Field name made lowercase.
    hora_trabalhada = models.TextField(blank=True, null=True)
    genero = models.TextField(blank=True, null=True)
    idade = models.TextField(blank=True, null=True)
    tipoprocesso = models.TextField(db_column='tipoProcesso', blank=True, null=True)  # Field name made lowercase.
    regravida = models.TextField(db_column='regraVida', blank=True, null=True)  # Field name made lowercase.
    tipoocorpatr = models.TextField(db_column='tipoOcorPatr', blank=True, null=True)  # Field name made lowercase.
    tipoacidente = models.TextField(db_column='tipoAcidente', blank=True, null=True)  # Field name made lowercase.
    tipodado = models.TextField(db_column='tipoDado', blank=True, null=True)  # Field name made lowercase.
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


class BiApbNfEntradas(Base):
    data_transaþÒo = models.DateField(db_column='Data transaþÒo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    usußrio_recebimento = models.CharField(db_column='Usußrio recebimento', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_emissÒo = models.DateField(db_column='Data emissÒo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    filial = models.CharField(db_column='Filial', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emitente = models.CharField(db_column='Emitente', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    documento = models.CharField(db_column='Documento', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sÚrie = models.CharField(db_column='SÚrie', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pedido = models.CharField(db_column='Pedido', max_length=255, blank=True, null=True)  # Field name made lowercase.
    situaþÒo = models.CharField(db_column='SituaþÒo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emergencial = models.CharField(db_column='Emergencial', max_length=255, blank=True, null=True)  # Field name made lowercase.
    requisitante = models.CharField(db_column='Requisitante', max_length=255, blank=True, null=True)  # Field name made lowercase.
    condiþÒo = models.CharField(db_column='CondiþÒo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descriþÒo = models.CharField(db_column='DescriþÒo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vencimento = models.DateField(db_column='Vencimento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_apb_nf_entradas'


class BiApbNfEntradasCompleto(Base):
    dt_emissao = models.DateField(blank=True, null=True)
    dt_trans = models.DateField(blank=True, null=True)
    dt_atualiza = models.DateField(blank=True, null=True)
    ap = models.CharField(db_column='AP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cod_estabel = models.IntegerField(blank=True, null=True)
    uf = models.CharField(max_length=5, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    cod_emitente = models.IntegerField(blank=True, null=True)
    desc_emitente = models.CharField(max_length=255, blank=True, null=True)
    cgc = models.CharField(max_length=20, blank=True, null=True)
    nro_docto = models.CharField(max_length=12, blank=True, null=True)
    serie_docto = models.CharField(max_length=5, blank=True, null=True)
    seq_item = models.IntegerField(blank=True, null=True)
    esp_docto = models.IntegerField(blank=True, null=True)
    especie = models.CharField(max_length=20, blank=True, null=True)
    natureza = models.IntegerField(blank=True, null=True)
    desc_nat_oper = models.CharField(max_length=255, blank=True, null=True)
    cod_conta_contabil_trans = models.CharField(max_length=20, blank=True, null=True)
    desc_conta_contabil_trans = models.CharField(max_length=255, blank=True, null=True)
    cod_deposito = models.CharField(max_length=5, blank=True, null=True)
    tipo_controle = models.CharField(max_length=20, blank=True, null=True)
    cod_item = models.CharField(max_length=20, blank=True, null=True)
    descricao_item = models.CharField(max_length=255, blank=True, null=True)
    cod_conta_contabil = models.CharField(max_length=20, blank=True, null=True)
    desc_conta_contabil = models.CharField(max_length=255, blank=True, null=True)
    cod_ccusto = models.CharField(max_length=20, blank=True, null=True)
    desc_cc = models.CharField(max_length=255, blank=True, null=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    un = models.CharField(max_length=10, blank=True, null=True)
    unid_fornec = models.CharField(db_column='UNID_FORNEC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    preco_unit = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    desconto = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    cod_class_fiscal = models.CharField(max_length=20, blank=True, null=True)
    desc_fiscal = models.CharField(db_column='DESC_FISCAL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cod_natur_rendimento = models.CharField(max_length=5, blank=True, null=True)
    desc_natur_rendimento = models.CharField(db_column='DESC_NATUR_RENDIMENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valor_total = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    cod_cst_icms = models.CharField(db_column='COD_CST_ICMS', max_length=3, blank=True, null=True)  # Field name made lowercase.
    calcbc = models.DecimalField(db_column='CalcBC', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    aliquota_icms = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    valor_icms_deb_cred = models.DecimalField(db_column='Valor_ICMS_Deb_Cred', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_icms_complementar = models.DecimalField(db_column='Valor_ICMS_Complementar', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_icms_nao_tributado = models.DecimalField(db_column='Valor_ICMS_nao_tributado', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    base_calculo_icms_outras = models.DecimalField(db_column='Base_calculo_ICMS_Outras', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_bc_cofins = models.DecimalField(db_column='Valor_BC_COFINS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    bccofins_sem_icms = models.DecimalField(db_column='BcCofins_SEM_ICMS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    aliquota_cofins = models.DecimalField(db_column='Aliquota_COFINS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_cofins = models.DecimalField(db_column='Valor_COFINS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_bc_pis = models.DecimalField(db_column='Valor_BC_PIS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    bc_pis_sem_icms = models.DecimalField(db_column='Bc_Pis_sem_ICMS', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    aliquota_pis = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    valor_pis = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    valor_bc_icms_st = models.DecimalField(db_column='valor_bc_ICMS_st', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_icms_st = models.DecimalField(db_column='Valor_ICMS_ST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    codigo_cst_ipi = models.CharField(db_column='Codigo_CST_IPI', max_length=5, blank=True, null=True)  # Field name made lowercase.
    base_calculo_ipi = models.DecimalField(db_column='Base_calculo_IPI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_ipi_deb_cred = models.DecimalField(db_column='Valor_IPI_Deb_Cred', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_ipi_nao_tributado = models.DecimalField(db_column='Valor_IPI_nao_tributado', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_ipi_despesas = models.DecimalField(db_column='Valor_IPI_despesas', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valor_ipi_outras = models.DecimalField(db_column='Valor_IPI_Outras', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    valo_outras = models.DecimalField(db_column='Valo_Outras', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    despesas_nota = models.DecimalField(db_column='Despesas_nota', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    oi = models.CharField(db_column='OI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pedido = models.IntegerField(db_column='Pedido', blank=True, null=True)  # Field name made lowercase.
    processo = models.CharField(db_column='Processo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numero_ordem = models.IntegerField(blank=True, null=True)
    ordserv = models.IntegerField(db_column='OrdServ', blank=True, null=True)  # Field name made lowercase.
    codobs = models.CharField(db_column='CodObs', max_length=20, blank=True, null=True)  # Field name made lowercase.
    chave = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.CharField(max_length=20, blank=True, null=True)
    usuario_fiscal = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_apb_nf_entradas_completo'


class BiApbTitAp(Base):
    cod_empresa = models.CharField(max_length=6, blank=True, null=True)
    cod_estab = models.CharField(max_length=10)
    cod_espec_docto = models.CharField(max_length=6)
    cod_ser_docto = models.CharField(max_length=6)
    cdn_fornecedor = models.IntegerField(primary_key=True)  # The composite primary key (cdn_fornecedor, cod_estab, cod_espec_docto, cod_ser_docto, cod_tit_ap, cod_parcela) found, that is not supported. The first column is selected.
    nom_pessoa = models.CharField(max_length=80, blank=True, null=True)
    cod_grp_fornec = models.CharField(max_length=30, blank=True, null=True)
    cod_tit_ap = models.CharField(max_length=20)
    cod_parcela = models.CharField(max_length=4)
    dat_emis_docto = models.DateField(blank=True, null=True)
    dat_vencto_tit_ap = models.DateField(blank=True, null=True)
    val_origin_tit_ap = models.DecimalField(max_digits=17, decimal_places=0, blank=True, null=True)
    val_sdo_tit_ap = models.DecimalField(max_digits=17, decimal_places=0, blank=True, null=True)
    cod_indic_econ = models.CharField(max_length=16, blank=True, null=True)
    cod_refer = models.CharField(max_length=20, blank=True, null=True)
    num_dias = models.IntegerField(blank=True, null=True)
    responsavel = models.CharField(max_length=80, blank=True, null=True)
    nome_abrev = models.CharField(max_length=80, blank=True, null=True)
    cnpj = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_apb_tit_ap'
        unique_together = (('cdn_fornecedor', 'cod_estab', 'cod_espec_docto', 'cod_ser_docto', 'cod_tit_ap', 'cod_parcela'),)


class BiCentroCusto(Base):
    centrocusto = models.CharField(db_column='centroCusto', max_length=22)  # Field name made lowercase.
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_centro_custo'


class BiChamadosSatisfacaoServiceUp(Base):
    ticket_number = models.CharField(db_column='Ticket_Number', primary_key=True, max_length=255)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=100)  # Field name made lowercase.
    data_fechamento = models.DateField(db_column='Data_Fechamento')  # Field name made lowercase.
    ano_mes = models.CharField(db_column='Ano_Mes', max_length=7)  # Field name made lowercase.
    customer_user_id = models.CharField(db_column='Customer_User_Id', max_length=50)  # Field name made lowercase.
    owner = models.CharField(db_column='Owner', max_length=255)  # Field name made lowercase.
    queue = models.CharField(db_column='Queue', max_length=255)  # Field name made lowercase.
    vote_time = models.DateTimeField(db_column='Vote_Time')  # Field name made lowercase.
    satisfacao = models.CharField(db_column='Satisfacao', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deixe_sua_sugestao_critica_ou_elogio = models.TextField(db_column='Deixe_Sua_Sugestao_Critica_Ou_Elogio', blank=True, null=True)  # Field name made lowercase.
    de_uma_nota_ao_nosso_atendimento = models.IntegerField(db_column='De_Uma_Nota_Ao_Nosso_Atendimento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_chamados_satisfacao_service_up'


class BiChamadosServiceUp(Base):
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
    queue_name = models.CharField(max_length=200)
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
    escalation_destination_in = models.CharField(max_length=20, blank=True, null=True)
    escalation_destination_date = models.DateTimeField(blank=True, null=True)
    escalation_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    escalation_time = models.CharField(max_length=20, blank=True, null=True)
    escalation_response_time = models.IntegerField(blank=True, null=True)
    escalation_update_time = models.IntegerField(blank=True, null=True)
    escalation_solution_time = models.IntegerField(blank=True, null=True)
    first_response_time_escalation = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_notification = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_destination_time = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_destination_date = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    first_response_time = models.CharField(max_length=20, blank=True, null=True)
    update_time_escalation = models.CharField(max_length=20, blank=True, null=True)
    update_time_notification = models.CharField(max_length=20, blank=True, null=True)
    update_time_destination_time = models.CharField(max_length=20, blank=True, null=True)
    update_time_destination_date = models.DateTimeField(blank=True, null=True)
    update_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time_escalation = models.CharField(max_length=20, blank=True, null=True)
    solution_time_notification = models.CharField(max_length=20, blank=True, null=True)
    solution_time_destination_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time_destination_date = models.DateTimeField(blank=True, null=True)
    solution_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time = models.CharField(max_length=20, blank=True, null=True)
    first_response = models.DateTimeField(blank=True, null=True)
    first_response_in_min = models.CharField(max_length=20, blank=True, null=True)
    first_response_diff_min = models.CharField(max_length=20, blank=True, null=True)
    solution_in_min = models.CharField(max_length=20, blank=True, null=True)
    solution_diff_in_min = models.CharField(max_length=20, blank=True, null=True)
    first_lock = models.DateTimeField(blank=True, null=True)
    unlock_timeout = models.CharField(max_length=50, blank=True, null=True)
    real_till_time_not_used = models.IntegerField(blank=True, null=True)
    number_of_articles = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    change_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bi_chamados_service_up'


class BiChamadosServiceUpGdi(Base):
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
    queue_name = models.CharField(max_length=200)
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
    escalation_destination_in = models.CharField(max_length=20, blank=True, null=True)
    escalation_destination_date = models.DateTimeField(blank=True, null=True)
    escalation_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    escalation_time = models.CharField(max_length=20, blank=True, null=True)
    escalation_response_time = models.IntegerField(blank=True, null=True)
    escalation_update_time = models.IntegerField(blank=True, null=True)
    escalation_solution_time = models.IntegerField(blank=True, null=True)
    first_response_time_escalation = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_notification = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_destination_time = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_destination_date = models.CharField(max_length=20, blank=True, null=True)
    first_response_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    first_response_time = models.CharField(max_length=20, blank=True, null=True)
    update_time_escalation = models.CharField(max_length=20, blank=True, null=True)
    update_time_notification = models.CharField(max_length=20, blank=True, null=True)
    update_time_destination_time = models.CharField(max_length=20, blank=True, null=True)
    update_time_destination_date = models.DateTimeField(blank=True, null=True)
    update_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time_escalation = models.CharField(max_length=20, blank=True, null=True)
    solution_time_notification = models.CharField(max_length=20, blank=True, null=True)
    solution_time_destination_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time_destination_date = models.DateTimeField(blank=True, null=True)
    solution_time_working_time = models.CharField(max_length=20, blank=True, null=True)
    solution_time = models.CharField(max_length=20, blank=True, null=True)
    first_response = models.DateTimeField(blank=True, null=True)
    first_response_in_min = models.CharField(max_length=20, blank=True, null=True)
    first_response_diff_min = models.CharField(max_length=20, blank=True, null=True)
    solution_in_min = models.CharField(max_length=20, blank=True, null=True)
    solution_diff_in_min = models.CharField(max_length=20, blank=True, null=True)
    first_lock = models.DateTimeField(blank=True, null=True)
    unlock_timeout = models.CharField(max_length=50, blank=True, null=True)
    real_till_time_not_used = models.IntegerField(blank=True, null=True)
    number_of_articles = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    change_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bi_chamados_service_up_gdi'


class BiContaContabil(Base):
    conta = models.CharField(primary_key=True, max_length=40)
    descricao = models.CharField(max_length=80, blank=True, null=True)
    id = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_conta_contabil'


class BiDadosInmet(Base):
    umid_med = models.IntegerField(db_column='UMID_MED', blank=True, null=True)  # Field name made lowercase.
    dt_medicao = models.DateField(db_column='DT_MEDICAO', blank=True, null=True)  # Field name made lowercase.
    dc_nome = models.CharField(db_column='DC_NOME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    umid_min = models.IntegerField(db_column='UMID_MIN', blank=True, null=True)  # Field name made lowercase.
    temp_med = models.FloatField(db_column='TEMP_MED', blank=True, null=True)  # Field name made lowercase.
    chuva = models.FloatField(db_column='CHUVA', blank=True, null=True)  # Field name made lowercase.
    vl_latitude = models.FloatField(db_column='VL_LATITUDE', blank=True, null=True)  # Field name made lowercase.
    temp_min = models.FloatField(db_column='TEMP_MIN', blank=True, null=True)  # Field name made lowercase.
    temp_max = models.FloatField(db_column='TEMP_MAX', blank=True, null=True)  # Field name made lowercase.
    uf = models.CharField(db_column='UF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vel_vento_med = models.FloatField(db_column='VEL_VENTO_MED', blank=True, null=True)  # Field name made lowercase.
    cd_estacao = models.CharField(db_column='CD_ESTACAO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vl_longitude = models.FloatField(db_column='VL_LONGITUDE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_dados_inmet'


class BiEfz1005Cep(Base):
    conta = models.CharField(max_length=40)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=120, blank=True, null=True)  # Field name made lowercase.
    datarealizado = models.DateField(db_column='dataRealizado', blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    valorrealizado = models.CharField(db_column='valorRealizado', max_length=17, blank=True, null=True)  # Field name made lowercase.
    mediorecebimento = models.CharField(db_column='medioRecebimento', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    historicomodulo = models.CharField(db_column='historicoModulo', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ordemmanutencao = models.IntegerField(db_column='ordemManutencao', blank=True, null=True)  # Field name made lowercase.
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    unidadenegocio = models.CharField(db_column='unidadeNegocio', max_length=16, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=24, blank=True, null=True)  # Field name made lowercase.
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=60, blank=True, null=True)  # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=80, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    observacao = models.CharField(db_column='Observacao', max_length=15000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_efz1005_cep'


class BiEfz1005Completo(Base):
    conta = models.CharField(max_length=40)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=120, blank=True, null=True)  # Field name made lowercase.
    datarealizado = models.DateField(db_column='dataRealizado', blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    valorrealizado = models.CharField(db_column='valorRealizado', max_length=17, blank=True, null=True)  # Field name made lowercase.
    mediorecebimento = models.CharField(db_column='medioRecebimento', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    historicomodulo = models.CharField(db_column='historicoModulo', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ordemmanutencao = models.IntegerField(db_column='ordemManutencao', blank=True, null=True)  # Field name made lowercase.
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    unidadenegocio = models.CharField(db_column='unidadeNegocio', max_length=16, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=24, blank=True, null=True)  # Field name made lowercase.
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=60, blank=True, null=True)  # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=80, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    observacao = models.CharField(db_column='Observacao', max_length=15000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_efz1005_completo'


class BiEfz1005Folha(Base):
    conta = models.CharField(max_length=40)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=120, blank=True, null=True)  # Field name made lowercase.
    datarealizado = models.DateField(db_column='dataRealizado', blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    valorrealizado = models.CharField(db_column='valorRealizado', max_length=17, blank=True, null=True)  # Field name made lowercase.
    mediorecebimento = models.CharField(db_column='medioRecebimento', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    historicomodulo = models.CharField(db_column='historicoModulo', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ordemmanutencao = models.IntegerField(db_column='ordemManutencao', blank=True, null=True)  # Field name made lowercase.
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    unidadenegocio = models.CharField(db_column='unidadeNegocio', max_length=16, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=24, blank=True, null=True)  # Field name made lowercase.
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=60, blank=True, null=True)  # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=80, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    observacao = models.CharField(db_column='Observacao', max_length=15000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_efz1005_folha'


class BiEfz1005Oi(Base):
    conta = models.CharField(max_length=40, blank=True, null=True)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=120, blank=True, null=True)  # Field name made lowercase.
    datarealizado = models.DateField(db_column='dataRealizado', blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    valorrealizado = models.CharField(db_column='valorRealizado', max_length=17, blank=True, null=True)  # Field name made lowercase.
    mediorecebimento = models.CharField(db_column='medioRecebimento', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    historicomodulo = models.CharField(db_column='historicoModulo', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ordemmanutencao = models.IntegerField(db_column='ordemManutencao', blank=True, null=True)  # Field name made lowercase.
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    unidadenegocio = models.CharField(db_column='unidadeNegocio', max_length=16, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=24, blank=True, null=True)  # Field name made lowercase.
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=60, blank=True, null=True)  # Field name made lowercase.
    emitente = models.IntegerField(db_column='Emitente', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=80, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    observacao = models.CharField(db_column='Observacao', max_length=15000, blank=True, null=True)  # Field name made lowercase.
    ordem_investimento = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_efz1005_oi'


class BiEsapb0002(Base):
    dt_emissao = models.DateField(blank=True, null=True)
    dt_aprova = models.DateField(blank=True, null=True)
    dt_trans = models.DateField(blank=True, null=True)
    dt_atualiza = models.DateField(blank=True, null=True)
    num_pedido = models.IntegerField(blank=True, null=True)
    dat_gerac_movto = models.DateField(blank=True, null=True)
    dat_vencto_tit_ap = models.DateField(blank=True, null=True)
    dat_ult_pagto = models.DateField(blank=True, null=True)
    cod_estab = models.CharField(max_length=5, blank=True, null=True)
    cdn_fornecedor = models.CharField(max_length=255, blank=True, null=True)
    nome_abrev = models.CharField(max_length=255, blank=True, null=True)
    cod_espec_docto = models.CharField(max_length=10, blank=True, null=True)
    cod_tit_ap = models.CharField(max_length=20, blank=True, null=True)
    cod_ser_docto = models.CharField(max_length=10, blank=True, null=True)
    cod_parcela = models.CharField(max_length=10, blank=True, null=True)
    val_origin_tit_ap = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    val_pagto_tit_ap = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_esapb0002'


class BiEstabelecimento(Base):
    estabelecimento = models.CharField(db_column='ESTABELECIMENTO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sigla_unidade = models.CharField(db_column='SIGLA_UNIDADE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nome_unidade = models.CharField(db_column='NOME_UNIDADE', max_length=80, blank=True, null=True)  # Field name made lowercase.
    endereco = models.CharField(max_length=70, blank=True, null=True)
    bairro = models.CharField(max_length=120, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    pais = models.CharField(max_length=40, blank=True, null=True)
    regional = models.CharField(db_column='Regional', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    ie = models.CharField(db_column='IE', max_length=38, blank=True, null=True)  # Field name made lowercase.
    nome_fantasia = models.CharField(db_column='NOME_FANTASIA', max_length=80, blank=True, null=True)  # Field name made lowercase.
    cnpj = models.CharField(db_column='CNPJ', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_estabelecimento'


class BiEstabelecimentoCcusto(Base):
    cod_empresa = models.CharField(primary_key=True, max_length=6)  # The composite primary key (cod_empresa, cod_estab, cod_ccusto) found, that is not supported. The first column is selected.
    cod_estab = models.CharField(max_length=10)
    nom_abrev = models.CharField(max_length=30, blank=True, null=True)
    cod_ccusto = models.CharField(max_length=22)
    des_tit_ctbl = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_estabelecimento_ccusto'
        unique_together = (('cod_empresa', 'cod_estab', 'cod_ccusto'),)


class BiFlgMonitorWorkflow(Base):
    seq_mov = models.IntegerField(db_column='SEQ_MOV')  # Field name made lowercase.
    solicitacao = models.IntegerField(db_column='SOLICITACAO')  # Field name made lowercase.
    descricao = models.CharField(db_column='DESCRICAO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    solicitante = models.CharField(db_column='SOLICITANTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    atividade = models.CharField(db_column='ATIVIDADE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    inicio_atividade = models.DateTimeField(db_column='INICIO_ATIVIDADE', blank=True, null=True)  # Field name made lowercase.
    fim_atividade = models.DateTimeField(db_column='FIM_ATIVIDADE', blank=True, null=True)  # Field name made lowercase.
    responsavel = models.CharField(db_column='RESPONSAVEL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inicio_solicitacao = models.DateTimeField(db_column='INICIO_SOLICITACAO', blank=True, null=True)  # Field name made lowercase.
    fim_solicitacao = models.DateTimeField(db_column='FIM_SOLICITACAO', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_flg_monitor_workflow'


class BiFlgMonitorWorkflowTemp(Base):
    seq_mov = models.IntegerField(db_column='SEQ_MOV', primary_key=True)  # Field name made lowercase. The composite primary key (SEQ_MOV, SOLICITACAO) found, that is not supported. The first column is selected.
    solicitacao = models.IntegerField(db_column='SOLICITACAO')  # Field name made lowercase.
    descricao = models.CharField(db_column='DESCRICAO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    solicitante = models.CharField(db_column='SOLICITANTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    atividade = models.CharField(db_column='ATIVIDADE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    inicio_atividade = models.DateTimeField(db_column='INICIO_ATIVIDADE', blank=True, null=True)  # Field name made lowercase.
    fim_atividade = models.DateTimeField(db_column='FIM_ATIVIDADE', blank=True, null=True)  # Field name made lowercase.
    responsavel = models.CharField(db_column='RESPONSAVEL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inicio_solicitacao = models.DateTimeField(db_column='INICIO_SOLICITACAO', blank=True, null=True)  # Field name made lowercase.
    fim_solicitacao = models.DateTimeField(db_column='FIM_SOLICITACAO', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_flg_monitor_workflow_temp'
        unique_together = (('seq_mov', 'solicitacao'),)


class BiItensDatasulCompleto(Base):
    data_implant = models.DateField(blank=True, null=True)
    cod_estabel = models.CharField(primary_key=True, max_length=10)  # The composite primary key (cod_estabel, it_codigo) found, that is not supported. The first column is selected.
    it_codigo = models.CharField(max_length=20)
    item_desc_item = models.CharField(db_column='ITEM_desc_item', max_length=255, blank=True, null=True)  # Field name made lowercase.
    item_narrativa = models.CharField(db_column='ITEM_narrativa', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ge_codigo = models.CharField(max_length=20, blank=True, null=True)
    grup_estoque_descricao = models.CharField(max_length=255, blank=True, null=True)
    familia = models.CharField(max_length=20, blank=True, null=True)
    desc_familia = models.CharField(max_length=255, blank=True, null=True)
    codfamcom = models.CharField(db_column='CodFamCom', max_length=20, blank=True, null=True)  # Field name made lowercase.
    descfamcom = models.CharField(db_column='DescFamCom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    un = models.CharField(max_length=20, blank=True, null=True)
    tab_unidade_descricao = models.CharField(max_length=255, blank=True, null=True)
    deposito_pad = models.CharField(max_length=20, blank=True, null=True)
    deposito_nome = models.CharField(max_length=255, blank=True, null=True)
    cod_localiz = models.CharField(max_length=20, blank=True, null=True)
    tpcontrole = models.CharField(db_column='TpControle', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cod_ccusto = models.CharField(max_length=20, blank=True, null=True)
    ccusto_descricao = models.CharField(max_length=255, blank=True, null=True)
    cod_cta_ctbl = models.CharField(max_length=20, blank=True, null=True)
    des_tit_ctbl = models.CharField(max_length=255, blank=True, null=True)
    cod_unid_negoc = models.CharField(max_length=20, blank=True, null=True)
    des_unid_negoc = models.CharField(max_length=255, blank=True, null=True)
    nat_despesa = models.CharField(max_length=20, blank=True, null=True)
    natureza_despesa_descricao = models.CharField(max_length=255, blank=True, null=True)
    class_fiscal = models.CharField(max_length=20, blank=True, null=True)
    classif_fisc_descricao = models.CharField(max_length=255, blank=True, null=True)
    compr_fabric = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_itens_datasul_completo'
        unique_together = (('cod_estabel', 'it_codigo'),)


class BiItensSinc(Base):
    codigo = models.CharField(primary_key=True, max_length=32)
    unitem = models.CharField(db_column='unItem', max_length=4, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(max_length=120, blank=True, null=True)
    narrativa = models.CharField(max_length=4000, blank=True, null=True)
    tipocontr = models.IntegerField(db_column='tipoContr', blank=True, null=True)  # Field name made lowercase.
    ctcodigo = models.CharField(db_column='ctCodigo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ncm = models.CharField(max_length=20, blank=True, null=True)
    codobsoleto = models.IntegerField(db_column='codObsoleto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_itens_sinc'


class BiMla(Base):
    cod_tip_doc = models.IntegerField(primary_key=True)  # The composite primary key (cod_tip_doc, cod_estabel, cod_lotacao, num_faixa) found, that is not supported. The first column is selected.
    tipo = models.CharField(max_length=255, blank=True, null=True)
    cod_estabel = models.IntegerField()
    cod_lotacao = models.CharField(max_length=50)
    desc_lotacao = models.CharField(max_length=255, blank=True, null=True)
    num_faixa = models.IntegerField()
    cod_usuar = models.CharField(max_length=50, blank=True, null=True)
    des_faixa = models.CharField(max_length=255, blank=True, null=True)
    limite_ini = models.CharField(max_length=255, blank=True, null=True)
    limite_fim = models.CharField(max_length=255, blank=True, null=True)
    seq_aprov = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_mla'
        unique_together = (('cod_tip_doc', 'cod_estabel', 'cod_lotacao', 'num_faixa'),)


class BiOrdemInvestimentoCompromissado(Base):
    ordem_investimento = models.IntegerField(db_column='ORDEM_INVESTIMENTO', blank=True, null=True)  # Field name made lowercase.
    ordem_compra = models.IntegerField(db_column='ORDEM_COMPRA', blank=True, null=True)  # Field name made lowercase.
    cod_item = models.CharField(db_column='COD_ITEM', max_length=32, blank=True, null=True)  # Field name made lowercase.
    desc_item = models.CharField(db_column='DESC_ITEM', max_length=120, blank=True, null=True)  # Field name made lowercase.
    preco_fornecedor_unitario = models.CharField(db_column='PRECO_FORNECEDOR_UNITARIO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qtd = models.CharField(db_column='QTD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=24, blank=True, null=True)  # Field name made lowercase.
    data_ordem = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_ordem_investimento_compromissado'


class BiOrdemInvestimentoOrcado(Base):
    filial = models.CharField(db_column='FILIAL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ordem_investimento = models.IntegerField(db_column='ORDEM_INVESTIMENTO', blank=True, null=True)  # Field name made lowercase.
    desc_projeto = models.CharField(db_column='DESC_PROJETO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    desc_ordem = models.CharField(db_column='DESC_ORDEM', max_length=80, blank=True, null=True)  # Field name made lowercase.
    sigla = models.CharField(max_length=30, blank=True, null=True)
    situacao_ordem_invest = models.CharField(db_column='SITUACAO_ORDEM_INVEST', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ccusto = models.CharField(db_column='CCUSTO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc_centro = models.CharField(db_column='DESC_CENTRO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    verba_original = models.CharField(db_column='VERBA_ORIGINAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    verba_atual = models.CharField(db_column='VERBA_ATUAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    valor_compromissado = models.CharField(db_column='VALOR_COMPROMISSADO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    valor_realizado = models.CharField(db_column='VALOR_REALIZADO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    valor_saldo = models.CharField(db_column='VALOR_SALDO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    saldo_compromissado = models.CharField(db_column='SALDO_COMPROMISSADO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    usuario_responsavel = models.CharField(db_column='USUARIO_RESPONSAVEL', max_length=24, blank=True, null=True)  # Field name made lowercase.
    saldo_oi = models.CharField(db_column='SALDO_OI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ano_emissao = models.IntegerField(db_column='ANO_EMISSAO', blank=True, null=True)  # Field name made lowercase.
    datainivalidade = models.DateField(db_column='DataIniValidade', blank=True, null=True)  # Field name made lowercase.
    datafimvalidade = models.DateField(db_column='dataFimValidade', blank=True, null=True)  # Field name made lowercase.
    dataemissao = models.DateField(db_column='DataEmissao', blank=True, null=True)  # Field name made lowercase.
    dataliberacao = models.DateField(db_column='DataLiberacao', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_ordem_investimento_orcado'


class BiPedidosPd(Base):
    filial = models.CharField(db_column='Filial', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_pedido = models.DateField(db_column='Data_pedido', blank=True, null=True)  # Field name made lowercase.
    pedido = models.IntegerField(db_column='Pedido', blank=True, null=True)  # Field name made lowercase.
    numero_ordem = models.IntegerField(blank=True, null=True)
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cod_custo = models.CharField(max_length=255, blank=True, null=True)
    conta = models.CharField(max_length=255, blank=True, null=True)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emitente = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(db_column='ITEM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=255, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=255, blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    preco_unitario = models.FloatField(blank=True, null=True)
    saldo_restante = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_pedidos_pd'


class BiPedidosPendentes(Base):
    filial = models.CharField(db_column='Filial', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_pedido = models.DateField(db_column='Data_pedido', blank=True, null=True)  # Field name made lowercase.
    pedido = models.IntegerField(db_column='Pedido', blank=True, null=True)  # Field name made lowercase.
    numero_ordem = models.IntegerField(blank=True, null=True)
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cod_custo = models.CharField(max_length=255, blank=True, null=True)
    conta = models.CharField(max_length=255, blank=True, null=True)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emitente = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(db_column='ITEM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=255, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=255, blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    preco_unitario = models.FloatField(blank=True, null=True)
    saldo_restante = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bi_pedidos_pendentes'


class BiTi(Base):
    ticket = models.IntegerField(db_column='TICKET', primary_key=True)  # Field name made lowercase.
    nome_fantasia_do_cliente = models.CharField(db_column='NOME_FANTASIA_DO_CLIENTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipo_do_ticket = models.CharField(db_column='TIPO_DO_TICKET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status_do_ticket = models.CharField(db_column='STATUS_DO_TICKET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_de_criacao_do_ticket = models.DateTimeField(db_column='DATA_DE_CRIACAO_DO_TICKET', blank=True, null=True)  # Field name made lowercase.
    data_da_solucao = models.CharField(db_column='DATA_DA_SOLUCAO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_do_tecnico = models.CharField(db_column='NOME_DO_TECNICO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_da_categoria_primaria = models.CharField(db_column='NOME_DA_CATEGORIA_PRIMARIA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_da_categoria_secundaria = models.CharField(db_column='NOME_DA_CATEGORIA_SECUNDARIA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contato_do_ticket = models.CharField(db_column='CONTATO_DO_TICKET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descricao_do_setor = models.CharField(db_column='DESCRICAO_DO_SETOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descricao_do_ticket = models.CharField(db_column='DESCRICAO_DO_TICKET', max_length=15200, blank=True, null=True)  # Field name made lowercase.
    data_do_primeiro_atendimento = models.CharField(db_column='DATA_DO_PRIMEIRO_ATENDIMENTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_de_saida = models.CharField(db_column='DATA_DE_SAIDA', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_ti'


class BiTiAbertos(Base):
    ticket = models.IntegerField(db_column='TICKET', primary_key=True)  # Field name made lowercase.
    nome_fantasia_do_cliente = models.CharField(db_column='NOME_FANTASIA_DO_CLIENTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipo_do_ticket = models.CharField(db_column='TIPO_DO_TICKET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status_do_ticket = models.CharField(db_column='STATUS_DO_TICKET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_de_criacao_do_ticket = models.DateTimeField(db_column='DATA_DE_CRIACAO_DO_TICKET', blank=True, null=True)  # Field name made lowercase.
    data_da_solucao = models.CharField(db_column='DATA_DA_SOLUCAO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_do_tecnico = models.CharField(db_column='NOME_DO_TECNICO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_da_categoria_primaria = models.CharField(db_column='NOME_DA_CATEGORIA_PRIMARIA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome_da_categoria_secundaria = models.CharField(db_column='NOME_DA_CATEGORIA_SECUNDARIA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contato_do_ticket = models.CharField(db_column='CONTATO_DO_TICKET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descricao_do_setor = models.CharField(db_column='DESCRICAO_DO_SETOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descricao_do_ticket = models.CharField(db_column='DESCRICAO_DO_TICKET', max_length=15000, blank=True, null=True)  # Field name made lowercase.
    data_do_primeiro_atendimento = models.CharField(db_column='DATA_DO_PRIMEIRO_ATENDIMENTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_de_saida = models.CharField(db_column='DATA_DE_SAIDA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_atualizacao = models.DateTimeField(db_column='DATA_ATUALIZACAO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_ti_abertos'


class BiUsersServiceUp(Base):
    id_serviceup = models.IntegerField(blank=True, null=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    filial = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='CentroCusto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    funcao = models.CharField(db_column='Funcao', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bi_users_service_up'


class DimItem(Base):
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)  # Field renamed to remove unsuitable characters.
    desc_item = models.CharField(db_column='desc-item', max_length=120, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_ult_ent = models.DateField(db_column='data-ult-ent', blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'dim_item'


class DimRegiao(Base):
    cod_estab = models.IntegerField(db_column='COD_ESTAB', blank=True, null=True)  # Field name made lowercase.
    regiao = models.CharField(db_column='REGIAO', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dim_regiao'


class DimTipFluxo(Base):
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
    ind_tip_lancto_livro_cx = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_tip_fluxo'


class DwFreteDatasul(Base):
    cod_transportador = models.TextField(db_column='COD_TRANSPORTADOR', blank=True, null=True)  # Field name made lowercase.
    natureza_operacao_cte = models.TextField(db_column='NATUREZA_OPERACAO_CTE', blank=True, null=True)  # Field name made lowercase.
    nr_docto_cte = models.TextField(db_column='NR_DOCTO_CTE', blank=True, null=True)  # Field name made lowercase.
    serie_cte = models.TextField(db_column='SERIE_CTE', blank=True, null=True)  # Field name made lowercase.
    valor_cte = models.FloatField(db_column='VALOR_CTE', blank=True, null=True)  # Field name made lowercase.
    emitente = models.TextField(db_column='Emitente', blank=True, null=True)  # Field name made lowercase.
    natureza_operacao_nf = models.TextField(db_column='NATUREZA_OPERACAO_NF', blank=True, null=True)  # Field name made lowercase.
    nr_docto_nf = models.TextField(db_column='NR_DOCTO_NF', blank=True, null=True)  # Field name made lowercase.
    serie_nf = models.TextField(db_column='SERIE_NF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dw_frete_datasul'


class Efz1005(Base):
    conta = models.CharField(max_length=40)
    descricaoconta = models.CharField(db_column='descricaoConta', max_length=120, blank=True, null=True)  # Field name made lowercase.
    datarealizado = models.DateField(db_column='dataRealizado', blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(max_length=10, blank=True, null=True)
    natureza = models.CharField(max_length=4, blank=True, null=True)
    valorrealizado = models.CharField(db_column='valorRealizado', max_length=17, blank=True, null=True)  # Field name made lowercase.
    mediorecebimento = models.CharField(db_column='medioRecebimento', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=120, blank=True, null=True)
    historicomodulo = models.CharField(db_column='historicoModulo', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ordemmanutencao = models.IntegerField(db_column='ordemManutencao', blank=True, null=True)  # Field name made lowercase.
    estabelecimento = models.CharField(max_length=10, blank=True, null=True)
    unidadenegocio = models.CharField(db_column='unidadeNegocio', max_length=16, blank=True, null=True)  # Field name made lowercase.
    centrocusto = models.CharField(db_column='centroCusto', max_length=24, blank=True, null=True)  # Field name made lowercase.
    descricaocusto = models.CharField(db_column='descricaoCusto', max_length=60, blank=True, null=True)  # Field name made lowercase.
    emitente = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    item = models.CharField(max_length=32, blank=True, null=True)
    descricaoitem = models.CharField(db_column='descricaoItem', max_length=80, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(max_length=4, blank=True, null=True)
    quantidade = models.CharField(max_length=19, blank=True, null=True)
    pedido = models.IntegerField(blank=True, null=True)
    requisitante = models.CharField(max_length=24, blank=True, null=True)
    observacao = models.CharField(db_column='Observacao', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'efz1005'


class EpmDif(Base):
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epm_dif'


class EpmPart(Base):
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epm_part'


class EpmProd(Base):
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    start_value = models.FloatField(blank=True, null=True)
    end_value = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epm_prod'


class EsAbastecimentoDieselUpv(Base):
    numero_solicitacao = models.IntegerField(primary_key=True)
    utilizacao_maquina_d = models.CharField(max_length=200, blank=True, null=True)
    horario_abastecimento = models.CharField(max_length=16, blank=True, null=True)
    horimetro_abastecimento = models.CharField(max_length=50, blank=True, null=True)
    volume_abastecido = models.CharField(max_length=100, blank=True, null=True)
    nf_diesel = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_abastecimento_diesel_upv'


class EsCaldeiraCombioUpv(Base):
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    parada_caldeira_redu_consu = models.CharField(max_length=10, blank=True, null=True)
    data_interrupcao_vapor = models.DateField(blank=True, null=True)
    hora_interrupcao_vapor = models.CharField(max_length=16, blank=True, null=True)
    data_retorno_caldeira = models.DateField(blank=True, null=True)
    hora_liberacao_manutencao = models.CharField(max_length=16, blank=True, null=True)
    hora_retorno_vapor = models.CharField(max_length=16, blank=True, null=True)
    comentar_detalhadamente_parada = models.CharField(max_length=120, blank=True, null=True)
    raiz_causou_parada = models.CharField(max_length=500, blank=True, null=True)
    outros_causa_raiz = models.CharField(max_length=500, blank=True, null=True)
    detalhes_causa_raiz = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_caldeira_combio_upv'


class EsCaldeiraCombioUpvTeste(Base):
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    parada_caldeira_redu_consu = models.CharField(max_length=10, blank=True, null=True)
    data_interrupcao_vapor = models.DateField(blank=True, null=True)
    hora_interrupcao_vapor = models.CharField(max_length=16, blank=True, null=True)
    data_retorno_caldeira = models.DateField(blank=True, null=True)
    hora_liberacao_manutencao = models.CharField(max_length=16, blank=True, null=True)
    hora_retorno_vapor = models.CharField(max_length=16, blank=True, null=True)
    comentar_detalhadamente_parada = models.CharField(max_length=120, blank=True, null=True)
    raiz_causou_parada = models.CharField(max_length=500, blank=True, null=True)
    outros_causa_raiz = models.CharField(max_length=500, blank=True, null=True)
    detalhes_causa_raiz = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_caldeira_combio_upv_teste'


class EsCentroCusto(Base):
    cod_ccusto = models.CharField(max_length=120, blank=True, null=True)
    des_tit_ctbl = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_centro_custo'


class EsContaContabil(Base):
    cod_cta_ctbl = models.CharField(max_length=120, blank=True, null=True)
    des_tit_ctbl = models.CharField(max_length=120, blank=True, null=True)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'es_conta_contabil'


class EsFolhaBi(Base):
    mes = models.IntegerField(primary_key=True)  # The composite primary key (mes, ano, cdn_funcionario, cdn_estab, cdn_empresa, Evento) found, that is not supported. The first column is selected.
    ano = models.IntegerField()
    cdn_funcionario = models.IntegerField()
    cdn_estab = models.CharField(max_length=200)
    cdn_empresa = models.CharField(max_length=6)
    evento = models.CharField(db_column='Evento', max_length=16)  # Field name made lowercase.
    tipo_movto = models.BigIntegerField(db_column='tipo-movto', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    quantidade = models.CharField(max_length=18, blank=True, null=True)
    horas = models.CharField(max_length=18, blank=True, null=True)
    base = models.CharField(max_length=18, blank=True, null=True)
    valor = models.CharField(max_length=18, blank=True, null=True)
    nom_funcionario = models.CharField(max_length=120, blank=True, null=True)
    dat_admis_func = models.DateField(blank=True, null=True)
    dat_desligto_func = models.DateField(blank=True, null=True)
    plano_lotacao = models.CharField(db_column='plano-lotacao', max_length=16, blank=True, null=True)  # Field renamed to remove unsuitable characters.
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
    mao_de_obra = models.CharField(db_column='mao-de-obra', max_length=16, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    desc_mao_de_obra = models.CharField(db_column='desc_mao-de-obra', max_length=80, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    desc_categ_sal = models.CharField(max_length=80, blank=True, null=True)
    cod_cargo = models.CharField(max_length=16, blank=True, null=True)
    cod_nivel = models.CharField(max_length=16, blank=True, null=True)
    des_nivel = models.CharField(max_length=80, blank=True, null=True)
    fpas = models.CharField(max_length=24, blank=True, null=True)
    tomador = models.CharField(max_length=16, blank=True, null=True)
    desc_tomador = models.CharField(max_length=80, blank=True, null=True)
    sat = models.CharField(max_length=17, blank=True, null=True)
    desc_evento = models.CharField(db_column='desc-evento', max_length=80, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    usuario = models.CharField(max_length=24, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    hora = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_folha_bi'
        unique_together = (('mes', 'ano', 'cdn_funcionario', 'cdn_estab', 'cdn_empresa', 'evento'),)


class EsFuncionario(Base):
    nome_funcionario = models.CharField(max_length=200, blank=True, null=True)
    cpf_funcionario = models.CharField(primary_key=True, max_length=16)  # The composite primary key (cpf_funcionario, cpf_superior) found, that is not supported. The first column is selected.
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


class EsInssBi(Base):
    cdn_estab = models.CharField(primary_key=True, max_length=10)  # The composite primary key (cdn_estab, mes, ano) found, that is not supported. The first column is selected.
    mes = models.IntegerField()
    ano = models.IntegerField()
    empregadosnormal = models.CharField(db_column='empregadosNormal', max_length=17, blank=True, null=True)  # Field name made lowercase.
    segurados = models.CharField(max_length=17, blank=True, null=True)
    autonomos = models.CharField(max_length=17, blank=True, null=True)
    recisao = models.CharField(max_length=17, blank=True, null=True)
    vlrecolhesegurados = models.CharField(db_column='vlRecolheSegurados', max_length=17, blank=True, null=True)  # Field name made lowercase.
    vlrecolhefamilia = models.CharField(db_column='vlRecolheFamilia', max_length=17, blank=True, null=True)  # Field name made lowercase.
    baserecolhimentogeral = models.CharField(db_column='baseRecolhimentoGeral', max_length=17, blank=True, null=True)  # Field name made lowercase.
    vlrecolheautonomos = models.CharField(db_column='vlRecolheAutonomos', max_length=17, blank=True, null=True)  # Field name made lowercase.
    vlrecolheempresa = models.CharField(db_column='vlRecolheEmpresa', max_length=17, blank=True, null=True)  # Field name made lowercase.
    vlrecolhesat = models.CharField(db_column='vlRecolheSAT', max_length=17, blank=True, null=True)  # Field name made lowercase.
    vlrecolheterceiros = models.CharField(db_column='vlRecolheTerceiros', max_length=17, blank=True, null=True)  # Field name made lowercase.
    totalliquido = models.CharField(db_column='totalLiquido', max_length=17, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'es_inss_bi'
        unique_together = (('cdn_estab', 'mes', 'ano'),)


class EsLinhaAmarelaUpv(Base):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    selecionar_maquina = models.CharField(max_length=70, blank=True, null=True)
    informar_horimetro_maquina = models.CharField(max_length=100, blank=True, null=True)
    houve_ocorrencia_maquina = models.CharField(max_length=5, blank=True, null=True)
    hora_inicio_indisponibilidade = models.CharField(max_length=16, blank=True, null=True)
    hora_termino_indisponibilidade = models.CharField(max_length=16, blank=True, null=True)
    comentarios_relacao_maquina = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_linha_amarela_upv'


class EsMudancaMixUpv(Base):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    horario_mudanca_mix = models.CharField(max_length=16, blank=True, null=True)
    mix_utilizado_volumetrica = models.CharField(max_length=30, blank=True, null=True)
    outros_mix_utili_propor = models.CharField(max_length=150, blank=True, null=True)
    comentario_relacao_caldeira = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_mudanca_mix_upv'


class EsOcorrenciasCaldeiraUpv(Base):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    informe_ocorrencia = models.CharField(max_length=70, blank=True, null=True)
    outros_ocorrencia_caldeira = models.CharField(max_length=500, blank=True, null=True)
    descreva_detalha_ocorrencia = models.CharField(max_length=1000, blank=True, null=True)
    inicio_ocorrencia = models.CharField(max_length=16, blank=True, null=True)
    termino_ocorrencia = models.CharField(max_length=16, blank=True, null=True)
    ocorrencia_afetou = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_ocorrencias_caldeira_upv'


class EsPedidoEmergencial(Base):
    numero_solicitacao = models.IntegerField(primary_key=True)  # The composite primary key (numero_solicitacao, pedido) found, that is not supported. The first column is selected.
    processo = models.CharField(max_length=40, blank=True, null=True)
    tipo_recebimento = models.CharField(max_length=40, blank=True, null=True)
    pedido = models.IntegerField()
    num_nf = models.CharField(max_length=20, blank=True, null=True)
    serie_nf = models.CharField(max_length=10, blank=True, null=True)
    cod_estabelecimento = models.CharField(max_length=16, blank=True, null=True)
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


class EsRelatorioProducaoUpv(Base):
    acionar_caldeira_cliente = models.CharField(max_length=100, blank=True, null=True)
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
    foi_necessario_abastecer = models.CharField(max_length=100, blank=True, null=True)
    gestor_aprov = models.CharField(max_length=100, blank=True, null=True)
    gestor_coments = models.TextField(blank=True, null=True)
    houve_mudanca_mix = models.CharField(max_length=100, blank=True, null=True)
    houve_ocorrencia_caldeira = models.CharField(max_length=100, blank=True, null=True)
    houve_remocao_cascas = models.CharField(max_length=100, blank=True, null=True)
    houve_remocao_finos = models.CharField(max_length=100, blank=True, null=True)
    localizacao = models.CharField(max_length=500, blank=True, null=True)
    mix_utilizado_proporcao = models.CharField(max_length=100, blank=True, null=True)
    nf_cascas = models.CharField(max_length=100, blank=True, null=True)
    nf_finos = models.CharField(max_length=100, blank=True, null=True)
    nf_residuos = models.CharField(max_length=100, blank=True, null=True)
    outros_causa_raiz = models.TextField(blank=True, null=True)
    outros_mix_utilizado = models.TextField(blank=True, null=True)
    parada_caldeira_combio = models.CharField(max_length=100, blank=True, null=True)
    parada_caldeira_redu_consu = models.CharField(max_length=500, blank=True, null=True)
    possui_maquina = models.CharField(max_length=100, blank=True, null=True)
    raiz_causou_parada = models.CharField(max_length=500, blank=True, null=True)
    remocao_cacamba_turno = models.CharField(max_length=100, blank=True, null=True)
    responsavel_conferencia = models.CharField(max_length=500, blank=True, null=True)
    responsavel_preenchimento = models.CharField(max_length=500, blank=True, null=True)
    unidade = models.CharField(max_length=500, blank=True, null=True)
    data_interrupcao_vapor = models.DateField(blank=True, null=True)
    data_preenchimento = models.DateField(blank=True, null=True)
    consumo_biomassa_tonelada = models.CharField(max_length=17, blank=True, null=True)
    consumo_tonelada = models.CharField(max_length=17, blank=True, null=True)
    conversao = models.CharField(max_length=17, blank=True, null=True)
    eficiencia_anterior = models.CharField(max_length=17, blank=True, null=True)
    estoque_total_tonelada = models.CharField(max_length=17, blank=True, null=True)
    pressao_vapor_turno = models.CharField(max_length=17, blank=True, null=True)
    qtd_cascas = models.CharField(max_length=17, blank=True, null=True)
    qtd_cinzas_geradas = models.CharField(max_length=17, blank=True, null=True)
    qtd_finos = models.CharField(max_length=17, blank=True, null=True)
    total_final_agua = models.CharField(max_length=17, blank=True, null=True)
    total_final_balanca = models.CharField(max_length=17, blank=True, null=True)
    total_final_vapor = models.CharField(max_length=17, blank=True, null=True)
    total_inicial_vapor = models.CharField(max_length=17, blank=True, null=True)
    total_inicio_agua = models.CharField(max_length=17, blank=True, null=True)
    total_inici_balanca = models.CharField(max_length=17, blank=True, null=True)
    total_vapor_vendido = models.CharField(max_length=17, blank=True, null=True)
    codigo_formulario = models.IntegerField(blank=True, null=True)
    numero_solicitacao = models.IntegerField(primary_key=True)
    comentario_geral = models.TextField(blank=True, null=True)
    hora_interrupcao_vapor = models.CharField(max_length=16, blank=True, null=True)
    hora_liberacao_manutencao = models.CharField(max_length=16, blank=True, null=True)
    hora_retorno_vapor = models.CharField(max_length=16, blank=True, null=True)
    inicio_caldeira_cliente = models.CharField(max_length=16, blank=True, null=True)
    termino_caldeira_cliente = models.CharField(max_length=16, blank=True, null=True)
    total_combio = models.CharField(max_length=17, blank=True, null=True)
    total_levedura = models.CharField(max_length=17, blank=True, null=True)
    data_retorno_caldeira = models.DateField(blank=True, null=True)
    hora_entrada = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_relatorio_producao_upv'


class EsRemocaoCascasUpv(Base):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_cascas = models.CharField(max_length=17, blank=True, null=True)
    nf_cascas = models.CharField(max_length=30, blank=True, null=True)
    comentarios_sobre_cascas = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_cascas_upv'


class EsRemocaoCinzasUpv(Base):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_cinzas_geradas = models.CharField(max_length=100, blank=True, null=True)
    nf_residuos = models.CharField(max_length=20, blank=True, null=True)
    comentarios_sobre_cinzas = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_cinzas_upv'


class EsRemocaoFinosUpv(Base):
    id = models.IntegerField(primary_key=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_finos = models.DecimalField(max_digits=17, decimal_places=5, blank=True, null=True)
    nf_finos = models.CharField(max_length=100, blank=True, null=True)
    comentarios_sobre_finos = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_finos_upv'


class EsRemocaoRedlerUpv(Base):
    id_redler = models.IntegerField(blank=True, null=True)
    numero_solicitacao = models.IntegerField(blank=True, null=True)
    qtd_cinzas_redler = models.DecimalField(max_digits=17, decimal_places=2, blank=True, null=True)
    comentarios_cinzas_redler = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'es_remocao_redler_upv'


class EstabelecimentoDatasul(Base):
    cod_estabelecimento = models.IntegerField(db_column='COD_ESTABELECIMENTO', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='SIGLA', blank=True, null=True, max_length=100)  # Field name made lowercase.
    cidade = models.CharField(db_column='CIDADE', blank=True, null=True, max_length=100)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', blank=True, null=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estabelecimento_datasul'


class EstrutTipFinanc(Base):
    cod_tip_fluxo_financ_pai = models.CharField(max_length=24)
    cod_tip_fluxo_financ_filho = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'estrut_tip_financ'


class FatMovtoFluxoCx(Base):
    cod_estab = models.IntegerField()
    dat_movto_fluxo_cx = models.DateField()
    ind_fluxo_movto_cx = models.CharField(max_length=6)
    cod_cenario = models.IntegerField(db_column='Cod_cenario', blank=True, null=True)  # Field name made lowercase.
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    des_tip_fluxo_financ = models.CharField(max_length=80)
    val_movto_fluxo_cx = models.CharField(max_length=100)
    regiao = models.CharField(db_column='REGIAO', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fat_movto_fluxo_cx'


class FatSaldo(Base):
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)  # Field renamed to remove unsuitable characters.
    cod_depos = models.CharField(db_column='cod-depos', max_length=6)  # Field renamed to remove unsuitable characters.
    qtidade_atu = models.DecimalField(db_column='qtidade-atu', max_digits=19, decimal_places=4)  # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'fat_saldo'


class Item(Base):
    it_codigo = models.CharField(db_column='it-codigo', primary_key=True, max_length=32)  # Field renamed to remove unsuitable characters.
    desc_item = models.CharField(db_column='desc-item', max_length=120, blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'item'


class MylimsAccount(Base):
    complement = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    related_account_required = models.IntegerField()
    culture_id = models.CharField(max_length=255, blank=True, null=True)
    identification = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mylims_account'


class MylimsCollectionPoints(Base):
    active = models.IntegerField()
    address1 = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField()
    unrestricted_access_service_center = models.IntegerField()
    identification = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mylims_collection_points'


class MylimsInfo(Base):
    force_scale = models.IntegerField(blank=True, null=True)
    force_signif_digits = models.IntegerField(blank=True, null=True)
    read_only_value = models.IntegerField()
    equipment_type_id = models.IntegerField(blank=True, null=True)
    account_type_id = models.IntegerField(blank=True, null=True)
    allow_any_value = models.IntegerField()
    allow_text = models.IntegerField()
    consumable_type_id = models.IntegerField(blank=True, null=True)
    identification = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mylims_info'


class MylimsSample(Base):
    identification = models.CharField(max_length=255)
    control_identification = models.CharField(max_length=255, blank=True, null=True)
    control_number = models.CharField(max_length=255)
    reference_key = models.CharField(max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255, blank=True, null=True)
    group_id = models.IntegerField()
    number = models.IntegerField()
    year = models.IntegerField()
    sub_number = models.IntegerField()
    revision = models.IntegerField()
    active = models.IntegerField()
    sync_portal = models.IntegerField()
    received = models.IntegerField()
    finalized = models.IntegerField()
    published = models.IntegerField()
    reviewed = models.IntegerField()
    conclusion = models.DateTimeField(blank=True, null=True)
    taken_date_time = models.DateTimeField(blank=True, null=True)
    received_time = models.DateTimeField(blank=True, null=True)
    finalized_time = models.DateTimeField(blank=True, null=True)
    published_time = models.DateTimeField(blank=True, null=True)
    reviewed_time = models.DateTimeField(blank=True, null=True)
    expected_collection_time = models.DateTimeField(blank=True, null=True)
    reference_sample_id = models.IntegerField(blank=True, null=True)
    conclusion_time = models.IntegerField(blank=True, null=True)
    conclusion_time_fixed = models.IntegerField()
    collection_point_id = models.IntegerField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    total_price_business_unit = models.FloatField(blank=True, null=True)
    sample_type_id = models.IntegerField(blank=True, null=True)
    sample_type_identification = models.CharField(max_length=255, blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    account_identification = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mylims_sample'


class MylimsSampleAnalysis(Base):
    edition_date_time = models.DateTimeField()
    info01 = models.CharField(max_length=255, blank=True, null=True)
    info02 = models.CharField(max_length=255, blank=True, null=True)
    info03 = models.CharField(max_length=255, blank=True, null=True)
    info04 = models.CharField(max_length=255, blank=True, null=True)
    info05 = models.CharField(max_length=255, blank=True, null=True)
    info06 = models.CharField(max_length=255, blank=True, null=True)
    info07 = models.CharField(max_length=255, blank=True, null=True)
    info08 = models.CharField(max_length=255, blank=True, null=True)
    info09 = models.CharField(max_length=255, blank=True, null=True)
    info10 = models.CharField(max_length=255, blank=True, null=True)
    attribute = models.CharField(max_length=255, blank=True, null=True)
    required_value = models.IntegerField()
    display_value = models.CharField(max_length=255, blank=True, null=True)
    force_scale = models.IntegerField(blank=True, null=True)
    force_signif_digits = models.IntegerField(blank=True, null=True)
    input_scale = models.IntegerField(blank=True, null=True)
    input_signif_digits = models.IntegerField(blank=True, null=True)
    input_format = models.IntegerField(blank=True, null=True)
    value_text = models.CharField(max_length=255, blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_number = models.FloatField(blank=True, null=True)
    value_date_time = models.DateTimeField(blank=True, null=True)
    value_boolean = models.IntegerField(blank=True, null=True)
    value_account = models.IntegerField(blank=True, null=True)
    info_type_id = models.IntegerField()
    order = models.IntegerField()
    uncertainty = models.IntegerField(blank=True, null=True)
    k = models.IntegerField(blank=True, null=True)
    veff = models.IntegerField(blank=True, null=True)
    detection_limit = models.FloatField(blank=True, null=True)
    quantification_limit = models.FloatField(blank=True, null=True)
    detection_limit_display = models.CharField(max_length=255, blank=True, null=True)
    quantification_limit_display = models.CharField(max_length=255, blank=True, null=True)
    reference_method = models.CharField(max_length=255, blank=True, null=True)
    sample_id = models.IntegerField()
    conclusion_id = models.IntegerField(blank=True, null=True)
    info_id = models.IntegerField(blank=True, null=True)
    info_identification = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mylims_sample_analysis'


class MylimsSampleAnalysisConclusions(Base):
    identification = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mylims_sample_analysis_conclusions'


class MylimsSampleInfo(Base):
    order = models.IntegerField()
    info_id = models.IntegerField()
    info_type_id = models.IntegerField()
    measurement_unit_id = models.IntegerField(blank=True, null=True)
    display_value = models.CharField(max_length=255, blank=True, null=True)
    force_scale = models.IntegerField(blank=True, null=True)
    force_signif_digits = models.IntegerField(blank=True, null=True)
    value_text = models.CharField(max_length=255, blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)
    value_float = models.IntegerField(blank=True, null=True)
    value_date_time = models.IntegerField(blank=True, null=True)
    value_boolean = models.IntegerField(blank=True, null=True)
    value_account_id = models.IntegerField(blank=True, null=True)
    dependent_info_id = models.IntegerField(blank=True, null=True)
    sample_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mylims_sample_info'


class MylimsSampleTypes(Base):
    prefix = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    sample_class_id = models.IntegerField()
    sample_publish_type_id = models.IntegerField()
    sample_reason_id = models.IntegerField(blank=True, null=True)
    sample_type_parent_id = models.IntegerField(blank=True, null=True)
    packaging_alert = models.IntegerField()
    identification = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mylims_sample_types'


class OrdemCompra(Base):
    numero_ordem = models.IntegerField(db_column='numero-ordem', primary_key=True)  # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)  # Field renamed to remove unsuitable characters.
    natureza = models.IntegerField()
    situacao = models.IntegerField()
    origem = models.IntegerField()
    op_codigo = models.IntegerField(db_column='op-codigo')  # Field renamed to remove unsuitable characters.
    data_emissao = models.DateField(db_column='data-emissao')  # Field renamed to remove unsuitable characters.
    ct_codigo = models.CharField(db_column='ct-codigo', max_length=40)  # Field renamed to remove unsuitable characters.
    sc_codigo = models.CharField(db_column='sc-codigo', max_length=40)  # Field renamed to remove unsuitable characters.
    requisitante = models.CharField(max_length=24)
    dep_almoxar = models.CharField(db_column='dep-almoxar', max_length=6)  # Field renamed to remove unsuitable characters.
    ordem_servic = models.IntegerField(db_column='ordem-servic')  # Field renamed to remove unsuitable characters.
    cod_comprado = models.CharField(db_column='cod-comprado', max_length=24)  # Field renamed to remove unsuitable characters.
    narrativa = models.CharField(max_length=4000)
    num_pedido = models.IntegerField(db_column='num-pedido')  # Field renamed to remove unsuitable characters.
    data_pedido = models.DateField(db_column='data-pedido', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_emitente = models.IntegerField(db_column='cod-emitente')  # Field renamed to remove unsuitable characters.
    data_cotacao = models.DateField(db_column='data-cotacao', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    preco_orig = models.CharField(db_column='preco-orig', max_length=20)  # Field renamed to remove unsuitable characters.
    preco_unit = models.CharField(db_column='preco-unit', max_length=20)  # Field renamed to remove unsuitable characters.
    pre_unit_for = models.CharField(db_column='pre-unit-for', max_length=20)  # Field renamed to remove unsuitable characters.
    preco_fornec = models.CharField(db_column='preco-fornec', max_length=20)  # Field renamed to remove unsuitable characters.
    nr_alt_preco = models.IntegerField(db_column='nr-alt-preco')  # Field renamed to remove unsuitable characters.
    mo_codigo = models.IntegerField(db_column='mo-codigo')  # Field renamed to remove unsuitable characters.
    codigo_ipi = models.TextField(db_column='codigo-ipi')  # Field renamed to remove unsuitable characters. This field type is a guess.
    aliquota_ipi = models.CharField(db_column='aliquota-ipi', max_length=17)  # Field renamed to remove unsuitable characters.
    codigo_icm = models.IntegerField(db_column='codigo-icm')  # Field renamed to remove unsuitable characters.
    aliquota_icm = models.CharField(db_column='aliquota-icm', max_length=17)  # Field renamed to remove unsuitable characters.
    aliquota_iss = models.CharField(db_column='aliquota-iss', max_length=17)  # Field renamed to remove unsuitable characters.
    frete = models.TextField()  # This field type is a guess.
    valor_frete = models.CharField(db_column='valor-frete', max_length=19)  # Field renamed to remove unsuitable characters.
    taxa_financ = models.TextField(db_column='taxa-financ')  # Field renamed to remove unsuitable characters. This field type is a guess.
    valor_taxa = models.CharField(db_column='valor-taxa', max_length=19)  # Field renamed to remove unsuitable characters.
    saldo_emb = models.CharField(db_column='saldo-emb', max_length=17, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    perc_descto = models.CharField(db_column='perc-descto', max_length=20)  # Field renamed to remove unsuitable characters.
    saldo_gi = models.CharField(db_column='saldo-gi', max_length=17, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_cond_pag = models.IntegerField(db_column='cod-cond-pag')  # Field renamed to remove unsuitable characters.
    prazo_entreg = models.IntegerField(db_column='prazo-entreg')  # Field renamed to remove unsuitable characters.
    contato = models.CharField(max_length=80)
    impr_ficha = models.TextField(db_column='impr-ficha')  # Field renamed to remove unsuitable characters. This field type is a guess.
    comentarios = models.CharField(max_length=4000)
    usuario = models.CharField(max_length=24)
    data_atualiz = models.DateField(db_column='data-atualiz')  # Field renamed to remove unsuitable characters.
    hora_atualiz = models.CharField(db_column='hora-atualiz', max_length=16)  # Field renamed to remove unsuitable characters.
    nr_ord_orig = models.IntegerField(db_column='nr-ord-orig')  # Field renamed to remove unsuitable characters.
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)  # Field renamed to remove unsuitable characters.
    ind_reajuste = models.CharField(db_column='ind-reajuste', max_length=17)  # Field renamed to remove unsuitable characters.
    linha = models.IntegerField()
    cod_refer = models.CharField(db_column='cod-refer', max_length=16)  # Field renamed to remove unsuitable characters.
    nr_processo = models.IntegerField(db_column='nr-processo')  # Field renamed to remove unsuitable characters.
    valor_descto = models.CharField(db_column='valor-descto', max_length=19, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_dias_taxa = models.IntegerField(db_column='nr-dias-taxa')  # Field renamed to remove unsuitable characters.
    tp_despesa = models.IntegerField(db_column='tp-despesa', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    qt_acum_nec = models.CharField(db_column='qt-acum-nec', max_length=19, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    qt_acum_rec = models.CharField(db_column='qt-acum-rec', max_length=19, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    qt_acum_dev = models.CharField(db_column='qt-acum-dev', max_length=19, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ind_extrac = models.TextField(db_column='ind-extrac', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    cons_mrp = models.TextField(db_column='cons-mrp', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    cons_pmp = models.TextField(db_column='cons-pmp', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    item_pai = models.CharField(db_column='item-pai', max_length=32)  # Field renamed to remove unsuitable characters.
    cod_roteiro = models.CharField(db_column='cod-roteiro', max_length=32)  # Field renamed to remove unsuitable characters.
    op_seq = models.IntegerField(db_column='op-seq')  # Field renamed to remove unsuitable characters.
    num_ord_inv = models.IntegerField(db_column='num-ord-inv', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_requisicao = models.IntegerField(db_column='nr-requisicao')  # Field renamed to remove unsuitable characters.
    sequencia = models.IntegerField()
    reaj_tabela = models.TextField(db_column='reaj-tabela', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    nr_tab = models.CharField(db_column='nr-tab', max_length=20)  # Field renamed to remove unsuitable characters.
    ep_codigo = models.CharField(db_column='ep-codigo', max_length=6, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    conta_contabil = models.CharField(db_column='conta-contabil', max_length=34, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_seq_contr = models.IntegerField(db_column='nr-seq-contr', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ordem_emitida = models.TextField(db_column='ordem-emitida', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    expectativa = models.TextField(blank=True, null=True)  # This field type is a guess.
    qt_solic = models.CharField(db_column='qt-solic', max_length=19, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cota_ordem = models.IntegerField(db_column='cota-ordem', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    seq_evento = models.IntegerField(db_column='seq-evento', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pend_aprov = models.IntegerField(db_column='pend-aprov', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    perc_vat = models.CharField(db_column='perc-vat', max_length=17, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    perc_sales_tax = models.CharField(db_column='perc-sales-tax', max_length=17, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_maq_origem = models.IntegerField(db_column='cod-maq-origem', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    num_processo_mp = models.IntegerField(db_column='num-processo-mp', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    char_1 = models.CharField(db_column='char-1', max_length=1000, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    char_2 = models.CharField(db_column='char-2', max_length=200, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dec_1 = models.CharField(db_column='dec-1', max_length=23, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dec_2 = models.CharField(db_column='dec-2', max_length=23, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    int_1 = models.IntegerField(db_column='int-1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    int_2 = models.IntegerField(db_column='int-2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    log_1 = models.TextField(db_column='log-1', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    log_2 = models.TextField(db_column='log-2', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    data_1 = models.DateField(db_column='data-1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_2 = models.DateField(db_column='data-2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_transp = models.IntegerField(db_column='cod-transp', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    num_id_documento = models.IntegerField(db_column='num-id-documento', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_contrato = models.IntegerField(db_column='nr-contrato')  # Field renamed to remove unsuitable characters.
    num_seq_item = models.IntegerField(db_column='num-seq-item')  # Field renamed to remove unsuitable characters.
    sit_ordem_contrat = models.IntegerField(db_column='sit-ordem-contrat', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dat_ordem = models.DateField(db_column='dat-ordem', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    check_sum = models.CharField(db_column='check-sum', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    prioridade_aprov = models.IntegerField(db_column='prioridade-aprov', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    origem_aprov = models.IntegerField(db_column='origem-aprov', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    gera_edi = models.TextField(db_column='gera-edi')  # Field renamed to remove unsuitable characters. This field type is a guess.
    cod_estab_gestor = models.CharField(db_column='cod-estab-gestor', max_length=10)  # Field renamed to remove unsuitable characters.
    licenca_import = models.CharField(db_column='licenca-import', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    loc_entrega = models.CharField(db_column='loc-entrega', max_length=60, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_entrega = models.CharField(db_column='cod-entrega', max_length=24, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    estab_entrega = models.CharField(db_column='estab-entrega', max_length=10, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_pedcli = models.CharField(db_column='nr-pedcli', max_length=24, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    seq_ped_venda = models.IntegerField(db_column='seq-ped-venda', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    local_entrega = models.IntegerField(db_column='local-entrega', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_estab_ctr = models.CharField(db_column='cod-estab-ctr', max_length=10, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_seq_contr_it = models.IntegerField(db_column='nr-seq-contr-it', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_contrato_venda = models.IntegerField(db_column='nr-contrato-venda', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_refer_b2b = models.CharField(db_column='cod-refer-b2b', max_length=100, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dat_inicio_leilao_rfq = models.DateField(db_column='dat-inicio-leilao-rfq', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dat_fim_leilao_rfq = models.DateField(db_column='dat-fim-leilao-rfq', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    hra_inicio_leilao_rfq = models.CharField(db_column='hra-inicio-leilao-rfq', max_length=16, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    hra_fim_leilao_rfq = models.CharField(db_column='hra-fim-leilao-rfq', max_length=16, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    log_cot_aberta = models.TextField(db_column='log-cot-aberta', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    log_leilao = models.TextField(db_column='log-leilao', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    cod_grp_compra = models.CharField(db_column='cod-grp-compra', max_length=24, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cdn_fabrican = models.IntegerField(db_column='cdn-fabrican')  # Field renamed to remove unsuitable characters.
    des_referencia = models.CharField(db_column='des-referencia', max_length=30, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_unid_negoc = models.CharField(db_column='cod-unid-negoc', max_length=6, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cdn_tip_lote_pregao = models.IntegerField(db_column='cdn-tip-lote-pregao', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    qtd_recbda_fut = models.CharField(db_column='qtd-recbda-fut', max_length=19, blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'ordem_compra'


class PedidoCompr(Base):
    num_pedido = models.IntegerField(db_column='num-pedido', primary_key=True)  # Field renamed to remove unsuitable characters.
    num_ped_benef = models.IntegerField(db_column='num-ped-benef')  # Field renamed to remove unsuitable characters.
    natureza = models.IntegerField()
    data_pedido = models.DateField(db_column='data-pedido')  # Field renamed to remove unsuitable characters.
    situacao = models.IntegerField()
    cod_emitente = models.IntegerField(db_column='cod-emitente')  # Field renamed to remove unsuitable characters.
    end_entrega = models.CharField(db_column='end-entrega', max_length=10)  # Field renamed to remove unsuitable characters.
    end_cobranca = models.CharField(db_column='end-cobranca', max_length=10)  # Field renamed to remove unsuitable characters.
    frete = models.IntegerField()
    cod_transp = models.IntegerField(db_column='cod-transp')  # Field renamed to remove unsuitable characters.
    via_transp = models.IntegerField(db_column='via-transp')  # Field renamed to remove unsuitable characters.
    cod_cond_pag = models.IntegerField(db_column='cod-cond-pag')  # Field renamed to remove unsuitable characters.
    responsavel = models.CharField(max_length=24)
    cod_mensagem = models.IntegerField(db_column='cod-mensagem')  # Field renamed to remove unsuitable characters.
    impr_pedido = models.TextField(db_column='impr-pedido')  # Field renamed to remove unsuitable characters. This field type is a guess.
    comentarios = models.CharField(max_length=1000)
    mot_elimina = models.CharField(db_column='mot-elimina', max_length=1000)  # Field renamed to remove unsuitable characters.
    nome_ass = models.CharField(db_column='nome-ass', max_length=186, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cargo_ass = models.CharField(db_column='cargo-ass', max_length=186, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    emergencial = models.TextField()  # This field type is a guess.
    nr_prox_ped = models.IntegerField(db_column='nr-prox-ped')  # Field renamed to remove unsuitable characters.
    contr_forn = models.TextField(db_column='contr-forn')  # Field renamed to remove unsuitable characters. This field type is a guess.
    nr_processo = models.IntegerField(db_column='nr-processo')  # Field renamed to remove unsuitable characters.
    compl_entrega = models.CharField(db_column='compl-entrega', max_length=14, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    l_tipo_ped = models.IntegerField(db_column='l-tipo-ped', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    l_classificacao = models.IntegerField(db_column='l-classificacao', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    l_ind_prof = models.TextField(db_column='l-ind-prof', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    i_importador = models.IntegerField(db_column='i-importador')  # Field renamed to remove unsuitable characters.
    i_situacao = models.IntegerField(db_column='i-situacao', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    c_cod_tabela = models.CharField(db_column='c-cod-tabela', max_length=20, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    i_moeda = models.IntegerField(db_column='i-moeda')  # Field renamed to remove unsuitable characters.
    i_cod_forma = models.IntegerField(db_column='i-cod-forma')  # Field renamed to remove unsuitable characters.
    i_cod_via = models.IntegerField(db_column='i-cod-via')  # Field renamed to remove unsuitable characters.
    c_prazo = models.CharField(db_column='c-prazo', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    c_descr_merc = models.CharField(db_column='c-descr-merc', max_length=324, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    i_cod_porto = models.IntegerField(db_column='i-cod-porto')  # Field renamed to remove unsuitable characters.
    de_vl_fob = models.CharField(db_column='de-vl-fob', max_length=19)  # Field renamed to remove unsuitable characters.
    c_embalagem = models.CharField(db_column='c-embalagem', max_length=186, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    c_observacao = models.CharField(db_column='c-observacao', max_length=760, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    i_exportador = models.IntegerField(db_column='i-exportador')  # Field renamed to remove unsuitable characters.
    desc_forma = models.CharField(db_column='desc-forma', max_length=72, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    desc_via = models.CharField(db_column='desc-via', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    de_vl_frete_i = models.CharField(db_column='de-vl-frete-i', max_length=17, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ind_orig_entrada = models.IntegerField(db_column='ind-orig-entrada', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    ind_via_envio = models.IntegerField(db_column='ind-via-envio', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nro_proc_entrada = models.IntegerField(db_column='nro-proc-entrada', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nro_proc_saida = models.IntegerField(db_column='nro-proc-saida', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nro_proc_alteracao = models.IntegerField(db_column='nro-proc-alteracao', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_maq_origem = models.IntegerField(db_column='cod-maq-origem', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    num_processo_mp = models.IntegerField(db_column='num-processo-mp', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    char_1 = models.CharField(db_column='char-1', max_length=200, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    char_2 = models.CharField(db_column='char-2', max_length=200, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dec_1 = models.CharField(db_column='dec-1', max_length=23, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dec_2 = models.CharField(db_column='dec-2', max_length=23, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    int_1 = models.IntegerField(db_column='int-1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    int_2 = models.IntegerField(db_column='int-2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    log_2 = models.TextField(db_column='log-2', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    data_1 = models.DateField(db_column='data-1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_2 = models.DateField(db_column='data-2', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    num_id_documento = models.IntegerField(db_column='num-id-documento', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_contrato = models.IntegerField(db_column='nr-contrato')  # Field renamed to remove unsuitable characters.
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)  # Field renamed to remove unsuitable characters.
    check_sum = models.CharField(db_column='check-sum', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    gera_edi = models.TextField(db_column='gera-edi')  # Field renamed to remove unsuitable characters. This field type is a guess.
    cod_estab_gestor = models.CharField(db_column='cod-estab-gestor', max_length=10)  # Field renamed to remove unsuitable characters.
    cod_emit_terc = models.IntegerField(db_column='cod-emit-terc', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    nr_ped_venda = models.IntegerField(db_column='nr-ped-venda', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_entrega = models.CharField(db_column='cod-entrega', max_length=24, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    endereco_text = models.CharField(max_length=1000, blank=True, null=True)
    endereco = models.CharField(max_length=80, blank=True, null=True)
    bairro = models.CharField(max_length=60, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    pais = models.CharField(max_length=40, blank=True, null=True)
    cep = models.CharField(max_length=24, blank=True, null=True)
    jurisdicao = models.CharField(max_length=40, blank=True, null=True)
    local_entrega = models.IntegerField(db_column='local-entrega', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_usuar_criac = models.CharField(db_column='cod-usuar-criac', max_length=24, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    dat_criac = models.DateField(db_column='dat-criac', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    cod_usuar_alter = models.CharField(db_column='cod-usuar-alter', max_length=24, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    hra_criac = models.CharField(db_column='hra-criac', max_length=16, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    hra_alter = models.CharField(db_column='hra-alter', max_length=16, blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'pedido_compr'


class StgEpm(Base):
    name = models.CharField(db_column='NAME', max_length=100)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TIMESTAMP', blank=True, null=True)  # Field name made lowercase.
    doubleval_value_field = models.FloatField(db_column='DOUBLEVAL(VALUE)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'stg_epm'


class StgItem(Base):
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)  # Field renamed to remove unsuitable characters.
    desc_item = models.CharField(db_column='desc-item', max_length=120, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_ult_ent = models.DateField(db_column='data-ult-ent', blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'stg_item'


class StgMovtoFluxoCx(Base):
    dat_movto_fluxo_cx = models.DateField()
    cod_estab = models.CharField(max_length=10)
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    val_movto_fluxo_cx = models.DecimalField(max_digits=17, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'stg_movto_fluxo_cx'


class StgRegiao(Base):
    cod_estab = models.IntegerField(db_column='COD_ESTAB', blank=True, null=True)  # Field name made lowercase.
    regiao = models.CharField(db_column='REGIAO', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stg_regiao'


class StgSaldo(Base):
    cod_estabel = models.CharField(db_column='cod-estabel', max_length=10)  # Field renamed to remove unsuitable characters.
    cod_depos = models.CharField(db_column='cod-depos', max_length=6)  # Field renamed to remove unsuitable characters.
    qtidade_atu = models.DecimalField(db_column='qtidade-atu', max_digits=19, decimal_places=4)  # Field renamed to remove unsuitable characters.
    it_codigo = models.CharField(db_column='it-codigo', max_length=32)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'stg_saldo'


class StgTipFluxo(Base):
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
    ind_tip_lancto_livro_cx = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_tip_fluxo'


class TipFluxoFinanc(Base):
    cod_tip_fluxo_financ = models.CharField(max_length=24)
    des_tip_fluxo_financ = models.CharField(max_length=80)
    ind_fluxo_movto_financ = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'tip_fluxo_financ'


class UmidadeBiomassa(Base):
    observacoes = models.TextField(db_column='OBSERVACOES', blank=True, null=True)  # Field name made lowercase.
    peso_liquido = models.TextField(db_column='PESO_LIQUIDO', blank=True, null=True)  # Field name made lowercase.
    peso_bruto = models.TextField(db_column='PESO_BRUTO', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='EMAIL', blank=True, null=True)  # Field name made lowercase.
    cnpj_fornecedor = models.TextField(db_column='CNPJ_FORNECEDOR', blank=True, null=True)  # Field name made lowercase.
    hr_entrada = models.TextField(db_column='HR_ENTRADA', blank=True, null=True)  # Field name made lowercase.
    utiliza_balde = models.TextField(db_column='UTILIZA_BALDE', blank=True, null=True)  # Field name made lowercase.
    transportadora = models.TextField(db_column='TRANSPORTADORA', blank=True, null=True)  # Field name made lowercase.
    umidade = models.TextField(db_column='UMIDADE', blank=True, null=True)  # Field name made lowercase.
    cod_unidade = models.TextField(db_column='COD_UNIDADE', blank=True, null=True)  # Field name made lowercase.
    unidade_medida = models.TextField(db_column='UNIDADE_MEDIDA', blank=True, null=True)  # Field name made lowercase.
    result_umidade_1 = models.TextField(db_column='RESULT_UMIDADE_1', blank=True, null=True)  # Field name made lowercase.
    entrada = models.DateField(db_column='ENTRADA', blank=True, null=True)  # Field name made lowercase.
    cnpj_unidade = models.TextField(db_column='CNPJ_UNIDADE', blank=True, null=True)  # Field name made lowercase.
    tipo_biomassa = models.TextField(db_column='TIPO_BIOMASSA', blank=True, null=True)  # Field name made lowercase.
    identificador = models.TextField(db_column='IDENTIFICADOR', blank=True, null=True)  # Field name made lowercase.
    num_nf = models.TextField(db_column='NUM_NF', blank=True, null=True)  # Field name made lowercase.
    qtd_item = models.TextField(db_column='QTD_ITEM', blank=True, null=True)  # Field name made lowercase.
    hr_saida = models.TextField(db_column='HR_SAIDA', blank=True, null=True)  # Field name made lowercase.
    peso_amostra_2 = models.TextField(db_column='PESO_AMOSTRA_2', blank=True, null=True)  # Field name made lowercase.
    metragem = models.TextField(db_column='METRAGEM', blank=True, null=True)  # Field name made lowercase.
    local_descarregamento = models.TextField(db_column='LOCAL_DESCARREGAMENTO', blank=True, null=True)  # Field name made lowercase.
    result_umidade_2 = models.TextField(db_column='RESULT_UMIDADE_2', blank=True, null=True)  # Field name made lowercase.
    result_umidade_3 = models.TextField(db_column='RESULT_UMIDADE_3', blank=True, null=True)  # Field name made lowercase.
    placa = models.TextField(db_column='PLACA', blank=True, null=True)  # Field name made lowercase.
    frete = models.TextField(db_column='FRETE', blank=True, null=True)  # Field name made lowercase.
    valor_frete = models.TextField(db_column='VALOR_FRETE', blank=True, null=True)  # Field name made lowercase.
    tempo_descarregamento = models.TextField(db_column='TEMPO_DESCARREGAMENTO', blank=True, null=True)  # Field name made lowercase.
    peso_amostra_1 = models.TextField(db_column='PESO_AMOSTRA_1', blank=True, null=True)  # Field name made lowercase.
    solicitacao = models.TextField(db_column='SOLICITACAO', blank=True, null=True)  # Field name made lowercase.
    fornecedor = models.TextField(db_column='FORNECEDOR', blank=True, null=True)  # Field name made lowercase.
    localizacao = models.TextField(db_column='LOCALIZACAO', blank=True, null=True)  # Field name made lowercase.
    valor_total = models.TextField(db_column='VALOR_TOTAL', blank=True, null=True)  # Field name made lowercase.
    emissao = models.DateField(db_column='EMISSAO', blank=True, null=True)  # Field name made lowercase.
    desc_item = models.TextField(db_column='DESC_ITEM', blank=True, null=True)  # Field name made lowercase.
    natureza = models.TextField(db_column='NATUREZA', blank=True, null=True)  # Field name made lowercase.
    cod_item = models.TextField(db_column='COD_ITEM', blank=True, null=True)  # Field name made lowercase.
    tara = models.TextField(db_column='TARA', blank=True, null=True)  # Field name made lowercase.
    cod_fornecedor = models.TextField(db_column='COD_FORNECEDOR', blank=True, null=True)  # Field name made lowercase.
    unidade = models.TextField(db_column='UNIDADE', blank=True, null=True)  # Field name made lowercase.
    valor_unit = models.TextField(db_column='VALOR_UNIT', blank=True, null=True)  # Field name made lowercase.
    motorista = models.TextField(db_column='MOTORISTA', blank=True, null=True)  # Field name made lowercase.
    peso_excedente = models.TextField(db_column='PESO_EXCEDENTE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'umidade_biomassa'
