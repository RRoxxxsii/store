from account.models import Customer
from store.models import Brand, Category, Vendor


class FixtureUsers:

    def setUp(self) -> None:

        self.user1 = Customer.objects.create(user_name='testuser1', email='testuser1@gmail.com', password='somepswrd1',
                                             mobile='88005553535')

        self.user2 = Customer.objects.create(user_name='testuser2', email='testuser2@gmail.com',
                                             password='somepswrd1', mobile='88005553536', on_mail_listing=True)

        self.user3 = Customer.objects.create(user_name='testuser3', email='testuser3@gmail.com',
                                             password='somepswrd1', mobile='88005553537', on_mail_listing=True)

        self.vendor = Vendor.objects.create(vendor_name='vendor', description='description')

        self.category = Category.objects.create(category_name='category', description='description', slug='category',
                                                is_parent_category=True)

        self.brand = Brand.objects.create(brand_name='brand')


