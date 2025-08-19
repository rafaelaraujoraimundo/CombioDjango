# Entrar no diretório do projeto
cd /app/CombioDjango

# Ativar o ambiente virtual
source venv/bin/activate

# Gerar migrações com base em alterações nos modelos
python manage.py makemigrations

# Aplicar migrações no banco de dados
python manage.py migrate

# Coletar arquivos estáticos para produção
python manage.py collectstatic --noinput

# Sair do ambiente virtual (caso necessário)
deactivate

# Reiniciar os serviços
sudo systemctl restart gunicorn
sudo systemctl restart celery
sudo systemctl restart celery-beat
sudo systemctl restart zrok

# Verificar status de todos os serviços (descomente se quiser checar)
# sudo systemctl status gunicorn
# sudo systemctl status celery
# sudo systemctl status celery-beat
# sudo systemctl status zrok

# Ver logs em tempo real (opcional, descomente se precisar)
# journalctl -u gunicorn -f
# journalctl -u celery -f
# journalctl -u celery-beat -f
# tail -f /var/log/nginx/error.log