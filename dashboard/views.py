from django.shortcuts import get_object_or_404, render
from dashboard.forms import DateForm
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import mysql.connector
from api_v1.tasks import get_FluigServer, get_datasets
from django.contrib.auth.decorators import permission_required
from dashboard.models import BiChamadosServiceUp
from bokeh.plotting import figure
from bokeh.embed import components  
from bokeh.transform import dodge
from bokeh.resources import CDN
from api_v1.models import FluigDatabaseInfo, FluigDatabaseSize, FluigOperationSystem, FluigRuntime, Dataset
from administration.models import ServidorFluig
import chartify
from django.utils import timezone
from inventario.tasks import populate_hardware_data
from django.contrib.auth.decorators import login_required, permission_required


def view_padrao(request):
    activegroup = 'Dashboard'
    
    context = {'activegroup': activegroup}
    return render(request, 'dashboards/ti.html', context)

@login_required(login_url='account_login') 
@permission_required('global_permissions.combio_dashboard', login_url='erro_page')
def dashboard_fluig(request, servidor_id=None):
    activegroup = 'Dashboard'
    title = 'Servidores Fluig'
    servidores = ServidorFluig.objects.all().order_by('id')
    servidor_id = request.GET.get('servidor_id')
    status = request.GET.get('status', 'todos') 

    servidor_selecionado = get_object_or_404(ServidorFluig, id=servidor_id) if servidor_id else servidores.first()

    datasets = Dataset.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at')
    if status != 'todos':
        if status == 'sucesso':
            datasets = datasets.filter(syncstatussuccess=True)
        elif status == 'warning':
            datasets = datasets.filter(syncstatuswarning=True)
        elif status == 'erro':
            datasets = datasets.filter(syncstatuserror=True)

    # Inicializa um dicionário para o servidor selecionado
    dados_servidor = {
        'servidor': servidor_selecionado,
        'ultimo_database_info': FluigDatabaseInfo.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'ultimo_database_size': FluigDatabaseSize.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'ultimo_runtime': FluigRuntime.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'ultimo_operation_system': FluigOperationSystem.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'dados_memoria': FluigOperationSystem.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at'),
        'datasets': datasets,
        'lasted_update_dataset': Dataset.objects.latest('created_at').created_at,
        'lasted_update_operation_system': FluigOperationSystem.objects.latest('created_at').created_at,
    }

    if dados_servidor['ultimo_operation_system']:
        try:
            server_hd_space = float(dados_servidor['ultimo_operation_system'].server_hd_space.replace(',', '.'))
            server_hd_space_free = float(dados_servidor['ultimo_operation_system'].server_hd_space_free.replace(',', '.'))
            server_hd_space_used = server_hd_space - server_hd_space_free
        except ValueError:
            server_hd_space_used = None

    dados_servidor['server_hd_space_used'] = server_hd_space_used

    agora = timezone.now()

# Filtra objetos criados no início do dia até o momento atual
    inicio_do_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_do_dia = inicio_do_dia + timedelta(days=1)
    dados_memoria = FluigOperationSystem.objects.filter(
                                                        servidor_fluig=servidor_selecionado,
                                                        created_at__range=(inicio_do_dia, fim_do_dia)
                                                ).order_by('-created_at'
                                                                        ).values('created_at', 'server_memory_size', 'server_memory_free')

    # Preparar os dados para o gráfico
    datas = [dado['created_at'].strftime("%Y-%m-%dT%H:%M:%S") for dado in dados_memoria]
    memoria_usada_mb = [int((dado['server_memory_size'] - dado['server_memory_free']) / (1024 * 1024)) for dado in dados_memoria]
    memoria_total_mb = [int(dado['server_memory_size'] / (1024 * 1024)) for dado in dados_memoria]


    # Convertendo os dados para JSON para serem utilizados pelo JavaScript
    dados_grafico = {
        'datas': datas,
        'memoria_usada_mb': memoria_usada_mb,
        'memoria_total_mb': memoria_total_mb,
     }
    dados_grafico_json = json.dumps(dados_grafico)
    context = {
        'servidor_selecionado': dados_servidor,  # Passa os dados do servidor selecionado
        'servidores': servidores,  # Passa a lista de todos os servidores para o template
        'activegroup': activegroup,
        'dados_grafico_json': dados_grafico_json, 
        'title': title,
    }
    return render(request, 'dashboards/ti.html', context)

