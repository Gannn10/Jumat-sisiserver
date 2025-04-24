from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Admin, Category, Supplier, Item

# Register Admin user with custom fields
class CustomAdminAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'position', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'position')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'position')}),
    )

# Register Category with custom display
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_by', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

# Register Supplier with custom display
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_by', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    list_filter = ['created_at']

# Register Item with custom display
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'supplier', 'price', 'stock_quantity', 'created_by', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['category', 'supplier', 'created_at']

admin.site.register(Admin, CustomAdminAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Item, ItemAdmin)