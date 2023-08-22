
$(document).ready(function() {
// Close alert when the close (x) button is clicked
$('.alert button.close').on('click', function() {
  $(this).closest('.alert').fadeOut('slow', function() {
    $(this).remove();
  });
});
});
