from unittest import TestCase

import rx
from rx import operators as ops

from shared.BaseUnitTest import BaseUnitTest
from shared.products import get_products
from shared.users import get_users

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


class TestStream(BaseUnitTest):
    def test_compose_functions_functional_stream(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()
        start_profiler()
        #2893 function calls (2823 primitive calls) in 0.020 seconds

        product_stream = rx.from_(products)

        total_products_observer = product_stream.pipe(
            ops.filter(is_rating_greater_than_three),
            ops.count()
        )

        product_prices_for_clothing_observer = product_stream.pipe(
            ops.filter(is_clothing),
            ops.map(price_from_product)
        )

        total_products = total_products_observer.run()
        product_prices_for_clothing = product_prices_for_clothing_observer.run()
        stop_profiler()
        print(total_products)
        print(product_prices_for_clothing)
        self.assertEqual(57, total_products)
        self.assertEqual(
             2499.0,
            product_prices_for_clothing)


    def test_compose_functions_users_rx(self):

        is_salary_greater_than_5000 = lambda user: user['salary'] > 50000
        is_male = lambda user: user['gender'] == "Male"
        name_from_user = lambda user: user['first_name']
        users = get_users()

        start_profiler()

        #1754 function calls (1700 primitive calls) in 0.013 seconds
        userstream = rx.from_(users)
        results_stream = userstream.pipe(
                    ops.filter(is_salary_greater_than_5000),
                    ops.filter(is_male),
                    ops.map(name_from_user)
                    )
        results = results_stream.run()

        stop_profiler()


        print("results", results)
        self.assertEqual('Windham',results)