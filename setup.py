from setuptools import setup
from version import get_git_version

setup(name='lwa-antpos',
      version=get_git_version(),
      url='http://github.com/ovro-lwa/lwa-antpos/',
      packages=['antpos'],
      requirements=['openpyxl', 'pandas', 'numpy'],
      package_data={
          'antpos': ['data/LWA-352*xlsx']},
      zip_safe=False)
