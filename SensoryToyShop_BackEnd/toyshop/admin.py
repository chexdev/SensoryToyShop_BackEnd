'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import Product, ProductCategory, ProductInfo
import datetime


bp = Blueprint('admin', __name__, url_prefix='/admin/')

# function to put some seed data in the database


@bp.route('/dbseed/')
def dbseed():
    pc1 = ProductCategory(name='Calming Toys', image='jumbocalm.jpg',
                          description='''Reduce stress and anxiety''')
    pc2 = ProductCategory(name='Fidget Toys', image='fidget2.jpg',
                          description='''Improve focus and attention''')
    pc3 = ProductCategory(name='Squishy Toys', image='squish1.jpg',
                          description='''Release stress and tension''')
    try:
        db.session.add(pc1)
        db.session.add(pc2)
        db.session.add(pc3)
        db.session.commit()
    except:
        return 'There was an issue adding product categories in dbseed function'

    p1 = Product(productCategory_id=pc1.id, image='calm1.jpg', price=32.99,
                 date=datetime.datetime(2020, 5, 17),
                 name='Glowy Fish Lamp',
                 description='Fish lamp that calms and glows')
    p2 = Product(productCategory_id=pc1.id, image='calm2.jpg', price=32.99,
                 date=datetime.datetime(2020, 6, 17),
                 name='Volcano Lava Lamp',
                 description='Volcano lamp with calming glowy lava eruption')
    p3 = Product(productCategory_id=pc1.id, image='calm3.jpg', price=32.99,
                 date=datetime.datetime(2020, 6, 20),
                 name='Blue Jellyfish Lamp',
                 description='Jellyfish lamp with blue calming glow')
    p4 = Product(productCategory_id=pc2.id, image='fidget1.jpg', price=9.99,
                 date=datetime.datetime(2020, 4, 20),
                 name='Rainbow Sluggy',
                 description='Cute rainbow slug')
    p5 = Product(productCategory_id=pc2.id, image='fidget2.jpg', price=15.99,
                 date=datetime.datetime(2020, 4, 20),
                 name='Magical Polyhedron',
                 description='Cool dazzling magical polyhedron')
    p6 = Product(productCategory_id=pc2.id, image='fidget3.jpg', price=180.99,
                 date=datetime.datetime(2020, 2, 1),
                 name='Ultimate Fidget Set',
                 description='Complete fidget set for hours of non-stop fidgetting')
    p7 = Product(productCategory_id=pc3.id, image='squish1.jpg', price=10.99,
                 date=datetime.datetime(2020, 2, 1),
                 name='Squishy Rabbit',
                 description='Cute squishy rabbit for your squishy needs')
    p8 = Product(productCategory_id=pc3.id, image='squish2.jpg', price=11.99,
                 date=datetime.datetime(2020, 3, 8),
                 name='Squish Monster',
                 description='Assortment of squishy monsters for your squishy needs')
    p9 = Product(productCategory_id=pc3.id, image='squish3.jpg', price=10.99,
                 date=datetime.datetime(2020, 8, 2),
                 name='Stretchy Llama',
                 description='Ridiculous stretchy llama for hours of squish and fun')

    try:
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p5)
        db.session.add(p6)
        db.session.add(p7)
        db.session.add(p8)
        db.session.add(p9)
        db.session.commit()
    except:
        return 'There was an issue adding product items in dbseed function'

    pi1 = ProductInfo(product_id=p1.id,
                      description='Perfect tool for emotional regulation or just something soothing and calming to look at. 3 AAA Batteries required. TIP: Turn the lamp off when not in use to get longer out of it before batteries need changing. Size: 23cm tall')
    pi2 = ProductInfo(product_id=p2.id,
                      description='Perfect tool for emotional regulation or just something soothing and calming to look at. 3 AAA Batteries required. TIP: Turn the lamp off when not in use to get longer out of it before batteries need changing. Size: 23cm tall')
    pi3 = ProductInfo(product_id=p3.id,
                      description='Perfect tool for emotional regulation or just something soothing and calming to look at. 3 AAA Batteries required. TIP: Turn the lamp off when not in use to get longer out of it before batteries need changing. Size: 23cm tall')
    pi4 = ProductInfo(product_id=p4.id,
                      description='This cute little Rainbow Fidget Slug makes a great desk-mate. The way he feels when he moves in your hands is hard to describe, it’s so smooth and oddly satisfying. You can shake him to hear his body click and clack as he moves back and forth, move and twist him around in your hands. Don’t miss out on getting yours – click to buy now! Size: approx 17cm')
    pi5 = ProductInfo(product_id=p5.id,
                      description='A colourful endlessly flexible hexaflexagon-shaped fidget toy. Designed to fit in the palm of your hand and to roll around your fingertips. The colourful swirl patterns adds to the mesmersizing looks. Available in 2 colours - Blue and Yellow!')
    pi6 = ProductInfo(product_id=p6.id,
                      description='The Kaiko Mega Works Kit is the big daddy version of our best selling Works Kit.  It is a top of the range fidget kit for any fidget lover.  It contains fidgets that are discreet yet large in size than the standard works kit which means its ideally suited to older teens and adults.  We have also ensured the kit contains a different selection to the works (with the exception of the spikey) so that if you own a works kit already you are adding to your Kaiko collection and not duplicating. It contains a chain link jumbo, millipede, xl hexa, fidget spikey, and more! Not suitable for 5 and under.')
    pi7 = ProductInfo(product_id=p7.id,
                      description='Squishy Bunny toys have a really soft rubbery texture. They are excellent fidget toys and stress relievers. While not indestructible, in the event of breakage, these fidgets wont make a mess! Product size: approx 4 x 3 cm (each squeezy toy).')
    pi8 = ProductInfo(product_id=p8.id,
                      description='Squishy Monster toys have a really soft rubbery texture. They are excellent fidget toys and stress relievers. While not indestructible, in the event of breakage, these fidgets wont make a mess! Product size: approx 4 x 3 cm (each squeezy toy).')
    pi9 = ProductInfo(product_id=p9.id,
                      description='Ridiculous Stretchy Llama toys have a really soft rubbery texture. They are excellent fidget toys and stress relievers. While not indestructible, in the event of breakage, these fidgets wont make a mess! Product size: approx 4 x 3 cm (each squeezy toy).')

    try:
        db.session.add(pi1)
        db.session.add(pi2)
        db.session.add(pi3)
        db.session.add(pi4)
        db.session.add(pi5)
        db.session.add(pi6)
        db.session.add(pi7)
        db.session.add(pi8)
        db.session.add(pi9)
        db.session.commit()
    except:
        return 'There was an issue adding product information in dbseed function'

    return 'DATA LOADED'
