import random
import sys

from faker import Faker

class MockObject(Faker):
    def __init__(self):
        self.mock = Faker()

    def first_name(self):
        return self.mock.first_name()
    
    def last_name(self):
        return self.mock.last_name()
    
    def address(self):
        return self.mock.address()
    
    def municipality(self, county=None):
        return self.get_random(county, 1) + ' County'
    
    def application_id(self):
        return 'AAA-' +  self.get_random_caps() + '-' + self.get_random_nums()
    
    def postalcode(self):
        return self.mock.postalcode()
    
    def get_random(self, chars, size=5):
            return ''.join(random.choice(chars) for _ in range(size))

    def get_random_nums(self,size=5):
        num = self.get_random([chr(i) for i in range(48,58)], size)
        return num

    def get_random_small(self,size=5):
        small = self.get_random([chr(i) for i in range(97,123)], size)
        return small
    
    def get_random_caps(self,size=5):
        caps = self.get_random([chr(i) for i in range(65,91)], size)
        return caps
    
    def get_random_specials(self,size=5):
        specials = self.get_random([chr(i) for i in [33,35,36,37,38,42,59,61,63] + list(range(43,47))], size)
        return specials

    def get_random_characters(self,size=5):
        num = self.get_random([chr(i) for i in range(48,58)], size)
        small = self.get_random([chr(i) for i in range(97,123)], size)
        caps = self.get_random([chr(i) for i in range(65,91)], size)
        specials = self.get_random([chr(i) for i in [33,35,36,37,38,42,59,61,63] + list(range(43,47))], size)
        characters = [i for i in (''.join([num, small, caps, specials]))]
        return self.get_random(characters, size)

m = MockObject()
print("Random Number :: " ,m.get_random_nums())
print("Random Small Alphabets :: " ,m.get_random_small())
print("Random Caps Alphabets :: " ,m.get_random_caps())
print("Random Special Characters :: " ,m.get_random_specials())
print("Random Combination Characters :: " ,m.get_random_characters(10))


