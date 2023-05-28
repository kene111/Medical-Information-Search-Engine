import os
import re
import nltk
import string
import pickle
stopwords_lst = nltk.corpus.stopwords.words('english')

class QueryEmbedder:
    """Query handler class handles cleaning and embedding the query.
        
    Attributes
    ----------
    cache : str
        Dictionary variable for the request data, originally set to None.

    embedder_tag : str
        Holds the Query Embedder class

    embedder : Embedding Array
        contains the embedding array
    
    Methods
    -------

    _emed_query
        embedds the query.

    _load_embedder
        loads the serialized embedding object from storage.

    _preprocess_query
        prepares query for embedding.

    prepare_query
        runs the entire process of embedding the query.
    """

    def __init__(self):
        self.cache = "pre_trained_storage"
        self.embedder_tag = "pre-trained_embedder.pkl"
        self.embedder = self._load_embedder()

    def _preprocess_query(self, query):
        """Sets the requests data to temp_data. 
        
        Parameters
        ----------
        api_request: dict
            this is the request data
        Returns
        -------
        """
        qry = ' '.join([word for word in query.split() if word not in (stopwords_lst)])
        qry = re.sub('[%s]' % re.escape(string.punctuation), ' ' , qry)
        qry = qry.lower()
        return qry

    def _load_embedder(self):
        """Load the serialized embedding object from the storage path
        
        Parameters
        ----------
        
        Returns
        -------
        embedder: np.array 
            embedding array
        """
        path = os.path.join(self.cache,self.embedder_tag)
        with open(path, "rb") as f:
            embedder = pickle.load(f)
        return embedder["pre_trained_embedder"]

    def _emed_query(self, cleaned_query):
        """Converts the query string to an embedding.
        
        Parameters
        ----------
        cleaned_query: str
            pre-processed query.
        Returns
        -------
        query_embedding: array ** confirm **
            embedding representation of the query.
        """
        query_embedding = self.embedder.encode(cleaned_query)
        return query_embedding

    def prepare_query(self, query):
        """Runs the process of preparing cleaning and embedding the query
        
        Parameters
        ----------
        query: str
            contains the question from the request.
        
        Returns
        -------
        embedded_query: array ** confirm **
            embedding representation of the query.
        """
        query = self._preprocess_query(query)
        embedded_query = self._emed_query(query)
        return embedded_query