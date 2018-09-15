class Config():
    DATABASE = {
        'NAME': 'mdtech8',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'wikasta123',
    }
    BASE_URL = 'http://localhost:8000/'

class ConfigProd():
    DATABASE = {
        'NAME': 'mdproddb',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mdprod.cow21ijx99fo.ap-south-1.rds.amazonaws.com',
        'USER': 'md1',
        'PASSWORD': 'pwd4mdprod',
    }
    BASE_URL = 'http://coreapi-test.3j6wudg4pu.ap-southeast-1.elasticbeanstalk.com/'
