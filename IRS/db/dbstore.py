import os
import pandas as pd
import pyarrow.parquet as pq

class DBStore:
    """DBStore class handles parsing and filtering through corpus data.
        
    Attributes
    ----------
    mssn_tag : str
        string containing the "MSSN" tag.

    dataset_location : str
        root directory location of the dataset in ".parquet" format.
    
    main_table_path : str
        path to the main dataframe containing the whole dataset.

    related_drug_table_path : str
        path to the related drugs dataframe containing the related_drug column and the related_drug_url column.

    information_store_path : str
        path to the information dataframe containing the drug_name column and the drug_information column.

    main_table : pandas dataframe 
        Dataframe containing the main data table.

    related_drug_table : pandas dataframe 
        Dataframe containing the related drug table. The related_drugs column serves as a foriegn key to the main table.

    information_table : pandas dataframe 
        Dataframe containing the related drug information table. The drug_name column serves as a foriegn key to the main table.

    all_features : list
        contains all the column names in the main dataframe.

    special_columns : list
        contains the special columns that need special transformations.
    
    Methods
    -------
    _get_drug_name:
        gets the drug name from the main table.

    _get_related_drugs_url:
        gets the urls of the related drugs from the related_drug_table.

    _special_filter_conditions:
        rearranges output for specific columns.

    _filter_conditons:
        performs filtering of the data based on certain conditions.

    _filter_main_table:
        filters through the main data table to get drug information.

    extract_drug_information:
    """

    def __init__(self):
        self.mssn_tag = "MSSN"
        self.dataset_location = "db/store"
        self.main_table_path = "db.parquet"
        self.related_drug_table_path = "related_db.parquet"
        self.information_store_path = "prod_feature_db.parquet"
        self.main_table = pd.read_parquet(os.path.join(self.dataset_location, self.main_table_path), engine='pyarrow') #running on pyarrow engine to interact with data in parquet format
        self.related_drug_table = pd.read_parquet(os.path.join(self.dataset_location, self.related_drug_table_path), engine='pyarrow')
        self.information_table = pd.read_parquet(os.path.join(self.dataset_location, self.information_store_path), engine='pyarrow')
        self.all_features = list(self.main_table.columns)
        self.special_columns = ["related_drugs","brand_names"]

    def _get_drug_name(self, result):
        """Get drug name from the main table.

        Parameters
        ----------
        result: list
            list of results provided from semantic search.

        Returns
        -------
        drug: str
            string containing the drug name.
        """
        drug_name = self.information_table._get_value(result['corpus_id'], 'drug_name')
        return drug_name

    def _get_related_drugs_url(self, related_drugs):
        """Get the urls of the related drugs.

        Parameters
        ----------
        related_drugs: str
            string containing the related drugs.

        Returns
        -------
        temp_related_drugs_list: list
            list of the related drug names.

        temp_dict: dict
            dictionary containing a mapping of the related drug names to their respective urls.
        """
        temp_dict = {}
        if related_drugs == self.mssn_tag:
            return related_drugs, self.mssn_tag
        temp_related_drugs_list = related_drugs.split(",")
        temp_related_drugs_list = [drug_name.strip() for drug_name in temp_related_drugs_list]
        for drug in temp_related_drugs_list:
            drug_url = self.related_drug_table[self.related_drug_table["related_drugs"] == f"{drug}"].iloc[0]["related_drugs_url"]
            temp_dict[drug] = drug_url
        return temp_related_drugs_list, temp_dict

    def _special_filter_conditions(self, filter, drug_filter_results, filter_dict):
        """Performs filtering and restructing for specific columns.

        Parameters
        ----------
        filter: str
            string containing the column name to filter.

        drug_filter_results: str
            string containing the results from filtering.

        filter_dict: dict
            dictionary to store filtering results.

        Returns
        -------
        filter_dict: dict
            dictionary containing updated results.
        """

        if filter == "related_drugs":
            related_drugs_list, related_drugs_url= self._get_related_drugs_url(drug_filter_results)
            filter_dict["related_drugs_url"]  = related_drugs_url
            filter_dict[filter] = related_drugs_list

        if filter == "brand_names":
            drug_filter_results = drug_filter_results.split(",")
            filter_dict[filter] = [brand_name.strip() for brand_name in drug_filter_results ]
        return filter_dict

    def _filter_conditons(self, filter, drug_filter_results, filter_dict):

        """Performs filtering based on defined conditions.

        Parameters
        ----------
        filter: str
            string containing the column name to filter.

        drug_filter_results: str
            string containing the results from filtering.

        filter_dict: dict
            dictionary to store filtering results.

        Returns
        -------
        filter_dict: dict
            dictionary containing updated results.
        """

        if filter in self.special_columns:
            filter_dict = self._special_filter_conditions(filter, drug_filter_results, filter_dict)
            return filter_dict

        filter_dict[filter] = drug_filter_results
        return filter_dict
        
    def _filter_main_table(self, filters, drug_name):
        """Filters the main table to get drug information.

        Parameters
        ----------
        filters: str or list
            if list, it contains the column names to filter. If filters ==  all, filters through all the columns.

        drug_name: str
            string containing the name of the drug.

        Returns
        -------
        filter_results: dict
            contains the results of the filtering for each drug.
        """
        temp_filter_dict = {}
        filter_results = []
    
        for filter in filters:
            if filter == "drug_name":
                continue
            drugname_filter_result = self.main_table[self.main_table["drug_name"] == f"{drug_name}"].iloc[0][filter]
            filter_dict = self._filter_conditons(filter, drugname_filter_result, temp_filter_dict)
        filter_results.append(filter_dict)
        return filter_results

    def extract_drug_information(self, results, filters):
        """Performs the entire process of filtering for results with the provided filters.

        Parameters
        ----------
        results: str
            dictionary to store filtering results.

        filters: str or list
            if list, it contains the column names to filter. If filters ==  all, filters through all the columns.

        Returns
        -------
        output_results: dict
            contains the results of the filtering for each drug.
        """

        output_results = {}

        for i, result in enumerate(results):
            output_result = {}
            drug_name = self._get_drug_name(result)
        
            if filters == "all":
                filters = self.all_features
                filter_result =  self._filter_main_table(filters, drug_name)
            else:
                filter_result =  self._filter_main_table(filters, drug_name)


            output_result["drug_name"] = drug_name
            output_result["filter_result"] = filter_result

            output_results[i] = output_result

        return output_results








