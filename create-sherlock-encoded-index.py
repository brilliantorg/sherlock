#!/usr/local/bin/python3
# coding=utf-8
import json

# Make a more compressed representation of the story index
# Replace all lists of { doc, len, pos, ndx } records with a number,
# the _offset_ where that list's data is stored, compressed, in the 
# data file. 

with open('assets/sherlock-index.json') as f:
    data = json.loads(f.read())

texts = data['texts'] # list of { text, name }
index = data['index'] # map from strings to lists of { doc, len, pos, ndx }

# This part is just analysis to make sure we're not screwing up too badly
hits = 0 # 33035 (16 bits)
doc_ = 0 # 101   (7 bits - use 8)
len_ = 0 # 28    (5 bits - use 6)
pos_ = 0 # 68050 (17 bits - use 18)
ndx_ = 0 # 12625 (14 bits - use 16)
for k in index.keys():
    ds = index[k]
    hits = max(hits, len(ds))
    for d in ds:
        doc_ = max(doc_, d['doc'])
        len_ = max(len_, d['len'])
        pos_ = max(pos_, d['pos'])
        ndx_ = max(ndx_, d['ndx'])

def check(field, max_size, bits):
    if max_size < 2**bits:
        print('%s max: %d (< %d, ok)' % (field, max_size, 2**bits))
    else:
        print('%s max: %d (>= %d)' % (field, max_size, 2**bits))
        print('ERROR. Nothing will work.')
        raise TypeError
check('match length', hits, 16)
check('doc', doc_, 8)
check('len', len_, 6)
check('pos', pos_, 18)
check('ndx', ndx_, 16)

keys = sorted([k for k in index.keys()])

output_bytes = []
ref_index = {}
for k in keys:
    # In the compressed index, the word maps to an offset into the output byte file
    ref_index[k] = len(output_bytes)
    locations = index[k]

    # TWO BYTES - number of matching locations
    # Followed by that many 7-byte records
    output_bytes.append(len(locations) >> 8)
    output_bytes.append(len(locations) & 0xFF)
    for loc in locations:
        # RECORD BYTE 1 - document number
        output_bytes.append(loc['doc'])

        # RECORD BYTE 2, 3, 4 - length (6 of 24 bytes) and document position offset (18 of 24 bytes) 
        output_bytes.append((loc['len'] << 2) | (loc['pos'] >> 16))
        output_bytes.append((loc['pos'] >> 8) & 0xFF)
        output_bytes.append(loc['pos'] & 0xFF)

        # RECORD BYTE 5, 6 - sequence number for this token in document
        output_bytes.append(loc['ndx'] >> 8)
        output_bytes.append(loc['ndx'] & 0xFF)
    
json_data = json.dumps({ 'texts': texts, 'index': ref_index })
print('JSON data: %d bytes uncompressed' % len(json_data))
with open('assets/sherlock-encoded-index.json', 'w') as f:
    f.write(json_data)

record_data = bytearray(output_bytes)
print('Record data: %d bytes uncompressed' % len(record_data))
with open('assets/sherlock-encoded-index.data', 'wb') as f:
    f.write(record_data)

    

