from django.db import models

# Create your models here.
# -- CreateTable
# CREATE TABLE "Products" (
#     "id" SERIAL NOT NULL,
#     "title" TEXT NOT NULL,
#     "description" TEXT NOT NULL,
#     "url" TEXT NOT NULL,
#     "price" INTEGER NOT NULL,
#     "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

#     CONSTRAINT "Products_pkey" PRIMARY KEY ("id")
# );

class Products(models.Model):
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=1000)
    # url = models.TextField()
    image = models.ImageField(upload_to='products/Images/')
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title