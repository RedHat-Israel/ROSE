from distutils.core import setup

setup(name='RaananaTiraProject',
      version='1.0',
      license="GNU GPLv2+",
      description="game",
      py_modules=['server/game', 'server/gameServer', 'server/main',
                  'client/game', 'client/config', 'client/__init__',
                  'client/main',
                  'components/car', 'components/component',
                  'components/__init__', 'components/matrix_config',
                  'components/matrix', 'components/message'],
      author='Yaniv Bronhaim',
      author_email='ybronhei@redhat.com',
      url="https://github.com/emesika/RaananaTiraProject",
      scripts=["start_client", "start_server"])
