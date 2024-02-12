// Works for Inline
// document.addEventListener('DOMContentLoaded', function() {
//     function toggleFields(assignedPositionSelect) {
//         var isCook = assignedPositionSelect.value === 'Cook';
//         // Traverse up to the common parent fieldset, then find the respective fields within
//         var fieldset = assignedPositionSelect.closest('fieldset');
//         var foodDropOffRow = fieldset.querySelector('.field-food_drop_off');
//         var addressRow = fieldset.querySelector('.field-volunteer_address');
//         var phoneRow = fieldset.querySelector('.field-volunteer_phone');
//         var emailRow = fieldset.querySelector('.field-volunteer_email');
//
//         // Toggle the display of the food drop off checkbox and related label
//         if (foodDropOffRow) {
//             foodDropOffRow.style.display = isCook ? 'block' : 'none';
//             var foodDropOffCheckbox = foodDropOffRow.querySelector('input[type=checkbox]');
//             if (foodDropOffCheckbox) {
//                 foodDropOffCheckbox.checked = false; // Uncheck if not a cook
//                 foodDropOffCheckbox.disabled = !isCook; // Disable if not a cook
//             }
//         }
//
//         // Toggle the display of the address, phone, and email
//         if (addressRow) addressRow.style.display = isCook ? 'block' : 'none';
//         if (phoneRow) phoneRow.style.display = isCook ? 'block' : 'none';
//         if (emailRow) emailRow.style.display = isCook ? 'block' : 'none';
//     }
//
//     // Handler for change event on assigned position select elements
//     function handlePositionChange(event) {
//         toggleFields(event.target);
//     }
//
//     // Attach the handler to all assigned position select elements
//     document.querySelectorAll('[id^="id_assignments-"][id$="-assigned_position"]').forEach(function(assignedPositionSelect) {
//         assignedPositionSelect.addEventListener('change', handlePositionChange);
//         // Set the initial state of the fields
//         toggleFields(assignedPositionSelect);
//     });
// });

// // Works for Tabular
document.addEventListener('DOMContentLoaded', function() {
    function toggleFields(selectElement) {
        // Assuming the function gets the select DOM element as input
        var parentRow = selectElement.closest('tr');
        var isCook = selectElement.value === 'Cook';

        // Query all related fields within this parent row
        var foodDropOffField = parentRow.querySelector('.field-food_drop_off select');
        var detailsField = parentRow.querySelector('.field-details');

        // Toggle the display of these fields based on the selected position
        if (foodDropOffField) foodDropOffField.style.visibility = isCook ? 'visible' : 'hidden';
        if (detailsField) detailsField.style.visibility = isCook ? 'visible' : 'hidden';
    }

    function bindChangeEventToPositionSelects() {
        document.querySelectorAll('select[id^="id_assignments-"][id$="-assigned_position"]').forEach(function(selectElement) {
            // Unbind the event first to avoid multiple bindings
            selectElement.removeEventListener('change', handlePositionChange);
            // Then bind the event
            selectElement.addEventListener('change', handlePositionChange);
            // Initialize the correct display based on the current value
            toggleFields(selectElement);
        });
    }

    function handlePositionChange(event) {
        toggleFields(event.target);
    }

    // Initialize the script for the first time
    bindChangeEventToPositionSelects();

    // Set up a mutation observer to monitor changes in the DOM for the inline group
    new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                // If new nodes are added, re-initialize the script
                bindChangeEventToPositionSelects();
            }
        });
    }).observe(document.querySelector('.js-inline-admin-formset.inline-group'), { childList: true, subtree: true });
});
