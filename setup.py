from setuptools import find_packages, setup

setup(
    name="stc_sources_rec",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "mysql-connector-python", "django", "djangorestframework",
        "tf-nightly", "numpy", "pandas"
    ],
)
