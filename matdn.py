from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv, os, time, json
import couchdb

url = f'http://admin:comp90024-60@172.26.133.94:5984/'
couch = couchdb.Server(url)

database = 'mastodon'
db = couch[database]


m = Mastodon(
        api_base_url=f'https://mastodon.social',
        #access_token=os.environ['Avy5Af-yjYcuKvTlPNEmTPp_M9Eq_tAEeCse5P8hq4w']
        access_token='Avy5Af-yjYcuKvTlPNEmTPp_M9Eq_tAEeCse5P8hq4w'
    )

class Listener(StreamListener):
    def on_update(self, status):
        json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
        doc_id, doc_rev = db.save(json.loads(json_str))
        #print(f"Document saved with ID: {doc_id} and revision: {doc_rev}")

m.stream_public(Listener())

#m.stream_hashtag(Listener(), tag='lol')