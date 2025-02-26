

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt',encoding='utf-8') as requirements_file:
    all_pkgs = requirements_file.readlines()

requirements = [pkg.replace('\n', '') for pkg in all_pkgs if "#" not in pkg]
test_requirements = []

setup(
    name='mofa', 
    author="mofa",
    author_email='cheng.chen@.net',
    # python_requires='>=3.10',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
    ],
    description="Moxin-App-Engine Example",
    entry_points={
        'console_scripts': [
            'mofa=mofa.cli:mofa_cli_group',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mofa',
    packages=find_packages(where='python', include=['mofa', 'mofa.*']),
    package_dir={'mofa': 'python/mofa'},
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.1.dev0',
    zip_safe=False,
    dependency_links=[]
)
