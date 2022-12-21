import bgpkit

# parser = bgpkit.Parser(url="https://spaces.bgpkit.org/parser/update-example",
#                        filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"})
# elems = parser.parse_all()
# assert len(elems) == 4227

aggregated_routes = dict()
print( "here")
def identifyAgg(mrtfileURL:str, filters_of_interest:dict()):
    parser = bgpkit.Parser(url =mrtfileURL, filters =filters_of_interest)
    elems = parser.parse_all()
    aggregated_summary =[]
    non_aggregations_summary =[]
    count =0
    for element in elems:
        print (element)
        if element ['atomic'] == 'AG': #and element['origin' =='EBGP']
            keys_to_consider = set(('peer_ip','peer_asn','prefix','as_path','origin_asns','aggr_asn','aggr_ip','elem_type'))
            aggregated_routes[element['aggr_asn']] = {k:v for k,v in element.items() if k in keys_to_consider}
            #aggregated_routes[element['aggr_asn']] = element
            aggregated_summary.append(aggregated_routes)
        elif ['atomic'] == 'NAG':
            keys_to_consider = set(('peer_ip','peer_asn','prefix','as_path','origin_asns','aggr_asn','aggr_ip','elem_type'))
            aggregated_routes[element['aggr_asn']] = {k:v for k,v in element.items() if k in keys_to_consider}
            #aggregated_routes[element['aggr_asn']] = element
            aggregated_summary.append(aggregated_routes)
            non_aggregations_summary.append(element)
    return aggregated_summary # list o dictionnaries where the keys are the aggregator ASNs

def check_stability(aggregated_prefix: dict(), non_aggregated_prefix: dict()) -> dict():
    
    return True          

if __name__ == '__main__':
    # print(identifyAgg('https://spaces.bgpkit.org/parser/update-example',
    # {"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"}))
    print(identifyAgg('https://spaces.bgpkit.org/parser/update-example',
    {"origin_asn": "37020", "prefix":" 41.222.196.0/22"}))

''' curl -s "https://ris-live.ripe.net/v1/stream/?format=json&client=cli-example-1" \
{"type":"UPDATE","data":'{host":"rrc01","type":"UPDATE","require":"announcements","path":"64496,64497$"}'
'''






