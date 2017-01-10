from setuptools import setup

setup(name='framefilejson',
      version='0.9',
      description='The common json API for Toyota project',
      url='https://bitbucket.org/datasectiondl/frame_file_json_api',
      author='Kju',
      author_email='quanns@datasection.com.vn',
      license='MIT',
      packages=['framefilejson'],
      install_requires=[
          'ujson'
      ],
      zip_safe=False)