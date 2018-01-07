"""
ALISYSTEM 1.0 - TEST/LOCAL VERSION
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
#from app.models import Convenio, Dentista, Atendimento

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
"""
class EscolherConvenioForm(forms.Form):
	convenio=Convenio.objects.all()
	lista = [("0", "--")]
	contador=0
	for linha in convenio:
		contador = contador + 1
		lista.append((contador,linha.convenio))
	convenio = forms.ChoiceField(required=False, choices=lista)
#	convenio = forms.CharField(max_length=40, widget=forms.Select(choices=lista))
#	dentista = forms.CharField(max_length=100, help_text="Escolha o dentista aqui")

class RegistrarPagamentosForm(forms.Form):
	num_GTO = forms.CharField(max_length = 30, label="Número da GTO")
	dentista = forms.CharField(max_length=100)
	paciente = forms.CharField(max_length=100)
	convenio = forms.CharField(max_length=40)

"""
"""
	forma_pagamento = forms.CharField(max_length=30)
	
	procedimento = forms.CharField() # Procedimentos padronizados a partir da tabela de preços
	descr_anterior = forms.CharField(max_length = 200)
	data_atendimento = forms.DateField()
	valor_real = forms.FloatField()
	valor_recebido = forms.FloatField()
	desconto = forms.FloatField()
	data_envio = forms.DateField()
	mes_recebimento = forms.DateField()
	recebido = forms.BooleanField()
	glosado = forms.BooleanField()
"""
"""
class EscolherDentistaForm(forms.Form):
	dentista=Dentista.objects.all()
	lista = [("0", "--")]
	contador=0
	for linha in dentista:
		contador = contador + 1
		lista.append((contador,linha.nome_completo))
	dentista = forms.ChoiceField(required=False, choices=lista)

class EscolherDataForm(forms.Form):
	atendimentos=Atendimento.objects.all()
	lista = [("0", "--")]
	contador=0
	for linha in atendimentos:
		contador = contador + 1
		if linha not in lista: lista.append((contador,linha.data_repasse))
	data_repasse = forms.ChoiceField(required=False, choices=lista)

"""
"""
class RegistrarPagamentosForm(forms.Form):
	dentista = forms.CharField(max_length=100)
	paciente = forms.CharField(max_length=100)
	convenio = forms.CharField(max_length=40)
	forma_pagamento = forms.CharField(max_length=30)
	num_GTO = forms.CharField(max_length = 30, label="Número da GTO")
	procedimento = forms.CharField() # Procedimentos padronizados a partir da tabela de preços
	descr_anterior = forms.CharField(max_length = 200)
	data_atendimento = forms.DateField()
	valor_real = forms.FloatField()
	valor_recebido = forms.FloatField()
	desconto = forms.FloatField()
	data_envio = forms.DateField()
	mes_recebimento = forms.DateField()
	recebido = forms.BooleanField()
	glosado = forms.BooleanField()
	motivo_glosa = forms.CharField()
	data_repasse = forms.DateField()
	repassado = forms.BooleanField()
	comentarios = forms.CharField(max_length = 500)
	encaminhamento = forms.CharField()
	encaminhado_por = forms.CharField(max_length = 30)
"""
