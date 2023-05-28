import os
import pickle
from sentence_transformers import SentenceTransformer, util


class SemanticLogic:

    """SemanticLogic class handles querying the embeddins and returning n results.
        
    Attributes
    ----------
    cache : str
        Dictionary variable for the request data, originally set to None.

    embeddings_tag : str
        Holds the Query Embedder class

    embeddings_store : np.array
        contains the embedding array
    
    Methods
    -------

    _load_embeddings
        loads the serialized embedding object from storage.

    _search_embeddins
        prepares query for embedding.

    get_n_results
        runs the entire process of embedding the query.
    """

    def __init__(self):
        self.cache = "pre_trained_storage"
        self.embeddings_tag = "pre-trained_embedder.pkl"
        self.embeddings_store = self._load_embeddings()

    def _load_embeddings(self):

        """Load the serialized embedding object from the storage path

        Parameters
        ----------

        Returns
        -------
        embeddings: np.array
            embedding array
        """
        path = os.path.join(self.cache,self.embeddings_tag)
        with open(path, "rb") as f:
            embedding = pickle.load(f)
        return embedding["pre_trained_embeddings"]

    def _search_embeddings(self, embedded_query):
        """Search the embedding storage for the most similar embeddings to the embedded_query.

        Parameters
        ----------
        embedded_query : np.array
            the embedding representation of the query string.

        Returns
        -------
        resp: List
            contains the results from the semantic search.
        """
        resp = util.semantic_search(embedded_query, self.embeddings_store)
        resp = resp[0]
        return resp

    
    def get_n_results(self, embedded_query, n=1):
        """Gets n results from the results of the semantic search.

        Parameters
        ----------
        embedded_query : np.array
            the embedding representation of the query string.

        n : int 
            the number of results to return to the user, Default: 1

        Returns
        -------
        n_results: List
            contains the n number of results from the semantic search.
        """
        results = self._search_embeddings(embedded_query)
        n_results = results[:n]
        return n_results


