from distutils.core import setup

setup(name='ROSE Project',
      version='0.1',
      license="GNU GPLv2+",
      description="game",
      packages=['rtp', 'rtp.server', 'rtp.client', 'rtp.common'],
      package_data={'rtp': ['res/*/*.png']},
      author='Yaniv Bronhaim',
      author_email='ybronhei@redhat.com',
      url="https://github.com/emesika/RaananaTiraProject",
      scripts=["rtp-client", "rtp-server", "rtp-admin"],)
