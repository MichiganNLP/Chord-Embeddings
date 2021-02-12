import pickle

enharmonics = {'A#': 'Bb', 'A#7': 'Bb7', 'A#m7': 'Bbm7', 'A#m': 'Bbm', 'Bb': 'A#', 'Bb7': 'A#7', 'Bbm7': 'A#m7', 'Bbm': 'A#m', 'B#': 'Cb', 'B#7':'Cb7', 'B#m7': 'Cbm7', 'B#m': 'Cbm', 'Cb': 'B#', 'Cb7': 'B#7', 'Cbm7': 'B#m7', 'Cbm': 'B#m', 'C#': 'Db', 'C#7': 'Db7', 'C#m7': 'Dbm7', 'C#m': 'Dbm', 'Db': 'C#', 'Db7': 'C#7', 'Dbm7': 'C#m7', 'Dbm': 'C#m', 'D#': 'Eb', 'D#7': 'Eb7', 'D#m7': 'Ebm7', 'D#m': 'Ebm', 'Eb': 'D#', 'Eb7': 'D#7', 'Ebm7': 'D#m7', 'Ebm': 'D#m', 'E#': 'F', 'E#7': 'F7', 'E#m7': 'Fm7', 'E#m': 'Fm', 'F': 'E#', 'F7': 'E#7', 'Fm7': 'E#m7', 'Fm': 'E#m', 'F#': 'Gb', 'F#7': 'Gb7', 'F#m7': 'Gbm7', 'F#m': 'Gbm', 'Gb': 'F#', 'Gb7': 'F#7', 'Gbm7': 'F#m7', 'Gbm': 'F#m', 'G#':'Ab', 'Ab':'G#'}

pitch_idxs = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
solfege = {'do':[1, 5, 8, 0, 0], 'mi':[5, 8, 11, 0, 0], 're':[3, 6, 10, 0, 0], 'sol':[8, 12, 3, 0, 0], 'la':[10, 1, 5, 0, 0], 'lam':[10, 1, 5, 0, 0]}

major = [1, 5, 8]
minor = [1, 4, 8]
majmin7 = [1, 5, 8, 11]
min7 = [1, 4, 8, 11]
dim = [1, 4, 7]
aug = [1, 5, 9]
pitch_exceptions = {'FA#': 'F#'}
chord_exceptions = {'UNK': [0,0,0,0,0], 'C*': [1,5,8,13,0], 'G*': [8, 12, 3, 13, 0], 'Hm':[14,13,13,14,14], 'H':[14,14,14,14,14], 'A*': [10, 2, 5, 13, 0], 'D*':[2,7,10,13,0]}

def map_notes(rule, root):
	idx = get_pitch_idx(root)

	vec = [idx + c if c else 0 for c in rule]

	for i, item in enumerate(vec):
		if item > 12:
			new = item % 12
			vec[i] = new

	return vec 

def get_pitch_idx(note):
	if note in pitch_idxs:
		return pitch_idxs.index(note)
	elif note in enharmonics and enharmonics[note] in pitch_idxs:
		return pitch_idxs.index(enharmonics[note])
	elif note in pitch_exceptions:
		return get_pitch_idx(pitch_exceptions[note])
	return 'error, no idx for ' + note

def generate_vector(pitch_idxs):
	for i, p in enumerate(pitch_idxs):
		major_vec = map_notes(major, p)
		minor_vec = map_notes(minor, p)
		majmin7_vec = map_notes(majmin7, p)
		min7_vec = map_notes(min7, p)
		dim_vec = map_notes(dim, p)
		aug_vec = map_notes(aug, p)
		print("Pitch:\t{}\t| Major:\t{}\t| Minor:\t{}".format(p, major_vec, minor_vec))
	return

def load_vocab():
	with open('vocab.bin', "rb") as f:
		vocab = pickle.load(f)
	return vocab

