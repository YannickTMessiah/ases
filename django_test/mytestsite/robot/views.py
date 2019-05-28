from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, date, timedelta
from pytz import timezone
import os

# CONSTANTES
PASTA_RELATORIOS = '../../relatorios'
ARQ_URLS         = '../../paginas.txt'

class Relatorio:
    
    def __init__(self, link, data, nota):
        self.link = link
        self.data = data
        self.nota = nota
        
    def pos(self):
        if int(self.nota[:2]) >= 95:
            return True
        else:
            return False
    
    def __lt__(self, other):
        return self.nota < other.nota
    
    def __eq__(self, other):
        return self.nota == other.nota

def report_list(request, n_dias=10):
    urls = []
    urls_sem_relatorio = []
    pastas = []
    datas = []
    relatorios = {}
    datas_relatorios = {}
    
    # datas dos ultimos N dias
    hoje = datetime.now(timezone(settings.TIME_ZONE)).date()
    for i in range(n_dias):
        data = hoje - timedelta(days = i)
        data_str = data.strftime('%d-%m-%Y')
        datas.append(data_str)

    # carrega lista com URLs
    with open(ARQ_URLS, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            lin = linha.strip()
            if len(lin) == 0 or lin[0] == '#':
                continue
            if 'http' in lin:
                urls.append(lin)

    # transforma URLs em nomes de pastas
    # inicializa o dicionario dos relatorios
    for url in urls:
        pastas.append(url.replace('/', '-'))
        relatorios[url] = []
        datas_relatorios[url] = []

    # processando as pastas
    for i, pasta in enumerate(pastas):
        diretorios = os.listdir(PASTA_RELATORIOS)
        if pasta in diretorios:
            arq_nota = os.path.join(PASTA_RELATORIOS, pasta, 'nota.txt')
            if os.path.isfile(arq_nota):
                with open(arq_nota, 'r', encoding='utf-8') as arquivo:
                    for linha in arquivo:
                        data_horario, nota = linha.strip().split()
                        data = data_horario[:10]
                        if data in datas:
                            link = os.path.join(pasta, data_horario + '.pdf')
                            relatorio = Relatorio(link, data, nota)
                            relatorios[urls[i]].append(relatorio)
                            datas_relatorios[urls[i]].append(data)
        else:
            urls_sem_relatorio.append(urls[i])
        
    # ordena as urls pela nota do relatório
    #urls = sorted(relatorios, key=relatorios.get, reverse=False)
    urls.sort(key=relatorios.get, reverse=False)
    
    return render(
        request, 
        'robot/report_list.html', 
        {
            'urls': urls, 
            'datas': datas, 
            'relatorios': relatorios, 
            'datas_relatorios': datas_relatorios
        }
    )

def report_show(request, report_link):
    arquivo = os.path.join(PASTA_RELATORIOS, report_link)
    with open(arquivo, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename='+report_link[-23:-13]
        return response