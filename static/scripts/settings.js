const button = document.getElementById("url_duration_button");

button.addEventListener('click', () => {
  var input = document.getElementById("global_duration").value;

  // Validate the input
  if (input === "" || isNaN(input) || input < 1 || input > 24) {
    document.getElementById("global_duration").value = "";
    alert("Unesite broj između 1 i 24.");
    return;
  }

  // Send the input value to the Flask server
  document.getElementById("global_duration_label").innerHTML = "Trajanje generisanog linka podešeno je na : " + durationText(document.getElementById("global_duration").value)
  document.getElementById("global_duration").value = ""
  fetch(`/settings_set?input=${input}`)
      .then(response => response.json())
      .then(data)
      .catch(error => console.error('Error:', error));
});

function durationText(inputDuration) {
  if (inputDuration == 1) {
      return "1 čas";
  } else if (inputDuration >= 2 && inputDuration <= 4) {
      return inputDuration + " časa";
  } else if (inputDuration >= 5 && inputDuration <= 20) {
      return inputDuration + " časova";
  } else if (inputDuration == 21) {
      return "21 čas";
  } else {
      return inputDuration + " časa";
  }
}

function resetSettings(data) {
  fetch(`/settings_reset?data=${encodeURIComponent(data)}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
    })
    .catch(error => console.error('Error:', error));
}