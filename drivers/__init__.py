import glob, imp, os

IPHONE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"

def discover_drivers():
    cdir = os.path.dirname(os.path.realpath(__file__))
    drivers = list(filter(lambda p: not os.path.basename(p).startswith('_'), glob.glob(os.path.join(cdir, '*.py'))))

    return dict([(os.path.basename(os.path.splitext(driver)[0]), driver) for driver in drivers])


def get_driver_by_name(name):
    for driver_name, driver_path in discover_drivers().items():
        if driver_name == name:
            return imp.load_source(driver_name, driver_path)

    raise ModuleNotFoundError("%s driver not found", name)
