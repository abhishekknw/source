from __future__ import absolute_import, unicode_literals

from io import StringIO
import os

from django.conf import settings
import boto
from boto.s3.key import Key
from celery import shared_task

import v0.constants as v0_constants
import v0.errors as messages


def get_system_error(exception_object):
    """
    Takes an exception object and returns system error.
    Args:
        exception_object:

    Returns: system error

    """
    error_file = open('email_error.txt', 'a')
    error_file.write(str(exception_object))
    error_file.close()
    if not exception_object:
        return []
    return str(exception_object.message) if exception_object.message else str(exception_object.args) if exception_object.args else ""


def send_excel_file(file_name):
    """
    converts the file in binary before returning  it. and sends the required mail
    """
    function = send_excel_file.__name__
    try:
        if os.path.exists(file_name):

            excel = open(file_name, "rb")
            file_content = excel.read()
            output = StringIO.StringIO(file_content)
            out_content = output.getvalue()
            output.close()
            excel.close()
        else:
            # return response
            raise Exception(function, 'File does not exist on disk')
        return out_content
    except Exception as e:
        raise Exception(function, get_system_error(e))


@shared_task()
def bulk_download_from_amazon_per_supplier(folder_path, file_name_list):
    """
    downloads each image file puts all files in archive
    Args:
        file_name_list: list of file_names to download.
        folder_path: The name of the folder to keep the downloaded files in
    Returns: count of files successfully downloaded
    """
    function = bulk_download_from_amazon_per_supplier.__name__
    try:

        bucket_name = settings.ANDROID_BUCKET_NAME
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(bucket_name)

        if not os.path.exists(folder_path):
            # os.makedirs(folder_path)
            os.system("mkdir "+folder_path)
        os.system("chmod 777 "+folder_path)
        count = 0
        for file_name in file_name_list:
            key = bucket.get_key(file_name)
            file_path = folder_path + '/'+ file_name
            if key:
                image_file = open(file_path, 'wb')
                key.get_contents_to_filename(file_path)
                image_file.close()
                
                count +=1
        return count
    except Exception as e:
        raise Exception(function, get_system_error(e))


@shared_task()
def upload_to_amazon(file_name, file_content=None):
    """
    Args:
        file_name: The file name
        file_content: optional file content
    Returns: success in case file is uploaded, failure otherwise error
    """
    function = upload_to_amazon.__name__
    try:

        if not os.path.exists(file_name) and (not file_content):
            raise Exception(function, 'The file path {0} does not exists also NO content provided.'.format(file_name))

        bucket_name = settings.BUCKET_NAME
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(bucket_name)

        k = Key(bucket)
        k.key = file_name
        if file_content:
            k.set_contents_from_string(file_content.read())
        else:
            k.set_contents_from_filename(file_name)
        k.make_public()
        return messages.UPLOAD_AMAZON_SUCCESS

    except Exception as e:
        raise Exception(function, get_system_error(e))


