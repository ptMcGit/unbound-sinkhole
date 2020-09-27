import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='unbound-sinkhole',
        version='0.1',

        packages=setuptools.find_packages(),

        entry_points={
            'console_scripts': [
                'unbound-sinkhole = unbound_sinkhole.cli:main',
            ]
        },

        test_suite='unbound_sinkhole.tests',
        description='Script for sinkholing hosts using Unbound.',

        license='MIT'
    )
