#!/usr/local/bin/python3
# coding=utf-8
# Copyright 2019 Brilliant Worldwide
import json

# Create search index from sherlock.txt

with open('assets/sherlock.txt') as f:
  fulltext = f.read()

# Split the single file back up into (title, text) pairs
splits = fulltext.split("\n" + "#"*80 + "\n")
stories = []
while len(splits) > 1:
  text = splits.pop()
  title = splits.pop()
  stories.append((title, text))
stories.reverse()

story_number = 0
story_index = []
word_index = {}

# Add a single word occurance (the token represented by chars) to the index 
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
  story_index.append({
    "name": title,
    "text": text,
  })

  # Bespoke tokenization
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

  # Make sure to get the token at the end of the file!
  if current_token is not None:
    add_token(current_token, token_number, start_index, index)

  story_number += 1

with open('assets/sherlock-index.json', 'w+') as output:
  output.write(json.dumps({
    "texts": story_index,
    "index": word_index
  }))

print('Index for %d documents created, %d distinct words' % (len(story_index), len(word_index.keys())))