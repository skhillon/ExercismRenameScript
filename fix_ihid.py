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

# Tests I used.
# assert pascal_to_snake('Rookie') == 'rookie'
# assert pascal_to_snake('FirstSubmission') == 'first_submission'
# assert pascal_to_snake('XyZ') == 'xy_z'
# assert pascal_to_snake('Ab::Cd') == 'ab/cd'


def capitalize_after_colons(s: str, substitution: str) -> str:
  """
  Checks if substitutions happened right after a `::`.
  If so, uppercases first character of each substitution.
  """
  substitution_indices = [match.start() for match in re.finditer(substitution, s)]
  indices_to_uppercase = list()

  # Find indices to uppercase so we only construct a new string one time.
  for index in substitution_indices:
    if index < 2:
      continue  # There's no way for a `::` to exist.

    if s[index - 2:index] == '::':
      indices_to_uppercase.append(index)

  # Construct final string.
  components = list()
  slice_start = 0
  for index in indices_to_uppercase:
    components.append(s[slice_start:index])  # Substring up to this point.
    components.append(s[index].upper())  # Capitalized letter.
    slice_start = index + 1

  components.append(s[slice_start:])  # Everything after last substitution.
  return ''.join(components)


# Tests I used.
# assert capitalize_after_colons(
#   'assert_equal Badges::rookieBadge, user_badge.class',
#   'rookie'
# ) == 'assert_equal Badges::RookieBadge, user_badge.class'

# assert capitalize_after_colons(
#   "factory :badge, class: 'Badges::rookieBadge' do",
#   'rookie'
# ) == "factory :badge, class: 'Badges::RookieBadge' do"

# assert capitalize_after_colons(
#   ':rookieBadge',
#   'rookie'
# ) == ':rookieBadge'

# assert capitalize_after_colons(
#   "factory :badge, class: 'Badges::rookieBadge' do Things::rookieThing again Again::rookiePerson",
#   'rookie'
# ) == "factory :badge, class: 'Badges::RookieBadge' do Things::RookieThing again Again::RookiePerson"

# Main functionality
substitution = pascal_to_snake(after)
snake_before = pascal_to_snake(before)

# Help from https://stackoverflow.com/a/2578059/3131790
for path, dirs, files in os.walk(directory):
  for filename in files:
    fullpath = os.path.join(path, filename)

    with open(fullpath) as f:
      sub_result = re.sub(rf'{before}|{snake_before}', substitution, f.read(), 0, re.MULTILINE)
      if not sub_result:
        print(f'Failed to convert file at path {fullpath}', file=sys.stderr)
        continue

      sub_result = capitalize_after_colons(sub_result, substitution)

    with open(fullpath, 'w') as f:
      f.write(sub_result)
