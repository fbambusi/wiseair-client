from distutils.core import setup
setup(
  name = 'wiseair',         # How you named your package folder (MyLib)
  packages = ['wiseair'],   # Chose the same as "name"
  version = '0.1.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A client to access and use Wiseair API',
  long_description = "A client to access and use Wiseair API. Wiseair measures air quality using hyperlocal,\
   capillar networks of autonomous sensors, called Arianna. This client offers a convenient way to access the data: for installation and quickstart, see https://github.com/fbambusi/wiseair-client.",
  author = 'Fulvio Bambusi',
  author_email = 'fulvio.bambusi@wiseair.it',
  url = 'https://github.com/fbambusi/wiseair-client',
  download_url = 'https://github.com/fbambusi/wiseair-client/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['AIR QUALITY', 'DATA ANALYSIS', 'WISEAIR', "API"],   # Keywords that define your package best
  install_requires=[
        'pandas',
        'numpy',
        "requests"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)