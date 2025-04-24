from rest_framework import serializers
from .models import Admin, Category, Supplier, Item

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'email', 'phone_number', 'position', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at']

class SupplierSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'email', 'phone', 'address', 'created_by', 'created_at', 'updated_at']

class ItemSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    stock_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'category_name', 'supplier', 'supplier_name',
                 'price', 'stock_quantity', 'threshold', 'stock_value', 'created_by', 'created_at', 'updated_at']