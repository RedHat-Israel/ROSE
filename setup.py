import subprocess
import sys
from distutils.core import setup


DATA_FILES = []


def generate_requirements():
    with open('requirements.txt', 'w') as f:
        subprocess.check_call(['pipenv', 'lock', '--requirements'], stdout=f)
    return 'requirements.txt'


if 'sdist' in sys.argv:
    DATA_FILES.append(('requirements.txt', generate_requirements()))


setup(name='rose-project',
      version='0.1',
      license="GNU GPLv2+",
      description="game",
      packages=['rose', 'rose.server', 'rose.client', 'rose.common'],
      package_data={'rose': ['res/*/*.png']},
      author='Yaniv Bronhaim',
      author_email='ybronhei@redhat.com',
      url="https://github.com/emesika/RaananaTiraProject",
      scripts=["rose-client", "rose-server", "rose-admin"],
      data_files=DATA_FILES)
