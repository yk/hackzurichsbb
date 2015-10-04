
window.addEventListener('WebComponentsReady', function(e) {
	var nowData = new Date();

	//Example listner 
	document.querySelector("hz-app").addEventListener("notifyuser", function(e) {
		if(e.detail.length<150)
		 console.log("heared event:",e.detail); 
		 else
		 console.log("heared event:"); 
	});

	
	if(!!localStorage.bookingList){
		localBookings = JSON.parse(localStorage.bookingList)

		for (i = 0; i < localBookings.length; i++) { 
	     	curSecList = localBookings[i].data.sections
   			if(!localBookings[i].feedback){
				console.log("Booking"+i+"has no feedback");
				
				for( j = 0; j <curSecList.length ; j++){
					section = curSecList[j];
					if(true||section.departure.handicappedAccess=='0'||section.departure.handicappedAccess==''||section.arrival.handicappedAccess=='0'||section.arrival.handicappedAccess==''){
						
					var conAsString =  JSON.stringify(localBookings[i].data)
						if(section.departure.departureTimestamp < nowData.getTime()/1000 ){
							var event = new CustomEvent("pastbooking", { "detail": conAsString }  );
							document.querySelector("hz-app").dispatchEvent(event);
						}
						else{
							setTimeout(
							function(){ 
								var event = new CustomEvent("notifyuser", { "detail": conAsString }  )
								document.querySelector("hz-app").dispatchEvent(event);  } 
							, (section.departure.departureTimestamp - nowData.getTime()/1000 +340 )*1000 ); //Debug presentation 5000
						}

						break;
						
						
					}
				
}		
					
						
			}
			else{
				console.log("Booking"+i+"has some feedback");
			}
			
		}
	}
	else{
    console.log("no booking found");
	}
  });

  function markAsResponded(queryID){
		localBookings = JSON.parse(localStorage.bookingList)

		foundBooking = false;
		for (i = 0; i < localBookings.length; i++) { 
	   	    curBooking = localBookings[i].data
	   		if( curBooking.ourID==queryID){
	   			foundBooking=true;
	   			 localBookings[i].feedback=true
	   			 localStorage.bookingList=JSON.stringify(localBookings)
	   			 break;
	   		}
		}
		if(!foundBooking)
			print("Warning Booking id not found")


  }
