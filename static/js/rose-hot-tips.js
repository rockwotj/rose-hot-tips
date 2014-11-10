var rh = rh || {};
rh.ht = rh.ht || {};

rh.ht.addEventHandlers = function() {
	$("#insert-tip").on("shown.bs.modal", function() {
		$("input[name=prof_name]").focus();
	});

};

rh.ht.enableButtons = function() {
	$("#add-tip").click(function() {
		$("#insert-tip .modal-title").html("Add a Tip");
		$("#insert-tip button[type=submit]").html("Add Tip");

		$("#insert-tip input[name=prof_name]").val("");
		$("#insert-tip input[name=helpfulness]").val("");
		$("#insert-tip input[name=clarity]").val("");
		$("#insert-tip input[name=p_ease]").val("");
		$("#insert-tip input[name=class_name]").val("");
		$("#insert-tip input[name=grasp]").val("");
		$("#insert-tip input[name=workload]").val("");
		$("#insert-tip input[name=c_ease]").val("");
		$("#insert-tip textarea[name=comments]").val("");
		$("#insert-tip input[name=entity_key]").val("").prop("disabled", true);
	});

	$("#edit-tip").click(
			function() {
				$("#insert-tip .modal-title").html("Edit this Tip");
				$("#insert-tip button[type=submit]").html("Edit Tip");

				prof_name = $(this).find(".prof-name").html();
				helpfulness = $(this).find(".helpfulness").html();
				clarity = $(this).find(".clarity").html();
				p_ease = $(this).find(".p-ease").html();
				class_name = $(this).find(".class-name").html();
				grasp = $(this).find(".grasp").html();
				workload = $(this).find(".workload").html();
				c_ease = $(this).find(".c-ease").html();
				comments = $(this).find(".comments").html();
				entityKey = $(this).find(".entity-key").html();

				$("#insert-tip input[name=prof_name]").val(prof_name);
				$("#insert-tip input[name=helpfulness]").val(helpfulness);
				$("#insert-tip input[name=clarity]").val(clarity);
				$("#insert-tip input[name=p_ease]").val(p_ease);
				$("#insert-tip input[name=class_name]").val(class_name);
				$("#insert-tip input[name=grasp]").val(grasp);
				$("#insert-tip input[name=workload]").val(workload);
				$("#insert-tip input[name=c_ease]").val(c_ease);
				$("#insert-tip textarea[name=comments]").val(comments);
				$("#insert-tip input[name=entity_key]").val(entityKey).prop(
						"disabled", false);
			});

	$("#delete-tip").click(function() {
		entityKey = $(this).find(".entity-key").html();
		$("#delete-tip input[name=entity_key]").val(entityKey);
	});
};

$(document).ready(function() {
	rh.ht.addEventHandlers();
	rh.ht.enableButtons();
	$('[data-toggle="tooltip"]').tooltip();
});
