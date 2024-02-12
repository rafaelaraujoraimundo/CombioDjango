from django.shortcuts import render
from dashboard.forms import DateForm
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import mysql.connector
from django.contrib.auth.decorators import permission_required
from dashboard.models import BiChamadosServiceUp
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import FactorRange
from plotly.offline import plot
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource, Select
from bokeh.transform import factor_cmap
from chartkick.django import ColumnChart
from bokeh.resources import CDN
import numpy as np
from bokeh.models import LabelSet, Label, TapTool, CustomJS, CDSView, GroupFilter
from bokeh.layouts import column, row, gridplot
import chartify


def view_padrao(request):
    activegroup = 'Dashboard'
    context = {'activegroup': activegroup}
    return render(request, 'dashboards/ti.html', context)


@permission_required('global_permissions.combio_dashboard_ti', login_url='erro_page')
def dashboard_ti(request):
    activegroup = 'Dashboard'
    start = request.GET.get('start')
    end = request.GET.get('end')
    chamadosti = BiChamadosServiceUp.objects.raw(""" SELECT 1 as ticket_id, queue_name fila,
    DATE(DATE_SUB(created, INTERVAL (DAYOFMONTH(created) - 1) DAY)) AS ANO_MES,
            COUNT(created) abertos, count(closed) fechados
    FROM bi_chamados_service_up
    group by CONCAT(SUBSTR(created, 1, 4), '-', SUBSTR(created, 6, 2), queue_name )""")

    # Criar DataFrame

    if start:
        start = datetime.strptime(start, '%Y-%m-%d').date()
    if end:
        end = datetime.strptime(end, '%Y-%m-%d').date()

    if start:
        chamadosti = [c for c in chamadosti if c.ANO_MES >= start]
    if end:
        chamadosti = [c for c in chamadosti if c.ANO_MES <= end]

    ano_mes = []
    fila = []
    abertos = []
    fechados = []

    for chamado in chamadosti:
        # Acessar os atributos do objeto e adicionar os valores às listas
        ano_mes.append(chamado.ANO_MES.strftime('%Y-%m'))
        fila.append(chamado.fila)
        abertos.append(chamado.abertos)
        fechados.append(chamado.fechados)
    data = {
        'ANO_MES': ano_mes,
        'fila': fila,
        'fechados': fechados,
    }
    df = pd.DataFrame(data)
    ANO_MES = ano_mes
    Abertos = abertos
    Fechados = fechados
    filas = fila

    # Dashboard Aninhado e agrupado
    palette = ["#c9d9d3", "#718dbf", "#e84d60"]

    x = [(str(ano_mes), fila)
         for ano_mes, fila in zip(df['ANO_MES'], df['fila'])]
    counts = sum(zip(df['fechados']), ())

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), width=1600, height=600, title="Chamados fechados por Fila",
               toolbar_location="above", resizable=True)

    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
           fill_color=factor_cmap('x', palette=palette, factors=[str(fila) for fila in df['fila']], start=1, end=2))
    labels = LabelSet(x='x', y='counts', text='counts', level='glyph',
                      x_offset=-11, y_offset=10, source=source)
    p.add_layout(labels)
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = -45
    p.xgrid.grid_line_color = None

    p1 = figure(x_range=ANO_MES, height=600, width=900,
                title="Bar Chart", toolbar_location="above", resizable=True, sizing_mode="stretch_width")

    bar_width = 0.3  # Largura das barras
    bar_offset = 0.30  # Deslocamento das barras
    bar_offset2 = 0.70
    p1.vbar(x=np.arange(len(ANO_MES)) + bar_offset2, top=Abertos, width=bar_width,
            color='blue', legend_label='Abertos')
    p1.vbar(x=np.arange(len(ANO_MES)) + bar_offset, top=Fechados, width=bar_width,
            color='red', legend_label='Fechados')

    p1.legend.location = "top_left"  # Posição da legenda
    p1.legend.title = "Legenda"  # Título da legenda
    p1.legend.click_policy = "hide"
    text_offset = 3
    p1.text(x=np.arange(len(ANO_MES)) + bar_offset2, y=np.add(Abertos, text_offset), text=Abertos, text_font_size='10pt', text_color='black',
            text_baseline='bottom', text_align='center')

    p1.text(x=np.arange(len(ANO_MES)) + bar_offset, y=np.add(Fechados, text_offset), text=Fechados, text_font_size='10pt', text_color='black',
            text_baseline='bottom', text_align='center')

    p2 = figure(width_policy="auto", height_policy="auto", x_range=ANO_MES, height=600, width=900,
                title="Bar Chart Nested", toolbar_location="above", resizable=True, sizing_mode="stretch_width")
    source = ColumnDataSource(
        data={'ANO_MES': ANO_MES, 'Filas': filas, 'Abertos': Abertos, 'Fechados': Fechados})
    p2.vbar(x='ANO_MES', top='Abertos', width=0.5, fill_alpha=0.5,
            color='blue', legend_field='Filas', source=source)
    p2.vbar(x='ANO_MES', top='Fechados', width=0.5, fill_alpha=0.5,
            color='blue', legend_field='Filas', source=source)
    p2.legend.click_policy = "hide"

    p3 = figure(width_policy="auto", height_policy="auto", x_range=ANO_MES, height=600, title="Bar Chart Stacking and Grouping",
                toolbar_location="above", resizable=True, width=900, sizing_mode="stretch_width")

    source = ColumnDataSource(
        data={'ANO_MES': ANO_MES, 'Abertos': Abertos, 'Fechados': Fechados})

    p3.vbar_stack(['Abertos', 'Fechados'], x='ANO_MES', width=0.5, color=['blue', 'red'],
                  legend_label=['Abertos', 'Fechados'], source=source)

    p3.legend.location = "top_left"  # Posição da legenda
    p3.legend.title = "Legenda"  # Título da legenda

    text_offset = 5  # Ajuste de posição vertical dos textos

    # Conversão das datas para strings para as posições horizontais

    p3.xaxis.major_label_orientation = 1  # Orientação dos rótulos do eixo x

    # Line Chart
    p4 = figure(x_range=ANO_MES, height=600,
                title="Line Chart", toolbar_location="above", resizable=True, sizing_mode="stretch_width")
    p4.line(ANO_MES, Abertos, line_width=2, color='blue')

    # Multiple Lines
    p5 = figure(x_range=ANO_MES, height=600,
                title="Multiple Lines", toolbar_location="above", resizable=True, sizing_mode="stretch_width")

    p5.line(ANO_MES, Abertos, line_width=2,
            color='blue', legend_label='Abertos')
    p5.line(ANO_MES, Fechados, line_width=2,
            color='red', legend_label='Fechados')

