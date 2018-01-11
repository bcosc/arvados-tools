import arvados
import arvados.collection
import sys
import re

# Input a collection
# Input a variable number of regexes and file names that will be removed from the Collection
# Iterate over input collection and check against regex and file names and add to new collection if it doesn't match.
# Save new collection and output uuid

def return_file_path(c, filename, found=None, *subdir):
  """Returns file path of a sample"""
  if found is None:
    found = []
  for item in c:
    if isinstance(c[item], ArvadosFile):
      if item == filename:
        path = os.path.join(c[item].parent.stream_name(),item)
        found.append(path)
        return found
    else:
      func = return_file_path(c.find(item), filename, found, item)
      if func is not None:
        return func

def return_all_paths

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--project-uuid', metavar='UUID', help='Project to output to')
  parser.add_argument('collection_uuid', metavar='UUID', help='Collection UUID')
  parser.add_argument('filters', nargs='*', help='Regexes or filenames to use to remove files from Collection')
  args = parser.parse_args()
  collection_uuid = args.collection_uuid
  project_uuid = args.project_uuid
  c = Collection(collection_uuid)
  dest = Collection()
  for i in c:
    if isinstance(c[i], ArvadosFile):
      # Check regex, return path, copy if wanted
      dest.copy('./'+i, target_path='./'+i, source_collection=c)
    if isinstance(c[i], Subcollection):
      # go deeper recursively and look for files, return path
  dest.save_new(owner_uuid=project_uuid)
  print(dest.manifest_locator())


if __name__ == '__main__':
    main()

