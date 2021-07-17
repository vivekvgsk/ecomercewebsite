from django.db import models


# Create your models here.
class Item(models.Model):
    product_category = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.product_category


class Product(models.Model):
    product_name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    specs = models.CharField(max_length=250)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(max_length=120)
    options = (("Ordernotplaced", "Ordernotplaced"), ("oredrplaced", "oredrplaced"))
    status = models.CharField(max_length=50, choices=options, default="Ordernotplaced")


class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(max_length=120)
    address = models.CharField(max_length=250)
    options = (
        ("ordered", "ordered"),
        ("packed", "packed"),
        ("shipped", "shipped"),
        ("deliverd", "deliverd"),
        ("cancelled", "cancelled")
    )
    status = models.CharField(max_length=120, choices=options, default="ordered")
    date = models.DateField(auto_now=True)


