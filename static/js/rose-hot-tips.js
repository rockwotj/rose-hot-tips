var rh = rh || {};
rh.ht = rh.ht || {};

rh.ht.enableButtons = function() {
	$("#add-tip").click(function() {
		$("#insert-tip .modal-title").html("Add a Tip");
		$("#insert-tip button[type=submit]").html("Add Tip");

		$("#insert-tip input[name=prof_name]").val("None");
		$("#insert-tip input[name=helpfulness]").val("3");
		$("#insert-tip input[name=clarity]").val("3");
		$("#insert-tip input[name=p_ease]").val("3");
		$("#insert-tip input[name=hot_or_not]").prop("checked", false);
		$("#insert-tip input[name=class_name]").val("None");
		$("#insert-tip input[name=grasp]").val("3");
		$("#insert-tip input[name=workload]").val("3");
		$("#insert-tip input[name=c_ease]").val("3");
		$("#insert-tip textarea[name=comments]").val("");
		$("#insert-tip input[name=entity_key]").val("").prop("disabled", true);
	});

	$(".edit-tip").click(function() {
				$("#insert-tip .modal-title").html("Edit this Tip");
				$("#insert-tip button[type=submit]").html("Edit Tip");

				var prof_name = $(this).parent().parent().parent().find(".data").attr("data-prof");
				var helpfulness = $(this).parent().parent().parent().find(".helpfulness").html();
				var clarity = $(this).parent().parent().parent().find(".clarity").html();
				var p_ease = $(this).parent().parent().parent().find(".p-ease").html();
				var hot_or_not = $(this).parent().parent().parent().find(".data").attr("data-hot");
				console.log(hot_or_not);
				var class_name = $(this).parent().parent().parent().find(".data").attr("data-class");
				var grasp = $(this).parent().parent().parent().find(".grasp").html();
				var workload = $(this).parent().parent().parent().find(".workload").html();
				var c_ease = $(this).parent().parent().parent().find(".c-ease").html();
				var comments = $(this).parent().parent().parent().find(".comments").html();
				var entityKey = $(this).parent().parent().parent().find(".entity-key").html();

				$("#insert-tip select[name=prof_name]").selectpicker('val', prof_name);
				$("#insert-tip input[name=helpfulness]").val(helpfulness);
				$("#insert-tip input[name=clarity]").val(clarity);
				$("#insert-tip input[name=p_ease]").val(p_ease);
				$("#insert-tip input[name=hot_or_not]").prop("checked", (hot_or_not.toLowerCase() === 'true'));
				$("#insert-tip select[name=class_name]").selectpicker('val', class_name);
				$("#insert-tip input[name=grasp]").val(grasp);
				$("#insert-tip input[name=workload]").val(workload);
				$("#insert-tip input[name=c_ease]").val(c_ease);
				$("#insert-tip textarea[name=comments]").val(comments);
				$("#insert-tip input[name=entity_key]").val(entityKey).prop(
						"disabled", false);
			});

	$(".delete-tip").click(function() {
		entityKey = $(this).parent().parent().parent().find(".entity-key").html();
		$("#delete-tip input[name=entity_key]").val(entityKey);
	});
};

	


$(document).ready(function() {
	rh.ht.enableButtons();
	$(".display-if-hot").onload = function() {
		var hot_or_not = $(this).parent().parent().parent().find(".data").attr("data-hot");
		console.log(hot_or_not);
	};
	$('[data-toggle="tooltip"]').tooltip();
});
