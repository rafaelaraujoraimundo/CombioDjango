from django.db import models
from administration.models import ServidorFluig

class FluigDatabaseInfo(models.Model):
    servidor_fluig = models.ForeignKey(ServidorFluig, on_delete=models.PROTECT)
    database_name = models.CharField(max_length=255)
    database_version = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255)
    driver_version = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fluig_database_info'
        app_label = 'api_v1'

class FluigDatabaseSize(models.Model):
    servidor_fluig = models.ForeignKey(ServidorFluig, on_delete=models.PROTECT)
    size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fluig_database_size'

class FluigRuntime(models.Model):
    servidor_fluig = models.ForeignKey(ServidorFluig, on_delete=models.PROTECT)
    start_time = models.BigIntegerField()
    uptime = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fluig_runtime'

class FluigOperationSystem(models.Model):
    servidor_fluig = models.ForeignKey(ServidorFluig, on_delete=models.PROTECT)
    server_memory_size = models.BigIntegerField()
    server_memory_free = models.BigIntegerField()
    server_hd_space = models.CharField(max_length=255)
    server_hd_space_free = models.CharField(max_length=255)
    server_core_system = models.IntegerField()
    server_arch_system = models.CharField(max_length=255)
    server_temp_size = models.BigIntegerField()
    server_log_size = models.BigIntegerField()
    heap_max_size = models.BigIntegerField()
    heap_size = models.BigIntegerField()
    system_uptime = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fluig_operation_system'

class Dataset(models.Model):
    servidor_fluig = models.ForeignKey(ServidorFluig, on_delete=models.PROTECT)
    datasetid = models.CharField(max_length=255)
    datasetdescription = models.TextField(blank=True, null=True)
    datasetimpl = models.TextField(blank=True, null=True)
    datasetbuilder = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    serveroffline = models.BooleanField(default=False)
    mobilecache = models.BooleanField(default=False)
    internal = models.BooleanField(default=False)
    custom = models.BooleanField(default=True)
    generated = models.BooleanField(default=False)
    offlinemobilecache = models.BooleanField(default=False)
    mobileofflinesummary = models.CharField(max_length=100)
    updateinterval = models.BigIntegerField(default=0)
    lastreset = models.BigIntegerField(default=0)
    lastremotesync = models.BigIntegerField(default=0)
    joblastexecution = models.CharField(max_length=100, blank=True, null=True)
    jobnextexecution = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100)
    journalingadherencefull = models.BooleanField(default=False)
    journalingadherencehalf = models.BooleanField(default=True)
    journalingadherencenone = models.BooleanField(default=False)
    syncstatussuccess = models.BooleanField(default=True)
    syncstatuswarning = models.BooleanField(default=False)
    syncstatuserror = models.BooleanField(default=False)
    syncdetails = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'fluig_dataset'