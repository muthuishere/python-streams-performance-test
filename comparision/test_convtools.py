from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from shared.products import get_products
from shared.users import get_users
from convtools import conversion as c
import cProfile
import pstats

from streams.Stream import Stream

profiler = None


def start_profiler():
    global profiler
    profiler = cProfile.Profile()
    profiler.enable()


def stop_profiler():
    global profiler
    profiler.disable()
    pstats.Stats(profiler).print_stats()


users = [
    {
        "id": 1,
        "first_name": "Mandy",
        "last_name": "Gowan",
        "email": "mgowan0@aol.com",
        "gender": "Female",
        "loves": ['Soccer', 'Cricket', 'Golf'],
        "salary": 119885
    },
    {
        "id": 2,
        "first_name": "Janessa",
        "last_name": "Cotterell",
        "email": "jcotterell1@aol.com",
        "gender": "Female",
        "loves": ['Cricket'],
        "salary": 107629
    },
    {
        "id": 6,
        "first_name": "Jasen",
        "last_name": "Franzini",
        "email": "jfranzini5@aol.com",
        "gender": "Male",
        "loves": ['Soccer', 'Golf'],
        "salary": 78373
    }
]



class TestStream(BaseUnitTest):
    def test_compose_functions_convtools(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()
        start_profiler()

      # 3979 function calls (3817 primitive calls) in 0.006 seconds
        total_products_converter = (
            c.filter(is_rating_greater_than_three).pipe(
                c.aggregate(
                    c.ReduceFuncs.Count()
                )

            ).gen_converter()
        )

        total_products = total_products_converter(products)

        product_prices_for_clothing_converter = (
            c.filter(is_clothing)
                .iter(c.item("price"))
                .as_type(list)
                .gen_converter()

        )

        product_prices_for_clothing = product_prices_for_clothing_converter(products)
        stop_profiler()
        print(total_products)
        print(product_prices_for_clothing)
        #TODO How to do?
        self.assertEqual(154, total_products)
        self.assertListEqualsInAnyOrder(
            [999.0, 699.0, 1199.0, 1199.0, 2299.0, 999.0, 999.0, 2499.0, 2400.0, 1299.0, 699.0, 2199.0, 999.0, 1200.0,
             899.0, 899.0, 1399.0, 1499.0, 750.0, 1299.0, 5398.0, 2795.0, 4999.0, 2699.0, 2499.0],
            product_prices_for_clothing)


    def test_compose_functions_users_convtools(self):
        #length 200

        users = get_users()
        start_profiler()
        #3285 function calls (3199 primitive calls) in 0.004 seconds
        converter = (
            c.filter(c.item("salary") > 50000)
                .filter(c.item("gender") == "Male")
                .iter(c.item("first_name"))
                .as_type(list)
                .gen_converter()
        )
        results = converter(users)
        stop_profiler()


        print("results", results)
        self.assertListContains(['Jasen', 'Vasili', 'Lind', 'Darbee', 'Britte', 'Layton', 'Rosabelle', 'Wiley', 'Timoteo', 'Cly', 'Syman', 'Windham'],results)

