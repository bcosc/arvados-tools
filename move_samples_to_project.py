#!/usr/bin/env python

# Read txt document

# Split txt document into Samples, file extensions, Project name

# Find project uuid with Project name

# Create new collection in Project ? create new subproject and add all collections there and merge and put to parent?
# Find files with Sample*FileExtension

# Merge Files with new collection recursively

import arvados
import sys, os
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('samples', metavar='FILE', help='File with one sample in each line')
  parser.add_argument('--project_uuid', metavar='UUID', help='Customer project UUID to copy outputs to')
  parser.add_argument('--file-extensions', choices=['vcf', 'bam'], nargs='*', help='File extensions of samples to copy')
  parser.add_argument('--dry-run', help='Prints out what script will copy but not do copy', action='store_true')
  args = parser.parse_args()
  print args

  with open(args.samples,'r') as samples:
    for sample in samples:
      if args.dry_run:
        print "Copying %s" % sample

if __name__ == '__main__':
  main()

