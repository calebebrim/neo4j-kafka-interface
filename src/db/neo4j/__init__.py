from neo4j import GraphDatabase
import os

driver = None


def get_neo4j_connection():
    global driver
    if driver is None:
        driver = GraphDatabase.driver(os.environ['NEO4J_URI'], auth=(os.environ['NEO4J_USER'], os.environ['NEO4J_PASS']))
    return driver

def query_result_iterator(result):
    for row in result:
        yield row

def query_executor(query:str):
    driver = get_neo4j_connection()
    with driver.session() as sess:
        res = sess.run(query)
        for row in res.value():
            yield row


def command_executor(command:str):
    driver = get_neo4j_connection()
    with driver.session() as session:
        session.write_transaction(lambda tx: tx.run(command))
