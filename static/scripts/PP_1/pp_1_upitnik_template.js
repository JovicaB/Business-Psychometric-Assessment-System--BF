let radioButtons = document.querySelectorAll('input[type="radio"]')
let username = localStorage.getItem('username')

//on load clears radio buttons and suggestion box
for (var i = 0; i < radioButtons.length; i++) {
  radioButtons[i].checked = false
  document.getElementsByName('sug')[0].value = ''
}

var input_credit_button = document.getElementById('submit')
input_credit_button.addEventListener('click', getResults)

// Gathers radio button values into array for BE
let scores = []
function getResults() {
  scores = []
  let uncheckedRadioButtons = []
  for (let i = 1; i <= 20; i++) {
    let scoreName = 'score' + i
    let radios = document.getElementsByName(scoreName)
    let scoreValue = ''

    // ALERT if any radio button is left unchecked
    let unchecked = true
    for (let j = 0; j < radios.length; j++) {
      if (radios[j].checked) {
        scoreValue = parseInt(radios[j].id.split('_')[2])
        unchecked = false
        break
      }
    }

    if (unchecked) {
      uncheckedRadioButtons.push(scoreName)
    }

    scores.push(scoreValue)
  }

  let sugestija = document.getElementsByName('sug')[0].value
  scores.push(sugestija)
  let error_res = uncheckedRadioButtons.map((score) => {
    return '\n' + 'PITANJE:' + score.substring(5)
  })

  if (uncheckedRadioButtons.length > 0) {
    alert('Pitanja na koja nije dat odgovor: ' + error_res.join(', '))
  } else {
    postUpitnikToBE(scores)
    clearRadioButtons()
    document.getElementsByName('sug')[0].value = ''

    fetch('/pp_1_zavrseno', {
      method: 'GET',
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = '/pp_1_zavrseno'
          window.history.replaceState({}, '', '')
        }
      })
      .catch((error) => {
        console.error('Error:', error)
      })
  }
}

//clears radio buttons
function clearRadioButtons() {
  let radioButtons = document.querySelectorAll('input[type="radio"]')

  for (let i = 0; i < radioButtons.length; i++) {
    radioButtons[i].checked = false
  }
}

//POST results to BE
function postUpitnikToBE(data) {
  let json = JSON.stringify(data)
  const url = 'http://127.0.0.1:5000/pp_1_upitnik' //IZMENA
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