@login_required(login_url='account_login') 
@permission_required('global_permissions.combio_dashboard_ti', login_url='erro_page')
def dashboard_ti2(request):
    activegroup = 'Dashboard'
    chamadosti = BiChamadosServiceUp.objects.raw(""" SELECT 1 as ticket_id,
    DATE(DATE_SUB(created, INTERVAL (DAYOFMONTH(created) - 1) DAY)) AS ANO_MES,
            COUNT(created) abertos, count(closed) fechados
    FROM bi_chamados_service_up
    group by CONCAT(SUBSTR(created, 1, 4), '-', SUBSTR(created, 6, 2))""")
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start:
        start = datetime.strptime(start, '%Y-%m-%d').date()
    if end:
        end = datetime.strptime(end, '%Y-%m-%d').date()

    if start:
        chamadosti = [c for c in chamadosti if c.ANO_MES >= start]
    if end:
        chamadosti = [c for c in chamadosti if c.ANO_MES <= end]
    ano_mes = []
    abertos = []
    fechados = []
    for chamado in chamadosti:
        # Acessar os atributos do objeto e adicionar os valores às listas
        ano_mes.append(chamado.ANO_MES.strftime('%Y-%m'))
        abertos.append(chamado.abertos)
        fechados.append(chamado.fechados)

    # Criando o plot2 do Bokeh
    plot2 = figure(title="Dashboard de Abertos e Fechados", x_axis_name='Data', y_axis_name='Quantidade',
                   x_range=ano_mes, width=600, height=400)

    # Criando uma fonte de dados do Bokeh
    source = {
        'data2': ano_mes,
        'abertos2': abertos,
        'fechados2': fechados,
    }

    # Adicionando as colunas "Abertos" e "Fechados" ao gráfico
    plot2.vbar(x=dodge('data2', -0.15, range=plot2.x_range), top='abertos2', width=0.25, color='blue', legend_name='Abertos',
               source=source)
    plot2.vbar(x=dodge('data2', 0.15, range=plot2.x_range), top='fechados2', width=0.25, color='red', legend_name='Fechados',
               source=source)

    # Ajustando o estilo do plot2
    plot2.legend.location = "top_right"
    plot2.legend.click_policy = "hide"

    # Convertendo o plot2 em HTML e JavaScript usando o método components do Bokeh
    script2, div2 = components(plot2)

    context = {'form': DateForm, 'script2': script2,
               'div2': div2, 'activegroup': activegroup}
    return render(request, 'dashboards/ti.html', context)

@login_required(login_url='account_login') 
@permission_required('global_permissions.combio_dashboard_controladoria', login_url='erro_page')
def dashboard_controladoria(request):
    activegroup = 'Dashboard'
    # Conectar ao banco de dados
   # con = mysql.connector.connect(
    #    host='172.16.0.15', database='dw_combio', user='usr_combio',
    #    password='Cmb@Dw12.2020')

    # Definir a consulta SQL
    sql_query = '''
        SELECT
            be.Regional,
            be.NOME_FANTASIA,
            centroCusto,
            descricaoCusto,
            conta,
            descricaoConta,
            bec.estabelecimento,
            DATE_FORMAT(dataRealizado, '%Y-%m-01') AS primeiroDiaMes,
            IFNULL(ROUND(SUM(valorRealizado), 2),0) AS valorTotalRealizado
        FROM
            bi_efz1005_cep bec
        LEFT JOIN
            bi_estabelecimento be ON bec.estabelecimento = be.estabelecimento
        WHERE dataRealizado between '2023-01-01' and '2023-05-31'
        GROUP BY
            be.Regional,
            be.NOME_FANTASIA,
            conta,
            descricaoConta,
            bec.estabelecimento,
            centroCusto,
            descricaoCusto,
            primeiroDiaMes
    '''

    # Executar a consulta SQL e obter os resultados como um dataframe do Pandas
    df = pd.read_sql(sql_query, con)
    # Criar a primeira tabela usando Plotly
    pivot_df = df.pivot_table(values='valorTotalRealizado',
                              index=['Regional', 'NOME_FANTASIA', 'centroCusto',
                                     'descricaoCusto', 'conta',
                                     'descricaoConta'],
                              columns='primeiroDiaMes')

# Resetar o índice para converter em colunas
    pivot_df.reset_index(inplace=True)

# Renomear as colunas
    pivot_df.columns = ['REGIONAL', 'NOME_FANTASIA', 'CENTRO DE CUSTO',
                        'descricaoCusto', 'CONTA', 'DESCRICAO_CONTA'] + pivot_df.columns[6:].tolist()
    pivot_df.fillna(0, inplace=True)
# Verificar as colunas presentes no pivot_df
    print(pivot_df.columns)

    fig1 = go.Figure(data=[go.Table(
        header=dict(values=list(pivot_df.columns)),
        cells=dict(values=[pivot_df[col] for col in pivot_df.columns]),
        # Ajustar o tamanho das colunas
        columnwidth=[50] + [100] * (len(pivot_df.columns) - 1),
    )])
