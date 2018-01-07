# Alisystem_GTO Experiência de colocar vários procedimentos na mesma GTO

from django.db import models
from django.core.urlresolvers import reverse # Para possibilitar a manipulação de dados com forms


# Create your models here.

class Convenio(models.Model):
    convenio = models.CharField(max_length=40)
    
    def get_absolute_url(self):	# Para possibilitar a manipulação de dados com forms
    	return reverse('convenio_list') #, kwargs={'pk': self.pk})
    
    def __str__(self): # Ordenação por 'convenio'
        return self.convenio
    class Meta:	ordering = ['convenio']
    


class Paciente(models.Model):
    nome_completo = models.CharField(max_length=100)
    nome_responsavel = models.CharField(max_length=100, blank = True, verbose_name = 'Nome do responsável')
#   convenio = models.ForeignKey(Convenio)
    data_nascimento = models.DateField(blank = True, null = True, verbose_name = 'Data de nascimento')
    email = models.EmailField(blank = True, verbose_name = 'e-mail')
    
    def __str__(self):
        return self.nome_completo
    class Meta: ordering = ['nome_completo']

class Formas_pagamento(models.Model):
    forma_pagamento = models.CharField(max_length=30, verbose_name = 'Forma de pagamento')
    comissao = models.FloatField(blank=True, null=True, verbose_name = 'Comissão/ impostos (%)', help_text='Registre aqui o valor da comissão dos meios de pagamento ou da alíquota de impostos')
    taxa_fixa = models.FloatField(blank=True, null=True, verbose_name = 'Taxa Fixa (R$)')
    
    def __str__(self):
        return self.forma_pagamento

class Dentista(models.Model):
    nome_completo = models.CharField(max_length=100)
    num_CRO = models.CharField(max_length=100, blank = True, verbose_name = 'Número do CRO')
    email = models.EmailField(blank = True, verbose_name = 'E-mail')
    cpf = models.CharField(max_length=11, blank = True)
    banco = models.CharField(max_length=30, blank = True)
    num_agencia = models.CharField(max_length=4, blank = True, verbose_name = 'Agência número')
    num_conta = models.CharField(max_length=20, blank = True, verbose_name = 'Conta número')
    
    def __str__(self):
        return self.nome_completo
    class Meta: ordering = ['nome_completo']
       
class Tipos_procedimento(models.Model):
	tipo_procedimento = models.CharField(max_length=30, blank = True, verbose_name = 'Tipo do procedimento')
	
	def __str__(self):
		return self.tipo_procedimento

class Procedimento(models.Model):
    procedimento = models.CharField(max_length=100)
    tipo_procedimento = models.ForeignKey(Tipos_procedimento, blank = True, null = True, verbose_name = 'Tipo do procedimento')
    tabela_preço = models.FloatField(blank=True, null=True, verbose_name = 'Tabela de preço')
        
    def __str__(self):
        return self.procedimento
    class Meta: ordering = ['procedimento']

class Tabela_preco(models.Model):
    procedimento = models.ForeignKey(Procedimento)
    convenio = models.ForeignKey(Convenio)
    preco = models.FloatField(blank=True, null=True, verbose_name = 'Preço')
    
    
#    def __str__(self):
#       return self.procedimento
    class Meta: ordering = ['procedimento']

class Encaminhamento(models.Model):
	descricao = models.CharField(max_length = 200, blank=True)
	paciente = models.ForeignKey(Paciente)
	dentista = models.ForeignKey(Dentista)
	data_encaminhamento = models.DateField(verbose_name = 'Data do encaminhamento')
	
	def __str__(self):
		return self.descricao

	class Meta:
		ordering = ['paciente']

## Tabela Atendimento contém a GTO
class Atendimento(models.Model):
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
	
#	def valor_GTO(self):
#		valor_GTO = 
	
	def get_absolute_url(self):
		return reverse('atendimento_convenio_list', kwargs={'pk': self.pk})
	
	def __str__(self):
		dentista = self.dentista
		convenio = self.convenio
		paciente = self.paciente
		atendimento = dentista.nome_completo + "/ " + convenio.convenio + "/ " + paciente.nome_completo
		return atendimento

	class Meta:
		ordering = ['data_atendimento']



## Tabela Procedimentos_aplicado, em relacionamento 1-muitos com Atendimento (que contém a GTO)
## Cada Atendimento (GTO), contém vários Procedimentos_aplicados
class Procedimentos_aplicado(models.Model):
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
	#	desconto = models.FloatField(blank=True, null = True)	
    
	def __str__(self):
		procedimento = self.procedimento
		valor_real = self.valor_real
		nome_procedimento = procedimento.procedimento + "/ " + str(valor_real)
		return nome_procedimento
		
