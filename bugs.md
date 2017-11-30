Known bugs:
30/11/2017, BUG00002
            Currently module name and module variable checks in connectivity matrix on simulation
            initialisation is not complete, currently only the module name in the dictionary key 
            is being checked.
23/11/2017, Nothing on pylator directly that I know off.
10/08/2017, BUG00001
            Reading matrix sheet from excel, fails if an entry has been made within the row 
            containing the index names. pandas can not infer the names of the index columns.