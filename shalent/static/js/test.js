jQuery(document).ready(function($) {
	$(".result-show").hide();
	$(".yes-btn").hide();
	$(".no-btn").hide();
	$(".submit-btn").click(function() {
		var code = $("#code-text").val();
		if(code != "")
		{
			$(".wrapper").hide();
			$("#final-code").val(code);
			$(".result-value").text(code);
			$(".result-show").fadeIn();
		}
		else
		{
			alert("Please Enter any Code");
		}
	});

	$(".change-btn").click(function() {
		$(".result-show").hide();
		$(".wrapper").fadeIn();
		$(".submit-btn").hide();
		$(".yes-btn").show();
		$(".no-btn").show();
	});
	$(".yes-btn").click(function() {
		var code = $("#code-text").val();
		if(code != "")
		{
			$(".wrapper").hide();
			$("#final-code").val(code);
			$(".result-value").text(code);
			$(".result-show").fadeIn();
		}
		else
		{
			alert("Please Enter any Code");
		}
	});
	$(".no-btn").click(function() {
		$(".wrapper").hide();
		$(".result-show").fadeIn();
	});
});
