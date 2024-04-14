from setuptools import setup, find_packages

setup(
    name='clexer',
    version='1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'ply',
    ],
    author=['Oscar Ramirez', 'Ruben Vazquez', 'Iker Guerrero'],
    author_email=['oscardiaz.dev@gmail.com', 'developerrv1024@gmail.com', 'ikerguerrero@yahoo.com'],
    description='Python based lexicographic c analyzer',
    license='MIT',
    keywords='lexer ply',
    url='https://github.com/elP4drino/CLexer',
)