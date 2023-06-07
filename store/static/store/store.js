$(document).ready(function () {
    // Handler for .ready() called.
    $(".dropdown-trigger").dropdown({ "hover": false });
    $(".add-product-dropdown-trigger").dropdown({ "hover": false });
    $('.materialboxed').materialbox();
    $('.sidenav').sidenav();
    $('select').formSelect();

    $('#show-form-button').click(function () {
        $('#form-container').fadeIn();
        $('#form-overlay').fadeIn();
    });

    $('#form-overlay').click(function () {
        $('#form-container').fadeOut();
        $('#form-overlay').fadeOut();
    });

});

