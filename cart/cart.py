from myapp.models import Product
from decimal import Decimal

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = request.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart
        
    def __len__(self):
        return sum(int(item['qty']) for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * Decimal(item['qty']) for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            if 'product' in item:
                item['price'] = Decimal(item['price'])
                item['qty'] = Decimal(item['qty'])
                item['total'] = item['price'] * item['qty']
                yield item

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = int(product_qty)
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': int(product_qty)}
            
        self.session.modified = True            

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = int(qty)
        self.session.modified = True

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
            self.session.modified = True
