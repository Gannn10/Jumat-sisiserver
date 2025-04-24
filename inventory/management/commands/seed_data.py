from django.core.management.base import BaseCommand
from inventory.models import Admin, Category, Supplier, Item
from django.db import transaction

class Command(BaseCommand):
    help = 'Seed database with initial data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Create admin user if not exists
        if not Admin.objects.filter(username='admin').exists():
            admin = Admin.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                phone_number='123456789',
                position='Administrator'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            admin = Admin.objects.get(username='admin')
            self.stdout.write('Admin user already exists')
        
        # Create categories
        categories = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and accessories'
            },
            {
                'name': 'Food',
                'description': 'Food and beverage items'
            },
            {
                'name': 'Clothing',
                'description': 'Clothing and fashion items'
            },
            {
                'name': 'Office Supplies',
                'description': 'Office supplies and stationery'
            }
        ]
        
        created_categories = []
        for cat_data in categories:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'created_by': admin
                }
            )
            created_categories.append(cat)
            if created:
                self.stdout.write(f'Category "{cat.name}" created')
            else:
                self.stdout.write(f'Category "{cat.name}" already exists')
        
        # Create suppliers
        suppliers = [
            {
                'name': 'ElectroTech Inc.',
                'contact_person': 'John Doe',
                'email': 'john@electrotech.com',
                'phone': '123-456-7890',
                'address': '123 Tech St, San Francisco, CA'
            },
            {
                'name': 'Fresh Foods Ltd.',
                'contact_person': 'Jane Smith',
                'email': 'jane@freshfoods.com',
                'phone': '098-765-4321',
                'address': '456 Food Ave, Chicago, IL'
            },
            {
                'name': 'Fashion Forward Co.',
                'contact_person': 'Sam Wilson',
                'email': 'sam@fashionforward.com',
                'phone': '555-123-4567',
                'address': '789 Fashion Blvd, New York, NY'
            }
        ]
        
        created_suppliers = []
        for sup_data in suppliers:
            sup, created = Supplier.objects.get_or_create(
                name=sup_data['name'],
                defaults={
                    'contact_person': sup_data['contact_person'],
                    'email': sup_data['email'],
                    'phone': sup_data['phone'],
                    'address': sup_data['address'],
                    'created_by': admin
                }
            )
            created_suppliers.append(sup)
            if created:
                self.stdout.write(f'Supplier "{sup.name}" created')
            else:
                self.stdout.write(f'Supplier "{sup.name}" already exists')
        
        # Create items
        items = [
            {
                'name': 'Laptop',
                'description': 'High performance laptop',
                'category': created_categories[0],  # Electronics
                'supplier': created_suppliers[0],  # ElectroTech
                'price': 999.99,
                'stock_quantity': 10
            },
            {
                'name': 'Smartphone',
                'description': 'Latest smartphone model',
                'category': created_categories[0],  # Electronics
                'supplier': created_suppliers[0],  # ElectroTech
                'price': 599.99,
                'stock_quantity': 15
            },
            {
                'name': 'Chocolate Bar',
                'description': 'Delicious chocolate bar',
                'category': created_categories[1],  # Food
                'supplier': created_suppliers[1],  # Fresh Foods
                'price': 2.99,
                'stock_quantity': 100
            },
            {
                'name': 'T-Shirt',
                'description': 'Cotton t-shirt',
                'category': created_categories[2],  # Clothing
                'supplier': created_suppliers[2],  # Fashion Forward
                'price': 19.99,
                'stock_quantity': 50
            },
            {
                'name': 'Notebook',
                'description': 'Spiral notebook',
                'category': created_categories[3],  # Office Supplies
                'supplier': created_suppliers[0],  # ElectroTech
                'price': 3.99,
                'stock_quantity': 200
            },
            {
                'name': 'Headphones',
                'description': 'Wireless headphones',
                'category': created_categories[0],  # Electronics
                'supplier': created_suppliers[0],  # ElectroTech
                'price': 89.99,
                'stock_quantity': 5
            },
        ]
        
        for item_data in items:
            item, created = Item.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'description': item_data['description'],
                    'category': item_data['category'],
                    'supplier': item_data['supplier'],
                    'price': item_data['price'],
                    'stock_quantity': item_data['stock_quantity'],
                    'created_by': admin
                }
            )
            if created:
                self.stdout.write(f'Item "{item.name}" created')
            else:
                self.stdout.write(f'Item "{item.name}" already exists')
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully'))