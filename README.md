# Библиотека для работы с корзиной покупателя в rest_framework проектах
Для работы библиотека использует сессии, подробнее о сессиях можно прочитать <https://docs.djangoproject.com/en/5.0/topics/http/sessions/>

## Установка и использование
Установим пакет
`pip install rest-framework-cart.tag.gz` (скоро будет доступен)

или скопируйте репозиторий `git clone https://github.com/alxkahovsky/rest_framework_cart.git`

В файле `settings.py`:

```
# Зарегистрируйте библиотеку:
INSTALLED_APPS = [
    ...
    'rest_framework_cart',
    ...
]

# Убедитесь что используетe SessionMiddleware:
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]

# Обявите переменную CART_SESSION_ID:
CART_SESSION_ID = 'cart'
```
Работа с корзиной подразумевает, что у Вас в проекте уже существует сущность для товара, пожалуйста, убедитесь, что модель товара имеет необходимые поля для работы с корзиной (title, price), Вы можете объявить их самостоятельно в модели Вашего товара или используйте абстрактную модель `AbstractProduct`. Подробнее про абстактную модель можно прочитать тут <https://docs.djangoproject.com/en/5.0/topics/db/models/>
```
# Для работы с абстрактной моделью товара достаточно просто импортировать и использовать ее
from rest_framework_cart.models import AbstractProduct


class Product(AbstractProduct):
    description = models.TextField(max_length=20000, default=None, verbose_name='Description')
    
```
Теперь, когда у нас в проекте есть модель для товара,можно приступить к работе с корзиной:

1. Создаем приложение `cart` коммандой `python  manage.py startapp cart`,
далее в файле `cart\views`:

```
from rest_framework_cart.cart import Cart
from rest_framework_cart.serializers import CartItemSerializer
from rest_framework_cart.viewsets import CartViewSet
from products.models import Product  # Необходимо использовать ранее созданную модель товара


class CartView(CartViewSet):
    serializer_class = CartItemSerializer
    cart_manager = Cart
    product_model = Product
    product_lookup_field = 'id'
    queryset = Product.objects.all()
```

2. Далее добавим код в файл `cart/urls`:

```from rest_framework.routers import DefaultRouter
from .views import CartView

app_name = 'cart'

router = DefaultRouter()
router.register(r'', CartView, basename='cart')

urlpatterns = router.urls
```
Как вы уже заметили в представлениях мы используем ViewSet, что очень удобно и позволяет писать код в стиле rest_framework, библиотека уже содержит базовые методы и эндпоинты для работы с корзиной, но вы всегда можете кастомизировать корзину создав подклассы от классов `AbstractProduct`, `Cart`, `CartItemSerializer` иобъявив свои @action в классе `CartView`

