
$(window).ready(function(){
	$("#display_html").on("click", display_html);
	$("#go_distance").on("click", calc_distance);
	});

function calc_distance(){
	// extract json from html
	var js = $("#json").data("json");

	// create and send the google maps request, calling the callback
	var distance_request = new google.maps.DistanceMatrixService();
	distance_request.getDistanceMatrix({
								origins: js.cities,
								destinations: js.cities,
								travelMode: google.maps.TravelMode.DRIVING,
								}, calc_distance_callback);
	}

function calc_distance_callback(response, status) {
	if (status == google.maps.DistanceMatrixStatus.OK) {
		// push the response to the app engine
		$.ajax({
			url: '/post_distance',
			type: 'POST',
			data: JSON.stringify(response),
			contentType: 'application/json; charset=UTF-8',
			dataType: 'json',
		}).done(function(data){	// print results in html
			var html = "Result of the DISTANCE request was ";
			html += data.distance_result;
			$("#result").append(html);
			});
	}
	else {
		// if the request was not satisfied by google maps
        alert('Distance was not successfully calculated ' +
						'for the following reason: ' + status);
    }
}

function display_html(){
	alert($("body").html());
	}
