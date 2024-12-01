# setup.py is a module used to build and distribute Python packages. It typically contains information about the package, such as its name,
# version, and dependencies, as well as instructions for building and installing the package. This information is used by the pip tool, which is 
# a package manager for Python that allows users to install and manage Python packages from the command line. By running the setup.py file with 
# the pip tool, you can build and distribute your Python package so that others can use it.

from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
        This function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('\n','') for req in requirements]
    
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements



setup(
    name = 'Machine-Learning-Project',
    version = '0.0.1',
    author = 'Subrat Mishra',
    author_email = '3subratmishra1sep@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)
