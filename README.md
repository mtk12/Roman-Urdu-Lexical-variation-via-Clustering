# Roman-Urdu-Lexical-variation-via-Clustering
Research based project in which we built a model to discover Lexical Variations in Roman Urdu Informal Text using Python and Machine Learning

<h2>How to run:</h2>
To run the project only run main.py from command prompt
For modication change weights and Previous and Next Dict on UrduID and WordID

<h2>Folders Description:</h2>

Pre-Processed Files are in Processed_File folder

Clusters and Fscore is stored in Results folder

<h2>Files Description:</h2>

Processing.py contains the code for pre-processing of the data set

Similarity.py contains code for calculating similarity between two words that is phonetic,string, and contextual

UrduPhone.py contains code for calculating urduphone encoding of the words

Lex_C.py contains code for clustering

Evaluation.py contains code evaluating clustering performance against gold standard
