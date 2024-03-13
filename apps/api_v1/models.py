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