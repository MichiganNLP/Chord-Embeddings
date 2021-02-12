# Chord Embeddings: Analyzing What They Capture and Their Role for Next Chord Prediction and Artist Attribute Prediction

This repository contains resources from our Chord Embeddings paper from [Evo* 2021](https://arxiv.org/pdf/2102.02917.pdf).


## Introduction

Natural language processing methods have been applied in a variety of music studies, drawing the connection between music and language. We expand those approaches by 
investigating *chord embeddings*, which we apply in two case studies. First, we demonstrate that using chord embeddings in a next chord prediction task yields predictions that more closely match those by experienced musicians. Second, we show the potential benefits of using the representations in tasks related to musical stylometrics.

This release includes the set of annotations from the next chord selection task, the pitch representations and chord embeddings used for the analysis and case studies, and the code to generate the chord representations. 

## Annotations

The annotations are available at [Annotations/Annotations.csv](./Annotations/Annotations.csv).

The "Question" column contains first the expertise ratings followed by the chord progression samples the annotators were given. Following this column, there is a column for each participant's reponses. The annotators were allowed to provide up to three chords for their response. The chords they provided are separated by spaces and have an underscore if the annotator chose not to provide an additional chord option. 

**Example:** The table below shows a sample of [Annotations.csv](./Annotations/Annotations.csv). "Annotator 0" rated their expertise at 25. For the chord progression *Gm F7 Bb*, they supplied *Cm7* and *D7*, meaning they created progressions *Gm F7 Bb Cm7* and *Gm F7 Bb D7*. For the second, they created *E F#m A D Bm E F#7* and *E F#m A D Bm E D#7-Eb7*.

|    | Question               | Annotator 0   |
|---:|:-----------------------|:--------------|
|  0 | Expertise              | 25            |
|  1 | Gm F7 Bb               | Cm7 D7 _      |
|  2 | E F#m A D Bm E         | F#7 D#7-Eb7 _ |


## Representations available for use

The [ChordRepresentations](./ChordRepresentations/) directory contains representations used in the paper.


## Creating chord representations

The [Generate](./Generate/) directory contains code for creating chord embeddings and pitch representations.

### word2vec chord embeddings

The code for creating chord embeddings utilizes the [Gensim framework](https://radimrehurek.com/gensim/). We've provided our script for generating the embeddings in [chord2vec.py](./Generate/chord2vec.py). Guidance for using the script follows below.

**Requirements:**
```
gensim-3.8.3
```

**Usage:**
```
python chord2vec.py [-h] [-cv CHORDVOCAB] [-d DATA] [-o OUTPUT] [-cw CONTEXTWINDOW] [-dim EMBEDDINGDIM] [-m {cbow,sg}] [-w WORKERS] [-e EPOCHS] [-v]
```

**Arguments:**
| flags                                            | help                                                                                                    | default        |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------ | :------------- |
| -h, --help                                       | show this help message and exit                                                                         |                |
| -cv CHORDVOCAB, --chordvocab CHORDVOCAB          | Binarized file of the chord vocabulary list to use. The default are chords that appear in .1% of songs. | vocab.bin      |
| -d DATA, --data DATA                             | Binarized file of a list of chord progressions as space-separated strings.                              | data.bin       |
| -o OUTPUT, --output OUTPUT                       | Filepath at which to save the embeddings.                                                               | embeddings.bin |
| -cw CONTEXTWINDOW, --contextwindow CONTEXTWINDOW | Context window used in word2vec model.                                                                  | 5              |
| -dim EMBEDDINGDIM, --embeddingdim EMBEDDINGDIM   | Desired embedding size.                                                                                 | 200            |
| -m {cbow,sg}, --model {cbow,sg}                  | The word2vec model to use; cbow for continuous-bag-of-words or sg for skip-gram.                        | cbow           |
| -w WORKERS, --workers WORKERS                    | Number of worker threads to train the model.                                                            | 3              |
| -e EPOCHS, --epochs EPOCHS                       | Number of epochs.                                                                                       | 5              |
| -v, --verbose                                    | Use for verbose logging of the execution progress.                                                      |                |

### pitch representations

The script for generating the pitch representations with the procedure described in the paper is provided in [chord-pitches.py](./Generate/chord-pitches.py). 

Fuller documentation for the code is coming soon.

**Usage:**
```bash
python chord-pitches.py
```

## Citation

```bibtex
@inproceedings{lahnala2021chord,
    title={Chord Embeddings: Analyzing What They Capture and Their Role for Next Chord Prediction and Artist Attribute Prediction},
    author={Lahnala, Allison and Kambhatla, Gauri and Peng, Jiajun and Whitehead, Matthew and Minnehan, Gillian and Guldan, Eric and Kummerfeld, Jonathan K. and \c{C}amc{\i}, An{\i}l and Mihalcea, Rada},
    booktitle={International Conference on Computational Intelligence in Music, Sound, Art and Design},
    pages={},
    year={2021},
    organization={Springer}
}
```

## Acknowledgements

This material is based in part upon work supported by the Michigan Institute for Data Science, and by Girls Encoded and Google for sponsoring Jiajun Peng through the Explore Computer Science Research program. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the Michigan Institute for Data Science, Girls Encoded or Google.


