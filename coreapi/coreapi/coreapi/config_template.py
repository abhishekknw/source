class Config():
    DATABASE = {
        'NAME': 'machadalotech',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'wikasta123',
    }
    BASE_URL = 'http://localhost:8000/'

class ConfigProd():
    DATABASE = {
        'NAME': 'mdtestnew',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mdtest.cncgdhp3beic.ap-southeast-1.rds.amazonaws.com',
        'USER': 'mdtest',
        'PASSWORD': 'mdtestmachadalo',
    }
    BASE_URL = 'http://coreapi-test.3j6wudg4pu.ap-southeast-1.elasticbeanstalk.com/'
