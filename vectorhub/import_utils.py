"""
    Utilities for importing libraries.
"""
import sys
import warnings
import pkg_resources
import json
from pkg_resources import resource_filename, resource_exists
from importlib import import_module, invalidate_caches


def get_package_requirements(requirement_type: str):
    """
        Load in extra_requirements.json from the package
    """
    if resource_exists('vectorhub', 'extra_requirements.json'):
        requirements_fn = resource_filename('vectorhub', 'extra_requirements.json')
        requirements = json.load(open(requirements_fn, 'r'))
    else:
        requirements_fn = resource_filename('vectorhub', '../extra_requirements.json')
        requirements = json.load(open(requirements_fn))
    
    dependencies = []
    for k, v in requirements.items():
        if requirement_type in v:
            dependencies.append(k) 
    return dependencies

def is_dependency_installed(dependency: str):
    """
        Returns True if the dependency is installed else False.
    """
    IS_INSTALLED = True
    try:
        pkg_resources.get_distribution(dependency)
    except:
        IS_INSTALLED = False
    return IS_INSTALLED

def is_all_dependency_installed(requirement_type: str, raise_warning=True):
    """
        Returns True/False if the dependency is isntalled
        Args:
            requirement_type: The type of requirement. This can be found in the values in extra_requirements.json
            raise_warning: Raise warning if True
    """
    IS_ALL_INSTALLED = True
    requirements = get_package_requirements(requirement_type)
    for r in requirements:
        if not is_dependency_installed(r):
            if raise_warning:
                warnings.warn(f"You are missing dependencies for this submodule. Run `pip install vectorhub[{requirement_type}]`")
            IS_ALL_INSTALLED = False
    return IS_ALL_INSTALLED
