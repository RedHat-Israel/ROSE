import subprocess
from distutils.core import setup
from distutils.command import sdist


class rose_sdist(sdist.sdist):
    def run(self):
        self.generate_files()
        sdist.sdist.run(self)

    def generate_files(self):
        with open('requirements.txt', 'w') as f:
            f.write("# Generated automatically from Pipfile - do not edit!\n")
            f.flush()
            subprocess.check_call(['pipenv', 'lock', '--requirements'],
                                  stdout=f)


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
      data_files=[('requirements.txt', ['requirements.txt'])],
      cmdclass={'sdist': rose_sdist})
