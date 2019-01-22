from django.db import connection
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'coreapi.settings'

cursor = connection.cursor()
cursor.execute('show tables;')

tables_not_to_be_dropped = (
    'django_admin_log', 'django_content_type', 'django_migrations', 'django_session', 'auth_group',
    'auth_group_permissions', 'auth_permission', 'auth_user', 'auth_user_groups', 'auth_user_user_permissions'
    )
parts = ('TRUNCATE TABLE %s;' % table for (table,) in cursor.fetchall() if table not in tables_not_to_be_dropped)

sql = 'SET FOREIGN_KEY_CHECKS = 0;\n' + '\n'.join(parts) + 'SET FOREIGN_KEY_CHECKS = 1;\n'
connection.cursor().execute(sql)
