import sys
import math

# get the command line parameters
input_filename = sys.argv[1].strip()
percentile_filename = sys.argv[2].strip()
output_filename = sys.argv[3].strip()

# read the percentile value from the file
with open(percentile_filename) as percentile_file:
    percentile = float(percentile_file.read())

# start reading the input and writing to the output
with open(input_filename) as input_file, open(output_filename, 'w+') as output_file:
    # we need these data structures to keep track of repeat donors and contributions
    repeat_donor_set = set()
    contributions = {}

    for line in input_file:
        # load data, count donor
        parts = line.strip().split("|")

        # extract the relevant data
        cmte_id = parts[0].strip()
        name = parts[7].strip()
        zip_code = parts[10].strip()
        transation_dt = parts[13].strip()
        transation_atm = parts[14].strip()
        other_id = parts[15].strip()

        # skip bad records
        if cmte_id == "" or name == "" or len(zip_code) < 5 or \
            len(transation_dt) < 4 or transation_atm == "" or other_id != "":
            continue

        # clean up the data
        transation_atm = float(transation_atm)
        zip_code = zip_code[:5] if len(zip_code) > 5 else zip_code
        transation_dt = transation_dt[-4:] if len(transation_dt) > 4 else transation_dt

        # check for repeat donors
        donor_key = (name, zip_code)

        if donor_key not in repeat_donor_set:
            # not a repeat donor
            repeat_donor_set.add(donor_key)
            continue

        # we keep track of contributions by key from recipient id, zip code, and date
        contribution_key = (cmte_id, zip_code, transation_dt)

        if contribution_key in contributions:
            # if it's existing contribution add the total ammount, and update the list of amounts recieved
            contribution = contributions[contribution_key]
            contribution['total_amount'] += transation_atm
            contribution['amounts'].append(transation_atm)
            # we need to sort to calculate the percentile
            contribution['amounts'].sort()
        else:
            contributions[contribution_key] = {'total_amount': transation_atm,
                                               'amounts': [transation_atm]}
            contribution = contributions[contribution_key]

        # nearest percentile calculation using the formulat from wikipedia
        percentile_rank = int(math.ceil((percentile / 100.0) * len(contribution['amounts'])))

        # output to the file
        output_file.write("{}|{}|{}|{:d}|{:d}|{:d}\n".format(
            cmte_id,
            zip_code,
            transation_dt,
            int(round(contribution['amounts'][percentile_rank - 1])),
            int(round(contribution['total_amount'])),
            len(contribution['amounts'])))
