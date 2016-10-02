from django.utils import timezone


def add_date_to_filename(filename, **kwargs):
    new_filename = dict()
    #path_parts = filename.split(os.path.se)
    if '/' in filename and '\\' in filename:
        raise ValueError('Filename %s contains both / and \\ separators' % filename)
    if '\\' in filename:
        path_parts = filename.split('\\')
        file = path_parts[-1]
        path = '\\'.join(path_parts[:-1])
        separator = '\\'
    elif '/' in filename:
        path_parts = filename.split('/')
        file = path_parts[-1]
        path = '/'.join(path_parts[:-1])
        separator = '/'
    else:
        file=filename
        path = ''
        separator = ''

    new_filename['path'] = path
    parts = file.split('.')
    new_filename['extension'] = parts[-1]
    new_filename['separator'] = separator
    new_filename['filename_with_out_extension'] = '.'.join(parts[:-1])
    new_filename['datetime'] = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M')
    date_position = kwargs.get('date_position', 'suffix')
    if date_position=='suffix':
        return '{path}{separator}{filename_with_out_extension}_{datetime}.{extension}'.format(**new_filename)
    else:
        return '{path}{separator}{datetime}_{filename_with_out_extension}.{extension}'.format(**new_filename)
