import arvados
import arvados.collection
import sys

api = arvados.api('v1')
project_uuid = sys.argv[1]

collection_uuids = []
for arg in sys.argv[2:len(sys.argv)]:
  collection_uuids.append(arg)

combined_manifest = ""
for u in collection_uuids:
    id = arvados.api().collections().list(filters=[["portable_data_hash","=", u]]).execute()
    uuid = id.items()[1][1][0]['uuid']
    c = api.collections().get(uuid=uuid).execute()
    combined_manifest += c["manifest_text"]

newcol = arvados.collection.Collection(combined_manifest)
print newcol.portable_data_hash()
newcol.save_new(name="%s" % (str(newcol.keys()[0])), owner_uuid=project_uuid)
