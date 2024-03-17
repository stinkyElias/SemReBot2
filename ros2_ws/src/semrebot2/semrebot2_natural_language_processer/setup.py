import os

from glob import glob
from setuptools import find_packages, setup

package_name = 'semrebot2_natural_language_processer'

setup(
    name=package_name,
    version='0.0.2',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
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
            # 'whisper_node = nlp_handler.whisper_node:main',
            'whisper_lifecycle_node = semrebot2_natural_language_processer.whisper_lifecycle_node:main',
            # 'mistral_node = nlp_handler.mistral_node:main',
            'mistral_lifecycle_node = semrebot2_natural_language_processer.mistral_lifecycle_node:main',
        ],
    },
)
