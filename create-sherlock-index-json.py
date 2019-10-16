# coding=utf-8
import json

with open('assets/sherlock.txt') as f:
  fulltext = f.read()

splits = fulltext.split("\n" + "#"*80 + "\n")
stories = []
while len(splits) > 1:
  text = splits.pop()
  title = splits.pop()
  stories.append((title, text))
stories.reverse()

fulltext_offset = 0
story_number = 0
story_index = []
word_index = {}

def add_token(chars, token_number, start_index, end_index):
  global story_number
  global word_index
  token = "".join(chars)
  if token not in word_index: word_index[token] = []
  word_index[token].append({
    "doc": story_number,
    "ndx": token_number,
    "pos": start_index,
    "len": end_index - start_index
  })
  return None

for (title, text) in stories:
  fulltext_offset += 82 * 2 + len(title)

  story_index.append({
    "name": title,
    "text": text,
  })

  start_index = None
  current_token = None
  index = 0
  token_number = 0
  while index < len(text):
    ch = text[index].lower()

    # Simplify accented characters
    if ch in 'àâ': ch = 'a'
    elif ch in 'èé': ch = 'e'
    elif ch in 'ï': ch = 'i'
    elif ch in 'ñ': ch = 'n'

    # Advancing-through-whitespace mode
    if current_token is None:
      if ch in '\r\n !"#&\'(),-./:;?[]':
        index += 1
      elif ch in '0123456789abcdefghijklmnopqrstuvwxyz':
        start_index = index
        current_token = [ch]
        index += 1
      else:
        print("ERROR: didn't anticipate " + ch)
        index += 1

    # Advancing-through-a-token mode
    else:
      if ch in '\r\n !"#&(),./:;?[]' or (ch in '-' and text[index+1] == '-'):
        add_token(current_token, token_number, start_index, index)
        start_index = None
        current_token = None
        index += 1
        token_number += 1
      elif ch in '0123456789abcdefghijklmnopqrstuvwxyz':
        current_token.append(ch)
        index += 1
      elif ch in "'-":
        index += 1
      else:
        print("ERROR: didn't anticipate " + ch)
        index += 1

  if current_token is not None:
    add_token(current_token, token_number, start_index, index)

  story_number += 1
  fulltext_offset += len(text)

with open('assets/sherlock-index.json', 'w+') as output:
  output.write(json.dumps({
    "texts": story_index,
    "index": word_index
  }))

print('Index created, %d distinct words' % len(word_index.keys()))