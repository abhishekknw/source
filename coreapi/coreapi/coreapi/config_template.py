class Config():
    DATABASE = {
        'NAME': 'mdtech9',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '',
    }
    MONGO_DB = 'machadalo'
    MONGO_DB_TEST = 'mdtest'
    BASE_URL = 'http://localhost:8000/'
    DEFAULT_CC_EMAILS = []

class ConfigProd():
    DATABASE = {
        'NAME': 'mdproddb',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'USER': 'md1',
        'PASSWORD': '',
    }
    MONGO_DB = 'machadalo'
    MONGO_DB_TEST = 'mdtest'
    BASE_URL = 'http://coreapi-test.3j6wudg4pu.ap-southeast-1.elasticbeanstalk.com/'
    DEFAULT_CC_EMAILS = ['anupam@machadalo.com', 'anmol.prabhu@gmail.com', 'sathya.sharma@machadalo.com',
                               'madhu.atri@machadalo.com']

