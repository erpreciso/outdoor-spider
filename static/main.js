
$(window).ready(function(){
	$("#display_html").on("click", display_html);
	$("#go_distance").on("click", calc_distance);
	});


function display_html(){
	alert($("body").html());
	}

function calc_distance(){
	// extract json from html
	var js = $("#json").data("json");

	// create and send the google maps request, calling the callback
	var distance_request = new google.maps.DistanceMatrixService();
	distance_request.getDistanceMatrix({
								origins: js.origins,
								destinations: js.destinations,
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
		});
	}
	else {
		// if the request was not satisfied by google maps
        alert('Distance was not successfully calculated ' +
						'for the following reason: ' + status);
    }
}

// all code below is to visualize the map, so need to be cleaned

var map;
var map_center;
var directions;
var distance;

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


test_geocoding = {
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "21",
               "short_name" : "21",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Via Magenta",
               "short_name" : "Via Magenta",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Busto Arsizio",
               "short_name" : "Busto Arsizio",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Busto Arsizio",
               "short_name" : "Busto Arsizio",
               "types" : [ "administrative_area_level_3", "political" ]
            },
            {
               "long_name" : "Varese",
               "short_name" : "VA",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Lombardy",
               "short_name" : "Lombardy",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Italy",
               "short_name" : "IT",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "21052",
               "short_name" : "21052",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "Via Magenta, 21, 21052 Busto Arsizio Varese, Italy",
         "geometry" : {
            "location" : {
               "lat" : 45.6067461,
               "lng" : 8.8464537
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 45.60809508029149,
                  "lng" : 8.847802680291503
               },
               "southwest" : {
                  "lat" : 45.60539711970849,
                  "lng" : 8.845104719708498
               }
            }
         },
         "types" : [ "street_address" ]
      }
   ],
   "status" : "OK"
}
