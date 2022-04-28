from datetime import datetime
import random
from faker.factory import Factory
from collections import OrderedDict
from faker import Faker

Faker = Factory.create
fake = Faker("zh_CN")

class BaseGenerator(object):
    
    def __init__(self) -> None:
        global fake
        fake.seed(datetime.now().timestamp())   
    
    def generate(self):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

class IntGenerator(BaseGenerator):

    def generate(self,min=None,max=None,only_positive=None,only_negative=None,**kwargs):
        res = random.randint(min or -99999,max or 99999)
        if only_positive:
            return res if res > 0 else (0-res)
        elif only_negative:
            return res if res < 0  else (0-res)
        else:
            return res

class AgeGenerator(IntGenerator):

    def generate(self, min=None, max=None,**kwargs):
        return super().generate(min, max, only_positive=True, only_negative=False)


class MailGenerator(BaseGenerator):
    
    def generate(self,mail_serve=None,**kwargs): 
        return fake.ascii_email()


class IP4Generator(BaseGenerator):
    
    def generate(self,**kwargs): 
        return fake.ipv4()

class IP6Generator(BaseGenerator):
    
    def generate(self,**kwargs): 
        return fake.ipv6()

class GenderGenerator(BaseGenerator):
    options=["男","女"]
    def generate(self,**kwargs):
        return GenderGenerator.options[random.randint(0,1)]

class AddressGenerator(BaseGenerator):
    def generate(self,**kwargs):
        return fake.address()

class TelePhoneGenerator(BaseGenerator):
    def generate(self,**kwargs):
        return fake.phone_number()

class PhoneNumberGenerator(BaseGenerator):
    def generate(self,**kwargs):
        return fake.phone_number()

class LocationGenerator(BaseGenerator):
    def generate(self,**kwargs):
        return "{}{}".format(fake.administrative_unit(),fake.city())

class PayGenerator(BaseGenerator):

    def generate(self,min=None,max=None,precision=None,**kwargs):
        """ 
            pydecimal(left_digits=None, right_digits=None, positive=False, min_value=None, max_value=None)
        """
        return fake.pydecimal(right_digits=precision or 2,min_value = min or -99999,max_value =max or 99999)

