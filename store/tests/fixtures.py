from account.models import Customer
from reviews.models import ProductReview
from store.models import Product, Brand, Category, Vendor, ProductImage


class FixtureTestData:

    def setUp(self) -> None:
        self.vendor = Vendor.objects.create(vendor_name='vendor', description='description')

        # Category
        self.category = Category.objects.create(category_name='category', description='description', slug='category',
                                                is_parent_category=True)

        self.category2 = Category.objects.create(category_name='category2', description='description', slug='category2',
                                                 is_parent_category=True)

        # Subcategory
        self.subcategory = Category.objects.create(category_name='subcategory', description='description',
                                                   parent_id=self.category.id, slug='subcategory')

        self.subcategory2 = Category.objects.create(category_name='subcategory2', description='description',
                                                    parent_id=self.category.id, slug='subcategory2')

        self.subcategory3 = Category.objects.create(category_name='subcategory3', description='description',
                                                    parent_id=self.category2.id, slug='subcategory3')

        # Brand
        self.brand = Brand.objects.create(brand_name='brand')

        # Products
        self.product1 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, vendor_id=self.vendor.id, category_id=self.subcategory.id,
                                               brand_id=self.brand.id,
                                               )

        self.product2 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, discount_percent=50, vendor_id=self.vendor.id,
                                               category_id=self.subcategory.id, brand_id=self.brand.id,
                                               )

        self.product3 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, discount_percent=5, vendor_id=self.vendor.id,
                                               category_id=self.subcategory.id, brand_id=self.brand.id,
                                               )

        self.product4 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=5000, discount_percent=5, vendor_id=self.vendor.id,
                                               category_id=self.subcategory.id, brand_id=self.brand.id,
                                               )

        self.product5 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=10000, discount_percent=5, vendor_id=self.vendor.id,
                                               category_id=self.subcategory.id, brand_id=self.brand.id,
                                               )


        # Images
        ProductImage.objects.create(product_id=self.product1.id, is_feature=True, image='media/images.png')
        ProductImage.objects.create(product_id=self.product1.id, is_feature=False, image='media/images.png')
        ProductImage.objects.create(product_id=self.product1.id, is_feature=False, image='media/images.png')

        ProductImage.objects.create(product_id=self.product3.id, is_feature=True, image='media/images.png')

        # Users
        self.user1 = Customer.objects.create(user_name='testuser1', email='testuser1@gmail.com', password='somepswrd1',
                                             mobile='88005553535')

        self.user2 = Customer.objects.create(user_name='testuser2', email='testuser2@gmail.com',
                                             password='somepswrd1', mobile='88005553536')

        self.user3 = Customer.objects.create(user_name='testuser3', email='testuser3@gmail.com', password='somepswrd1',
                                             mobile='88005553537')

        # Reviews
        self.product_review1 = ProductReview.objects.create(user=self.user1, product=self.product1, rating=5,
                                                            usage_period='LESS THAN MONTH', advantages='price',
                                                            disadvantages='None', comment='Best product')

        self.product_review2 = ProductReview.objects.create(user=self.user1, product=self.product2, rating=2,
                                                            usage_period='LESS THAN MONTH', advantages='None',
                                                            disadvantages='The product is disadvantage',
                                                            comment='The worst product ever bought')

        self.product_review3 = ProductReview.objects.create(user=self.user2, product=self.product1, rating=1,
                                                            usage_period='LESS THAN MONTH', advantages='None',
                                                            disadvantages='The product is disadvantage',
                                                            comment='The worst product ever bought')

        self.product_review4 = ProductReview.objects.create(user=self.user3, product=self.product2, rating=4,
                                                            usage_period='LESS THAN MONTH', advantages='price',
                                                            disadvantages='None', comment='Almost the best product')



