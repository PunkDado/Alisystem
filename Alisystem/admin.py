# ALISYSTEM_GTO 1.0 LOCAL VERSION

from django.contrib import admin

# Register your models here.

from .models import Convenio, Paciente, Formas_pagamento, Dentista, Tipos_procedimento
from .models import Procedimento, Tabela_preco, Encaminhamento, Procedimentos_aplicado, Atendimento

class EncaminhamentosAdmin(admin.ModelAdmin):
	list_display = ('data_encaminhamento', 'descricao', 'paciente', 'dentista')

class Procedimentos_aplicadoInline(admin.StackedInline):
	model = Procedimentos_aplicado
		

class AtendimentosAdmin(admin.ModelAdmin):
	list_display = ('data_atendimento', 'num_GTO', 'paciente', 'dentista', 'convenio', 'verificado')#, 'forma_pagamento', 'recebido', 'repassado', 'valor_real','valor_liquido', 'valor_repasse')
	fields = ['data_atendimento', 'num_GTO', 'paciente', 'dentista', 'convenio', ('forma_pagamento', 'data_envio'), 'encaminhado_por', 'verificado']
	search_fields = (['num_GTO'])
	list_filter = ('verificado', 'dentista', 'convenio', 'data_atendimento')#, 'recebido', 'repassado')
	date_hierarchy = 'data_atendimento'
	raw_id_fields = ('paciente',)#,'procedimentos_aplicados')
	ordering = ('-data_atendimento',)
	inlines = [Procedimentos_aplicadoInline]
#	filter_horizontal = ('procedimentos_aplicados',) # Para relacionamentos muitos para muitos
#	fields = ('valor_recebido', 'data_atendimento') #Especifica campos que podem ser alterados/ os demais não podem, nem serão mostrados

class Formas_pagamentoAdmin(admin.ModelAdmin):
	list_display = ('forma_pagamento', 'comissao', 'taxa_fixa')
	ordering = ('id',)

class Tabela_precosAdmin(admin.ModelAdmin):
	list_display = ('procedimento', 'convenio', 'preco')
	ordering = ('procedimento', 'convenio')
	
class ProcedimentosAdmin(admin.ModelAdmin):
	list_display = ('procedimento', 'tipo_procedimento', 'tabela_preço')
	
class PacientesAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome_completo')
	search_fields = (['nome_completo'])
	
class Procedimentos_aplicadoAdmin(admin.ModelAdmin):
	list_display = ('id', 'procedimento', 'valor_real')
	fields = [('procedimento', 'dente'), 'descr_anterior', 'valor_real', ('valor_liquido_recebido', 'valor_repassado'), 'recebido', ('glosado', 'motivo_glosa'), ('data_recebimento','data_repasse'), 'repassado']
	list_filter = ('recebido', 'repassado')
	date_hierarchy = 'data_recebimento'

	

admin.site.register(Convenio)
admin.site.register(Paciente, PacientesAdmin)
admin.site.register(Formas_pagamento, Formas_pagamentoAdmin)
admin.site.register(Dentista)
admin.site.register(Tipos_procedimento)
admin.site.register(Procedimento, ProcedimentosAdmin)
admin.site.register(Tabela_preco, Tabela_precosAdmin)
admin.site.register(Encaminhamento, EncaminhamentosAdmin)
admin.site.register(Procedimentos_aplicado, Procedimentos_aplicadoAdmin)
admin.site.register(Atendimento, AtendimentosAdmin)


