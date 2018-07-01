# ALISYSTEM_GTO - Código de teste local


from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Sum, F
from django.db import transaction
from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView # Para possibilitar a manipulação de dados com forms
from django.core.urlresolvers import reverse_lazy # Para possibilitar a manipulação de dados com forms
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from datetime import datetime, date
from Alisystem.models import Atendimento, Procedimentos_aplicado, Dentista
from Alisystem.forms import RegistrarPagamentosForm, InserirAtendimentoForm, InserirProcedimentos_aplicadoForm, Procedimentos_aplicadoFormSet


############ FUNÇÕES QUE PODEM SER UTILIZADAS AO LONGO DO CÓDIGO #################################

# Faz o total de valor real para uma lista de objetos de tabelas
def somar_valor_real(objetos, data_repasse): # Funciona tranquilo
	tabela = objetos.filter(data_repasse=data_repasse)
	soma = 0
	for linha in tabela:
		if linha.valor_real != None: soma = soma + linha.valor_real
	soma = round(soma * 100,0) / 100
	return soma

# Faz o total de valor líquido para uma lista de objetos de tabelas
# Funciona, mas o código ficou super lento na tabela que totaliza os pagamentos/ Nem roda no Heroku
# Talvez a solução seja armazenar o resultado na base de dados
# Criado o campo valor_liquido_recebido para tornar a operação mais ágil
def somar_valor_liquido(objetos, data_repasse): 
	tabela = objetos.filter(data_repasse=data_repasse)
	soma = 0
	for linha in tabela:
		if linha.valor_liquido_recebido != None: soma = soma + linha.valor_liquido_recebido
	soma = round(soma * 100,0) / 100
	return soma

# Faz o total de valor líquido para uma lista de objetos de tabelas
# Funciona, mas o código ficou super lento na tabela que totaliza os pagamentos/ Nem roda no Heroku
# Talvez a solução seja armazenar o resultado na base de dados
# Criado o campo valor_repassado para armazenar o valor repassado a cada nova data de repasse
def somar_valor_repasse(objetos, data_repasse): 
	tabela = objetos.filter(data_repasse=data_repasse)
	soma = 0
	for linha in tabela:
		if linha.valor_repassado != None: soma = soma + linha.valor_repassado
	soma = round(soma * 100,0) / 100
	return soma

############ FIM DE FUNÇÕES QUE PODEM SER UTILIZADAS AO LONGO DO CÓDIGO #################################

###################### VERSÃO 1.0 ################################################################

