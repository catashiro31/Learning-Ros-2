from setuptools import find_packages, setup

package_name = 'turtlesim_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='catashiro31',
    maintainer_email='catashiro31@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "turtle_spawner = turtlesim_project.turtle_spawner:main",
            "predator = turtlesim_project.predator:main",
            "processer = turtlesim_project.processer:main"
        ],
    },
)