def get_primary_rule(chord):
	major = [1, 5, 8, 0, 0]
	if chord in ['A', 'Ab', 'A#', 'B', 'Bb', 'B#', 'C', 'Cb', 'C#', 'D', 'Db', 'D#', 'E', 'Eb', 'E#', 'F', 'Fb', 'F#', 'G', 'Gb', 'G#'] or chord in ['AM', 'AbM', 'A#M', 'BM', 'BbM', 'B#M', 'CM', 'CbM', 'C#M', 'DM', 'DbM', 'D#M', 'EM', 'EbM', 'E#M', 'FM', 'FbM', 'F#M', 'GM', 'GbM', 'G#M'] or chord in ['Amaj', 'Abmaj', 'A#maj', 'Bmaj', 'Bbmaj', 'B#maj', 'Cmaj', 'Cbmaj', 'C#maj', 'Dmaj', 'Dbmaj', 'D#maj', 'Emaj', 'Ebmaj', 'E#maj', 'Fmaj', 'Fbmaj', 'F#maj', 'Gmaj', 'Gbmaj', 'G#maj']:
		return major
	minor = [1, 4, 8, 0, 0]
	if chord in ['Am', 'Abm', 'A#m', 'Bm', 'Bbm', 'B#m', 'Cm', 'Cbm', 'C#m', 'Dm', 'Dbm', 'D#m', 'Em', 'Ebm', 'E#m', 'Fm', 'Fbm', 'F#m', 'Gm', 'Gbm', 'G#m']:
		return minor
	majmin7 = [1, 5, 8, 11, 0]
	if chord in ['A7', 'Ab7', 'A#7', 'B7', 'Bb7', 'B#7', 'C7', 'Cb7', 'C#7', 'D7', 'Db7', 'D#7', 'E7', 'Eb7', 'E#7', 'F7', 'Fb7', 'F#7', 'G7', 'Gb7', 'G#7']:
		return majmin7
	maj7 = [1, 5, 8, 12, 0]	
	if chord in ['Amaj7', 'Abmaj7', 'A#maj7', 'Bmaj7', 'Bbmaj7', 'B#maj7', 'Cmaj7', 'Cbmaj7', 'C#maj7', 'Dmaj7', 'Dbmaj7', 'D#maj7', 'Emaj7', 'Ebmaj7', 'E#maj7', 'Fmaj7', 'Fbmaj7', 'F#maj7', 'Gmaj7', 'Gbmaj7', 'G#maj7'] or chord in ['AM7', 'AbM7', 'A#M7', 'BM7', 'BbM7', 'B#M7', 'CM7', 'CbM7', 'C#M7', 'DM7', 'DbM7', 'D#M7', 'EM7', 'EbM7', 'E#M7', 'FM7', 'FbM7', 'F#M7', 'GM7', 'GbM7', 'G#M7']:
		return maj7
	min7 = [1, 4, 8, 11, 0]		
	if chord in ['Am7', 'Abm7', 'A#m7', 'Bm7', 'Bbm7', 'B#m7', 'Cm7', 'Cbm7', 'C#m7', 'Dm7', 'Dbm7', 'D#m7', 'Em7', 'Ebm7', 'E#m7', 'Fm7', 'Fbm7', 'F#m7', 'Gm7', 'Gbm7', 'G#m7']:
		return min7
	dim = [1, 4, 7, 0, 0]	
	if chord in ['Adim', 'Abdim', 'A#dim', 'Bdim', 'Bbdim', 'B#dim', 'Cdim', 'Cbdim', 'C#dim', 'Ddim', 'Dbdim', 'D#dim', 'Edim', 'Ebdim', 'E#dim', 'Fdim', 'Fbdim', 'F#dim', 'Gdim', 'Gbdim', 'G#dim']:
		return dim

	aug = [1, 5, 9, 0, 0]
	if chord in ['Aaug', 'Abaug', 'A#aug', 'Baug', 'Bbaug', 'B#aug', 'Caug', 'Cbaug', 'C#aug', 'Daug', 'Dbaug', 'D#aug', 'Eaug', 'Ebaug', 'E#aug', 'Faug', 'Fbaug', 'F#aug', 'Gaug', 'Gbaug', 'G#aug'] or chord in ['A+', 'Ab+', 'A#+', 'B+', 'Bb+', 'B#+', 'C+', 'Cb+', 'C#+', 'D+', 'Db+', 'D#+', 'E+', 'Eb+', 'E#+', 'F+', 'Fb+', 'F#+', 'G+', 'Gb+', 'G#+']:
		return aug

	sus4 = [1, 6, 8, 0, 0]	
	if chord in ['Asus4', 'Absus4', 'A#sus4', 'Bsus4', 'Bbsus4', 'B#sus4', 'Csus4', 'Cbsus4', 'C#sus4', 'Dsus4', 'Dbsus4', 'D#sus4', 'Esus4', 'Ebsus4', 'E#sus4', 'Fsus4', 'Fbsus4', 'F#sus4', 'Gsus4', 'Gbsus4', 'G#sus4']:
		return sus4
	sus2 = [1, 3, 8, 0, 0]
	if chord in ['Asus2', 'Absus2', 'A#sus2', 'Bsus2', 'Bbsus2', 'B#sus2', 'Csus2', 'Cbsus2', 'C#sus2', 'Dsus2', 'Dbsus2', 'D#sus2', 'Esus2', 'Ebsus2', 'E#sus2', 'Fsus2', 'Fbsus2', 'F#sus2', 'Gsus2', 'Gbsus2', 'G#sus2']:
		return sus2
	
	# have secondary rule
	major_ = [1, 5, 8] # has secondary rule
	minor_ = [1, 4, 8] # has secondary rule
	majmin7_ = [1, 5, 8, 11]
	maj7_ = [1, 5, 8, 12]
	min7_ = [1, 4, 8, 11]
	dim_ = [1, 4, 7]
	aug_ = [1, 5, 9]

	sus4_ = [1, 6, 8]
	sus2_ = [1, 3, 8]

	chord = chord.split('/')[0]
	if chord in ['A', 'Ab', 'A#', 'B', 'Bb', 'B#', 'C', 'Cb', 'C#', 'D', 'Db', 'D#', 'E', 'Eb', 'E#', 'F', 'Fb', 'F#', 'G', 'Gb', 'G#'] or chord in ['AM', 'AbM', 'A#M', 'BM', 'BbM', 'B#M', 'CM', 'CbM', 'C#M', 'DM', 'DbM', 'D#M', 'EM', 'EbM', 'E#M', 'FM', 'FbM', 'F#M', 'GM', 'GbM', 'G#M'] or chord in ['Amaj', 'Abmaj', 'A#maj', 'Bmaj', 'Bbmaj', 'B#maj', 'Cmaj', 'Cbmaj', 'C#maj', 'Dmaj', 'Dbmaj', 'D#maj', 'Emaj', 'Ebmaj', 'E#maj', 'Fmaj', 'Fbmaj', 'F#maj', 'Gmaj', 'Gbmaj', 'G#maj']:
		return major_
	if chord in ['Am', 'Abm', 'A#m', 'Bm', 'Bbm', 'B#m', 'Cm', 'Cbm', 'C#m', 'Dm', 'Dbm', 'D#m', 'Em', 'Ebm', 'E#m', 'Fm', 'Fbm', 'F#m', 'Gm', 'Gbm', 'G#m']:
		return minor_
	if chord in ['A7', 'Ab7', 'A#7', 'B7', 'Bb7', 'B#7', 'C7', 'Cb7', 'C#7', 'D7', 'Db7', 'D#7', 'E7', 'Eb7', 'E#7', 'F7', 'Fb7', 'F#7', 'G7', 'Gb7', 'G#7']:
		return majmin7_
	if chord in ['Amaj7', 'Abmaj7', 'A#maj7', 'Bmaj7', 'Bbmaj7', 'B#maj7', 'Cmaj7', 'Cbmaj7', 'C#maj7', 'Dmaj7', 'Dbmaj7', 'D#maj7', 'Emaj7', 'Ebmaj7', 'E#maj7', 'Fmaj7', 'Fbmaj7', 'F#maj7', 'Gmaj7', 'Gbmaj7', 'G#maj7'] or chord in ['AM7', 'AbM7', 'A#M7', 'BM7', 'BbM7', 'B#M7', 'CM7', 'CbM7', 'C#M7', 'DM7', 'DbM7', 'D#M7', 'EM7', 'EbM7', 'E#M7', 'FM7', 'FbM7', 'F#M7', 'GM7', 'GbM7', 'G#M7']:
		return maj7_
	if chord in ['Am7', 'Abm7', 'A#m7', 'Bm7', 'Bbm7', 'B#m7', 'Cm7', 'Cbm7', 'C#m7', 'Dm7', 'Dbm7', 'D#m7', 'Em7', 'Ebm7', 'E#m7', 'Fm7', 'Fbm7', 'F#m7', 'Gm7', 'Gbm7', 'G#m7']:
		return min7_
	if chord in ['Adim', 'Abdim', 'A#dim', 'Bdim', 'Bbdim', 'B#dim', 'Cdim', 'Cbdim', 'C#dim', 'Ddim', 'Dbdim', 'D#dim', 'Edim', 'Ebdim', 'E#dim', 'Fdim', 'Fbdim', 'F#dim', 'Gdim', 'Gbdim', 'G#dim']:
		return dim_

	if chord in ['Aaug', 'Abaug', 'A#aug', 'Baug', 'Bbaug', 'B#aug', 'Caug', 'Cbaug', 'C#aug', 'Daug', 'Dbaug', 'D#aug', 'Eaug', 'Ebaug', 'E#aug', 'Faug', 'Fbaug', 'F#aug', 'Gaug', 'Gbaug', 'G#aug'] or chord in ['A+', 'Ab+', 'A#+', 'B+', 'Bb+', 'B#+', 'C+', 'Cb+', 'C#+', 'D+', 'Db+', 'D#+', 'E+', 'Eb+', 'E#+', 'F+', 'Fb+', 'F#+', 'G+', 'Gb+', 'G#+']:
		return aug_

	if chord in ['Asus4', 'Absus4', 'A#sus4', 'Bsus4', 'Bbsus4', 'B#sus4', 'Csus4', 'Cbsus4', 'C#sus4', 'Dsus4', 'Dbsus4', 'D#sus4', 'Esus4', 'Ebsus4', 'E#sus4', 'Fsus4', 'Fbsus4', 'F#sus4', 'Gsus4', 'Gbsus4', 'G#sus4']:
		return sus4_
	if chord in ['Asus2', 'Absus2', 'A#sus2', 'Bsus2', 'Bbsus2', 'B#sus2', 'Csus2', 'Cbsus2', 'C#sus2', 'Dsus2', 'Dbsus2', 'D#sus2', 'Esus2', 'Ebsus2', 'E#sus2', 'Fsus2', 'Fbsus2', 'F#sus2', 'Gsus2', 'Gbsus2', 'G#sus2']:
		return sus2_

	if chord in ['A7', 'Ab7', 'A#7', 'B7', 'Bb7', 'B#7', 'C7', 'Cb7', 'C#7', 'D7', 'Db7', 'D#7', 'E7', 'Eb7', 'E#7', 'F7', 'Fb7', 'F#7', 'G7', 'Gb7', 'G#7'] or chord.split('/')[0] in ['A7', 'Ab7', 'A#7', 'B7', 'Bb7', 'B#7', 'C7', 'Cb7', 'C#7', 'D7', 'Db7', 'D#7', 'E7', 'Eb7', 'E#7', 'F7', 'Fb7', 'F#7', 'G7', 'Gb7', 'G#7'] or chord.split('/')[0].replace('maj', '') in ['A7', 'Ab7', 'A#7', 'B7', 'Bb7', 'B#7', 'C7', 'Cb7', 'C#7', 'D7', 'Db7', 'D#7', 'E7', 'Eb7', 'E#7', 'F7', 'Fb7', 'F#7', 'G7', 'Gb7', 'G#7']:
		return majmin7_
	if 'sus4' in chord:
		return sus4
	if 'sus2' in chord:
		return sus2
	if 'sus' in chord:
		return sus4
	if 'm7' in chord:
		return min7_
	chord = ''.join([l for l in chord if l.isalpha()]).replace('add', '').replace('maj', '')
	if chord.lower() in solfege:
		return solfege[chord.lower()]


	if 'dim' in chord:
		return dim
	if 'aug' in chord:
		return aug
	if chord in ['Am', 'Abm', 'A#m', 'Bm', 'Bbm', 'B#m', 'Cm', 'Cbm', 'C#m', 'Dm', 'Dbm', 'D#m', 'Em', 'Ebm', 'E#m', 'Fm', 'Fbm', 'F#m', 'Gm', 'Gbm', 'G#m'] or chord.split('/')[0] in ['Am', 'Abm', 'A#m', 'Bm', 'Bbm', 'B#m', 'Cm', 'Cbm', 'C#m', 'Dm', 'Dbm', 'D#m', 'Em', 'Ebm', 'E#m', 'Fm', 'Fbm', 'F#m', 'Gm', 'Gbm', 'G#m']:
		return minor_

	if chord in ['A', 'Ab', 'A#', 'B', 'Bb', 'B#', 'C', 'Cb', 'C#', 'D', 'Db', 'D#', 'E', 'Eb', 'E#', 'F', 'Fb', 'F#', 'G', 'Gb', 'G#'] or chord in ['AM', 'AbM', 'A#M', 'BM', 'BbM', 'B#M', 'CM', 'CbM', 'C#M', 'DM', 'DbM', 'D#M', 'EM', 'EbM', 'E#M', 'FM', 'FbM', 'F#M', 'GM', 'GbM', 'G#M']:
		return major_

	else:
		# return 'no rule for ' + chord
		return [0,0,0,0]


