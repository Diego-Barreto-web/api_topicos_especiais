from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Venda

class CustomUserAdmin(UserAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    campos = list(UserAdmin.fieldsets)
    campos.append(('Adicionais', {'fields': ('phone',)}))
    campos.append(('Permissões', {'fields': ('admin',)}))
    campos.append(('Datas', {'fields': ('created_at', 'updated_at', 'deleted_at')}))
    fieldsets = tuple(campos)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Venda)
