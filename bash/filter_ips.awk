$0 ~ /^HOSTS$/, $0 ~ /^HOSTS_END$/ {
    if( $0 !~ /^HOSTS$/ && $0 !~ /^HOSTS_END$/ && ( now - $2 ) <= period ) { 
        if( list == 0 && $1 !~ ip ) {
            Lines[i++] = $0; 
        }
        else {
            #Lines[i++] = $1;
            print( $1 );
        }
    } 
    else  { next; }
} 
END { print( "HOSTS" ); for( idx in Lines ) print( Lines[idx] ); print( "HOSTS_END" ); } 
