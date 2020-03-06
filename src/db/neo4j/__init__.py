from neo4j import GraphDatabase
import os
import logging
driver = None


def get_neo4j_connection():
    global driver
    if driver is None:
        driver = GraphDatabase.driver(
                    os.environ['NEO4J_URI'],
                    auth=(
                        os.environ['NEO4J_USER'],
                        os.environ['NEO4J_PASS']
                    ))
    return driver


def query_result_iterator(result):
    for row in result:
        yield row


def query_executor(query: str):
    with get_neo4j_connection().session() as sess:
        try:
            res = sess.run(query)
        except Exception as ex:
            raise Exception("Query error: {}".format(str(ex)))
        try:
            for row in res.value():
                yield row
        except Exception as ex:
            raise Exception("Something happend while yelding results: {}".format(str(ex)))

def command_executor(command: str):
    with get_neo4j_connection().session() as session:
        logging.info("Executing Command: {}".format(command))
        try:
            session.write_transaction(lambda tx: tx.run(command))
        except Exception as ex:
            logging.error("Error while executting command '{}': {}".format(command, ex))
            raise ex
