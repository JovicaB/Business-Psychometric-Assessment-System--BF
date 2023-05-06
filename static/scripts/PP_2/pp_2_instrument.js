function clearRadio() {
  const radioButtons = document.querySelectorAll('input[type="radio"]');
  const pp2_name_input = document.getElementsByClassName('pp2_instrument_name')[0];

  if (pp2_name_input) {
    pp2_name_input.value = '';
  }
  radioButtons.forEach((button) => {
    button.checked = false;
  });
}



var pp2_button = document.getElementById('pp2_button')
pp2_button.addEventListener('click', gatherRasults)

function gatherRasults() {
  const pp2_name_input = document.getElementsByClassName('pp2_instrument_name')[0];
  let scores = []
  let results = {}
  let uncheckedRadioButtons = []
  for (let i = 1; i <= 20; i++) {
    let scoreName = 'score' + i
    let radios = document.getElementsByName(scoreName)
    let scoreValue = ''

    let unchecked = true
    for (let j = 0; j < radios.length; j++) {
      if (radios[j].checked) {
        scoreValue = parseInt(radios[j].id.split('_')[2] - 1)
        unchecked = false
        break
      }
    }
    if (unchecked) {
      uncheckedRadioButtons.push(scoreName)
    }

    scores.push(scoreValue)
  }
  results = {'name': pp2_name_input.value, 'results': scores}

  let error_res = uncheckedRadioButtons.map((score) => {
    return '\n' + 'PITANJE:' + score.substring(5)
  })

  if (uncheckedRadioButtons.length > 0) {
    alert('Pitanja na koja nije dat odgovor: ' + error_res.join(', '))
  } else {
    postUpitnikToBE(results)
    clearRadio()
  }
}

function postUpitnikToBE(data) {
  let json = JSON.stringify(data)
  //const url = 'http://127.0.0.1:5000/pp_2_upitnik' //IZMENA
  const url = '/pp_2_upitnik' //IZMENA
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: json,
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {})
    .catch((error) => {})
}


