from distutils.core import setup

setup(name='rose-project',
      version='0.1',
      license="GNU GPLv2+",
      description="game",
      packages=['rose', 'rose.server', 'rose.client', 'rose.common'],
      package_data={'rose': ['res/*/*.png']},
      author='Yaniv Bronhaim',
      author_email='ybronhei@redhat.com',
      url="https://github.com/emesika/RaananaTiraProject",
      scripts=["rose-client", "rose-server", "rose-admin", "requirements.txt"],)
