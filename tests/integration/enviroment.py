# USE: behave -D BEHAVE_DEBUG_ON_ERROR         (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=yes     (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=no      (to disable debug-on-error)

import os
import ipdb
import mysql.connector
import configparser
from tests.integration.steps.utils import *

config = configparser.ConfigParser()
config.read(
    os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)) + '/config.properties')

BEHAVE_DEBUG_ON_ERROR = True
ROOT_DIR = os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])
DB = 'MYSQL'


def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def before_all(context):
    setup_debug_on_error(context.config.userdata)
    pass


def before_step(context, step):
    pass


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).

        ipdb.post_mortem(step.exc_traceback)


def before_scenario(context, scenario):
    clean_db()

def after_scenario(context, scenario):
    clean_db()


def clean_db():
    try:
        cnx = mysql.connector.connect(
            user=config.get(DB, 'USER'),
            password=config.get(DB, 'PASSWORD'),
            host=config.get(DB, 'HOST'),
            database=config.get(DB, 'DATABASE')
        )
    except mysql.connector.Error as e:
        print(e)
        raise e
    cursor = cnx.cursor()
    destroy_user = "DELETE FROM mercadolibre_user WHERE Id > 0"
    destroy_realstate = "DELETE FROM mercadolibre_realstate WHERE Id > 0"
    cursor.execute(destroy_user)
    cursor.execute(destroy_realstate)
    cnx.commit()
    cursor.close()
    cnx.close()
