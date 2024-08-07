from django.db import models
from django.contrib.auth.models import Group, Permission
import json
# Create your models here.


class GrupoMenu(models.Model):
    codigo = models.CharField(max_length=40, default='codigo default')
    nomegrupo = models.CharField(max_length=40)
    icon_grupo = models.CharField(max_length=80)
    grupo = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)
    order = models.PositiveIntegerField(default=99)

    class Meta:
        db_table = 'grupomenu'

    def __str__(self):
        return self.nomegrupo


class ItensMenu(models.Model):
    codigo = models.CharField(max_length=40)
    item = models.CharField(max_length=40)
    grupo_id = models.ForeignKey(
        GrupoMenu, on_delete=models.PROTECT)
    icon_item = models.CharField(max_length=80)
    url = models.CharField(max_length=80)
    permission = models.ForeignKey(
        Permission, on_delete=models.PROTECT, null=True)
    order = models.PositiveIntegerField(default=99)
    class Meta:
        db_table = 'itensmenu'

    def __str__(self):
        return self.grupo_id.nomegrupo + ' - ' + self.item
