Summary of the approach
-----------------------

First, I read the three script arguments from sys.argv. Then, I read the percentile value from the percentile file.

After that, I start reading line by line from the input file and writing to the output file. For, each line I split by "|", 
and check that the all data is valid. If not valid, I go to the next line. If valid, I convert the amount to float, and extract the zip code and date from the strings.

Then I check for repeat donors using the repeat_donor_set based on the name and zipcode key. If the donor is in the set, it is a repeat donor and we proceeed. If not I skip the donor and add the donor the repeat_donor_set. If I have a repaet donor, I accumulate his contributions in a organization contributions dictionary with key recipent id, zip code, and date. To get the percentile, I maintain a sorted list of donations amounts, and get the percentile using the nearest rank method as described in wikipedia. 
