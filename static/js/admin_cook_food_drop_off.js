document.addEventListener('DOMContentLoaded', function() {
    function toggleFields(assignedPositionSelect) {
        var isCook = assignedPositionSelect.value === 'Cook';
        // Traverse up to the common parent fieldset, then find the respective fields within
        var fieldset = assignedPositionSelect.closest('fieldset');
        var foodDropOffRow = fieldset.querySelector('.field-food_drop_off');
        var addressRow = fieldset.querySelector('.field-volunteer_address');
        var phoneRow = fieldset.querySelector('.field-volunteer_phone');
        var emailRow = fieldset.querySelector('.field-volunteer_email');

        // Toggle the display of the food drop off checkbox and related label
        if (foodDropOffRow) {
            foodDropOffRow.style.display = isCook ? 'block' : 'none';
            var foodDropOffCheckbox = foodDropOffRow.querySelector('input[type=checkbox]');
            if (foodDropOffCheckbox) {
                foodDropOffCheckbox.checked = false; // Uncheck if not a cook
                foodDropOffCheckbox.disabled = !isCook; // Disable if not a cook
            }
        }

        // Toggle the display of the address, phone, and email
        if (addressRow) addressRow.style.display = isCook ? 'block' : 'none';
        if (phoneRow) phoneRow.style.display = isCook ? 'block' : 'none';
        if (emailRow) emailRow.style.display = isCook ? 'block' : 'none';
    }

    // Handler for change event on assigned position select elements
    function handlePositionChange(event) {
        toggleFields(event.target);
    }

    // Attach the handler to all assigned position select elements
    document.querySelectorAll('[id^="id_assignments-"][id$="-assigned_position"]').forEach(function(assignedPositionSelect) {
        assignedPositionSelect.addEventListener('change', handlePositionChange);
        // Set the initial state of the fields
        toggleFields(assignedPositionSelect);
    });
});
