function requestForLocation(){
	navigator.geolocation.getCurrentPosition(function(position){
		var lat = position.coords.latitude;
		var lon = position.coords.longitude;
		var allTogether = lat+","+lon;
		console.log(allTogether);
		document.getElementById("coords").value = allTogether;
		document.getElementById("coords").disabled=false;
		document.getElementsByTagName("form")[0].submit();

	})
}