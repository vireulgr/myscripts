# example invocation: awk -f ~/parse_node_info.awk -v which=all -v what=id /opt/db_agent/db_agent.cfg 

BEGIN { 

    FS = "[: ]+";
# to sort associative array by index, treated as integer numbers, ascending
    PROCINFO["stored_in"] = "@ind_num_asc";
    max_node_id = 0;
}

NR == 1 { 
    which_opts = "all local remote master"
    what_opts = "ip id"
    if( index( which_opts, which ) == 0 || index( what_opts, what ) == 0 ) {
        print "which: " which_opts "; what: " what_opts;
    }
}

/^\s*node_id/ { local_id = $2; }
/^\s*cluster_nodes/ { Nodes[ $2 ] = $3; if( max_node_id < $2 ) max_node_id = $2; }

END { 
    if( !which ) which = "local";
    if( !what ) what = "ip";
    for( i=0; i<max_node_id; i++ ) {
        if( i in Nodes ) {
            master_id=i;
            break;
        }
    }
#print( "master: " master_id "; max_node_id:" max_node_id );
#master_id = "0";
#print( "which:", which, "what:",  what );
    if( which == "master" ) {
        if( what == "ip" ) print Nodes[ master_id ];
        if( what == "id" ) print master_id;
    }
    else if( which == "local" ) {
        if( what == "ip" ) print Nodes[ local_id ];
        if( what == "id" ) print local_id;
    }
    else if( which == "all" ) {
        if( what == "ip" ) {
            for( i in Nodes ) print Nodes[ i ];
        }
        if( what == "id" ) {
            i = 0;
            for( i in Nodes ) {
                if( Nodes[i] != "" ) print i++;
            }
        }
    }
    else if( which == "remote" ) {
        if( what == "ip" ) {
            i = 0;
            for( i in Nodes ) {
                if( Nodes[i] != "" && i != local_id ) print Nodes[i];
            }
        }
        if( what == "id" ) {
            i = 0;
            for( i in Nodes ) {
                if( Nodes[i] != "" && i != local_id ) print i++;
            }
        }
    }
}
