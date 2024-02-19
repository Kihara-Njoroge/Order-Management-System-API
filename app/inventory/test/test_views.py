from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import Category, Product
from .views import ProductCategoryViewSet, ProductViewSet
from .serializers import ProductCategoryReadSerializer, CreateProductSerializer, ProductReadSerializer


class ProductCategoryViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductCategoryViewSet.as_view({'get': 'list'})
        self.category = Category.objects.create(name="Others", is_active=True)

    def test_list_categories(self):
        request = self.factory.get('/api/v1/categories/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ProductCategoryReadSerializer(Category.objects.all(), many=True).data)

    def test_retrieve_category(self):
        request = self.factory.get('/v1/api/categories/1/')
        response = self.view(request, pk=self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ProductCategoryReadSerializer(self.category).data)

class ProductViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductViewSet.as_view({'post': 'create'})

    def test_create_product(self):
        data = {
        "category": 1,
        "name": "Test 1",
        "description": "Test Product",
        "price": 1900,
        "quantity": 10
        }
        request = self.factory.post('/api/products/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')
        
    def test_list_products(self):
        Product.objects.create(name="Another Product 1", description="description 1", category=1, price=29.99, quantity=10)
        request = self.factory.get('/api/v1/products/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Another Product 1')

    def test_retrieve_product(self):
        Product.objects.create(name="Another Product 2", description="description 2", category=1, price=29.99, quantity=10)
        request = self.factory.get('/api/v1/products/{}/'.format(product.pk))
        response = self.view(request, pk=product.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Another Product 2')

    def test_update_product(self):
        Product.objects.create(name="Another Product 3", description="description 3", category=1, price=29.99, quantity=10)
        data = {'price': 15.00}
        request = self.factory.put('/api/v1/products/{}/'.format(product.pk), data)
        response = self.view(request, pk=product.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.get().price, 15.00)

    def test_destroy_product(self):
        Product.objects.create(name="Another Product 4", description="description 4", category=1, price=29.99, quantity=10)
        request = self.factory.delete('/api/v1/products/{}/'.format(product.pk))
        response = self.view(request, pk=product.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