# Adicionando os valores acima das linhas Abertos
    p5.text(ANO_MES, Abertos, text=Abertos, text_font_size='10pt',
            text_color='blue', text_baseline='bottom', text_align='center')

# Adicionando os valores acima das linhas Fechados
    p5.text(ANO_MES, Fechados, text=Fechados, text_font_size='10pt',
            text_color='red', text_baseline='bottom', text_align='center')

    # Stacked Lines
    p6 = figure(x_range=ANO_MES, height=600, width=500,
                title="Stacked Lines", toolbar_location=None, sizing_mode="stretch_width")
    p6.line(ANO_MES, Abertos, line_width=2,
            color='blue', legend_label='Abertos')
    p6.line(ANO_MES, [a + f for a, f in zip(Abertos, Fechados)],
            line_width=2, color='red', legend_label='Total')

    # Combining with Markers
    p7 = figure(x_range=ANO_MES, height=350, width=500,
                title="Combining with Markers", toolbar_location=None, sizing_mode="stretch_width")
    p7.line(ANO_MES, Abertos, line_width=2,
            color='blue', legend_label='Abertos')
    p7.circle(ANO_MES, Abertos, size=8, color='blue', fill_color='white')

    # Scatter Markers
    p8 = figure(x_range=ANO_MES, height=350,
                title="Scatter Markers", toolbar_location=None, sizing_mode="stretch_width")
    p8.scatter(ANO_MES, Abertos, size=8, color='blue')
    # p1.toolbar.autohide = True
    # p2.toolbar.autohide = True
   # p3.toolbar.autohide = True
    # p4.toolbar.autohide = True
   # p5.toolbar.autohide = True
   # p6.toolbar.autohide = True
   # p7.toolbar.autohide = True
   # p8.toolbar.autohide = True
    # Renderizar os gráficos

    layout = [
        [p],
        [row(p1, p2)],
        [row(p3, p4)],
        [row(p5, p6)],
        [row(p7, p8)]
    ]

    grid = gridplot(layout, sizing_mode="stretch_width")

    # Obter o HTML e o JavaScript para o layout responsivo
    script_layout, div_layout = components(grid)

    context = {
        'script_layout': script_layout,
        'div_layout': div_layout,
        'activegroup': activegroup
    }
    return render(request, 'dashboards/ti.html', context)


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


@permission_required('global_permissions.combio_dashboard_controladoria', login_url='erro_page')
def dashboard_controladoria(request):
    activegroup = 'Dashboard'
    # Conectar ao banco de dados
    con = mysql.connector.connect(
        host='172.16.0.15', database='dw_combio', user='usr_combio',
        password='Cmb@Dw12.2020')

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
        'nested_chart': a,
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
