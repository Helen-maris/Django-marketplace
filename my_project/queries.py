from django.contrib.auth.models import User
from main.models import Seller, Category, Tag, Ad

# 1.1 Sellers
user1 = User.objects.create_superuser('user13', 'user12_mail@mail.com', 'userpassword')
user1.save()
seller1 = Seller.objects.create(user=user1)
seller1.save()

user2 = User.objects.create_user('name', 'names_mail@mail.com', 'password')
user2.save()
seller2 = Seller.objects.create(user=user2)
seller2.save()

user3 = User.objects.create_user('username', 'example@gmail.com', 'password1')
user3.first_name = 'Firstname'
user3.last_name = 'Lastname'
user3.save()
seller3 = Seller.objects.create(user=user3)
seller3.save()

# 1.2 Ads

# Categories
electronics = Category.objects.create(name="electronics")
electronics.save()
clothes = Category.objects.create(name="clothes")
clothes.save()
sports = Category.objects.create(name="sports")
sports.save()
health = Category.objects.create(name="health")
health.save()

# Tags
cameras = Tag.objects.create(name="cameras")
cameras.save()
ebooks = Tag.objects.create(name="eBooks")
ebooks.save()
headphones = Tag.objects.create(name="headphones")
headphones.save()
tshirts = Tag.objects.create(name="t-shirts")
tshirts.save()
bicycles = Tag.objects.create(name="bicycles")
bicycles.save()
vitamins = Tag.objects.create(name="vitamins")
vitamins.save()

with_delivery = Tag.objects.create(name="delivery_available")
with_delivery.save()
without_delivery = Tag.objects.create(name="delivery_unavailable")
without_delivery.save()

new = Tag.objects.create(name="new")
new.save()
used = Tag.objects.create(name="used")
used.save()

# Ads
# Seller1
camera1 = Ad.objects.create(name='Fujifilm XF16mmF1.4 R WR',
                            description='FUJIFILM X-Mount is compatible with all FUJIFILM interchangeable system cameras',
                            category=electronics,
                            seller=seller1,
                            )

camera1.tag.add(cameras, with_delivery, new)
camera1.save()

headphone1 = Ad.objects.create(name='Sony Noise Cancelling Headphones WHCH710N',
                               description='Noise cancellation automatically senses your environment with Dual Noise '
                                           'Sensor Technology',
                               category=electronics,
                               seller=seller1,
                               )

headphone1.tag.add(headphones, without_delivery, new)
headphone1.save()

ebook1 = Ad.objects.create(name='Kindle Paperwhite',
                           description='Purpose-built for reading – With a flush-front design and 300 ppi glare-free '
                                       'display that reads like real paper, even in bright sunlight.',
                           category=electronics,
                           seller=seller1,
                           )

ebook1.tag.add(ebooks, with_delivery, new)
ebook1.save()

# Seller2
camera2 = Ad.objects.create(name='Canon EOS R6',
                            description='High Image Quality featuring a New 20 Megapixel Full-frame CMOS Sensor',
                            category=electronics,
                            seller=seller2,
                            )

camera2.tag.add(cameras, without_delivery, used)
camera2.save()

bicycle1 = Ad.objects.create(name='SIRDAR S-900 27',
                            description='3 gears front derailleur and 9 gears derailleur deliver 27 speeds of ultra '
                                        'smooth shifting, finger-type shifter. The front and rear double disc brakes '
                                        'provide powerful braking and it\'s not easy to accumulate dust in the brakes',
                            category=sports,
                            seller=seller2,
                            )

bicycle1.tag.add(bicycles, without_delivery, used)
bicycle1.save()

bicycle2 = Ad.objects.create(name='Mountalk Adult Bike Helmet',
                            description='Lightweght inmold bike helmet for youth and adult',
                            category=sports,
                            seller=seller2,
                            )

bicycle2.tag.add(bicycles, without_delivery, used)
bicycle2.save()

# Seller3
vitamin1 = Ad.objects.create(name='Vitamin D',
                            description='160 gummies (80 servings), more than a two month supply (taken daily at '
                                        'listed serving size)',
                            category=health,
                            seller=seller3,
                            )

vitamin1.tag.add(vitamins, without_delivery, new)
vitamin1.save()

vitamin2 = Ad.objects.create(name='Vitamin B6',
                            description='B6 is key for supporting central nervous system function and cardiovascular '
                                        'health. B6 is essential for protein, fat and carbohydrate metabolism as well '
                                        'as the creation of red blood cells and neurotransmitters',
                            category=health,
                            seller=seller3,
                            )

vitamin2.tag.add(vitamins, without_delivery, new)
vitamin2.save()

tshirt1 = Ad.objects.create(name='Black T-shirt',
                            description='Featuring taped neck and shoulders, and double-needle collar, sleeves and hem '
                                        'for long-lasting comfort and durability',
                            category=clothes,
                            seller=seller3,
                            )

tshirt1.tag.add(tshirts, without_delivery, new)
tshirt1.save()


# 1.3 filter
Ad.objects.filter(category=clothes).values('name')
Ad.objects.filter(category=electronics).values('name')
Ad.objects.filter(category=health).values('name')
Ad.objects.filter(category=sports).values('name')


# 7_1

>>> from my_project.main.tasks import sum_values
>>> result = sum_values.apply()
>>> result
<EagerResult: 7f5c4324-bc7d-428d-9f7f-bab853b76309>

>>> from my_project.main.tasks import print_message
>>> print_message.apply()
<EagerResult: 4d02a96a-7d3a-4530-9670-860ccc8665d7>


