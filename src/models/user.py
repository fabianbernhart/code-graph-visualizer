class User:
    def __init__(self, name):
        self.name = name

    def purchase_product(self, product):
        print(f"{self.name} purchased {product.name}")
