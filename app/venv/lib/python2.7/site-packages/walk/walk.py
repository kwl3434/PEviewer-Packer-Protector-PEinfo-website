import getopt
import sys
import os
import datetime
import json
import psycopg2
import traceback

from walk.argsextractor import filter_args
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor

EXAMPLE_CONFIG = {
    'test': [
        'user=postgres',
        'dbname=test'
    ],
    'dev': [
        'user=postgres',
        'dbname=dev'
    ],
    'prod': [
        'user=postgres',
        'dbname=prod',
        'password=pw'
    ]
}
ALLOWED_CONFIG_PARAMS = ['user', 'dbname', 'password', 'host', 'port']
DB_CHANGE_LOG = 'database_change_log'
DB_LOG_SEEDS = 'database_seeds_log'
MIGRATIONS_DIR = 'migrations'
CONFIG_FILE_NAME = 'walk_config.json'

def connection(db_config):
    return psycopg2.connect(' '.join(db_config))

def cursor(con):
    return con.cursor(cursor_factory=DictCursor)

def generate_example_config(directory, force=False):
    # Check if the config file is existing
    file_path = '%s/%s' % (directory, CONFIG_FILE_NAME)
    if not force and os.path.exists(file_path):
        print('Config file is already existing. Use --force to replace the existing file with the default config file.')
        return

    if os.path.exists(file_path):
        os.remove(file_path)

    # Writing pretty json to file
    with open(file_path, 'w') as f:
        json.dump(EXAMPLE_CONFIG, fp=f, indent=4)

    # Creating migrations directory
    migrations_dir = '%s/%s' % (directory, MIGRATIONS_DIR)
    if not force and os.path.exists(migrations_dir):
        print('Migrations folder is already existing. Use --force to delete the existing folder.')
        return

    if os.path.exists(migrations_dir):
        os.remove(migrations_dir)
        return

    # Creating folder
    os.makedirs(migrations_dir)    

def new(file_name, t_dir, task='migrations'):
    # Creating migrations/seeds folder if not exists
    if not os.path.exists(t_dir):
        os.makedirs(t_dir)

    # Create new file with current timestamp
    d_file_name = '%s_%s.sql' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S'), file_name)
    open('%s/%s' % (t_dir, d_file_name), 'w')
    print('Created new %s file %s' % (task, d_file_name))        

def run(env, db_config, t_dir, task='migration', db_log=DB_CHANGE_LOG):
    # Task folder
    if os.path.exists(t_dir):
        # Open connection and create a cursor
        conn = connection(db_config=db_config)
        cur = cursor(con=conn)

        # Check if change log table exists
        cur.execute('select exists(select * from information_schema.tables where table_name=%s)',
                    (db_log,))
        if not cur.fetchone()[0]:
            print('creating database change log table')
            cur.execute('CREATE TABLE %s (id serial primary key, last_timestamp bigint)', (AsIs(db_log),))
            conn.commit()
        else:
            print('database changelog table already exists')

        # Iterate over task files
        files = os.listdir(t_dir)
        files = list(filter(lambda f: f.endswith('.sql') , files))
        ordered_files = sorted(files, key=lambda x: int(x.split('_')[0]))
        try:
            for file in ordered_files:  # Return the name of the files in directory
                if file.endswith('.sql'):
                    # Log timestamp
                    log_level = file.split('_')
                    log_level = log_level[0]

                    # Check if migration exists
                    cur.execute('SELECT * FROM %s ORDER BY last_timestamp DESC', (AsIs(db_log),))
                    last_entry = cur.fetchone()

                    if last_entry and last_entry['last_timestamp'] >= int(log_level):
                        print('%s already exists for file %s' % (task, file))
                    else:
                        # Execute sql
                        print('executing %s for file %s' % (task, file))
                        s = open('%s/%s' % (t_dir, file), 'rb').read().decode('UTF-8')
                        cur.execute(s)
                        conn.commit()

                        # Add migration log entry
                        print('Adding log entry for timestamp: %s' % log_level)
                        cur.execute('INSERT INTO %s (last_timestamp) VALUES (%s)', (AsIs(db_log), int(log_level),))
                        conn.commit()
        except Exception as e:
            print(e)
            traceback.print_exc()
            conn.rollback()
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
    else:
        print('%s folder does not exists: %s' % (task, t_dir))

def main():
    argv = sys.argv
    args = filter_args(argv=argv, opts=[('n:', 'new='), ('m', 'migrate'), 
            ('e:', 'env='), ('i', 'init'), ('f', 'force'), ('p:', 'param='),
            ('w:', 'newseed='), ('s', 'seeds')])
    
    # Print information
    if len(list(map(lambda k: k in ('new=', 'migrate', 'init', 'newseed=', 'seeds'), args.keys()))) == 0:
        print(  '' +
                '-i or --init                   Generates a default config file and the migrations directory. \n' +
                '-f or --force                  Forces the init function to recreate the default settings. \n' +
                '-n or --new test_abc           Creates a new migration file. \n' +
                '-w or --newseed test_abc     Creates a new seeds file. \n' +
                '-m or --migrate                Runs the migrations. \n' +
                '-s or --seed                   Runs the seeds. \n' +
                '-e or --env test               Database environment which will be chosen for the migrations. \n' +
                ('-p or --param dbname=db        Pass database connections parameters dynamically. Valid attributes: %s \n' % ALLOWED_CONFIG_PARAMS) +
                '')
        return

    ## Creating defaults settings
    if 'init' in args.keys():
        force = True if 'force' in args.keys() else False
        generate_example_config(directory='./', force=force)
        return
    
    ## New migrations file
    migrations_directory = './migrations' # Default
    if 'new=' in args.keys():
        new_file = args['new='][0]
        new(file_name=new_file, t_dir=migrations_directory)
        return

    ## New seeds file
    seeds_directory = './seeds' # Default
    if 'newseed=' in args.keys():
        new_file = args['newseed='][0]
        new(file_name=new_file, t_dir=seeds_directory, task='seeds')
        return    
    
    ## MIGRATIONS OR/AND SEEDS
    if not os.path.exists('./%s' % CONFIG_FILE_NAME):
        print('Missing config file. Use \'walk init\' to generate a config file and a migrations folder')
        return

    env = 'dev'
    if 'env=' in args.keys():
        env = args['env='][0]

    ## Merge config params
    config_to_merge = []
    config_params_to_merge = []
    if 'param=' in args.keys():
        config_to_merge = args['param=']
        config_params_to_merge = list(map(lambda f: f.split('=')[0], filter(lambda e: e.split('=')[0] in ALLOWED_CONFIG_PARAMS, config_to_merge)))

    with open('./%s' % CONFIG_FILE_NAME, mode='r') as f:
        configs = json.load(f)    
        if env not in configs and len(config_to_merge) == 0:
            print('Missing configuration for environment %s' % env)
            return

    config = configs[env]
    config_file = list(filter(lambda e: e.split('=')[0] not in config_params_to_merge, config))
    config = config_to_merge + config_file
    if 'migrate' in args.keys():
        run(env, t_dir=migrations_directory, db_config=config, task='migration', db_log=DB_CHANGE_LOG)

    if 'seeds' in args.keys():
        run(env, t_dir=seeds_directory, db_config=config, task='seed', db_log=DB_LOG_SEEDS)        

if __name__ == '__main__':
    main()            