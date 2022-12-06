def prefix_aggregation(rib_file):
    # Create a dictionary to store the prefixes
    prefixes = {}

    # Open the RIB file
    with open(rib_file, "r") as f:
        # Read each line in the file
        for line in f:
            # Split the line by whitespace
            fields = line.split()

            # Extract the prefix and next hop from the fields
            prefix = fields[0]
            next_hop = fields[1]

            # Check if the prefix is already in the dictionary
            if prefix in prefixes:
                # If it is, check if the next hop is different
                if prefixes[prefix] != next_hop:
                    # If it is different, set the prefix to "*" to indicate aggregation
                    prefixes[prefix] = "*"
            else:
                # If the prefix is not in the dictionary, add it with the next hop as the value
                prefixes[prefix] = next_hop

    # Return the prefixes dictionary
    return prefixes


#To use this function, you would call it like this:
aggregated_prefixes = prefix_aggregation("rib.txt")

'''
where rib.txt is the name of your RIB file. 
The function will return a dictionary where the keys are the prefixes and the values 
are the next hop for the prefix (or "*" if the prefix has been aggregated).
'''
