
$(window).ready(function(){
	$("#display_html").on("click", display_html);
	print_origins_list();
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
		html += "<select>";
		for (i = 0; i < origins.length; i++){
			html += "<option>" + origins[i] + "</option>";
		}
		html += "</select>";
		$("#dropdown").append(html);
		print_textbox_distance_request();
		print_go_button();
	}
	else {
		$("#dropdown").append("No origins list provided from app");
	}
}

function print_textbox_distance_request(){
	var html = "<br>";
	html += "Insert the distance to cover -->     ";
	html += "<input type='text' />";
	$("#dropdown").append(html);
}

function print_go_button(){
	var html = "<br>";
	html += "<button id='go'>let me see where I can go</button>";
	$("#dropdown").append(html);
	$("#go").on("click", calculate_web);
}

function calculate_web(){
	// main function to calculate from json where the user can go
	// TODO
	alert("hit");
}
