import astropy.config as astropyconfig


class ConfigNamespace(astropyconfig.ConfigNamespace):
    pass


class ConfigItem(astropyconfig.ConfigItem):
    rootname = '{{ cookiecutter._parent_project }}'
