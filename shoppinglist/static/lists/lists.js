jQuery(document).ready(function($){

    // Changes values numeric values in element attributes. This is to update values for Django formset processing.
 	updateElementIndex = function(elem, newvalue) {
 	 	elem.each( function(){
	        if ($(this).attr("for")) $(this).attr("for", $(this).attr("for").replace(/\d+/g, newvalue));
	        if ($(this).attr('id')) $(this).attr('id', $(this).attr('id').replace(/\d+/g, newvalue));
	        if ($(this).attr('name')) $(this).attr('name', $(this).attr('name').replace(/\d+/g, newvalue));
	   	});
	};

    // Add / remove class to forms to enable css to give user only one form is active. 
    activeForms = function( elem ) {
        $('.form-control').addClass('form-inactive');
        elem.removeClass('form-inactive');
        // Display this delete button, and hide all others
        $('.delete-item-button').css( "display", "none");
        elem.siblings('.delete-item-button').css( "display", "inline-block");
        // Show all edit buttons, but hide this one
        $('.edit-item-button').css( "display", "inline-block");
        elem.siblings('.edit-item-button').css( "display", "none");
    };

    $(document).on('click', '#add-item-button', function(e){
        var $inputForm = $('.form-section').last();
        if ( $inputForm.find('.form-control').val() ) {
            var $clone = $inputForm.clone();
            $(this).remove(); // remove existing add item button
            var formCount = $('.form-section').length;
       		updateElementIndex($clone.children().children().children(), formCount );
       		$clone.find('.form-group').children('input').val('');
            $clone.find('.form-group').children('input[type=checkbox]').prop('checked', false);
            $clone.css('display', 'list-item');
            $clone.removeClass('original-item');
            $inputForm.after( $clone );
            var newForm = $('.form-section').last().find('.form-control');
            activeForms(newForm);
            newForm.focus(); // Put cursor in new input field
            $('#id_item_set-TOTAL_FORMS').val(parseInt($('#id_item_set-TOTAL_FORMS').val(), 10)+1); // Increase django form-management value
        } else {
            $('.help-block').text('Wow there! Finish this item before adding another.');
        }
    });

    // If last element has help text and clicks elsewhere - remove help text
    $(document).click( function(e){
        // if click not on 'add item' button (this will hide help text immediately)
        if ( !( event.target.id == "add-item-button" ) ) {
            if ( $('.help-block').text() ) {
                $('.help-block').text('');
            }
        }
    });

    // If last element has help text and user types elsewhere - remove help text
    $(document).keypress( function(e){
        // if click not on 'add item' button (this will hide help text immediately)
        if ( $('.help-block').text() ) {
            $('.help-block').text('');
        }
    });

    // Activate clicked on form 
    $(document).on('click', '#item-edit-form .form-control', function(){
        activeForms($(this));
    });

    // Activate clicked on form 
    $(document).on('click', '.edit-item-button', function(){
        var $form = $(this).siblings('.form-control'); // Cache form
        $form.focus();
        activeForms($form);
    });

    // Delete item
    $(document).on('click', '.delete-item-button', function(){
        // Cache top level div of list item.
        var $formContainer = $(this).parents('.form-section');
        // if this is last list item, move add item button to previous list item before it is deleted from page.
        if ( $(this).siblings('#add-item-button') ) {
            var $clone = $(this).siblings('#add-item-button').clone();
            $formContainer.siblings('.form-section').filter(function () {
                console.log(!($(this).css("display") == "none"))
                return !($(this).css("display") == "none");
            }).last().find('.delete-item-button').after($clone);
        }
        // If the form has value add a placeholder value to satisfy form 'required' value and allow form to submit
        if ( !($(this).siblings('.form-control').val()) ) {
            $(this).siblings('.form-control').val('Delete item')
        }
        if ( $formContainer.hasClass('original-item') ) {
            // Hide and tick delete checkbox so Django process form delete
            $(this).parents('.form-section').css('display', 'none');
            $(this).siblings('input[type=checkbox]').prop('checked', true);
        } else {
            $formContainer.remove();
        }       
    });
});