#	def num_GTO(self):
#		atendimento = Atendimento_procedimentos_aplicados.atendimento
#		num_GTO = atendimento.
#		return 

	class Meta:
		ordering = ['procedimento']
			

	def valor_liquido(self): 		#Esse código pode melhorar, fazendo um loop sobre os elementos da tabela Formas_pagamento
	
		if self.valor_real != None: 

			particular = Convenio.objects.filter(convenio="Particular")[0]
			credito = Formas_pagamento.objects.filter(forma_pagamento="Cartão de crédito a vista")[0]
			credito_2_6_formas = (
				"Cartão de crédito 2 parcelas",
				"Cartão de crédito 3 parcelas",
				"Cartão de crédito 4 parcelas",
				"Cartão de crédito 5 parcelas",
				"Cartão de crédito 6 parcelas",
			)
			credito_2_6 = Formas_pagamento.objects.filter(forma_pagamento__in = credito_2_6_formas)[0]
			credito_7_12_formas = (
				"Cartão de crédito 7 parcelas",
				"Cartão de crédito 8 parcelas",
				"Cartão de crédito 9 parcelas",
				"Cartão de crédito 10 parcelas",
				"Cartão de crédito 11 parcelas",
				"Cartão de crédito 12 parcelas",
			)
			credito_7_12 = Formas_pagamento.objects.filter(forma_pagamento__in = credito_7_12_formas)[0]
			debito = Formas_pagamento.objects.filter(forma_pagamento="Cartão de débito")[0]
			boleto = Formas_pagamento.objects.filter(forma_pagamento="Boleto bancário")[0]
			repasse_convenio = Formas_pagamento.objects.filter(forma_pagamento="Repasse do convênio")[0]
            
            # Regra de negócios geral pacientes particulares pagamentos em cartão de crédito		
			if self.atendimento.convenio == particular and self.atendimento.forma_pagamento == credito:
				valor_liquido = self.valor_real * (1-credito.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em cartão de crédito 2-6 parcelas		
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == credito_2_6:
				valor_liquido = self.valor_real * (1-credito_2_6.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em cartão de crédito 7-12 parcelas
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == credito_7_12:
				valor_liquido = self.valor_real * (1-credito_7_12.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em cartão de débito			
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == debito:
				valor_liquido = self.valor_real * (1-debito.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em boleto bancário		
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == boleto:
				valor_liquido = self.valor_real - boleto.taxa_fixa
			# Regra de negócios geral pacientes particulares pagamentos em dinheiro, cheque ou transferência
			elif self.atendimento.convenio == particular:
				valor_liquido = self.valor_real
			# Regra de negócios geral pacientes de convênio
			else: valor_liquido = self.valor_real * (1-repasse_convenio.comissao/100)
			
			valor_liquido = round(valor_liquido * 100, 0)/100
		
		else: valor_liquido = self.valor_real
		
		return valor_liquido


#				particular = Convenio.objects.filter(id=41)[0] # Na base do Heroku, id = 11
#				for forma_pagamento in Formas_pagamento.objects.all():
#					if self.convenio == particular and self.forma_pagamento == forma_pagamento[0]:
#						valor_liquido = self.valor_real * (1 - forma_pagamento[0].comissao/100) - forma_pagamento[0].taxa_fixa

		
	def valor_repasse(self):
		
		if self.valor_real != None: 
			
			# Busca os objetos que contém os elementos que serão necessários nas regras de negócios (veja logo após a definição do método)
			tatiana = Dentista.objects.filter(id=30)[0]
			talita = Dentista.objects.filter(id=29)[0]
			camila = Dentista.objects.filter(id=20)[0]
			eduardo = Dentista.objects.filter(id=23)[0]
			fernando = Dentista.objects.filter(id=24)[0]
			ortodontia = Procedimento.objects.filter(tipo_procedimento=Tipos_procedimento.objects.filter(id=7))
#			orto_remo = Procedimento.objects.filter(id=83)
			orto_manu = Procedimento.objects.filter(procedimento__contains="MANUTENÇÃO")
			protese = Procedimento.objects.filter(tipo_procedimento=Tipos_procedimento.objects.filter(id=9))
			endodontia = Procedimento.objects.filter(tipo_procedimento=Tipos_procedimento.objects.filter(id=4))
			particular = Convenio.objects.filter(convenio="Particular")[0]
			credito = Formas_pagamento.objects.filter(forma_pagamento="Cartão de crédito a vista")[0]
			credito_2_6_formas = (
				"Cartão de crédito 2 parcelas",
				"Cartão de crédito 3 parcelas",
				"Cartão de crédito 4 parcelas",
				"Cartão de crédito 5 parcelas",
				"Cartão de crédito 6 parcelas",
			)
			credito_2_6 = Formas_pagamento.objects.filter(forma_pagamento__in = credito_2_6_formas)[0]
			credito_7_12_formas = (
				"Cartão de crédito 7 parcelas",
				"Cartão de crédito 8 parcelas",
				"Cartão de crédito 9 parcelas",
				"Cartão de crédito 10 parcelas",
				"Cartão de crédito 11 parcelas",
				"Cartão de crédito 12 parcelas",
			)
			credito_7_12 = Formas_pagamento.objects.filter(forma_pagamento__in = credito_7_12_formas)[0]
			debito = Formas_pagamento.objects.filter(forma_pagamento="Cartão de débito")[0]
			boleto = Formas_pagamento.objects.filter(forma_pagamento="Boleto bancário")[0]
			repasse_convenio = Formas_pagamento.objects.filter(forma_pagamento="Repasse do convênio")[0]

			# DEFINIÇÃO DA VARIÁVEL INTERMEDIÁRIA VALOR_LIQUIDO #
			# Regra de negócios geral pacientes particulares pagamentos em cartão de crédito		
			if self.atendimento.convenio == particular and self.atendimento.forma_pagamento == credito:
				valor_liquido = self.valor_real * (1-credito.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em cartão de crédito 2-6 parcelas		
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == credito_2_6:
				valor_liquido = self.valor_real * (1-credito_2_6.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em cartão de crédito 7-12 parcelas
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == credito_7_12:
				valor_liquido = self.valor_real * (1-credito_7_12.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em cartão de débito			
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == debito:
				valor_liquido = self.valor_real * (1-debito.comissao/100)
			# Regra de negócios geral pacientes particulares pagamentos em boleto bancário		
			elif self.atendimento.convenio == particular and self.atendimento.forma_pagamento == boleto:
				valor_liquido = self.valor_real - boleto.taxa_fixa
			# Regra de negócios geral pacientes particulares pagamentos em dinheiro, cheque ou transferência
			elif self.atendimento.convenio == particular:
				valor_liquido = self.valor_real
			# Regra de negócios geral pacientes de convênio
			else: valor_liquido = self.valor_real * (1-repasse_convenio.comissao/100)
		
			# REGRAS DE NEGÓCIOS DOS DENTISTAS #
			# Regra de negócios Dra. Tatiana
			if self.atendimento.dentista == tatiana and self.atendimento.convenio == particular and self.procedimento in protese:			
				valor_repasse = valor_liquido * 0.6
			# Regra de negócios Dra. Talita			
			elif self.atendimento.dentista == talita and self.atendimento.convenio == particular and self.procedimento in protese:
				valor_repasse = valor_liquido * 0.6
			# Regra de negócios Dra. Camila			
			elif self.atendimento.dentista == camila and self.procedimento in ortodontia:
				if self.procedimento in orto_manu: valor_repasse = 20 
				else: valor_repasse = 40
			# Regra de negócios Dr. Eduardo			
			elif self.atendimento.dentista == eduardo and self.procedimento in ortodontia:
				if self.procedimento in orto_manu: valor_repasse = 20 
				else: valor_repasse = 40
			# Regra de negócios Dr. Fernando		
			elif self.atendimento.dentista == fernando and self.atendimento.convenio != particular and self.procedimento in endodontia:
				valor_repasse = valor_liquido * 0.6
			# Regra de negócios geral		
			else: valor_repasse = valor_liquido * 0.5
			
			valor_repasse = round(valor_repasse * 100, 0)/100
			
		else: valor_repasse = self.valor_real
		
		return valor_repasse

""" REGRAS DE NEGÓCIO:
	- Regra geral: valor_repassado = 50% valor
	- Dra. Tatiana, Prótese: valor_repassado = 60% valor
	- Dra. Talita, Prótese: valor_repassado = 60% valor
	- Dra. Camila, Orto: valor_repassado = R$20,00 * count(valor)
	- Dr. Eduardo, Orto: valor_repassado = R$20,00 * count(valor)
	- Orto instalações/ remoções = R$40,00 * count(valor)
	- Dr. Fernando, Endo, convênio: valor_repassado = 60% valor
"""












