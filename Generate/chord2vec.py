from gensim.models import Word2Vec
import sys, pickle
import argparse
from gensim.models.callbacks import CallbackAny2Vec
import time, datetime
from tqdm import tqdm


def main():

	parser = argparse.ArgumentParser(description="Create chord embeddings using Gensim's Word2Vec")
	parser.add_argument('-cv', '--chordvocab', type=str, default='./vocab.bin', help=' Binarized file of the chord vocabulary list to use. The default are chords that appear in .1%% of songs.')
	parser.add_argument('-d', '--data', type=str, default='./data.bin', help='Binarized file of a list of chord progressions as space-separated strings.')
	parser.add_argument('-o', '--output', type=str, default='./embeddings.bin', help='Filepath at which to save the embeddings.')
	parser.add_argument('-cw', '--contextwindow', type=int, default=5, help='context window used in word2vec model.')
	parser.add_argument('-dim', '--embeddingdim', type=int, default=200, help='desired embedding size.')
	parser.add_argument('-m', '--model', type=str, default='cbow',choices=['cbow','sg'], help='cbow for continuous-bag-of-words or sg for skip-gram.')
	parser.add_argument('-w', '--workers', type=int, default=3, help='Number of worker threads to train the model.')
	parser.add_argument('-e', '--epochs', type=int, default=5, help='Number of epochs.')
	parser.add_argument('-v', '--verbose', action='store_true', help="Logs progress through epochs.")
	args = parser.parse_args()

	'''
	0. Get setup from arguments
	'''
	vocab_file = args.chordvocab
	data_file = args.data
	output = args.output

	context_window = args.contextwindow 
	dim = args.embeddingdim 
	workers = args.workers
	MODELIDX = {'cbow':0, 'sg':1}
	model = MODELIDX[args.model] 
	epochs = args.epochs
	verbose = args.verbose
	info = Print(verbose=verbose)
	callbacks = [EpochLogger()] if verbose else []


	'''
	1. Load vocab.
	'''
	with open(vocab_file, "rb") as f:
		vocab = pickle.load(f)
	info.out("Vocab length: {}".format(len(vocab)))

	'''
	2. Load chord progressions.
	'''
	info.out("Loading chord progressions...")
	with open(data_file, "rb") as f:
		chord_progressions = pickle.load(f)

	'''
	3. Replace out-of-vocab chords with UNK.
	'''
	sentences = []
	for progression in tqdm(chord_progressions) if verbose else chord_progressions:
		chord_tokens = [chord if chord in vocab else 'UNK' for chord in progression.split()]
		sentences.append(chord_tokens)
	
	print("Creating chord embeddings...")
	info.out("Training model...")

	'''
	4. Train word2vec model.
	'''
	model = Word2Vec(sentences, window=context_window, size=dim, sg=model, iter=epochs, workers=workers, callbacks=callbacks)
	info.out("Done training model.")


	'''
	5. Save embeddings.
	'''
	info.out("Saving model to {}".format(output))
	model.wv.save(output)
	print("Execution complete.")


	return

class Print(object):
	def __init__(self, verbose=False):
		self.verbose = verbose
	def out(self, msg):
		if self.verbose:
			print(msg)



class EpochLogger(CallbackAny2Vec):
	'''Callback to log information about training'''
	'''
	ref: https://radimrehurek.com/gensim_3.8.3/models/callbacks.html
	'''
	def __init__(self):
		self.epoch = 1
		self.st = 0
		self.et = 0
	def on_epoch_begin(self, model):
		self.st = time.time()
		timestamp_st = datetime.datetime.fromtimestamp(self.st).strftime('%Y-%m-%d %H:%M:%S')
		print("{}: Beginning Epoch #{}...".format(timestamp_st, self.epoch))
	
	def on_epoch_end(self, model):
		self.et = time.time()
		timestamp_et = datetime.datetime.fromtimestamp(self.et).strftime('%Y-%m-%d %H:%M:%S')
		dur = self.et - self.st

		print("{}: Epoch #{} completed in {:.1f} seconds.".format(timestamp_et, self.epoch, dur))
		self.epoch += 1


if __name__ == "__main__":
	main()
