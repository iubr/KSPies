import os
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

# From:
# https://stackoverflow.com/questions/64950460/link-f2py-generated-so-file-in-a-python-package-using-setuptools
class f2py_Extension(Extension):

    def __init__(self, name, sourcedirs):
        Extension.__init__(self, name, sources=[])
        self.sourcedirs = [os.path.abspath(sourcedir) for sourcedir in sourcedirs]
        self.dirs = sourcedirs

class f2py_Build(build_ext):

    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # compile
        for ind, to_compile in enumerate(ext.sourcedirs):
            module_loc = os.path.split(ext.dirs[ind])[0]
            module_name = os.path.split(to_compile)[1].split('.')[0]
            os.system('cd %s;f2py -c %s -m %s' % (module_loc, to_compile, module_name))

data_files = [
    ('fortran_source', ['kspies/kspies_fort.f90', 'kspies/compile.sh'])
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kspies", # Replace with your own username
    version="1.0.3",
    author="Seungsoo Nam,  Ryan J. McCarty, Hansol Park, Eunji Sim",
    author_email="skaclitz@yonsei.ac.kr",
    description="This is a python based Kohn-Sham Inversion Evaluation Software package for use with pySCF.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssnam92.github.io/KSPies/",
    packages=find_packages(),
    data_files=data_files,
    ext_modules = [f2py_Extension('fortran_external', ['kspies/kspies_fort.f90'])],
    cmdclass=dict(build_ext=f2py_Build),
    install_requires=[
      "numpy>=1.18.4",
      "scipy>=1.4.1",
      "opt_einsum>=3.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)

