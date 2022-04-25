from setuptools import find_packages, setup

setup(
    name='Jam-Sesh-Server',
    version='1.0.12',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'amqp', 'celery', 'psycopg2', 'SQLAlchemy', 'requests', 'python-dotenv'
    ],
)