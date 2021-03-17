from setuptools import setup
from version import get_git_version

setup(name='lwa-antpos',
      version=get_git_version(),
      url='http://github.com/ovro-lwa/lwa-antpos/',
      packages=['lwa_antpos'],
      install_requires=['openpyxl', 'pandas>=0.2.5', 'numpy'],
      package_data={
          'lwa_antpos': ['data/LWA-352*xlsx', 'data/*yml']},
      zip_safe=False)
