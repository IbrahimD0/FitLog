
function removeCard(button) {

    const card = button.closest(".card");
    card.remove();
}

// Optionally, you can add a confirmation message before deleting the workout
function confirmDelete(workoutId) {
    return confirm("Are you sure you want to delete this workout?");
}
