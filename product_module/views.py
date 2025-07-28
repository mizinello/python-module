from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product
from rest_framework.response import Response
from rest_framework import serializers
from .permissions import IsManager, IsUser, IsPublic, CanViewProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsManager()]
        elif self.request.method == 'PUT':
            return [IsManager()]
        elif self.request.method == 'POST':
            return [IsManager(), IsUser()]
        elif self.request.method == 'GET':
            return [CanViewProduct()]  # ✅ Pakai gabungan
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        confirm = request.query_params.get("confirm")
        if confirm != "true":
            return Response({"confirm": "Are you sure to delete this data?"})
        return super().destroy(request, *args, **kwargs)

@login_required
def landing_page(request):
    role = None
    if request.user.groups.filter(name='manager').exists():
        role = 'manager'
    elif request.user.groups.filter(name='user').exists():
        role = 'user'
    elif request.user.groups.filter(name='public').exists():
        role = 'public'

    # DELETE (hanya manager)
    if request.GET.get('delete') and role == 'manager':
        Product.objects.filter(id=request.GET['delete']).delete()
        return redirect('product-landing')

    # CREATE or UPDATE
    if request.method == 'POST':
        if role in ['manager', 'user']:
            product_id = request.POST.get('product_id')
            if product_id:  # UPDATE
                product = Product.objects.get(id=product_id)
                product.name = request.POST.get('name')
                product.barcode = request.POST.get('barcode')
                product.price = request.POST.get('price')
                product.stock = request.POST.get('stock')
                product.description = request.POST.get('description')
                product.save()
            else:  # CREATE
                Product.objects.create(
                    name=request.POST.get('name'),
                    barcode=request.POST.get('barcode'),
                    price=request.POST.get('price'),
                    stock=request.POST.get('stock'),
                    description=request.POST.get('description')
                )
        return redirect('product-landing')

    # Untuk pre-populate form edit
    edit_product = None
    if role in ['manager', 'user'] and request.GET.get('edit'):
        edit_product = Product.objects.get(id=request.GET['edit'])

    products = Product.objects.all()

    return render(request, 'product_module/landing.html', {
        'products': products,
        'role': role,
        'edit_product': edit_product
    })

