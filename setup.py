from setuptools import setup, find_packages

setup(
    name = 'django-xenforo',
    version = '1.2.0',
    packages = find_packages(),
    author = 'Augusto Destrero',
    author_email = 'a.destrero@gmail.com',
    license='MIT',
    description = 'A little app to integrate Xenforo 2 users in your Django project.',
    url = 'https://github.com/baxeico/django-xenforo',
    keywords = ['django', 'xenforo', 'authentication'],
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'phpserialize>=1.3',
    ]
)
