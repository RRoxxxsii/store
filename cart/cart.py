from _decimal import Decimal

from store.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product: Product, qty: int) -> None:
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'regular_price': str(product.price), 'price_with_discount': str(product.get_price_with_discount()), 'qty': qty}
        self.save()

    def __iter__(self) -> Product:
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['total_regular_price'] = item['regular_price'] * item['qty']

            item['total_price_with_discount'] = item['price_with_discount'] * item['qty']
            yield item

    def __len__(self) -> int:
        return sum(item['qty'] for item in self.basket.values())

    def get_sub_total_price(self) -> dict:
        sub_total_regular_price = sum(Decimal(item['regular_price']) * item['qty'] for item in self.basket.values())
        sub_total_price_with_discount = sum(Decimal(item['price_with_discount']) * item['qty']
                                            for item in self.basket.values())

        return {'sub_total_regular_price': sub_total_regular_price,
                'sub_total_price_with_discount': sub_total_price_with_discount}

    def delete(self, product: Product) -> None:
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product: Product, qty) -> None:
        """
        Update item in session data
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self) -> dict:
        subtotal_regular = sum(Decimal(item['regular_price']) * item['qty'] for item in self.basket.values())
        subtotal_discount = sum(Decimal(item['price_with_discount']) * item['qty'] for item in self.basket.values())

        if subtotal_regular == 0:
            shipping = 0
        else:
            shipping = 200

        total_discount = subtotal_discount + shipping
        total_regular = subtotal_regular + shipping
        return {'total_regular_price': total_regular, 'total_price_with_discount': total_discount}



