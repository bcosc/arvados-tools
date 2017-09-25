import arvados
import arvados.collection
import sys

api = arvados.api('v1')
project_uuid = sys.argv[1]

collection_uuids = []
for arg in sys.argv[2:len(sys.argv)]:
  print arg
  collection_uuids.append(arg)

combined_manifest = ""
for u in collection_uuids:
    c = api.collections().get(uuid=u).execute()
    combined_manifest += c["manifest_text"]

newcol = arvados.collection.Collection(combined_manifest)
newcol.save_new(name="foo", owner_uuid=project_uuid)