# Definir o layout do gráfico
    fig1.update_layout(
        # Adicionar barra de rolagem horizontal
        width=800,
        height=500,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2f2f2f'),
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        hovermode='closest',
        showlegend=True,
        autosize=False,
    )

    # Converter a primeira tabela para HTML
    table1_html = fig1.to_html(full_html=False)
    # Filtrar a segunda tabela com base na seleção da primeira tabela
    selected_col = request.GET.get('selected_col')
    if selected_col:
        selected_estabelecimento = pivot_df.index.get_level_values('estabelecimento')[
            int(selected_col)]
        filtered_df = df[df['estabelecimento'] == selected_estabelecimento]

        # Criar a segunda tabela usando Plotly
        pivot_filtered_df = filtered_df.pivot_table(values='valorTotalRealizado',
                                                    index=['Regional', 'NOME_FANTASIA', 'centroCusto',
                                                           'descricaoCusto', 'conta', 'descricaoConta'],
                                                    columns='primeiroDiaMes')

        fig2 = go.Figure(data=[go.Table(
            header=dict(values=list(pivot_filtered_df.columns)),
            cells=dict(values=[pivot_filtered_df[col] for col in pivot_filtered_df.columns]))
        ])

        # Converter a segunda tabela para HTML
        table2_html = fig2.to_html(full_html=False)

        # Renderizar o template com as tabelas em HTML
        return render(request, 'dashboards/controladoria.html', {'table1_html': table1_html, 'table2_html': table2_html})

    # Renderizar o template inicial
    return render(request, 'dashboards/controladoria.html', {'table1_html': table1_html, 'activegroup': activegroup})

@login_required(login_url='account_login') 
@permission_required('global_permissions.combio_dashboard_controladoria', login_url='erro_page')
def exemplo(request):
    activegroup = 'Dashboard'


# Exemplo de uso
    ANO_MES = ('2023-04', '2023-06', '2023-05', '2023-05', '2023-04')
    Abertos = (3, 107, 22, 147, 67)
    Fechados = (95, 18, 99, 19, 135)
    filas = ['TI::N2::Fluig', 'TI::N2::Diversos', 'TI::N2::Hardware', 'TI::N2::Software',
             'TI::N3::Projetos::Melhorias']

    data = {
        'ANO_MES': ANO_MES,
        'Abertos': Abertos,
        'Fechados': Fechados,
        'Filas': filas
    }

    df = pd.DataFrame(data)

    # Gráfico de Barras Aninhados
    nested_chart = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    nested_chart.set_title('Gráfico de Barras Aninhados')
    nested_chart.set_subtitle('Abertos e Fechados por Fila')
    nested_chart.plot.bar(
        data_frame=df,
        categorical_columns=['Filas', 'ANO_MES'],
        numeric_column='Abertos',
        color_column='Fechados'
    )
    a = nested_chart.show(format='html')

    context = {
        'activegroup': activegroup
    }

    return render(request, 'dashboards/exemplo.html', context)


def dashboard_exemplo2(request):
    # Dados para os gráficos
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    # Criação dos gráficos
    line_plot = figure(title="Gráfico de Linha",
                       x_axis_label='X', y_axis_label='Y')
    line_plot.line(x, y, legend_label='Linha', line_width=2)

    bar_plot = figure(title="Gráfico de Barras",
                      x_axis_label='Categoria', y_axis_label='Valores')
    bar_plot.vbar(x=['A', 'B', 'C', 'D'], top=[4, 6, 8, 2], width=0.5)

    bar_plot = figure(title="Gráfico de Barras",
                      x_axis_label='Categoria', y_axis_label='Valores')
    bar_plot.vbar(x=x, top=y, width=0.5)

    scatter_plot = figure(title="Gráfico de Dispersão",
                          x_axis_label='X', y_axis_label='Y')
    scatter_plot.circle(x, y, size=10, color='navy', alpha=0.5)
 # Criação do gráfico de barras clusterizadas
    clustered_bar_plot = figure(title="Gráfico de Barras Clusterizadas", x_range=[
                                'Grupo 1', 'Grupo 2', 'Grupo 3'], x_axis_label='Grupos', y_axis_label='Valores')
    clustered_bar_plot.vbar(x=['Grupo 1', 'Grupo 2', 'Grupo 3'], top=[
                            4, 5, 2], width=0.2, color='red', legend_label='Série 1')
    clustered_bar_plot.vbar(x=['Grupo 1', 'Grupo 2', 'Grupo 3'], top=[
                            2, 3, 4], width=0.2, color='blue', legend_label='Série 2')
    clustered_bar_plot.vbar(x=['Grupo 1', 'Grupo 2', 'Grupo 3'], top=[
                            1, 6, 5], width=0.2, color='green', legend_label='Série 3')

    # Criação do gráfico de linhas clusterizadas
    clustered_line_plot = figure(
        title="Gráfico de Linhas Clusterizadas", x_axis_label='X', y_axis_label='Y')
    clustered_line_plot.line(
        x, y, legend_label='Linha 1', line_width=2, color='red')
    clustered_line_plot.line(
        x, [5, 4, 3, 2, 1], legend_label='Linha 2', line_width=2, color='blue')
    clustered_line_plot.line(
        x, [2, 2, 2, 2, 2], legend_label='Linha 3', line_width=2, color='green')

    # Renderiza os gráficos para HTML
    script, div = components(line_plot, CDN)
    script2, div2 = components(bar_plot, CDN)
    script3, div3 = components(scatter_plot, CDN)
    script4, div4 = components(clustered_bar_plot, CDN)
    script5, div5 = components(clustered_line_plot, CDN)
    # Renderiza os gráficos para HTML

    return render(request, 'dashboards/exemplo2.html', {'script': script, 'div': div, 'script2': script2, 'div2': div2, 'script3': script3, 'div3': div3, 'script4': script4, 'div4': div4, 'script5': script5, 'div5': div5})
