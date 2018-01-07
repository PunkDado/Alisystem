
"""
Importa a biblioteca csv
Abre o arquivo .csv
Lê o arquivo .csv e transfere o conteúdo para a variável tabela, como uma lista
Imprime o conteúdo da lista
Colocar os arquivos csv em uma pasta dados, na mesma localização do arquivo manage.py
"""

"""
class Convenio(models.Model):
    convenio = models.CharField(max_length=30)
"""
# Popula a tabela Convenio

import csv
from Alisystem.models import Convenio
Convenio.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Convenio.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:
	print(linha['convenio'])
	a = Convenio.objects.create(
		convenio = linha['convenio']
		)

"""
Popular a tabela Paciente; abaixo o modelo da tabela:
class Paciente(models.Model):
    nome_completo = models.CharField(max_length=100)
    nome_responsavel = models.CharField(max_length=100, blank = True, verbose_name = 'Nome do responsável')
#   convenio = models.ForeignKey(Convenio)
    data_nascimento = models.DateField(blank = True, null = True, verbose_name = 'Data de nascimento')
    email = models.EmailField(blank = True, verbose_name = 'e-mail')
"""

# Popula a tabela Paciente
		
import csv
from Alisystem.models import Paciente
Paciente.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Paciente.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:
#	print(linha['nome_completo'].upper(), linha['nome_responsavel'], linha['data_nascimento'], linha['email'])
	a = Paciente.objects.create(
		nome_completo = linha['nome_completo'].upper(),
		nome_responsavel = linha['nome_responsavel'],
#		data_nascimento = linha['data_nascimento'],
		email = linha['email'],	
		)

"""
class Dentista(models.Model):
    nome_completo = models.CharField(max_length=100)
    num_CRO = models.CharField(max_length=100, blank = True, verbose_name = 'Número do CRO')
    email = models.EmailField(blank = True, verbose_name = 'E-mail')
    cpf = models.CharField(max_length=11, blank = True)
    banco = models.CharField(max_length=30, blank = True)
    num_agencia = models.CharField(max_length=4, blank = True, verbose_name = 'Agência número')
    num_conta = models.CharField(max_length=20, blank = True, verbose_name = 'Conta número')
"""

# Popula a tabela Dentista

import csv
from Alisystem.models import Dentista
Dentista.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Dentista.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:
	print(linha['nome_completo'])
	a = Dentista.objects.create(
		nome_completo = linha['nome_completo']	
		)

"""
class Procedimento(models.Model):
    procedimento = models.CharField(max_length=100)
    tipo_procedimento = models.ForeignKey(Tipos_procedimento, verbose_name = 'Tipo do procedimento')
    tabela_preco = models.FloatField(blank=True, null=True, verbose_name = 'Tabela de preço')
"""

# Popula a tabela Tipos_procedimento

import csv
from Alisystem.models import Tipos_procedimento
Tipos_procedimento.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Tipos_procedimento.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:
	print(linha['tipo_procedimento'])
	a = Tipos_procedimento.objects.create(
		
		tipo_procedimento = linha['tipo_procedimento']
	
		)

# Popula a tabela Procedimento

# Bom exemplo de como designar valores de Foreign Key para uma tabela => Designa-se um objeto, e não uma string ou int
import csv
from Alisystem.models import Procedimento, Tipos_procedimento
Procedimento.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Procedimento.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:
#	print(linha['procedimento'], linha['tipo_procedimento'], linha['tabela_preço'])
# Este código funcionou

	if linha['tipo_procedimento']!='':
		a = Procedimento.objects.create(
			procedimento = linha['procedimento'],
			tipo_procedimento = Tipos_procedimento.objects.get(tipo_procedimento=linha['tipo_procedimento']),
			tabela_preço = float(linha['tabela_preço']),	
			)
	else:
		a = Procedimento.objects.create(
			procedimento = linha['procedimento'],
			tabela_preço = float(linha['tabela_preço']),	
			)
			
