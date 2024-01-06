from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from adminsite.usermanagement.models import USER_TYPE
from vehiclemanagement import settings
from datetime import datetime
from random import choices
from pathlib import Path
import string


def admin_access_required():
    def wrapper(function):
        @login_required(login_url=settings.ADMIN_LOGIN_URL)
        def wrap(request, *args, **kwargs):
            if request.user.type == USER_TYPE.ADMIN:
                return function(request, *args, **kwargs)
            return redirect(settings.ADMIN_LOGIN_URL)
        return wrap
    return wrapper


def generate_cur_date():
    return datetime.now().strftime("%Y%m%d")


def generate_cur_time():
    return datetime.now().strftime("%H%M%S")


def generate_random_character(length=0, lower=None, letters=None):
    if lower:
        letters_set = string.ascii_lowercase
    elif letters:
        letters_set = string.ascii_letters
    else:
        letters_set = string.ascii_uppercase
    return ''.join(choices(letters_set, k=length))


def generate_image_name():
    return generate_cur_date() + generate_random_character(6) + generate_cur_time()


def change_file_name(filename):
    extension = filename.split(".")[-1]
    changed_file_name = generate_image_name()
    return f'{changed_file_name}.{extension}'


def file_upload_server(myfile, folder_name, base_url):
    try:
        fs = FileSystemStorage(location=Path.joinpath(settings.MEDIA_ROOT, folder_name), base_url=base_url)
        filename = fs.save(myfile.name, myfile.file)
        return fs.url(filename)
    except Exception as e:
        return None