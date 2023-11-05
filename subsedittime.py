import pysubs2
path = 'D:/TEST/NINJA/04/1.ass'
pysubs2.load(path)

subtitles = pysubs2.load(path)
for sub in subtitles.events:
    sub.end = sub.end - 100

subtitles.save(path)