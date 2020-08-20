import numpy as np
import os
import pandas as pd
from subprocess import call
from librosa import load, stft

path='./facenet-test-2' 
#path='./data'

def LoadFolder():
    #load all folder name
   
    videoID_list = os.listdir(path)
    videoID_list = [videoID for videoID in videoID_list]
    wrong=[]
    for list in videoID_list:
        if not os.path.isfile(path+"/"+list+"/"+list+".wav"):
            wrong.append(list)
          ##  print(list)
    for w in wrong:
        videoID_list.remove(w)
    return videoID_list

videoID_list=LoadFolder()

sample_freq=16000
duration=3
speech_list1=[]
speech_list2=[]
n_speech = len(videoID_list)
print(n_speech)
NUM_MIX = 3
com_list=[]
i=0
while i < NUM_MIX:
    x=np.random.randint(0,n_speech)
    y=np.random.randint(0,n_speech)
    if x==y or [x,y] in com_list or [y,x] in com_list:
        continue
    com_list.append([x,y])
    i=i+1
cnt=0
for xy in com_list:
    if cnt%100==0:
        print(cnt,"/",len(com_list))
              
    x=xy[0]
    y=xy[1]
    
    
    #synthesis wav
    _speech1=path+"/"+videoID_list[x]+"/"+videoID_list[x]+".wav"
    _speech2=path+"/"+videoID_list[y]+"/"+videoID_list[y]+".wav"
    topath='./facenet_mix/test/wav/'+str(cnt)+".wav"
    
    cmd = 'ffmpeg -loglevel quiet -i {0} -i {1} -t 00:00:{2} -filter_complex amix=2 -ar {3} -ac 1 -y {4}'.format(_speech1, _speech2, "3", "16000", topath)
    call(cmd, shell=True)
    
    #load wavs
    audio_speech1, _ =load(_speech1, sr=16000)
    audio_speech2, _ =load(_speech2, sr=16000)
    audio_mix, _ =load(topath, sr=16000)
    
    # convert spectrograms
    spectrogram_speech1 = np.abs(stft(audio_speech1, n_fft = 512, hop_length = 160, win_length = 400, center = False))
    spectrogram_speech2 = np.abs(stft(audio_speech2, n_fft = 512, hop_length = 160, win_length = 400, center = False))
    spectrogram_mix = np.abs(stft(audio_mix, n_fft = 512, hop_length = 160, win_length = 400, center = False))
    spectrogram_speech = np.concatenate((spectrogram_speech1, spectrogram_speech2), axis=0)
        
    # scaling
    m = np.max(spectrogram_mix)
    spectrogram_mix /= m
    spectrogram_speech /= m
    
    todir = os.path.join("./facenet_mix/test/spec","{}.npz".format(str(cnt)))
    np.savez(todir, mix=spectrogram_mix, true=spectrogram_speech)

    todir = os.path.join("./facenet_mix/test/vis", "{}".format(str(cnt)))
    if not os.path.exists(todir):
        os.makedirs(todir)
    
    ### VISUAL STREAM ###
    _speech1 = _speech1.replace(".wav", ".csv")
    _speech2 = _speech2.replace(".wav", ".csv")
    cmd = 'cp {0} {1}'.format(_speech1, os.path.join(todir, "speech1.csv"))
    call(cmd, shell=True)
    cmd = 'cp {0} {1}'.format(_speech2, os.path.join(todir, "speech2.csv"))
    call(cmd, shell=True)
    cnt=cnt+1
    
