function GetReserveTime (order){
    if ((order%2) == 0){
	    var Shour   = 8 + (0.5*(order-2))
        var Sminute = 30
	}
	else if ((order%2) == 1){
	    var Shour   = 8 + (0.5*(order-1))
        var Sminute = 0
	}
	return [ Shour, Sminute]
}