# Popula a tabela Formas_pagamento

import csv
from Alisystem.models import Formas_pagamento
Formas_pagamento.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Formas_pagamento_novo.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:
	print(linha['forma_pagamento'])
	a = Formas_pagamento.objects.create(
		forma_pagamento = linha['forma_pagamento']
#		comissao = linha['comissao']
#		taxa_fixa = linha['taxa_fixa']
		)

"""
class Atendimento(models.Model):
	dentista = models.ForeignKey(Dentista)
	paciente = models.ForeignKey(Paciente)
	convenio = models.ForeignKey(Convenio, null=True)
	forma_pagamento = models.ForeignKey(Formas_pagamento, blank=True, null=True, verbose_name = 'Forma de pagamento')
	num_GTO = models.CharField(max_length = 30, null=True, blank = True, verbose_name = 'Número da GTO')
	procedimento = models.ForeignKey(Procedimento, blank=True, null=True, help_text='Escolha o seu procedimento nesta lista, ou insira um novo procedimento clicando no sinal de +') # Procedimentos padronizados a partir da tabela de preços
	descr_anterior = models.CharField(max_length = 200, blank=True, verbose_name="Descrição anterior", help_text = 'Descrição anterior do procedimento')
	data_atendimento = models.DateField(blank=True, null=True, verbose_name = 'Data do atendimento')
	valor_real = models.FloatField(blank=True, null=True, verbose_name = 'Valor real (não registrar novos valores)')
	valor_recebido = models.FloatField(blank=True, null=True, verbose_name = 'Valor recebido (novos valores aqui)')
	desconto = models.FloatField(blank=True, null = True)
	data_envio = models.DateField(blank=True, null=True, verbose_name = 'Data de envio')
	mes_recebimento = models.DateField(blank=True, null=True, verbose_name = 'Mês de recebimento')
	recebido = models.BooleanField(blank=True, default=False)
	glosado = models.BooleanField(blank=True, default=False)
	motivo_glosa = models.CharField(max_length = 200, blank=True, verbose_name = 'Motivo da glosa')
	data_repasse = models.DateField(blank=True, null=True, verbose_name = 'Data de repasse')
	repassado = models.BooleanField(blank=True, default=False)
	comentarios = models.CharField(max_length = 200, blank=True, verbose_name = 'Comentários')
	encaminhamento = models.ForeignKey(Encaminhamento, blank=True, null=True, help_text="Registre novos encaminhamentos aqui")
	encaminhado_por = models.CharField(max_length = 30, blank=True, verbose_name = 'Encaminhado por', help_text='Não registrar novos valores')
"""
# Código para popular a tabela Atendimento, somente com os registros ainda não recebidos (Recebido = False)

import csv
from datetime import datetime
from Alisystem.models import Atendimento, Convenio, Dentista, Paciente, Formas_pagamento
Atendimento.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Atendimento.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:

#	if linha['recebido'] == 'False':

#		print(linha['dentista'], linha['paciente'])
		
	a = Atendimento.objects.create(
		dentista = Dentista.objects.get(nome_completo=linha['dentista']),
		paciente = Paciente.objects.get(nome_completo=linha['paciente'].upper()),
		num_GTO = linha['num_GTO'],
		descr_anterior = linha['descr_anterior'],
		recebido = linha['recebido'],				
		glosado = linha['glosado'],
		repassado = linha['repassado'],
		comentarios = linha['comentarios'],
		encaminhado_por = linha['encaminhado_por']
		)
	
	if linha['convenio']!='':
		convenio = Convenio.objects.get(convenio=linha['convenio'])
		b = Atendimento.objects.filter(id=a.id).update(convenio=convenio)
		
	if linha['forma_pagamento']!='': 
		forma_pagamento = Formas_pagamento.objects.get(forma_pagamento=linha['forma_pagamento'])
		b = Atendimento.objects.filter(id=a.id).update(forma_pagamento=forma_pagamento)
		
	if linha['valor_real']!='':
		valor_real = float(linha['valor_real'].replace(",","."))
		b = Atendimento.objects.filter(id=a.id).update(valor_real=valor_real)
	
	data = linha['data_atendimento']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(data_atendimento=data)
	
	data = linha['data_envio']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(data_envio=data)
		
	data = linha['mes_recebimento']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(mes_recebimento=data)
	
	data = linha['data_repasse']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(data_repasse=data)
	

