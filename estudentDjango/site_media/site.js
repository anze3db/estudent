$('.dropdown-toggle').dropdown();

$(document).ready(function() {
    var last_valid_selection = null;

    $('#id_instructors').change(function(event) {
        if ($(this).val().length > 3) {
            alert('Izberete lahko maksimalno 3 predavatelje!');
            $(this).val(last_valid_selection);
        } else {
            last_valid_selection = $(this).val();
        }
    });
});
