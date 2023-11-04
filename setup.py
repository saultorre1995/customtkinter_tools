from setuptools import setup,find_packages
import os


# Simple setup for the tkinter UI package

setup(
    name="customtkinter_tools",
    version="07.11.2023",
    author="Saul Gonzalez-Resines",
    author_mail="",
    python_requires=">=3.10",
    install_requires=["customtkinter"],
    packages=find_packages(),
    package_dir = {"":"./"})
#package_dir={"":"src"},


