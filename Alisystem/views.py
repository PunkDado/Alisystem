# ALISYSTEM_GTO


from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Sum, F
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView # Para possibilitar a manipulação de dados com forms
from django.core.urlresolvers import reverse_lazy # Para possibilitar a manipulação de dados com forms
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from datetime import datetime, date
from Alisystem.models import Atendimento, Procedimentos_aplicado, Dentista

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

######## MÓDULO PAGAMENTOS - VERSÃO 1 ########################################################

# Método que mostra todos os valores líquidos recebidos e valores repassados, por dentista e por data de repasse
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
def atribui_data_repasse(request):
	data_repasse = date.today()	
	return render(request, 'app/data_repasse.html', {'data_repasse': data_repasse})

# Método que atribui confirma a data de repasse e atribui os valores de VALOR_LIQUIDO_RECEBIDO e VALOR_REPASSADO aos registros com RECEBIDO=TRUE e REPASSADO=FALSE
def confirma_data_repasse(request):
	data_repasse = date.today()	
	a = Procedimentos_aplicado.objects.filter(recebido=True, data_repasse=None).update(data_repasse=data_repasse)
	b = Procedimentos_aplicado.objects.filter(data_repasse=data_repasse)
	b.update(repassado=True)
	for procedimentos_aplicados in b:
		procedimentos_aplicados.valor_liquido_recebido = procedimentos_aplicados.valor_liquido()
		procedimentos_aplicados.valor_repassado = procedimentos_aplicados.valor_repasse()
		procedimentos_aplicados.save()
	num = Procedimentos_aplicado.objects.filter(data_repasse=data_repasse).count()

	return render(request, 'app/data_repasse_confirma.html', {'data_repasse': data_repasse, 'num': num, 'b': b})

######## FIM DO MÓDULO PAGAMENTOS - VERSÃO 1 ########################################################

######## MÓDULO PAINEIS - VERSÃO 1 ###############################################################

# Classe que mostra uma lista de todos os dentistas
class DentistaList(ListView):
    model = Dentista
    template_name = 'app/dentista_list.html'

# Classe que mostra uma lista de todos os atendimentos
class AtendimentoList(ListView):
    model = Atendimento
    template_name = 'app/atendimento_list.html'

# Classe para apresentar todos os atendimentos para o dentista selecionado
class AtendimentoDentistaList(ListView):
    template_name = 'app/atendimento_list.html'
    def get_queryset(self):
        self.dentista = get_object_or_404(Dentista, nome_completo=self.args[0])
        return Atendimento.objects.filter(dentista=self.dentista)

# Classe para apresentar os detalhes do Atendimento, ou seja, os procedimentos para cada Atendimento
class ProcedimentoAtendimentoList(DetailView):
	model = Atendimento
	template_name = 'app/procedimentos_por_atendimento.html'


# Classe para apresentar os procedimentos repassados no mês atual para o dentista selecionado
class Procedimentos_aplicadoDentistaDataList(ListView):
    template_name = 'app/procedimentos_list.html'
    def get_queryset(self):
        self.dentista = get_object_or_404(Dentista, nome_completo=self.args[0])
        atendimentos_dentista = Atendimento.objects.filter(dentista=self.dentista)
        return Procedimentos_aplicado.objects.filter(atendimento__in=atendimentos_dentista).filter(data_repasse__year=datetime.now().year).filter(data_repasse__month=datetime.now().month)


# Classe para apresentar os atendimentos glosados para o dentista selecionado
# Não está retornando nada, estou tentando
class AtendimentoDentistaGlosadoList(ListView):
    template_name = 'app/procedimentos_glosados.html'
    def get_queryset(self):
        self.dentista = get_object_or_404(Dentista, nome_completo=self.args[0])
        atendimentos_dentista = Atendimento.objects.filter(dentista=self.dentista)
        return Procedimentos_aplicado.objects.filter(atendimento__in=atendimentos_dentista).filter(glosado="True")



######## FIM DO MÓDULO PAINEIS - VERSÃO 1 #########################################################

############ FIM DA VERSÃO 1.0 ###############################################################



