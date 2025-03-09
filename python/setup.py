

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
    name='pymofa',
    author="Cheng Chen, ZongHuan Wu",
    author_email='chenzi00103@gmail.net, zonghuan.wu@gmail.com',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
    ],
    description="MoFA is a software framework for building AI agents through a composition-based approach. Using MoFA, AI agents can be constructed via templates and combined in layers to form more powerful Super Agents.",
    entry_points={
        'console_scripts': [
            'mofa=mofa.cli:mofa_cli_group',
        ],
    },

    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    package_data={
        "": ["requirements.txt", "README.rst", "HISTORY.rst"],
    },
    keywords='mofa',
    packages=['mofa'],
    # packages=find_packages(where='python', include=['mofa', 'mofa.*']),
    # packages=find_packages(where='python'),
    # package_dir={'mofa': 'python/mofa'},
    package_dir={'mofa':'mofa'},
    py_modules=['mofa'],

    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.5',
    zip_safe=False,
    dependency_links=[]
)
