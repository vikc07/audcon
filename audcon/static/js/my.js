$(document).ready(function(){
    // Hide Spinner
    $('#spinner').html();
	$('#spinner').hide();

    //Init flash alerts
    $(".alert").alert();
	window.setTimeout(function() { $(".alert").alert('close'); }, 3000);

	// Set binding for forms
	$(document).on("submit", "form", function() {
	    // Hide the save button
        $(":submit", this).attr("disabled", "disabled");

        // Show the spinner
        $('#spinner').html('<i class="fas fa-spinner fa-spin"></i>');
	    $('#spinner').show();
    });
});