#!/usr/bin/python3
from os.path import isdir, join
from os import mkdir, listdir

if __name__ == "__main__":
	if not isdir("assets"):
		mkdir("assets")
	
	with open("assets/sherlock.txt", 'w+') as out:
		print("Chapter/story listing\n{'-':<16}")
		for method in ("stories", "novels"):
			function = globals()[method]
			for filename in sorted(listdir(method)):
				if filename.endswith(".txt"):
					with open(join(method, filename)) as in_:
						title = in_.readline().strip()
						function(title, in_, out)
						print(title)

def stories(title, in_, out):
	out.write(f"\n{'#':<80}\n{title}\n{'#':<80}\n")
	out.writelines(in_.readlines())

def novels(title, in_, out):
	part = str()
	for line in in_.readlines():
		if line.startswith("PART"):
			part = ", Part " + line[5]
		elif line.startswith("Chapter"):
			chapter_number = (line.split("--"))[0].split(" ")[1]
			chapter_title = title + part + ", Chapter " + chapter_number
			out.write(f"\n{'#':<80}\n{chapter_title}\n{'#':<80}\n")
		else:
			out.write(line)
