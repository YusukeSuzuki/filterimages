from setuptools import setup

setup(name='filterimages',
    version='0.1.0',
    desctiption='filter image file with many conditions',
    author='Yusuke Suzuki',
    license='MIT',
    packages=['filterimages'],
    entry_points={
        'console_scripts':[
            'filterimages = filterimages.main:run'
        ]
    },
    install_requires=[
        'pillow',
        'numpy'
    ],
    zip_safe=False)

