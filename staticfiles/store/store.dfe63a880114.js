$(document).ready(function () {
    // Handler for .ready() called.
    $(".dropdown-trigger").dropdown({ "hover": false });
    $(".add-product-dropdown-trigger").dropdown({ "hover": false });
    $('.materialboxed').materialbox();
    $('.sidenav').sidenav();
    $('select').formSelect();

    $('.op_edit').click(function () {
        $('#form-container').fadeIn();
        $('#form-overlay').fadeIn();
    })

    $('#show-form-button').click(function () {
        $('#form-container').fadeIn();
        $('#form-overlay').fadeIn();
    });

    $('#add_category_li').click(function () {
        $('#form_add_category').fadeIn();
        $('#form-overlay').fadeIn();
    });

    $('#form-overlay').click(function () {
        $('#form-container').fadeOut();
        $('#form-overlay').fadeOut();
    });

});

