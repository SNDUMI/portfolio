import ffmpeg
import os
import csv

def runBash(command):
    print(command)
    os.system(command)

f=open('avspeech_train.csv','r',encoding='utf-8')
rdr=csv.reader(f)

for line in rdr:

    id=line[0]
    start=float(line[1])
    end=float(line[2])

    if not(os.path.exists("/home/alticast1/avspeech-data/train/{0}_{1:f}-{2:f}.mp4".format(id,start,end))):
        continue

    n=0
    i=start
    while i+3<end:
        try:
            if not(os.path.isdir(id+"_"+str(n))):
                os.makedirs(os.path.join(id+"_"+str(n)))
            else:
                break;
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise
        command="ffmpeg -loglevel quiet -ss {0} -i /home/alticast1/avspeech-data/train/{1}_{2:f}-{3:f}.mp4 -to {4} -vf fps=25 {1}_{5}/{1}_{5}_%2d.png".format(n*3,id,start,end,3,n)
        runBash(command)

        command="ffmpeg -y -loglevel quiet -ss {0} -i /home/alticast1/avspeech-data/train/{1}_{2:f}-{3:f}.mp4 -to {4} -vn -ar 16000 -ac 1 -ab 192k -f wav {1}_{5}/{1}_{5}.wav".format(n*3,id,start,end,3,n)
        runBash(command)

        i=i+3
        n=n+1


