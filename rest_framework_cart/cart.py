from django.conf import settings


class CartBase:
    def __init__(self, request):
        self.session = request.session
        storage = self.session.get(settings.CART_SESSION_ID)
        if not storage:
            storage = self.session[settings.CART_SESSION_ID] = {}
        self.storage = storage

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        # Обновление сессии rest_framework_cart
        self.session[settings.CART_SESSION_ID] = self.storage
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True


class Cart(CartBase):
    def __init__(self, request, product_model, key_field='id'):
        self.session = request.session
        storage = self.session.get(settings.CART_SESSION_ID)
        if not storage:
            storage = self.session[settings.CART_SESSION_ID] = {}
        self.storage = storage
        self.product_model = product_model
        self.key_field = key_field
        super(Cart, self).__init__(request=request)

    def change(self, product, quantity, update=False):
        product_id = str(product.__getattribute__(self.key_field))
        if product_id not in self.storage:
            self.storage[product_id] = {'product': product.id,
                                        'quantity': 0,
                                        'price':  float(product.price),
                                        }
        if update:
            if quantity <= 0:
                self.remove(product_id)
            else:
                self.storage[product_id]['quantity'] = quantity
                self.storage[product_id]['subtotal'] = self.storage[product_id]['quantity'] * \
                                                       self.storage[product_id]['price']
        else:
            self.storage[product_id]['quantity'] += quantity
            if self.storage[product_id]['quantity'] <= 0:
                self.remove(product_id)
            else:
                self.storage[product_id]['subtotal'] = self.storage[product_id]['quantity'] * \
                                                       self.storage[product_id]['price']
        self.save()

    def remove(self, product_id):
        """
        Удаление товара из корзины.
        """
        if product_id in self.storage:
            del self.storage[product_id]
            self.save()

    @property
    def representation(self):
        response = {'items': [{"product": key,  "price": value['price'], "quantity": value['quantity'],
                               "subtotal": value['subtotal'], "title": value['title'],
                               "image": value['image'],
                               "unit": value["unit"],
                               "unit_step": value['unit_step']} for key, value in self.storage.items()]}
        return response

    @property
    def queryset(self):
        kw = {f'{self.key_field}__in': self.storage.keys()}
        result = self.product_model.objects.filter(**kw)
        return result

    @property
    def total(self):
        result = sum([value['price'] * value['quantity'] for value in self.storage.values()])
        return result

    @property
    def items(self):
        return [p for p in self.storage.values()]

    @property
    def size(self):
        return len(self.storage.keys())

    @property
    def is_empty(self):
        return self.size == 0

    def get_or_create(self, product):
        product_id = str(product.__getattribute__(self.key_field))
        if product_id not in self.storage:
            self.storage[product_id] = {'product': product.id,
                                        'quantity': 0,
                                        'price':  float(product.price),
                                        }
        return self.storage[product_id]