# Código para popular a tabela Atendimento

import csv
from datetime import datetime
from Alisystem.models import Atendimento, Convenio, Dentista, Paciente, Formas_pagamento
Atendimento.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Atendimento.csv", newline="")
tabela = csv.DictReader(csvfile)
for linha in tabela:

	print(linha['dentista'], linha['paciente'])
	
	a = Atendimento.objects.create(
		dentista = Dentista.objects.get(nome_completo=linha['dentista']),
		paciente = Paciente.objects.get(nome_completo=linha['paciente'].upper()),
		num_GTO = linha['num_GTO'],
		descr_anterior = linha['descr_anterior'],
		recebido = linha['recebido'],				
		glosado = linha['glosado'],
		repassado = linha['repassado'],
		comentarios = linha['comentarios'],
		encaminhado_por = linha['encaminhado_por']
		)
	
	if linha['convenio']!='':
		convenio = Convenio.objects.get(convenio=linha['convenio'])
		b = Atendimento.objects.filter(id=a.id).update(convenio=convenio)
		
	if linha['forma_pagamento']!='': 
		forma_pagamento = Formas_pagamento.objects.get(forma_pagamento=linha['forma_pagamento'])
		b = Atendimento.objects.filter(id=a.id).update(forma_pagamento=forma_pagamento)
		
	if linha['valor_real']!='':
		valor_real = float(linha['valor_real'].replace(",","."))
		b = Atendimento.objects.filter(id=a.id).update(valor_real=valor_real)
	
	data = linha['data_atendimento']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(data_atendimento=data)
	
	data = linha['data_envio']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(data_envio=data)
		
	data = linha['mes_recebimento']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(mes_recebimento=data)
	
	data = linha['data_repasse']
	if data != '':
		data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
		b = Atendimento.objects.filter(id=a.id).update(data_repasse=data)
		
# Fim do código



#Tabela preco: não vamos popular agora
#Encaminhamento: idem

# Popula a tabela Convenio. Primeira versão, mais prolixa

import csv
from Alisystem.models import Convenio
Convenio.objects.all().delete() # tire esta linha se estiver inserindo novos registros
csvfile = open("dados/Convenio.csv", newline="")
tabela = csv.reader(csvfile, delimiter = " ", quotechar="|")
lista = []
i=0
for linha in tabela:
	print(" ".join(linha))
	lista.append(" ".join(linha))
	if i == 0: i=i+1
	else:
		a = Convenio.objects.create(convenio = lista[i])
		lista[i]
		i=i+1

# Gerando Dentistas.csv
"""
class Dentista(models.Model):
    nome_completo = models.CharField(max_length=100)
    num_CRO = models.CharField(max_length=100, blank = True, verbose_name = 'Número do CRO')
    email = models.EmailField(blank = True, verbose_name = 'E-mail')
    cpf = models.CharField(max_length=11, blank = True)
    banco = models.CharField(max_length=30, blank = True)
    num_agencia = models.CharField(max_length=4, blank = True, verbose_name = 'Agência número')
    num_conta = models.CharField(max_length=20, blank = True, verbose_name = 'Conta número')


import csv
from Alisystem.models import Dentista
csvfile = open('dados/Dentista.csv', 'w')
fieldnames = ['nome_completo', 'num_CRO', 'email', 'cpf', 'banco', 'num_agencia', 'num_conta']
writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
writer.writeheader()
for i in Dentista.objects.all():
	writer.writerow(i)
"""

# Não funcionou; gerei a lista manualmente













