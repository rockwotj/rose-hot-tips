var rh = rh || {};
rh.ht= rh.ht || {};

rh.ht.addEventHandlers = function() {
	$("#addtip").on("shown.bs.modal", function() {
	});
	
};

rh.ht.enableButtons = function() {
	$("#addtip").click(function() {
	});
};


$(document).ready(function() {
	rh.ht.addEventHandlers();
	rh.ht.enableButtons();
	$('[data-toggle="tooltip"]').tooltip();
});
