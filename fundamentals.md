You use aggregates in order to minimize the size of routing tables. Aggregation is the process that combines the characteristics of several different routes in such a way that advertisement of a single route is possible.



With the as-set argument, the path information in the BGP table for the aggregate route includes a set (AS1, AS2) that  indicates that the aggregate actually summarizes routes that have passed through AS-1 and AS-2.

Benefit :  The avoidance of routing loops because the information records where the route has been.

In any closed network, this aggregate information propagates through BGP and back to one of the ASs that the as-set lists.
This propagation creates the possibility of a loop. The loop detection behavior of BGP notes its own AS number in the as-set of the aggregate update and drops the aggregate. This action prevents a loop.

OVERALL
The as-set argument contains information about each individual route that the aggregate summarizes.
Changes in the individual route cause an update of the aggregate : If AS-2 goes down, the aggregate is updated from AS-0 {AS-1,AS-2} to AS-0 {AS-1}.



One of the main enhancements of BGP4 over BGP3 is classless interdomain routing (CIDR). CIDR or supernetting is a new way to look at IP addresses.

With CIDR, there is no notion of classes, such as class A, B, or C
 For example, network 192.213.0.0 was once an illegal class C network. Now, the network is a legal supernet, 192.213.0.0/16.
 The "16" represents the number of bits in the subnet mask, when you count from the far left of the IP address. This representation is similar to 192.213.0.0 255.255.0.0.
 
 
# Two ways to confugure Preffix Aggregation 

-- Auto - summaries : easier to implement, to configure but with a lot restrictions
- it only summarises route that is class full summarised routes (network boundary)  : looking at the first octet (/8 , /16, 24)
- only summarises routes that are within your own iBGP learned routes, not BGP learned ones
- ave the network command of a classful route that you want it to advertise
- does work only for ipv4 , not ipv6 (does not have such a thing like classful route)

# aggregate-address 22.22.222.0 255.255.255.0 summary-only
 - Just specifies the aggregated prefix , while hiding the more specific ones
 - gives a clue to let the neighbour know that the prefix is from an aggregate operation : a.k.a "atomic-aggregate"
 - adding "as-set" : adds a set of autonomous systems that were suppressed/ that belong to the specific routes in no particular order  => 55 {27 200 7 100} ==> it simply used for loop prevention (not for as-path selection nor best path determination)
 - no need for atomic-aggregate path attribute anymore (it just says this path has been aggreagated)
 - As- set will not show up in a non-summarised route 


 # stability checkings

 In BGP routing, the stability of aggregated routes versus more specific routes can be studied by comparing the attributes of the two types of routes. Aggregated routes are routes that cover a larger range of IP addresses, while more specific routes cover a smaller range of IP addresses. 
 
 One way to study the stability of these routes is to 
 - compare their attributes, such as their AS path length, the number of times the routes have been withdrawn, and their origin. By comparing these attributes, you can get an idea of which type of route is more stable and therefore more likely to be used by BGP routers.

 - monitor the performance of the routes over time. This can be done by collecting data on the routes, such as the number of times they are used, the amount of traffic they carry, and the amount of time they remain in the BGP routing table. By analyzing this data, you can get an idea of which type of route is more stable and reliable


# WHAT CAN THE STUDY TELL US ABOUT DATA ENGINEERING

The analysis of the stability of aggregated routes versus more specific routes can provide valuable information for traffic engineering. 
By understanding which type of route is more stable and reliable,

-  traffic engineers can make more informed decisions about how to route traffic on a network. For example, if aggregated routes are found to be more stable, traffic engineers may choose to use them more often in order to improve the overall performance of the network. 

- On the other hand, if more specific routes are found to be more stable, traffic engineers may choose to use them more often in order to provide more granular control over traffic routing. 

- Ultimately, the analysis of route stability can help traffic engineers to better understand the behavior of BGP routing and make more effective decisions about how to manage traffic on a network.

# ALGORITHM FOR FINDIND PREFIX AGGREGATION

- bgpkit
 - call the parse and apply its arguments : URL of the MRT file, and filters in dictionary { BGP router's IP of choice and its prefix , and more}

 - access its elements
 - for each element  :
    - check if the 'atomic' = 'AG'
        - if yes :
                - add the element to AGGREGATED_JSON object

                ext install gencay.vscode-chatgpt