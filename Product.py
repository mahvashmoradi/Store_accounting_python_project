class Product:
    """
    product class
    """
    def __init__(self, id, name, price, brand, quantity):
        """
        :param id: barcode of product
        :param name: name of product
        :param price: price of product
        :param brand: brand of product
        :param quantity: quantity of product
        """
        self.id = id
        self.name = name
        self.price = price
        self.brand = brand
        self.quantity = quantity


    def __str__(self):
        """
        print the name, price and brand of product
        """
        return self.name, self.price, self.brand

