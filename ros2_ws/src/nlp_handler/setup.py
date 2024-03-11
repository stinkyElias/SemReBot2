from setuptools import find_packages, setup

package_name = 'nlp_handler'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Elias Helle Kalland',
    maintainer_email='elias.kalland@outlook.com',
    description='Package to handle NLP tasks as speech-to-text and text generation with a large language model.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'whisper_node = nlp_handler.whisper_node:main'
        ],
    },
)