###############    HOME, CONTATO E SOBRE    ###########################################################
############### CÓDIGO REUTILIZADO DO AZURE ###########################################################
# método context_instance() retirado do código; talvez tenha que voltar para publicar no Azure
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    dia = "%02d" % (datetime.now().day)
    mes = "%02d" % (datetime.now().month)
    minuto = "%02d" % (datetime.now().minute)
    hora_atual = '%s/%s/%s, %sh%s' % (dia, mes, datetime.now().year, datetime.now().hour, minuto)
    return render(
        request,
        'app/home.html',
        
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'hora_atual': hora_atual,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        
        {
            'title':'Contato',
            'message':'Entre em contato conosco',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        
        {
            'title':'Sobre Alisystem',
            'message':'Aplicação para gestão de clínicas odontológicas',
            'year':datetime.now().year,
        }
    )

############### FIM DE HOME, CONTATO E SOBRE ################################################

################ MÓDULO ATENDIMENTOS ########################################################

# Método que cria um formulário para inserir atendimentos
def registrar_pagamentos(request):
    if request.method == 'POST':
        form = InserirAtendimentoForm(request.POST)
        #form_1 = InserirProcedimentos_aplicadoForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit = False)
            atendimento.data_envio = datetime.now()
            atendimento.save()
            #form_1 = InserirProcedimentos_aplicadoForm(request.POST)
            #form_1.atendimento = atendimento
            #if form_1.is_valid():
            #    procedimento_aplicado = form_1.save(commint = False)
            #    procedimento_aplicado.save()

            return HttpResponseRedirect ('/registrar_pagamentos')
        

    else:
        form = InserirAtendimentoForm()
    return render(request, 'app/registrar_pagamentos.html', {'form': form})#, 'form_1': form_1})

def contact_thanks(request):
    return render(request, 'app/obrigado.html', {})

# Classe para criar procedimentos aplicadosm aninhados em cada atendimento
class AtendimentosProcedimentos_aplicadoCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Atendimento
    template_name = 'app/atendimento_form.html'
    fields = ['dentista', 'paciente', 'convenio', 'data_atendimento', 'num_GTO', 'data_envio', 'mes_recebimento',
    'comentarios', 'encaminhado_por', 'verificado']

    def get_context_data(self, **kwargs):
        data = super(AtendimentosProcedimentos_aplicadoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['procedimentos_aplicados'] = Procedimentos_aplicadoFormSet(self.request.POST)
        else:
            data['procedimentos_aplicados'] = Procedimentos_aplicadoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        procedimentos_aplicados = context['procedimentos_aplicados']
        with transaction.atomic():
            self.object = form.save()

            if procedimentos_aplicados.is_valid():
                procedimentos_aplicados.instance = self.object
                procedimentos_aplicados.save()
        return super(AtendimentosProcedimentos_aplicadoCreate, self).form_valid(form)

# Classe para inserir atendimentos
class AtendimentoCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Atendimento
    fields = ['dentista', 'paciente', 'convenio', 'data_atendimento', 'num_GTO', 'data_envio', 'mes_recebimento', 
    'comentarios', 'encaminhado_por', 'verificado']

############### FIM DE ATENDIMENTOS ################################################

######## MÓDULO PAGAMENTOS - VERSÃO 1 ########################################################

# Método que mostra todos os valores líquidos recebidos e valores repassados, por dentista e por data de repasse
@login_required(login_url = '/login/')
def mostra_pagamentos(request):
    header = ["Dentista"] 	# Lista todas as datas de repasse
    datas_repasse = Procedimentos_aplicado.objects.order_by('data_repasse').values_list('data_repasse', flat=True).distinct()
    for i in datas_repasse:
        if i != None: header.append(i)	# { DENTISTA, data1, data2, ... }
    procedimentos_aplicados = Procedimentos_aplicado.objects.all()
    table_liquido = [header]
    table_repasse = [header]
    d = Dentista.objects.all()
    for dentista in d: # Para cada dentista em Dentista, soma os valores recebidos em cada data de repasse
        pagamentos_dentista_liquido = [dentista.nome_completo]
        pagamentos_dentista_repasse = [dentista.nome_completo]
    
        for data in datas_repasse: # Para cada data em datas_repasse, soma os valores recebidos para cada dentista
            if data != None:
                atendimentos_dentista = Atendimento.objects.filter(dentista=dentista)
                procedimentos_aplicados_dentista = Procedimentos_aplicado.objects.filter(atendimento__in = atendimentos_dentista)
                soma_liquido = somar_valor_liquido(procedimentos_aplicados_dentista, data)
                soma_repasse = somar_valor_repasse(procedimentos_aplicados_dentista, data)
                
                if soma_liquido == None: pagamentos_dentista_liquido.append(soma_liquido)
                else: pagamentos_dentista_liquido.append(soma_liquido)
                
                if soma_repasse == None: pagamentos_dentista_repasse.append(soma_repasse)
                else: pagamentos_dentista_repasse.append(soma_repasse)
        
        table_liquido.append(pagamentos_dentista_liquido)
        table_repasse.append(pagamentos_dentista_repasse)
    
    return render(request, 'app/pagamentos.html', {'table_liquido': table_liquido, 'table_repasse': table_repasse})
	
# Método que atribui HOJE como data de repasse aos dentistas
@login_required(login_url = '/login/')
def atribui_data_repasse(request):
	data_repasse = date.today()	
	return render(request, 'app/data_repasse.html', {'data_repasse': data_repasse})

'''
# Método que executa queries SQL diretamete, eliminando a camada de models
def atribui_valores():
    query = "UPDATE public.'Alisystem_procedimentos_aplicado' AS papl SET valor_liquido_recebido = valor_real * (1 - 0.1133) FROM public.'Alisystem_atendimento' AS att WHERE papl.atendimento_id = att.id AND att.convenio_id <> 12 AND papl.data_repasse = '2018-05-05' AND papl.recebido = TRUE AND valor_liquido_recebido IS NULL;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = "Pronto"

    return row
'''

# Método que confirma a data de repasse e atribui TRUE para os valores repassados
@login_required(login_url = '/login/')
def confirma_data_repasse(request):
    data_repasse = date.today()
    a = Procedimentos_aplicado.objects.filter(recebido=True, data_repasse=None).update(data_repasse=data_repasse)
    b = Procedimentos_aplicado.objects.filter(data_repasse=data_repasse)
    num = b.count()
    b.update(repassado=True)
    
    # Este código faz o update usando SQL no sistema de teste; no sistema em produção não funciona
    query = ''' UPDATE public.'Alisystem_procedimentos_aplicado' AS papl 
                SET valor_liquido_recebido = valor_real * (1 - 0.1133) 
                FROM public.'Alisystem_atendimento' AS att 
                WHERE papl.atendimento_id = att.id 
                AND att.convenio_id <> 12 
                AND papl.data_repasse = '2018-05-05' 
                AND papl.recebido = TRUE 
                AND valor_liquido_recebido IS NULL;
                '''
    """cursor = connection.cursor()
    try:
        #cursor.execute("UPDATE Alisystem_procedimentos_aplicado AS papl SET valor_liquido_recebido = valor_real * (1 - 0.1133) FROM Alisystem_atendimento AS att WHERE papl.atendimento_id = att.id AND att.convenio_id <> 12 AND papl.data_repasse = '2018-05-05' AND papl.recebido = TRUE AND valor_liquido_recebido IS NULL;")
        #cursor.execute("SELECT COUNT(*) FROM Alisystem_procedimentos_aplicado;")
        cursor.execute('''  UPDATE Alisystem_procedimentos_aplicado 
                            SET valor_liquido_recebido = valor_real * (1 - 0.1333)
                            WHERE data_repasse = %s;''' % data_repasse)
        cursor.execute('''  UPDATE Alisystem_procedimentos_aplicado 
                            SET valor_repassado = valor_liquido_recebido * 0.5
                            WHERE data_repasse = %s;''' % data_repasse)
        #cursor.execute("UPDATE Alisystem_procedimentos_aplicado SET valor_liquido_recebido = valor_real * (1 - 0.1133) FROM Alisystem_atendimento WHERE atendimento_id = Alisystem_atendimento.id AND Alisystem_atendimento.convenio_id <> 12 AND data_repasse = '2018-05-05' AND recebido = TRUE AND valor_liquido_recebido IS NULL;")
    finally:
        cursor.close()
    """

    # Este trecho calcula corretamente no sistema de teste; no sistema em produção no Heroku não calcula
    '''
    for procedimentos_aplicados in b:
        procedimentos_aplicados.valor_liquido_recebido = procedimentos_aplicados.valor_liquido()
        procedimentos_aplicados.valor_repassado = procedimentos_aplicados.valor_repasse()
        procedimentos_aplicados.save()
    '''
    
    '''
    k = 5
    num_updates = int(num / k)
    
    # Descobri que o subset b[0:1] só traz o primeiro registro, e que b[0:10] só traz 10 registros, de b[0] a b[9];
    # Descobri também que b[um número] não retorna nada
    if num_updates >= 1:
        for i in range(num_updates):
            inicio_local = i*k
            fim_local = i*k+k
            c = b[inicio_local:fim_local]
            for procedimentos_aplicados in c:
                procedimentos_aplicados.valor_liquido_recebido = procedimentos_aplicados.valor_liquido()
                procedimentos_aplicados.valor_repassado = procedimentos_aplicados.valor_repasse()
                procedimentos_aplicados.save()
    
    c = b[num_updates * k:num]
    for procedimentos_aplicados in c:
                procedimentos_aplicados.valor_liquido_recebido = procedimentos_aplicados.valor_liquido()
                procedimentos_aplicados.valor_repassado = procedimentos_aplicados.valor_repasse()
                procedimentos_aplicados.save()
    '''
    

    return render(request, 'app/data_repasse_confirma.html', {'data_repasse': data_repasse, 'num': num, 'b': b})

# Método que atribui os valores de VALOR_LIQUIDO_RECEBIDO e VALOR_REPASSADO aos registros com RECEBIDO=TRUE e REPASSADO=FALSE    
def atualiza_valores(request):
    data_repasse = date.today()
    b = Procedimentos_aplicado.objects.filter(data_repasse=data_repasse)
    num = b.count()
    k = 5
    num_updates = int(num / k)
    
    # Descobri que o subset b[0:1] só traz o primeiro registro, e que b[0:10] só traz 10 registros, de b[0] a b[9];
    # Descobri também que b[um número] não retorna nada
    if num_updates >= 1:
        for i in range(num_updates):
            inicio_local = i*k
            fim_local = i*k+k
            c = b[inicio_local:fim_local]
            for procedimentos_aplicados in c:
                procedimentos_aplicados.valor_liquido_recebido = procedimentos_aplicados.valor_liquido()
                procedimentos_aplicados.valor_repassado = procedimentos_aplicados.valor_repasse()
                procedimentos_aplicados.save()
    
    c = b[num_updates * k:num]
    for procedimentos_aplicados in c:
                procedimentos_aplicados.valor_liquido_recebido = procedimentos_aplicados.valor_liquido()
                procedimentos_aplicados.valor_repassado = procedimentos_aplicados.valor_repasse()
                procedimentos_aplicados.save()

    return render(request, 'app/data_repasse_confirma.html', {'data_repasse': data_repasse, 'num': num, 'b': b})



"""
# Método que cria um formulário para registrar os pagamentos
def registrar_pagamentos(request):
    if request.method == 'POST':
        form = InserirAtendimentoForm(request.POST)
        #cd = form.cleaned_data
        form.save(commit = False)
        return HttpResponseRedirect ('/contact/thanks')
    else:
        form = InserirAtendimentoForm()
    return render(request, 'app/registrar_pagamentos.html', {'form': form})
"""



######## FIM DO MÓDULO PAGAMENTOS - VERSÃO 1 ########################################################

######## MÓDULO PAINEIS - VERSÃO 1 ###############################################################

# Classe que mostra uma lista de todos os dentistas
class DentistaList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Dentista
    template_name = 'app/dentista_list.html'

# Classe que mostra uma lista de todos os atendimentos

class AtendimentoList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Atendimento
    template_name = 'app/atendimento_list.html'



# Classe para apresentar todos os atendimentos para o dentista selecionado
class AtendimentoDentistaList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'app/atendimento_list.html'
    def get_queryset(self):
        self.dentista = get_object_or_404(Dentista, nome_completo=self.args[0])
        return Atendimento.objects.filter(dentista=self.dentista)

# Classe para apresentar os detalhes do Atendimento, ou seja, os procedimentos para cada Atendimento
class ProcedimentoAtendimentoList(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Atendimento
    template_name = 'app/procedimentos_por_atendimento.html'


# Classe para apresentar os procedimentos repassados no mês atual para o dentista selecionado
class Procedimentos_aplicadoDentistaDataList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'app/procedimentos_list.html'
    def get_queryset(self):
        self.dentista = get_object_or_404(Dentista, nome_completo=self.args[0])
        atendimentos_dentista = Atendimento.objects.filter(dentista=self.dentista)
        return Procedimentos_aplicado.objects.filter(atendimento__in=atendimentos_dentista).filter(data_repasse__year=datetime.now().year).filter(data_repasse__month=datetime.now().month)


# Classe para apresentar os atendimentos glosados para o dentista selecionado
# Não está retornando nada, estou tentando
class AtendimentoDentistaGlosadoList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'app/procedimentos_glosados.html'
    def get_queryset(self):
        self.dentista = get_object_or_404(Dentista, nome_completo=self.args[0])
        atendimentos_dentista = Atendimento.objects.filter(dentista=self.dentista)
        return Procedimentos_aplicado.objects.filter(atendimento__in=atendimentos_dentista).filter(glosado="True")



######## FIM DO MÓDULO PAINEIS - VERSÃO 1 #########################################################

############ FIM DA VERSÃO 1.0 ###############################################################



