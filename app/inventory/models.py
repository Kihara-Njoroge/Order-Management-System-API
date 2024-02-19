from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from enum import Enum


class CategoryChoices(Enum):
    OTHERS = "Others"
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    BOOKS = "Books"


class Category(models.Model):
    name = models.CharField(
        max_length=100, choices=[(tag.value, tag.name) for tag in CategoryChoices]
    )
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(
        default=False,
    )
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


def get_default_category():
    return Category.objects.get_or_create(name=CategoryChoices.ELECTRONICS.value)[0]



class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_default_category),
        related_name='product_list',
        null=True,
        blank=True,
    )    
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
