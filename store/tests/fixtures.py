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

        # Images
        ProductImage.objects.create(product_id=self.product1.id, is_feature=True, image='media/images.png')
        ProductImage.objects.create(product_id=self.product1.id, is_feature=False, image='media/images.png')
        ProductImage.objects.create(product_id=self.product1.id, is_feature=False, image='media/images.png')

        ProductImage.objects.create(product_id=self.product3.id, is_feature=True, image='media/images.png')
