##############################################################
# Script name: librosa_features.py
# Function: extract audio features by librosa
# Author: Jiao Wenxiang
# Date: 2019-08-02
##############################################################

import os
import librosa as l
import numpy as np
from tqdm import tqdm
import pickle
import time


def audio_features(audio_path, frame_rate):
	x, sr = l.load(audio_path, sr=22050)
	n_fft = int(sr * frame_rate)
	hop_length = n_fft              # non-overlapping, hop_length = n_fft//2 if overlapping

	mfccs = l.feature.mfcc(x, sr=sr, hop_length=hop_length, n_fft=n_fft)
	mels = l.feature.melspectrogram(x, sr=sr, hop_length=hop_length, n_fft=n_fft)
	spcen = l.feature.spectral_centroid(x, sr=sr, hop_length=hop_length, n_fft=n_fft)

	mfccs_delta = l.feature.delta(mfccs)
	mels_delta = l.feature.delta(mels)
	spcen_delta = l.feature.delta(spcen)

	# default size: 298 x n_frames
	feature = np.concatenate([mfccs, mels, spcen, mfccs_delta, mels_delta, spcen_delta], axis=0)

	return feature.transpose()


def audios_features(audios_path, save_path, frame_rate=0.01):
	# audio_path: path to audios
	audio_names = os.listdir(audios_path)
	features = {}
	time.sleep(1)
	for audio_name in tqdm(audio_names, ncols=100, ascii=True):
		audio_feature = {}
		audio_path = os.path.join(audios_path, audio_name)
		feat = audio_features(audio_path, frame_rate=frame_rate)
		fps = round(1/frame_rate, 0)
		audio_feature['fps'] = fps
		audio_feature['librosa'] = feat
		audio_name_noext = audio_name.split('.')[0]
		features[audio_name_noext] = audio_feature
		#print("Process audio {} FPS {} shape {}".format(audio_name_noext, fps, feat.shape))

	with open(save_path, 'wb') as f:
		pickle.dump(features, f)


def main():
	audios_path = "./Audios"
	audios_features(audios_path, 'librosa_audio_features.pt')


if __name__ == '__main__':
	main()
