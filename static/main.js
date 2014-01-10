
$(window).ready(function(){
	$("button.create_map").on("click", create_map);
	$("#run_js").on("click", load_cities);
});

var map;
var map_center;
var directions;
var distance;
var distance_matrix;

function load_cities(){
	// load the two cities lists in two arrays
	var cities_origin = new Array();
	var cities_destination = new Array();
	$("#city-list-start").children().each(function(){
		cities_origin.push($(this).text());
	});
	$("#city-list-end").children().each(function(){
		cities_destination.push($(this).text());
	});
	// create and send the google maps request, and save result 
	// in the json 'distance_matrix'
	var distance_request = new google.maps.DistanceMatrixService();
	distance_request.getDistanceMatrix({
								origins: cities_origin,
								destinations: cities_destination,
								travelMode: google.maps.TravelMode.DRIVING,
								}, distance_matrix_callback);
	
	// process response, and create HTML containing it
	alert('hit1');
}

function distance_matrix_callback(response, status) {
		if (status == google.maps.DistanceMatrixStatus.OK) {
			
			// TODO cosa faccio con la risposta?
			var origins = response.originAddresses;
			var destinations = response.destinationAddresses;
			var distance_matrix = response.rows[0].elements[0].duration.text;
			}
			alert(distance_matrix);
		}

function create_map(event) {
	var triggered = $(event.target).attr('id');
    var display_map = false;
    if (triggered == "display_default_map") {
        set_mapcenter_from_values(46.2, 11.2);
        display_map = true;
    }
    else if (triggered == "display_address_map" || 
             triggered == "display_coordinates_map" ||
             triggered == "display_directions_map") {
        var uinput = get_user_input()
        if (uinput.input_type == 'nothing')
        {
            alert("enter more info");
        }
        else if (uinput.input_type == 'latlng')
        {
            set_mapcenter_from_values(uinput.latitude, uinput.longitude);
            display_map = true;
        }
        else if (uinput.input_type == 'address') {
            set_mapcenter_from_address(uinput.address);
            display_map = true;
        }
        else if (uinput.input_type == 'direction') {
            get_directions(uinput.start, uinput.end);
            set_mapcenter_from_address(uinput.start);
            get_distance(uinput.start, uinput.end);
            
            display_map = true;
        }
        else {
            alert("OOPS");
        }
    }
    if (display_map) {
        initialize_map(map_center);
    }
}

function initialize_map(mapcenter) {
    directions = new google.maps.DirectionsRenderer();
    var mapOptions = {
          center: mapcenter,
          zoom: 12
          };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    if (typeof(directions) != "undefined") {
        directions.setMap(map);
    }
}
      
function get_user_input(){
	// return an object containing all user's string inputed
    var user = new Object();
    var lat = $("#user_lat").val();
    var lng = $("#user_lng").val();
    var addr = $("#user_address").val();
    var dir1 = $("#user_direction_address_1").val();
    var dir2 = $("#user_direction_address_2").val();
    if (dir1 != "" && dir2 != "") {
        user.input_type = "direction";
        user.start = dir1;
        user.end = dir2;
    }
    else if (addr != "") {
        user.input_type = "address";
        user.address = addr;
    }
    else if (lat != "" && lng != "") {
        user.input_type = "latlng";
        user.latitude = lat;
        user.longitude = lng;
    }
    else {
        user.input_type = "nothing";
    }
    return user;
}

function get_directions(start, end) {
    var directionsService = new google.maps.DirectionsService();
    var request = {
      origin:start,
      destination:end,
      travelMode: google.maps.TravelMode.DRIVING
    };
    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directions.setDirections(response);
        }
    });
}

function get_distance(start, end) {
	// send request for distance between two points start and end
	// the callback function 'distance_callback' store the result 
	// in the global var 'distance'
    var distance_service = new google.maps.DistanceMatrixService();
    distance_service.getDistanceMatrix(
          {
            origins: [start],
            destinations: [end],
            travelMode: google.maps.TravelMode.DRIVING,
          }, distance_callback);
}
function distance_callback(response, status) {
	// callback for the get_distance function
    if (status == google.maps.DistanceMatrixStatus.OK) {
        var origins = response.originAddresses;
        var destinations = response.destinationAddresses;
        var result = response.rows[0].elements[0];
        distance = result.distance.text;
        $("#user").append("<div>" + distance + "</div>");
    }
}

function set_mapcenter_from_address(address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address' : address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            set_mapcenter_from_values(latitude, longitude);
        }
        else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
        
    });
}

function set_mapcenter_from_values(latitude, longitude) {
    map_center = new google.maps.LatLng(latitude, longitude)
}