def get_root(chord):
	roots = ''.join(['A', 'Ab', 'A#', 'B', 'Bb', 'B#', 'C', 'Cb', 'C#', 'D', 'Db', 'D#', 'E', 'Eb', 'E#', 'F', 'Fb', 'F#', 'G', 'Gb', 'G#'])

	root = ''.join([l for l in chord.split('/')[0] if l in roots])
	return root


def get_secondary_rule(chord, rule):
	if '/' in chord:
		# inversions
		base = chord.split('/')[1]
		base_pitch = get_pitch_idx(base) + 1
		if base_pitch == (get_pitch_idx(get_root(chord)) + 5) % 13:
			reg = map_notes(rule, get_root(chord))

			inversion = [base_pitch] + [reg[0]] + reg[2:]

		elif base_pitch == (get_pitch_idx(get_root(chord)) + 8) % 13:
			reg = map_notes(rule, get_root(chord))
			inversion = [base_pitch] + reg[:-1]
		else:
			inversion = [base_pitch] + map_notes(rule, get_root(chord))
		while len(inversion) < 5:
			inversion.append(0)
		return inversion
	if 'add' in chord:
		add = int(chord.split('add')[1]) % 7
		root = get_root(chord)
		base_pitch = get_pitch_idx(root)
		if add == 2:
			add_pitch = (base_pitch + 3) % 12
			added = map_notes(rule, get_root(chord)) + [add_pitch]
			while(len(added)) < 5:
				added.append(0)
			return added
		print("need implementation if case occurs")
		return []
	if len([l for l in chord if l.isnumeric()]) == 1: 
		root = get_root(chord)
		base_pitch = get_pitch_idx(root)
		add = int([l for l in chord if l.isnumeric()][0]) % 7
		if add == 2:
			add_pitch = (base_pitch + 3) % 12
			added = map_notes(rule, root) + [add_pitch]
			while(len(added)) < 5:
				added.append(0)
			return added
		if add == 3:
			print(chord)
			pitches = map_notes(rule, root)
			added = [pitches[1], pitches[0], pitches[2]]
			while(len(added)) < 5:
				added.append(0)
			return 
		if add == 4:
			add_pitch = (base_pitch + 6) % 12
			added = map_notes(rule, root) + [add_pitch]
			while(len(added)) < 5:
				added.append(0)
			return added
		if add == 5:
			pitches = map_notes(rule, root)
			added = [pitches[-1]] + pitches[:-1]
			while(len(added)) < 5:
				added.append(0)
			return [pitches[-1]] + pitches[:-1] + [0, 0]
		if add == 6:
			if rule == minor:
				add_pitch = (base_pitch + 9) % 12
			else:
				add_pitch = (base_pitch + 10) % 12
			added = map_notes(rule, root) + [add_pitch]
			while(len(added)) < 5:
				added.append(0)
			return added
		else:
			return []

	return []

	

