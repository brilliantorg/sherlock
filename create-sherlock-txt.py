#!/usr/local/bin/python3
# coding=utf-8

import os

"""
sed -i~ 's/[“”]/"/g' * && rm *~
sed -i~ "s/[’‘]/'/g" * && rm *~
"""

out = open('sherlock.txt', 'w+')

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

          fullname = title + part + ', Chapter ' + chapternum + ': ' + chapter
          print(fullname)
          out.write('\n' + '#'*80 + '\n')
          out.write(fullname)
          out.write('\n' + '#'*80 + '\n')
        else:
          out.write(line)
