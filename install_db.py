import pymysql

sql_dump_file = 'helpers/dump-mh-201902072316.sql'
username = 'mh_selenium'
password = 'mh_selenium'


def parse_sql_dump(filename):
    list_commands = []
    with open(filename, 'r') as data:
        lines = data.readlines()
        multi_line_command = ''
        for line in lines:
            # skip empty string
            if not line.strip():
                continue
            # skip comments
            if line.startswith('--'):
                continue
            # add the line to this string of it doesn't contain ';'
            if ';' not in line:
                multi_line_command += line.strip()
                continue
            else:
                if not multi_line_command:
                    # confirm that there wasn't found any multi-line commands before and append right away
                    list_commands.append(line.strip())
                if multi_line_command:
                    # the multi-line command started already, concatenate it with the current line and append
                    list_commands.append(multi_line_command + line.strip())
                    multi_line_command = ''
    return list_commands


def create_db_user():
    conn = pymysql.connect(host='localhost', unix_socket='/run/mysqld/mysqld.sock',
                           user='root', charset='utf8')
    cur = conn.cursor()
    cur.execute(f"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}'")
    cur.connection.commit()
    cur.execute(f"GRANT ALL PRIVILEGES ON mh.* TO '{username}'@'localhost'")
    cur.connection.commit()
    cur.execute('FLUSH PRIVILEGES')
    cur.connection.commit()
    cur.close()
    conn.close()
    print(f'User "{username}" created at localhost. Password set to "{password}".')


def prepare_db_to_use():
    conn = pymysql.connect(host='localhost', unix_socket='/run/mysqld/mysqld.sock',
                           user=f'{username}', passwd=f'{password}', charset='utf8')
    print('Logged in.\n'
          '----------')
    cur = conn.cursor()
    cur.execute('CREATE DATABASE IF NOT EXISTS mh')
    cur.connection.commit()
    cur.execute('USE mh')
    cur.connection.commit()
    cur.execute('SET autocommit = 0')
    cur.connection.commit()

    for command in parse_sql_dump(sql_dump_file):
        cur.execute(command)
        cur.connection.commit()

    print('Database scheme for the "mh" database imported successfully and ready to use.')
    cur.close()
    conn.close()


create_db_user()
prepare_db_to_use()
