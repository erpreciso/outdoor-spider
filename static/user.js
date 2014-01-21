
$(window).ready(function(){
	$("#display_html").on("click", display_html);
	print_origins_list();
	create_first_map();
	});

function display_html(){
	alert($("body").html());
	}

function print_origins_list(){
	// get origins list from json data
	var js = $("#json").data("json");
	var origins = js.origins;
	
	// create html
	if (origins.length > 0){    // check of origins list has been provided
		var html = "Select a starting point for your trip -->   ";
		html += "<select id='start_city'>";
		for (i = 0; i < origins.length; i++){
			html += "<option>" + origins[i] + "</option>";
		}
		html += "</select>";
		$("#dbody").append(html);
		$("#start_city").change(center_map);
		print_textbox_distance_request();
		print_go_button();
	}
	else {
		$("#dbody").append("No origins list provided from app");
	}
}

function print_textbox_distance_request(){
	var html = "<br>";
	html += "Insert the distance to cover in km -->     ";
	html += "<input id='distance' type='text' />";
	html += "<br>Insert the tolerance of the research in km -->     ";
	html += "<input id='tolerance' type='text' />";
	$("#dbody").append(html);
}

function print_go_button(){
	var html = "<br>";
	html += "<button id='go'>let me see where I can go</button>";
	$("#dbody").append(html);
	$("#go").on("click", calculate_web);
}

function get_user_input(){
	var start = $("#start_city").val();
	var distance = $("#distance").val();
	var tolerance = $("#tolerance").val();
	distance = distance * 1000;   // transforms km inserted in meters
	tolerance = tolerance * 1000;
	return [start, distance, tolerance];
}

function calculate_web(){
	
	// get user input
	var inp = get_user_input();
	
	// push to the app engine
	var q = {
			"start": inp[0],
			"distance": inp[1],
			"tolerance": inp[2]
			};
	$.ajax({
		url: '/query',
		type: 'POST',
		data: JSON.stringify(q),
		//~ data: q,
		contentType: 'application/json; charset=UTF-8',
		dataType: 'json'
	}).done(function(data){append_result(data);});
}

function append_result(data){
	var res = data.near;
	$("#results").remove();
	var html = "<ul id='results'>"
	for (i = 0;i < res.length; i++){
		var name = res[i][0];
		var dist = res[i][1] / 1000;
		html += "<li>" + name + " is " + dist.toFixed(0) + " km far away</li>";
		}
	html += "</ul>"
	$("#dbody").append(html);
	draw_routes(res);
	}

var map;

function create_first_map(){
	var map_options = {
		center: new google.maps.LatLng(42.14, 12.8),
		zoom: 6
	};
	map = new google.maps.Map(document.getElementById("canvas"), map_options);
}

function center_map(){
	var new_center = $("#start_city").val();
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode({"address": new_center}, function(results, status){
		if (status == google.maps.GeocoderStatus.OK){
			map.setCenter(results[0].geometry.location);
			map.setZoom(10);
		}
		else {
			alert("Geocode not successful: " + status);
		}
	});
}

function draw_routes(cities){
	create_first_map();
	function renderDirections(result){
		var directionsRenderer = new google.maps.DirectionsRenderer({
			suppressMarkers:true
			});
		directionsRenderer.setMap(map);
		directionsRenderer.setDirections(result);
	}
	var directionsService = new google.maps.DirectionsService();
	function requestDirections(start, end){
		directionsService.route({
			origin: start,
			destination: end,
			travelMode: google.maps.DirectionsTravelMode.DRIVING
		}, function(result){
			renderDirections(result);});
	}			
	var start = $("#start_city").val();
	for (var i = 0; i < cities.length; i++){
		var end = cities[i][0];
		requestDirections(start, end);
	}
}
