The Public Domain Works of Sherlock Holmes
==========================================

This repository contains all the public domain stories that Arthur Conan Doyle
wrote about the character Sherlock Holmes.

The text in the directories novels/ and stories/ is originally sourced from
Project Gutenberg, which is not affiliated with this repository in any way. 
The text has been changed to make it more regular and easy for text tools
to process uniformly.

The text in the novels/ and stories/ directory is for the use of anyone 
anywhere in the United States and most other parts of the world at no cost 
and with almost no restrictions whatsoever. You may copy it, give it away 
or re-use it under the terms of the Project Gutenberg License included with 
this eBook or online at www.gutenberg.org. If you are not located in the 
United States, you'll have to check the laws of the country where you are 
located.

The code in the root directory, which processes the text in the two folders, is
copyright Brilliant Worldwide, all rights reserved, etc.

Running the code
----------------

Merge the file fragments into one file, `./assets/sherlock.txt`

```
python3 create-sherlock-txt.py
```

Build index as a single JSON file, `./assets/sherlock-index.json`

```
python3 create-sherlock-index-json.py
```

Build a more efficient representation in two files: a regular json file `./assets/sherlock-encoded-index.json` and file of packed binary data  `./assets/sherlock-encoded-index.data`.

```
python3 create-sherlock-encoded-index.py
```