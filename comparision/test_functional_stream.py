from unittest import TestCase

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
    def test_compose_functions_functional_stream(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        price_from_product = lambda product: product['price']

        products = get_products()
        start_profiler()
        #508 function calls in 0.000 seconds

        product_stream = Stream.create(products)

        total_products = (product_stream
                            .stream()
                          .filter(is_rating_greater_than_three)
                          .length())
        product_prices_for_clothing = (product_stream
                                       .stream()
                                       .filter(is_clothing)
                                       .map(price_from_product)
                                       .asList()
                                       )
        stop_profiler()
        print(total_products)
        print(product_prices_for_clothing)
        self.assertEqual(57,total_products)
        self.assertListEqualsInAnyOrder([999.0, 699.0, 1199.0, 1199.0, 2299.0, 999.0, 999.0, 2499.0, 2400.0, 1299.0, 699.0, 2199.0, 999.0, 1200.0, 899.0, 899.0, 1399.0, 1499.0, 750.0, 1299.0, 5398.0, 2795.0, 4999.0, 2699.0, 2499.0],product_prices_for_clothing)


    def test_compose_functions_with_200_users_functional_stream(self):

        is_salary_greater_than_5000 = lambda user: user['salary'] > 50000
        is_male = lambda user: user['gender'] == "Male"
        name_from_user = lambda user: user['first_name']
        users = get_users()


        start_profiler()
        #706 function calls in 0.000 seconds
        results = (Stream.create(users)
                     .filter(is_salary_greater_than_5000)
                     .filter(is_male)
                     .map(name_from_user)
                     .asList()
                     )

        stop_profiler()

        print("results", results)
        self.assertListContains(
            ['Jasen', 'Vasili', 'Lind', 'Darbee', 'Britte', 'Layton', 'Rosabelle', 'Wiley', 'Timoteo', 'Cly', 'Syman',
             'Windham'], results)


    def test_compose_functions_with_products_skip_take_functional_stream(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        products = get_products()
        start_profiler()

        product_stream = Stream.create(products)
        total_products_with_rating_greater_than_3 = (product_stream
                          .stream()
                          .filter(is_rating_greater_than_three)
                          .length())
        prices_for_clothes = (product_stream
                                .stream()
                                .filter(is_clothing)
                                .map(price_from_product)
                                .distinct()
                                .skip(5)
                                .take(8)
                                .asList()
                                )

        stop_profiler()
        print(total_products_with_rating_greater_than_3)
        print(prices_for_clothes)
        self.assertEqual(57,total_products_with_rating_greater_than_3)
        self.assertListEqualsInAnyOrder([2795.0, 2699.0, 750.0, 1199.0, 2299.0, 1200.0, 1299.0, 1499.0],prices_for_clothes)

    def test_compose_functions_with_multiple_compositions(self):
        is_clothing = lambda product: product['category'] == 'Clothing'
        is_rating_greater_than_three = lambda product: product['overAllRating'] > 3
        reviews_from_product = lambda product: product['reviews']
        rating_from_review = lambda review: review['rating']
        name_from_product = lambda product: product['name']
        price_from_product = lambda product: product['price']

        total_products = Stream.create(get_products()).length()
        products_of_rating_greater_than_three = (Stream.create(get_products())
                                                 .stream()
                                                 .filter(is_clothing)
                                                 .filter(is_rating_greater_than_three)
                                                 )
        rating_values = (products_of_rating_greater_than_three
                         .flatmap(reviews_from_product)
                         .map(rating_from_review)
                         .asList())

        product_prices_of_rating_greater_than_three = (products_of_rating_greater_than_three
                                                       .stream()
                                                       .map(price_from_product)
                                                       .asList())

        product_prices = (product_prices_of_rating_greater_than_three
                          .stream()
                          .asList())
        product_prices_skipped_nine_items = (product_prices_of_rating_greater_than_three
                                             .stream()
                                             .skip(9)
                                             .asList())

        product_prices_skip_first_five_take_next_two_items = (product_prices_of_rating_greater_than_three
                                                              .stream()
                                                              .skip(5)
                                                              .take(2)
                                                              .asList())
        unique_product_prices = (product_prices_of_rating_greater_than_three
                                 .stream()
                                 .distinct()
                                 .asList())
        product_names = (products_of_rating_greater_than_three
                         .stream()
                         .map(name_from_product)
                         .asList())
        print("rating_values", rating_values)
        print("total_products", total_products)
        print("product_names", product_names)
        print("product_prices", product_prices)
        print("product_prices_skipped_nine_items", product_prices_skipped_nine_items)
        print("product_prices_skip_first_five_take_next_two_items", product_prices_skip_first_five_take_next_two_items)
        print("unique_product_prices", unique_product_prices)
        self.assertIsNotNone(rating_values)
        self.assertEqual(rating_values, [5, 1, 2, 2, 1, 3, 2, 1, 2, 5, 1, 4, 1, 5, 5, 1])
        self.assertEqual(product_prices,
                         [699.0, 1199.0, 1199.0, 999.0, 999.0, 899.0, 899.0, 1499.0, 5398.0, 2795.0, 2499.0])
        self.assertEqual(product_prices_skipped_nine_items, [2795.0, 2499.0])
        self.assertEqual(product_prices_skip_first_five_take_next_two_items, [899.0, 899.0])
        self.assertEqual(unique_product_prices, [899.0, 2499.0, 999.0, 2795.0, 1199.0, 1499.0, 5398.0, 699.0])
        self.assertEqual(total_products, 154)
        self.assertIn('Alisha Solid Women s Cycling Shorts', product_names)
        self.assertIn(5, rating_values)
        self.assertIn(1, rating_values)
