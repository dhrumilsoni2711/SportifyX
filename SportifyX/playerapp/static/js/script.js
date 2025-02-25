$(document).ready(function() {
    $("#venue-details-form").submit(function(event) {
        event.preventDefault();

        var venueId = $("#venue-id").val();
        var venueDescription = $("#venue-description").val();
        var venueAmenities = $("#venue-amenities").val().split(",").map(item => item.trim());
        var venueTime = $("#venue-time").val();

        $.ajax({
            url: "/adminapp/add_venue_details/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                venue_id: venueId,
                venue_description: venueDescription,
                venue_amenities: venueAmenities,
                venue_time: venueTime,
            }),
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            },
            success: function(response) {
                if (response.success) {
                    $("#response-message").html('<div class="alert alert-success">' + response.message + '</div>');
                } else {
                    $("#response-message").html('<div class="alert alert-danger">' + response.error + '</div>');
                }
            },
            error: function() {
                $("#response-message").html('<div class="alert alert-danger">An error occurred.</div>');
            }
        });
    });
});
