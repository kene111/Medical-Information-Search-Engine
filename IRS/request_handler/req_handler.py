from utils.data_embedder import QueryEmbedder

class RequestHandler:
    """Request handler class handles getting, extracting, preparing and updating the variables of the request data.
        
    Attributes
    ----------
    temp_data : dict
        Dictionary variable for the request data, originally set to None.

    query_embedder : object
        Holds the Query Embedder class
    
    Methods
    -------
    _extract_info_from_request
        extract information from the request data.

    set_request
        set temp_data variable request data.

    prepare_request
        runs the process of extracting the data and embedding the data.
    """

    def __init__(self):
        self.temp_data = None
        self.query_embedder = QueryEmbedder()

    def set_request(self, api_request):
        """Sets the requests data to temp_data. 
        
        Parameters
        ----------
        api_request: dict
            this is the request data
        Returns
        -------
        """
        self.request = api_request

    def wrapper_results(self, embed_query, filters, n):
        temp_dict = {"embed_query":embed_query,
                    "filters":filters,
                    "n_results":n}
        return temp_dict


    def _extract_info_from_request(self):
        """Extracts the relevant keys fro the the requests data. 
        
        Parameters
        ----------
        
        Returns
        -------
        query : str
            this is a string containing the question asked.
        filters: list or str
            if str it contains the value "all", if this is a list containing certain fields used to query the Database

        n : int
            Number of results to return
        """
        query = self.request["query"]
        filters = self.request["filters"]
        n_results = self.request["n_results"]
        return query, filters, n_results

    def prepare_request(self):
        """Runs the process of preparing extracting the input from the request and preparing it for the system.
        
        Parameters
        ----------
        
        Returns
        -------
        wrapped_results : dict
            a dictionary containing the query, filters, n_results
        """
        query, filters, n_results = self._extract_info_from_request()
        embd_query = self.query_embedder.prepare_query(query)
        wrapped_results = self.wrapper_results(embd_query, filters, n_results)
        return wrapped_results

    



