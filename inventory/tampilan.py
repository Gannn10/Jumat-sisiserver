from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Avg, Count, F, ExpressionWrapper, DecimalField
from .models import Admin, Category, Supplier, Item
from .serializers import AdminSerializer, CategorySerializer, SupplierSerializer, ItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary information for each category
        """
        categories = Category.objects.annotate(
            item_count=Count('items'),
            total_stock_value=Sum(F('items__price') * F('items__stock_quantity'), output_field=DecimalField()),
            avg_price=Avg('items__price')
        )
        
        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'name': category.name,
                'item_count': category.item_count,
                'total_stock_value': category.total_stock_value or 0,
                'avg_price': category.avg_price or 0,
            })
        
        return Response(data)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary information for each supplier
        """
        suppliers = Supplier.objects.annotate(
            item_count=Count('supplied_items'),
            total_stock_value=Sum(F('supplied_items__price') * F('supplied_items__stock_quantity'), output_field=DecimalField()),
        )
        
        data = []
        for supplier in suppliers:
            data.append({
                'id': supplier.id,
                'name': supplier.name,
                'item_count': supplier.item_count,
                'total_stock_value': supplier.total_stock_value or 0,
            })
        
        return Response(data)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def below_threshold(self, request):
        """
        Get items below their threshold
        """
        items = Item.objects.filter(stock_quantity__lt=F('threshold'))
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get items filtered by a specific category
        """
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({"error": "category_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        items = Item.objects.filter(category_id=category_id)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stock_summary(self, request):
        """
        Get summary of all items in stock
        """
        total_items = Item.objects.count()
        total_stock = Item.objects.aggregate(Sum('stock_quantity'))['stock_quantity__sum'] or 0
        total_value = Item.objects.annotate(
            value=ExpressionWrapper(F('price') * F('stock_quantity'), output_field=DecimalField())
        ).aggregate(Sum('value'))['value__sum'] or 0
        avg_price = Item.objects.aggregate(Avg('price'))['price__avg'] or 0
        
        return Response({
            'total_items': total_items,
            'total_stock': total_stock,
            'total_value': total_value,
            'avg_price': avg_price
        })

class SystemSummaryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """
        Get overall system summary
        """
        total_items = Item.objects.count()
        total_categories = Category.objects.count()
        total_suppliers = Supplier.objects.count()
        
        total_stock = Item.objects.aggregate(Sum('stock_quantity'))['stock_quantity__sum'] or 0
        total_stock_value = Item.objects.annotate(
            value=ExpressionWrapper(F('price') * F('stock_quantity'), output_field=DecimalField())
        ).aggregate(Sum('value'))['value__sum'] or 0
        
        return Response({
            'total_items': total_items,
            'total_categories': total_categories,
            'total_suppliers': total_suppliers,
            'total_stock': total_stock,
            'total_stock_value': total_stock_value,
        })