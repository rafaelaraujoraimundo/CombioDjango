from django.db import models
from django.contrib.auth.models import Group, Permission
import json
# Create your models here.


class GrupoMenu(models.Model):
    codigo = models.CharField(max_length=40, default='codigo default')
    NomeGrupo = models.CharField(max_length=40)
    icon_grupo = models.CharField(max_length=80)
    grupo = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'grupoMenu'

    def __str__(self):
        return self.NomeGrupo


class ItensMenu(models.Model):
    codigo = models.CharField(max_length=40, default='codigo default')
    Item = models.CharField(max_length=40)
    grupo_id = models.ForeignKey(
        GrupoMenu, on_delete=models.PROTECT)
    icon_item = models.CharField(max_length=80)
    url = models.CharField(max_length=80)
    permission = models.ForeignKey(
        Permission, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'ItensMenu'

    def __str__(self):
        return self.Item
