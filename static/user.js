
$(window).ready(function(){
	$("#display_html").on("click", display_html);
	});

function display_html(){
	alert($("body").html());
	}
