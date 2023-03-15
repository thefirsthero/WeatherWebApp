from app import *
import unittest

class Test_App(unittest.TestCase):

    # test city insertion into db and city selection from db
    def test_city_insertion(self):
        # get initial cities list
        initial_cities = get_cities()
        # iinsert a new city
        insert_city('Pretoria')
        # get list of new cities
        new_cities = get_cities()
        # append initial cities list with new city
        initial_cities.append('Pretoria')
        # see if they are equal
        self.assertEqual(initial_cities, new_cities)

    # test city deletion from db and city selection from db
    def test_city_deletion(self):
        # get initial cities list
        initial_cities = get_cities()
        # if the list is not empty delete the last element
        if (initial_cities) != 0:
            del_city(initial_cities[-1])
        # get list of new cities
        new_cities = get_cities()
        # append initial cities list with new city
        initial_cities.pop()
        # see if they are equal
        self.assertEqual(initial_cities, new_cities)

    # test if city exists function
    def test_city_exists(self):
        # get initial cities list
        initial_cities = get_cities()
        # if the list is not empty delete the last element
        if (initial_cities) != 0:
            self.assertEqual(city_exists(initial_cities[0]), True)
        # if it is empty add an element to it and test it
        else:
            insert_city('Cape Town')
            self.assertEqual(city_exists(initial_cities[0]), True)

    

        
if __name__ == '__main__':
    unittest.main()