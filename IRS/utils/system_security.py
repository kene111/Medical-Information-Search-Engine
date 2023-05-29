class RequestSecurityChecks:
    """Request Security Checks performs security checks on the request data, making sure they confirm to the expected format.
        
    Attributes
    ----------
    request : dict
        Dictionary variable for the request data, originally set to None.

    expected_variable : str
        Holds the expected value of the filter if the dtype is a string.

    activity_tag : str
        Holds the string value 'activity'.

    dtype_expected_security_count : int
        Holds the expected value if all the values of the request data follow the expected format.

    system_request_keys : set
        Holds the values of the expected keys of the request data.
    
    Methods
    -------

    _check_request_keys
        Checks the keys of request data are the expected keys.

    _check_request_value_dtype
        Checks the data types of the values of the request data.

    _check_activity_filter
        Renames the activity filter if present.

    set_request
        Sets the request data to the class request variable.

    run_request_secruity_check
        Runs the process of performing security checks on the request data.
    """

    def __init__(self):
        self.request = None
        self.expected_variable = "all"
        self.activity_tag = "activity"
        self.dtype_expected_security_count = 3
        self.system_request_keys = set(["query","filters","n_results"])

    def set_request(self, request):
        """Sets the request data to the class request variable
        
        Parameters
        ----------
        request: dict
            dictionary contain the request data information

        Returns
        -------
        """
        self.request = request

    def _check_request_keys(self):
        """Checks the keys of request data are the expected keys.
        
        Parameters
        ----------

        Returns
        -------
        bool
            if true the keys follow the expected format, else the keys do not follow the expected format.
        """

        for request_key in self.request.keys():
            if request_key not in self.system_request_keys:
                return False
        return True

    def _check_request_value_dtype(self):
        """Checks the data types of the values of the request data.
        
        Parameters
        ----------

        Returns
        -------
        bool
            if true the values follow the expected format, else the values do notfollow the expected format.
        """
        count = 0
        for key in self.system_request_keys:
            if key == "query":
                if type(self.request[key]) == str:
                    count += 1
            if key == "filters":
                if type(self.request[key]) == list:
                    temp_count = 0
                    for val in self.request[key]:
                        if type(val) == str:
                            temp_count += 1
                    avg_temp_count = temp_count / len(self.request[key]) # if they are all strings the average should be 1
                    count += avg_temp_count
                elif type(self.request[key] == str):
                    if self.request[key] == self.expected_variable:
                        count += 1
            
            if key == "n_results":
                if type(self.request[key]) == int:
                    count += 1

        if count != self.dtype_expected_security_count:
            return False
        return True

    def _check_activity_filter(self):
        """Renames the activity filter if present"""
        if self.request["filters"] == self.expected_variable:
            return None
        else:
            if self.activity_tag in self.request["filters"]:
                self.request["filters"] = list(map(lambda x: x.replace(self.activity_tag, "activity(%)"), self.request["filters"]))
        return None

    def return_passed_request(self):
        """Returns the passed request data"""
        return self.request

    def run_request_secruity_check(self):
        """Runs the process of performing security checks on the request data.
        
        Parameters
        ----------

        Returns
        -------
        bool
            if true the request data is good, else something is wrong with the request data.
        """
        if self._check_request_keys():
            if self._check_request_value_dtype():
                self._check_activity_filter() # checks if the activity filter is present and renames it.
                return True
        return False










    
