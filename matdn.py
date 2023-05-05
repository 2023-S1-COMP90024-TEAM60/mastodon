from mastodon import Mastodon, StreamListener
import json
import couchdb
import argparse


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
        "--couchdb_endpoint", type=str, help="CouchDB endpoint"
    )
    parser.add_argument(
        "--couchdb_database", type=str, help="CouchDB database to store data", default="mastodon"
    )

    args = parser.parse_args()

    # initiate database
    url = args.couchdb_endpoint
    couch = couchdb.Server(url)
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
    m.stream_public(Listener(db, args.mastodon_server_tag), local=True)


if __name__ == "__main__":
    main()
