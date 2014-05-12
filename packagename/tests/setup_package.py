def get_package_data():
    d = {}
    for package_name in _ASTROPY_PROVIDES_:
        d[package_name + '.tests'] = ['coveragerc']
    return d
