"""ALISYSTEM_GTO

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
admin.autodiscover()
from Alisystem.forms import BootstrapAuthenticationForm, RegistrarPagamentosForm
from django.contrib.auth.views import *
from Alisystem.views import home, contact, about
from Alisystem.views import DentistaList, AtendimentoList, AtendimentoDentistaList, ProcedimentoAtendimentoList, Procedimentos_aplicadoDentistaDataList, AtendimentoDentistaGlosadoList
from Alisystem.views import mostra_pagamentos, atribui_data_repasse, confirma_data_repasse, atualiza_valores, registrar_pagamentos, contact_thanks
from Alisystem.views import AtendimentosProcedimentos_aplicadoCreate


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    
    # Telas básicas
    url(r'^$', home, name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about', about, name='about'),
    
    # Login e logout
	url(r'^login/$', login, {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Entre',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$', logout, {  'next_page': '/'  },        name='logout'),
    
    # MÓDULO INSERIR ATENDIMENTOS
    url(r'^inserir_atendimentos/$', AtendimentosProcedimentos_aplicadoCreate.as_view(), name='inserir_atendimentos'),
    
    # MÓDULO PAGAMENTOS
	url(r'^pagamentos/$', mostra_pagamentos, name="pagamentos"),
    url(r'^pagamentos/data_repasse/$', atribui_data_repasse),
	url(r'^pagamentos/data_repasse/confirma/$', confirma_data_repasse),
    url(r'^pagamentos/data_repasse/confirma/atualiza$', atualiza_valores),
    url(r'^registrar_pagamentos/$', registrar_pagamentos, name="registrar_pagamentos"),
    url(r'^registrar_pagamentos/apresenta$', registrar_pagamentos, name="registrar_pagamentos"),
    url(r'^contact/thanks$', contact_thanks),
    
    # MÓDULO PAINÉIS
    url(r'^dentistas/$', DentistaList.as_view(), name='dentistas'),
    url(r'^atendimentos/dentista/([\w-]+)/$', AtendimentoDentistaList.as_view()),
    url(r'^atendimentos/$', AtendimentoList.as_view(), name='atendimentos'),
    url(r'^atendimentos/(?P<pk>[0-9]+)/$', ProcedimentoAtendimentoList.as_view(), name = 'atendimento_list'),
    url(r'^atendimentos/dentista/([\w-]+)/(?P<pk>[0-9]+)/$', ProcedimentoAtendimentoList.as_view()),
    url(r'^procedimentos/dentista/([\w-]+)/$', Procedimentos_aplicadoDentistaDataList.as_view()),
    url(r'^procedimentos/dentista/([\w-]+)/glosado/$', AtendimentoDentistaGlosadoList.as_view()),
]


"""
URL no Alisystem_pg
from datetime import datetime
from django.conf.urls import url
from app.forms import BootstrapAuthenticationForm
from app.views import home, contact, about, AtendimentoList, AtendimentoConvenioList, AtendimentoDentistaList, AtendimentoDentistaDataList, AtendimentoDentistaGlosadoList, ConvenioList, Tipos_procedimentoList, Tipos_procedimentoDetail, escolher_convenio, apresenta_pagamentos, registrar_pagamentos, ConvenioCreate, ConvenioUpdate, ConvenioDelete, ConvenioDetail #, escolher_dentista
from app.views import painel_dentistas
from app.views import atribui_data_repasse, confirma_data_repasse, mostra_pagamentos
from app.models import *
from django.contrib.auth.views import *


# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
# URL's V1.0
	
	# Telas básicas
    url(r'^$', home, name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about', about, name='about'),
	
	# Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^admin/', include(admin.site.urls)),
	
	# MÓDULO PAGAMENTOS
	url(r'^pagamentos/$', mostra_pagamentos),
	url(r'^pagamentos/data_repasse/$', atribui_data_repasse),
	url(r'^pagamentos/data_repasse/confirma/$', confirma_data_repasse),
	
	# MÓDULO PAINEIS
	url(r'^painel/$', painel_dentistas, name='painel'),
	url(r'^painel/([\w-]+)/$', AtendimentoDentistaList.as_view()),
	url(r'^painel/data/([\w-]+)/$', AtendimentoDentistaDataList.as_view()),
	url(r'^painel/glosado/([\w-]+)/$', AtendimentoDentistaGlosadoList.as_view()),
	
	# Login e logout
	url(r'^login/$', login, {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Entre',
                'year':datetime.now().year,
            }
        },
        name='login'),
       url(r'^logout$', logout, {  'next_page': '/'  },        name='logout'),

# URL's V2.0

	# Escolher convenio em uma lista - Não consegui ligar o form à view
	url(r'^pagamentos/$', escolher_convenio, name='pagamentos'), 
	url(r'^pagamentos/registrar/$', registrar_pagamentos, name='registrar_pagamentos'), 
	url(r'^pagamentos/apresenta/$', apresenta_pagamentos), 

	# Manipulação da tabela Convenio (funciona)
	url(r'^convenio/$', ConvenioList.as_view(), name='convenio_list'),
#	url(r'^convenio/(?P<pk>[0-9]+)/detail/$', ConvenioDetail.as_view(), name='convenio_detail'),
	url(r'^convenio/add/$', ConvenioCreate.as_view(), name='convenio_add'),
	url(r'^convenio/(?P<pk>[0-9]+)/$', ConvenioUpdate.as_view(), name='convenio_update'),
	url(r'^convenio/(?P<pk>[0-9]+)/delete/$', ConvenioDelete.as_view(), name='convenio_delete'),

	# Listas de atendimentos: todos, por convenio e por dentista (funciona)       
 	url(r'^atendimentos/$', AtendimentoList.as_view()), 
	url(r'^atendimentos/convenio/([\w-]+)/$', AtendimentoConvenioList.as_view(), name='atendimento_convenio_list'),
	url(r'^atendimentos/dentista/([\w-]+)/$', AtendimentoDentistaList.as_view()),
	
	# Lista de tipos de atendimento (funciona)
	url(r'^tipos/$', Tipos_procedimentoList.as_view()),
#	url(r'^(?P<slug>[-\w]+)/$', Tipos_procedimentoDetail.as_view(), name='procedimentos-tipo'),
      
       
]


"""