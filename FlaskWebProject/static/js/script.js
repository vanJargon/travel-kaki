$(document).ready(function(){
    function initialize(){
        var place_options={
            types:['(cities)']
        };

        var place_input = document.getElementById('header_input');
        var autocomplete_place = new google.maps.places.Autocomplete(place_input,place_options);
    }

    google.maps.event.addDomListener(window,'load',initialize);

    $('#header_submit').on("click", function(){
        var query = $('#header_input').val();

    });
});