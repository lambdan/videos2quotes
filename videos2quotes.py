import os, sys, re, subprocess

if len(sys.argv) != 4:
	print "usage: videos2quotes.py name video.ext subtitle.srt"
	sys.exit(1)

prefix = sys.argv[1]

if not os.path.isfile(sys.argv[2]):
	print "error: no file: " + sys.argv[2]
	sys.exit(1)
else:
	video = sys.argv[2]

if not os.path.isfile(sys.argv[3]):
	print "error: no file: " + sys.argv[3]
	sys.exit(1)
else:
	subtitle = sys.argv[3]

accurate = False # if false: -ss and -to is before -i in the ffmpeg line (much faster). if True they're after -i (*much slower* but might be more accurate sometimes)
ffmpeg_options = '-map_metadata -1 -map 0:a:0 -map 0:v:0 -c:a aac -c:v libx264 -crf 21'

outputfolder = './' + prefix + '/'
if not os.path.exists(outputfolder):
	os.makedirs(outputfolder)

def get_valid_filename(s): # https://stackoverflow.com/a/46801075
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

with open(subtitle) as f:
	lines = f.read().splitlines()

i = 0
name =""
for line in lines:
	if line.isdigit():
		continue
	elif line == "":
		fn = prefix + '_' + '%05d' % i + '_' + name + '.mp4'
		fn = get_valid_filename(fn)
		outputvid = os.path.abspath(os.path.join(outputfolder, fn))
		try:
			if accurate:
				subprocess.call('ffmpeg -n -i "' + inputvid + '" -ss ' + start_time + ' -to ' + stop_time + ' ' + ffmpeg_options + ' "' + outputvid + '"', shell=True)
			else:
				subprocess.call('ffmpeg -n -ss ' + start_time + ' -to ' + stop_time + ' -i "' + inputvid + '" ' + ffmpeg_options + ' "' + outputvid + '"', shell=True)
		except:
			continue
		name = ""
		i+=1
	elif "-->" in line:
		start_time = line.split(" --> ")[0].replace(",", ".")
		stop_time = line.split(" --> ")[1].replace(",", ".")
		inputvid = os.path.abspath(video)
	else:
		name = name + " " + line