chords = load_vocab()

representations = {}
for chord in chords:
	primary_rule = get_primary_rule(chord)
	if len(primary_rule) < 5:
		secondary_rule = get_secondary_rule(chord, primary_rule)
		if not secondary_rule:
			secondary_rule = chord_exceptions[chord] if chord in chord_exceptions else []

		if not secondary_rule:
			# no mapping for chord
			# print("no mapping for", chord)
			pass
		representations[chord] = secondary_rule
	elif chord.lower() in solfege:
			representations[chord] = primary_rule
	else:
		representations[chord] = map_notes(primary_rule, get_root(chord))

def normalize(vec, max, min):
	normalized = []
	for i in vec:
		z = (i-min)/(max-min)
		normalized.append(z)
	return normalized


normalized = {}
reps_no_norm = {}
for r in representations:
	if len(representations[r]) != 5:
		continue
	assert len(representations[r]) == 5
	n = normalize(representations[r], 14, 0)
	normalized[r] = n
	reps_no_norm[r] = representations[r]


import pandas as pd 

columns = ['chord'] + [i for i in range(5)]
normalized_df = {col:[] for col in columns}
for chord, vector in normalized.items():
	normalized_df['chord'].append(chord)
	for i, val in enumerate(vector): 
		normalized_df[i].append(val)

df = pd.DataFrame(normalized_df, columns=columns)
vecs = df.to_numpy()
with open('pr-norm.bin', 'wb') as f:
	pickle.dump(vecs, f)


columns = ['chord'] + [i for i in range(5)]
pitch_df = {col:[] for col in columns}
for chord, vector in reps_no_norm.items():
	pitch_df['chord'].append(chord)
	for i, val in enumerate(vector): 
		pitch_df[i].append(val)

df = pd.DataFrame(pitch_df, columns=columns)
vecs = df.to_numpy()
with open('pr.bin', 'wb') as f:
	pickle.dump(vecs, f)
df