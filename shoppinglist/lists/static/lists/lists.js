jQuery(document).ready(function($){
 	 updateElementIndex = function(elem, newvalue) {
        console.log(elem.children().children().children());
 	 	elem.children().children().children().each( function(){
	        if ($(this).attr("for")) $(this).attr("for", $(this).attr("for").replace(/\d+/g, newvalue));
	        if ($(this).attr('id')) $(this).attr('id', $(this).attr('id').replace(/\d+/g, newvalue));
	        if ($(this).attr('name')) $(this).attr('name', $(this).attr('name').replace(/\d+/g, newvalue));
	   	});
	};

    activeForms = function( elem ) {
        $('.form-control').addClass('form-inactive');
        elem.removeClass('form-inactive');
        $('.delete-item-button').css( "display", "none");
        elem.siblings('.delete-item-button').css( "display", "inline-block");
    };

    $(document).on('click', '#addItemButton', function(e){
        var $inputForm = $('.form-section').last();
        if ( $inputForm.children('.form-inline').children('.form-group').children('.form-control').val() ) {
            var $clone = $inputForm.clone();
            $(this).remove(); // remove exizting add item button
            var formCount = $('.form-section').length;
       		updateElementIndex($clone, formCount );
       		$clone.children('.form-inline').children('.form-group').children('input').val('');
            $clone.children('.form-inline').children('.form-group').children('input[type=checkbox]').prop('checked', false);
            $clone.css('display', 'list-item');
            $inputForm.after( $clone );
            var newForm = $('.form-section').last().children('.form-inline').children('.form-group').children('.form-control');
            activeForms(newForm);
            newForm.focus(); // Put cursor in new input field
            $('#id_item_set-TOTAL_FORMS').val(parseInt($('#id_item_set-TOTAL_FORMS').val(), 10)+1); // Increase django form-management value
        } else {
            $('.help-block').text('Add this item first');
        }
    });

    $(document).on('keypress','.form-control', function(e){
        if ( !($('.form-section').last().children('.form-inline').children('.form-group').children('.form-control').val()) ) {
            $('.help-block').text('');
        }
    });

    $(document).on('click', '#item-edit-form .form-control', function(){
        activeForms($(this));
    });

    $(document).on('click', '.delete-item-button', function(){
        if ( $(this).siblings('.form-control').val() ) {
            $(this).parents('.form-section').css('display', 'none');
            $(this).siblings('input[type=checkbox]').prop('checked', true);
        } else {
            $(this).parents('.form-section').remove();
        }
    });
});