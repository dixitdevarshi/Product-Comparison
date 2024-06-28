from django.contrib import admin
from .models import *

# Register your models here.

class PhoneNameAdmin(admin.ModelAdmin):
  list_display = ('phone_name',)
  
class ProductAdmin(admin.ModelAdmin):
  list_display = ('id','phone_name', 'display_type','os','cpu',)
  search_fields = ('display_type','os',)
  list_filter = ('wlan','price','gpu',)
  
admin.site.register(PhoneName, PhoneNameAdmin)
  
admin.site.register(Product, ProductAdmin)