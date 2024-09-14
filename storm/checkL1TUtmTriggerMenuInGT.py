import CondCore.Utilities.conddblib as conddb
from Configuration.AlCa.autoCond import autoCond

# Connect to the pro database
con = conddb.connect(url=conddb.make_url("pro"))
session = con.session()

# Define the database types we will query
GTMAP = session.get_dbtype(conddb.GlobalTagMap)

# Loop over each global tag in autoCond
for key, global_tag in autoCond.items():
    # If the global tag is a tuple, handle it appropriately
    if isinstance(global_tag, tuple):
        # Check if 'L1GtTriggerMenuRcd' appears in the second element of the tuple
        if "L1TUtmTriggerMenuRcd" in global_tag[1]:
            # Extract information directly from the second element of the tuple
            #print(f"Processing GlobalTag tuple: {global_tag[0]} (custom L1TUtmTriggerMenuRcd entry found)")

            # Print the relevant part containing the L1TUtmTriggerMenuRcd directly
            #print(f"Custom entry: {global_tag[1]}")

            # You can split the second element and print details if necessary
            parts = global_tag[1].split(',')
            if len(parts) >= 2:
                record = parts[1]
                tag_name = parts[0]
                print(f"key: {key} GlobalTag: custom Record: {record}, Tag: {tag_name}")
        else:
            # Otherwise, treat it as a regular GT by using the first element
            global_tag = global_tag[0]
    
    if isinstance(global_tag, str):
        #print(f"Processing GlobalTag: {global_tag}")

        # Query the GlobalTagMap table for the selected Global Tag
        GTMap_ref = session.query(GTMAP.record, GTMAP.label, GTMAP.tag_name).\
            filter(GTMAP.global_tag_name == global_tag).\
            order_by(GTMAP.record, GTMAP.label).\
            all()

        # Loop over the results and print the record, label, and tag if the record matches 'L1TUtmTriggerMenuRcd'
        for element in GTMap_ref:
            record = element[0]
            label = element[1]
            tag_name = element[2]

            if record == "L1TUtmTriggerMenuRcd":
                print(f"key: {key} GlobalTag: {global_tag} | Record: {record}, Label: {label}, Tag: {tag_name}")
