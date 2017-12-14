import astropy.config as astropyconfig


class ConfigNamespace(astropyconfig.ConfigNamespace):
    rootname = '{{ cookiecutter._parent_project }}'


class ConfigItem(astropyconfig.ConfigItem):
    rootname = '{{ cookiecutter._parent_project }}'
