"""
ALISYSTEM 1.0 - TEST/LOCAL VERSION
Definition of forms.
"""

from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from Alisystem.models import Convenio, Dentista, Atendimento, Procedimentos_aplicado

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

class InserirAtendimentoForm(forms.ModelForm):
	class Meta:
		model = Atendimento
		fields = ['dentista', 'paciente', 'convenio', 'data_atendimento', 'num_GTO', 'data_envio', 'mes_recebimento', 
		'comentarios', 'encaminhado_por', 'verificado']

'''
	model Atendimento
	dentista = models.ForeignKey(Dentista)
	paciente = models.ForeignKey(Paciente)
	convenio = models.ForeignKey(Convenio, null=True)
	forma_pagamento = models.ForeignKey(Formas_pagamento, blank=True, null=True, verbose_name = 'Forma de pagamento')
	data_atendimento = models.DateField(blank=True, null=True, verbose_name = 'Data do atendimento')
	num_GTO = models.CharField(max_length = 30, null=True, blank = True, verbose_name = 'Número da GTO')
#	procedimentos_aplicados = models.ManyToManyField(Procedimentos_aplicado)
	data_envio = models.DateField(blank=True, null=True, verbose_name = 'Data de envio')
	mes_recebimento = models.DateField(blank=True, null=True, verbose_name = 'Mês de recebimento')
	comentarios = models.CharField(max_length = 500, blank=True, verbose_name = 'Comentários')
#	encaminhamento = models.ForeignKey(Encaminhamento, blank=True, null=True, help_text="Registre novos encaminhamentos aqui")
	encaminhado_por = models.CharField(max_length = 30, blank=True, verbose_name = 'Encaminhado por', help_text='Registrar nome do dentista ou funcionário que encaminhou o paciente')
	verificado = models.BooleanField(blank=True, default=False, verbose_name = 'Atendimento verificado', help_text='Atendimento verificado pela administração do consultório')
	''' 

class InserirProcedimentos_aplicadoForm(forms.ModelForm):
	class Meta:
		model = Procedimentos_aplicado
		fields = ['procedimento', 'dente', 'descr_anterior', 'valor_real', 'valor_liquido_recebido', 'valor_repassado', 'recebido', 'glosado', 'motivo_glosa', 
		'data_recebimento', 'data_recebimento', 'data_repasse', 'repassado']
		
Procedimentos_aplicadoFormSet = inlineformset_factory(Atendimento, Procedimentos_aplicado, form=InserirProcedimentos_aplicadoForm, extra=1)


'''
model Procedimentos_aplicado
	atendimento = models.ForeignKey(Atendimento, blank=True, null=True)
	procedimento = models.ForeignKey(Procedimento, blank=True, null=True, help_text='Escolha o seu procedimento nesta lista, ou insira um novo procedimento clicando no sinal de +') # Procedimentos padronizados a partir da tabela de preços
	dente = models.CharField(max_length = 20, blank = True, help_text='Registre qual o dente tratado')
	descr_anterior = models.CharField(max_length = 200, blank=True, verbose_name="Descrição do procedimento", help_text = 'Descrição anterior do procedimento (Opcional)')
	valor_real = models.FloatField(blank=True, null=True, verbose_name = 'Valor')
	valor_liquido_recebido = models.FloatField(blank=True, null=True, verbose_name = 'Valor líquido efetivamente recebido')
	valor_repassado = models.FloatField(blank=True, null=True, verbose_name = 'Valor repassado ao dentista')
	recebido = models.BooleanField(blank=True, default=False)
	glosado = models.BooleanField(blank=True, default=False)
	motivo_glosa = models.CharField(max_length = 200, blank=True, verbose_name = 'Motivo da glosa')
	data_recebimento = models.DateField(blank=True, null=True, verbose_name = 'Data de recebimento')
	data_repasse = models.DateField(blank=True, null=True, verbose_name = 'Data de repasse')
	repassado = models.BooleanField(blank=True, default=False)
'''