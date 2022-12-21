
import json
import time
import websocket
import sys

## update this with a unique identifier (after "client ="" )for the RIPE team
url = "wss://ris-live.ripe.net/v1/ws/?client=dieudonneishara@gmail.com"

asn = '37020'

aggregated_prefixes = {}
non_aggregated_prefixes = {}


#infinite loop, in which it tries to connect to the RIPE RIS-Live stream using the websocket library.
while True:
    ws = websocket.WebSocket() # WebSocket protocol to connect to the RIPE RIS-Live stream and process it
    try:
        ws.connect(url)
    # If the connection fails, the script will sleep for 30 seconds before attempting to reconnect    
    except websocket.WebSocketBadStatusException as e:
        print(e, "while calling connect()")
        time.sleep(30)
        continue

    # subscribe to all BGP Updates  and process the data received from the stream.
    ws.send(json.dumps({"type": "ris_subscribe", "data": {"type": "UPDATE", "path": asn}}))
    try:
        for data in ws:
            # get current time
            parsed = json.loads(data)
            #print(data)
            if parsed.get('type', None) == 'ris_error':
                print(data)
            if parsed.get('type', None) == 'ris_message':
                # print(parsed["type"], parsed["data"])
                parsed_data = parsed.get("data", None)
                announcements = parsed_data.get('announcements', None)
                withdrawls = parsed_data.get('withdrawls', None)
                try:
                    as_path = ' '.join(str(x) for x in parsed_data.get('path', None))
                except:
                    as_path = ''
                if announcements is not None:
                    print (f"Total BGP messages : {len(parsed_data.keys())}")
                    announcement_count = 0
                    for announcement in announcements:
                        prefix_list = announcement['prefixes']
                        prefix_length = len(announcement['prefixes'])
                        aggregated_prefix_count = {}
                        unaggregated_prefix_count = {}
                        #If the announcement contains multiple prefixes, it is an aggregated route
                        if prefix_length > 1:
                            print (f"Aggregation happening for {prefix_length} prefixes : {prefix_list} AS Path : {as_path}")
                            #check stability of route
                            for prefix in announcement['prefixes']:
                                aggregated_prefix_count[prefix] = aggregated_prefix_count.get(prefix, 0) + 1
                                # noisy_aspath[as_path] = noisy_aspath.get(as_path, 0) + 1
                            # Print the frequency of updates for each prefix
                            print("Aggregated prefixes:")
                            for prefix, count in aggregated_prefix_count.items():
                                print(f"{prefix}: {count} updates")

                        #If the announcement contains a single prefix, it is an unaggregated route       
                        else :
                            print (f"{prefix_length} prefix ==>{prefix_list} : No aggregation happening for AS Path {as_path}")
                            prefix = announcement['prefixes'][0]
                            unaggregated_prefix_count[prefix] = unaggregated_prefix_count.get(prefix, 0) + 1
                        
                            print("Unaggregated prefixes:")
                            for prefix, count in unaggregated_prefix_count.items():
                                print(f"{prefix}: {count} updates")
                        announcement_count += 1
                        print (f"==========Announcement : {announcent_count}===================")     

                if withdrawls is not None:
                    for announcement in withdrawls:
                        for prefix in announcement['prefixes']:
                            print(f"{prefix} Withdrawn")
#                            print("del|%s|%s" % (prefix, as_path))
                            # noisy_prefix[prefix] = noisy_prefix.get(prefix, 0) + 1
                            # noisy_aspath[as_path] = noisy_aspath.get(as_path, 0) + 1


    except websocket.WebSocketConnectionClosedException as e:
        print("Disconnected, sleeping for a few then reconnect", e)
        time.sleep(30)
    
    except ConnectionResetError as e:
        print("Disconnected, sleeping for a few then reconnect", e)
        time.sleep(30)
    except BrokenPipeError as e:
        print("Disconnected, sleeping for a few then reconnect", e)
        time.sleep(30)
    except websocket.WebSocketBadStatusException as e:
        print("Disconnected, sleeping for a few then reconnect", e)
        time.sleep(30)
    except websocket.WebSocketTimeoutException as e:
        print("Disconnected, sleeping for a few then reconnect", e)
        time.sleep(30)
    except KeyboardInterrupt:
        print("User stop requested")
        sys.exit()
    except Exception as e:
        print("some other error?", e)
        time.sleep(30)

# def check_prefix_aggregation(bgp_data):
#   announcements = bgp_data['data']['announcements']
#   for announcement in announcements:
#     if len(announcement['prefixes']) > 1:
#       return True
#   return False

# def assess_route_stability(bgp_data):
#   # Initialize empty dictionaries to store the frequency of updates for each prefix
#   aggregated_prefix_count = {}
#   unaggregated_prefix_count = {}

#   announcements = bgp_data['data']['announcements']
#   for announcement in announcements:
#     # If the announcement contains multiple prefixes, it is an aggregated route
#     if len(announcement['prefixes']) > 1:
#       for prefix in announcement['prefixes']:
#         aggregated_prefix_count[prefix] = aggregated_prefix_count.get(prefix, 0) + 1
#     # If the announcement contains a single prefix, it is an unaggregated route
#     else:
#       prefix = announcement['prefixes'][0]
#       unaggregated_prefix_count[prefix] = unaggregated_prefix_count.get(prefix, 0) + 1

#   # Print the frequency of updates for each prefix
#   print("Aggregated prefixes:")
#   for prefix, count in aggregated_prefix_count.items():
#     print(f"{prefix}: {count} updates")
#   print("Unaggregated prefixes:")
#   for prefix, count in unaggregated_prefix_count.items():
#     print(f"{prefix}: {count} updates")

