from mastodon import Mastodon, StreamListener
import json
import couchdb
import argparse
import os

username_file = os.environ.get('COUCHDB_USERNAME_FILE')
password_file = os.environ.get('COUCHDB_PASSWORD_FILE')

with open(username_file, 'r') as f:
    admin = f.read().strip()

with open(password_file, 'r') as f:
    password = f.read().strip()

couchdb_ip = os.environ.get('COUCHDB_IP')
couchdb_port = os.environ.get('COUCHDB_PORT')

url = f'http://{admin}:{password}@{couchdb_ip}:{couchdb_port}/'

couch = couchdb.Server(url)


class Listener(StreamListener):

    def __init__(self, db, server_tag) -> None:
        super().__init__()
        self.db = db
        self.server_tag = server_tag

    def on_update(self, status):
        json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
        record = json.loads(json_str)
        record["server_tag"] = self.server_tag
        self.db.save(record)


def main():
    """
    Main method of the program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mastodon_server_url", type=str, help="Mastodon server url"
    )
    parser.add_argument(
        "--mastodon_access_token", type=str, help="Mastodon access token"
    )
    parser.add_argument(
        "--mastodon_server_tag", type=str, help="Mastodon access token"
    )
    parser.add_argument(
        "--couchdb_database", type=str, help="CouchDB database to store data", default="mastodon"
    )

    args = parser.parse_args()

    # initiate database
    database = args.couchdb_database
    if database not in couch:
        couch.create(database)
    db = couch[database]

    # initiate mastodon
    m = Mastodon(
        api_base_url=args.mastodon_server_url,
        access_token=args.mastodon_access_token,
    )

    # start mastodon listener
    m.stream_public(Listener(db, args.mastodon_server_tag))


if __name__ == "__main__":
    main()
