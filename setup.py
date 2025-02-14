from setuptools import setup, find_packages, Extension

ffi = Extension(
  'arnelify-router-ffi',
  sources=['arnelify_router/cpp/ffi.cpp'],
  language='c++',
  extra_compile_args=['-std=c++2b', '-w'],
  include_dirs=['arnelify_router/cpp/include', '/usr/include', '/usr/include/jsoncpp/json'],
  extra_link_args=['-ljsoncpp', '-lz']
)

setup(
    name="arnelify-router",
    version="0.7.1",
    author="Arnelify",
    description="Minimalistic dynamic library which is a router written in C and C++.",
    url='https://github.com/arnelify/arnelify-router-python',
    keywords="arnelify arnelify-router-python arnelify-router",
    packages=find_packages(),
    license="MIT",
    install_requires=["cffi", "setuptools", "wheel"],
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    ext_modules=[ffi],
)