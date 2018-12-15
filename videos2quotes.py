import os, sys, re, subprocess

accurate = False # if false: -ss and -to is before -i in the ffmpeg line (much faster). if True they're after -i (*much slower* but might be more accurate sometimes)
ffmpeg_options = '-map_metadata -1 -map 0:a:0 -map 0:v:0 -c:a aac -c:v libx264 -crf 21'

if len(sys.argv) != 3:
	print "usage: videos2quotes.py video.ext subtitle.srt"
	sys.exit(1)

if not os.path.isfile(sys.argv[1]):
	print "error: no file: " + sys.argv[1]
	sys.exit(1)

if not os.path.isfile(sys.argv[2]):
	print "error: no file: " + sys.argv[2]
	sys.exit(1)

# flip around srt and video if necessary
if sys.argv[1].lower().endswith('.srt'):
	subtitle = sys.argv[1]
	video = sys.argv[2]
elif sys.argv[2].lower().endswith('.srt'):
	subtitle = sys.argv[2]
	video = sys.argv[1]
else:
	print "error: none of these are .srt files?"
	sys.exit(1)

def get_valid_filename(s): # https://stackoverflow.com/a/46801075
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

prefix = get_valid_filename(video[:-4]) # strip extension
outputfolder = './' + prefix + '/'
if not os.path.exists(outputfolder):
	os.makedirs(outputfolder)

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