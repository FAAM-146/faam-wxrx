import os

import faam_data

spec = faam_data.get_spec('wxrx-raw')
dataset = faam_data.get_product('wxrx-raw')

try:
    os.mkdir('_dynamic')
except Exception:
    pass

with open('_dynamic/wxrx.rst', 'w') as f:
    f.write('\nGlobal Attributes\n')
    f.write('-' * 18 + '\n\n')

    for key, value in spec['attributes'].items():
        if value is None:
            continue
        f.write(f'* ``{key}``: {value}\n')

    f.write('\nDimensions\n')
    f.write('-' * 10 + '\n\n')

    for dimension in spec['dimensions']:
        size = dimension["size"]
        if size is None:
            size = 'unlimited'
        f.write(f'* ``{dimension["name"]}``: {size}\n')

    f.write('\nVariables\n')
    f.write('-' * 9 + '\n\n')

    for variable in dataset.variables:
        f.write(f'* ``{variable.meta.name}``\n\n')
        f.write(f'  * datatype: `{variable.meta.datatype}`\n')
        f.write(f'  * dimensions:')

        f.write(f' {", ".join(variable.dimensions)}')
        f.write('\n\n')
        f.write(f'  * attributes:\n\n')
        for key, value in variable.attributes:
            if value is None:
                continue
            if key == 'FillValue':
                key = '_FillValue'
            f.write(f'    * {key}: `{value}`\n')
        f.write('\n')
