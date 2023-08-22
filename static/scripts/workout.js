let exerciseCount = 2;
function addExercise() {
    const exerciseDiv = document.createElement("tr");
    exerciseDiv.classList.add("exercise");
    exerciseDiv.innerHTML = `
        <td class="form-group">${exerciseCount}</td>
            <td>
                <div class="form-group">
                    <label for="exerciseName"></label>
                    <input type="text" class="form-control" id="exerciseName" name="name[]" required>
                </div>
            <td>
                <div class="form-group">
                    <label for="reps"></label>
                    <input type="number" class="form-control" id="reps" name="reps[]" required>
                </div>
            </td>
    
            <td>
                <div class="form-group">
                    <label for="sets"></label>
                    <input type="number" class="form-control" id="sets" name="sets[]" required>
                </div>
            </td>
            <td>

        </td>
    `;

    document.getElementById("tablebody").appendChild(exerciseDiv);
    exerciseCount++
}
function delExercise() {
    const tablebody = document.getElementById("tablebody");
    const exercises = tablebody.getElementsByClassName("exercise");

    // Assuming you want to remove the last exercise row
    if (exercises.length > 0) {
        tablebody.removeChild(exercises[exercises.length - 1]);
        exerciseCount--;
    }
}