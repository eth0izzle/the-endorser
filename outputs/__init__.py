import glob, imp, os


def _discover_output_modules():
    cdir = os.path.dirname(os.path.realpath(__file__))
    output_modules = list(filter(lambda p: not os.path.basename(p).startswith('_'), glob.glob(os.path.join(cdir, '*.py'))))

    return dict([(os.path.basename(os.path.splitext(output_module)[0]), output_module) for output_module in output_modules])


def get_output_module_by_name(name):
    for om_name, om_path in _discover_output_modules().items():
        if om_name == name:
            return imp.load_source(om_name, om_path)

    raise ModuleNotFoundError("%s output module not found", name)
