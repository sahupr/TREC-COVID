# shared config
SERVER_HOST = '10.23.10.219'
SERVER_PORT = 9999
BUF_SIZE = 1024
ERROR_STRING = '<!#ERROR#!>'
STOP_STRING = '<!#STOP#!>'

# server config
OVERWRITE = True
HOST = '10.23.10.219'
USER = 'vuhg'
PASSWD = 'Abcd1234!'
DATABASE = 'cord_19'
TABLE = 'trec_data'
ID = 'a_id'
TEXT = ['title']
RESULT = 'metamap_raw_' + '_'.join(TEXT)
MAX_NUM_CLIENTS = 100

# client config
RUN_DIR = '/tools/public_mm_lite'
RUN_ARGS = ['./metamaplite.sh', '--']
RUN_TIMEOUT = 300
NUM_THREADS = 4
