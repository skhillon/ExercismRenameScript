"""
@author Sarthak Khillon (github.com/skhillon)
"""
import os
import re
import sys

try:
  before = sys.argv[1]
  after = sys.argv[2]
  directory = sys.argv[3]
except IndexError:
  print('USAGE: python3 fix_ihid.py <before> <after> <directory>', file=sys.stderr)
  sys.exit(1)


# Mostly converts PascalCase to snake_case but doesn't handle `::`
# Taken from https://stackoverflow.com/a/1176023/3131790
name_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def pascal_to_snake(s: str) -> str:
  """Converts a string `s` in PascalCase to snake_case. See below for tests."""
  converted = name_pattern.sub('_', s).lower().replace('::', '/')

  # We end up with some '/_' so we remove the underscore.
  return converted.replace('/_', '/')


substitution = pascal_to_snake(after)

# Tests I used.
# assert pascal_to_snake('Rookie') == 'rookie'
# assert pascal_to_snake('FirstSubmission') == 'first_submission'
# assert pascal_to_snake('XyZ') == 'xy_z'
# assert pascal_to_snake('Ab::Cd') == 'ab/cd'

# Help from https://stackoverflow.com/a/2578059/3131790
for path, dirs, files in os.walk(directory):
  for filename in files:
    fullpath = os.path.join(path, filename)

    with open(fullpath) as f:
      sub_result = re.sub(rf'{before}|{pascal_to_snake(before)}', substitution, f.read(), 0, re.MULTILINE)
      if not sub_result:
        print(f'Failed to convert file at path {fullpath}', file=sys.stderr)
        continue

    with open(fullpath, 'w') as f:
      f.write(sub_result)
