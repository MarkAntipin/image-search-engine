import mimetypes

import filetype


def get_content_type(file_buff, file_name=None):
    if file_name:
        content_type, extension = mimetypes.guess_type(file_name)
        if content_type and extension:
            return content_type, extension
    f = filetype.guess(file_buff)
    file_buff.seek(0)
    extension = f.extension
    content_type = f.mime
    return content_type, extension
