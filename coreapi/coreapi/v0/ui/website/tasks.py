from __future__ import absolute_import, unicode_literals
import os
import json
import shutil

from django.conf import settings

from celery import shared_task
import boto


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
            os.makedirs(folder_path)
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
        raise Exception(function, e.message)
