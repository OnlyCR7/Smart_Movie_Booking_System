import gdown
import pickle
import io

# Google Drive links for the uploaded files
vec_url = 'https://drive.google.com/uc?id=1Vt-8TCKZ1_eew-3HfWKJZgtUcNLHNdb5'
sim_url = 'https://drive.google.com/uc?id=1wfLNeUyFfsag0za4UJ-QHpvJ15iYNs1O'

# Function to download and load a pickle file
def load_pickle_with_gdown(url):
    # Download the file to a temporary location
    temp_file = gdown.download(url, quiet=True)
    
    # Load the pickle object from the file
    with open(temp_file, 'rb') as f:
        return pickle.load(f)

# Load the vectorizer and similarity matrix
try:
    vectorizer = load_pickle_with_gdown(vec_url)
    print("Vectorizer loaded successfully.")

    similarity = load_pickle_with_gdown(sim_url)
    print("Similarity matrix loaded successfully.")

except Exception as e:
    print(e)
