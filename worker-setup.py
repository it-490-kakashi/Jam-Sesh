from setuptools import find_packages, setup

setup(
    name='Jam-Sesh-Worker',
    version='1.0.0',
    packages=["worker"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'amqp', 'celery', 'psycopg2-binary', 'SQLAlchemy', 'requests', 'python-dotenv', 'APScheduler'
    ],
)