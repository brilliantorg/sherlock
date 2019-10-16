#!/usr/local/bin/python3
# coding=utf-8
import os

# Concatenate all the files in stores/ and noves/ into one big
# text corpus, split up books into chapters


if not os.path.isdir('assets'):
    os.mkdir('assets')

out = open('assets/sherlock.txt', 'w+')
print('Chapter/story listing')
print('---------------')

# First, add all the short stories
# Their file names are set so that alphabetical
# ordering is the publication ordering
for file in sorted(os.listdir('stories')):
  if file.endswith('.txt'):
    with open('stories/' + file) as f:
      title = f.readline().strip()
      print(title)
      out.write('\n' + '#'*80 + '\n')
      out.write(title)
      out.write('\n' + '#'*80 + '\n')
      for line in f.readlines():
        out.write(line)

# Second, add all the chapters of novels 
# as individual documents.
for file in sorted(os.listdir('novels')):
  if file.endswith('.txt'):
    with open('novels/' + file) as f:
      title = f.readline().strip()
      part = ''
      for line in f.readlines():
        if line.startswith('PART'):
          part = ', Part ' + line[5]
        elif line.startswith('Chapter'):
          chapterline = line.split('--')
          chapter = chapterline[1].strip()
          chapternum = chapterline[0].split(' ')[1]

          # NB: The "chapter" bit was removed from the chapter title
          # because the extremely long titles it generated were causing
          # height overflow issues in the app
          chapter_title = title + part + ', Chapter ' + chapternum # + ': ' + chapter
          print(chapter_title)
          out.write('\n' + '#'*80 + '\n')
          out.write(chapter_title)
          out.write('\n' + '#'*80 + '\n')
        else:
          out.write(line)
