let result_table = document.getElementById('results_table')

//FETCH RESULTS name/MBTI type
fetch('/pp_0_results')
  .then((response) => response.json())
  .then((data) => {
    results = data
    populateResultsTable(result_table, data)
  })

function populateResultsTable(table, data) {
  for (var i = 1; i < table.rows.length; i++) {
    var row = table.rows[i]
    row.cells[0].innerHTML = ''
    row.cells[1].innerHTML = ''
  }

  for (var i = 0; i < data.length; i++) {
    var row = table.rows[i + 1]
    if (!row) {
      row = table.insertRow(-1)
    }
    var col1 = row.insertCell(0)
    var col2 = row.insertCell(1)
    var col3 = row.insertCell(2)
    col1.innerHTML = data[i][1]
    col2.innerHTML = data[i][2]
    col3.innerHTML = data[i][0]
  }
}

let modalName
let imeIspitanika
let MBTI_results
let MBTI_code
let MBTI_personality_title
let MBTI_personality_scoreA1
let MBTI_personality_scoreA2
let MBTI_personality_scoreB1
let MBTI_personality_scoreB2
let MBTI_personality_scoreC1
let MBTI_personality_scoreC2
let MBTI_personality_scoreD1
let MBTI_personality_scoreD2
let MBTI_personality_description
let MBTI_career

//dupli klik na red u tabeli za modal
result_table.addEventListener('dblclick', function (event) {
  if (
    event.target.cellIndex === 0 ||
    event.target.cellIndex === 1 ||
    event.target.cellIndex === 2
  ) {
    var id = event.target.parentNode.cells[2].textContent
    var columnText = event.target.parentNode.cells[0].textContent
    imeIspitanika = event.target.parentNode.cells[0].textContent
    getInterpretation(id).then(() => {
      openModal()
    })
  }
})

function getInterpretation(input_data) {
  if (!input_data) {
    return Promise.resolve()
  } else {
    const data = input_data
    return fetch('/pp_0_type_indicator', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        MBTI_results = JSON.stringify(data)
        MBTI_results = JSON.parse(MBTI_results)
        MBTI_code = MBTI_results['type']
        MBTI_personality_title = MBTI_results['title']
        MBTI_personality_scoreA1 = Math.round(
          MBTI_results['score'][0][0] * 100,
          0
        )
        MBTI_personality_scoreA2 = Math.round(
          MBTI_results['score'][0][1] * 100,
          0
        )
        MBTI_personality_scoreB1 = Math.round(
          MBTI_results['score'][1][0] * 100,
          0
        )
        MBTI_personality_scoreB2 = Math.round(
          MBTI_results['score'][1][1] * 100,
          0
        )
        MBTI_personality_scoreC1 = Math.round(
          MBTI_results['score'][2][0] * 100,
          0
        )
        MBTI_personality_scoreC2 = Math.round(
          MBTI_results['score'][2][1] * 100,
          0
        )
        MBTI_personality_scoreD1 = Math.round(
          MBTI_results['score'][3][0] * 100,
          0
        )
        MBTI_personality_scoreD2 = Math.round(
          MBTI_results['score'][3][1] * 100,
          0
        )
        MBTI_personality_description = MBTI_results['description']
        MBTI_career = MBTI_results['career']
      })
  }
}

// Interpretation modal
var modal = document.getElementById('pp_0-modal')
var span = document.getElementsByClassName('pp_0-close')[0]

span.onclick = function () {
  modal.style.display = 'none'
}

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none'
  }
}

function openModal() {
  var modal = document.getElementById('pp_0-modal')
  var modalName = document.getElementById('pp_0-modal-name')
  var modalCode = document.getElementById('pp_0-modal-code')
  var modalTitle = document.getElementById('pp_0-modal-title')
  var modalScoreA1 = document.getElementById('pp_0-modal-scoreA1')
  var modalScoreA2 = document.getElementById('pp_0-modal-scoreA2')
  var modalScoreB1 = document.getElementById('pp_0-modal-scoreB1')
  var modalScoreB2 = document.getElementById('pp_0-modal-scoreB2')
  var modalScoreC1 = document.getElementById('pp_0-modal-scoreC1')
  var modalScoreC2 = document.getElementById('pp_0-modal-scoreC2')
  var modalScoreD1 = document.getElementById('pp_0-modal-scoreD1')
  var modalScoreD2 = document.getElementById('pp_0-modal-scoreD2')
  var modalDescription = document.getElementById('pp_0-modal-description')
  var modalCareer = document.getElementById('pp_0-modal-career')
  modalName.textContent = imeIspitanika
  modalCode.textContent = MBTI_code
  modalTitle.textContent = MBTI_personality_title
  modalScoreA1.textContent = MBTI_personality_scoreA1 + '%'
  modalScoreA2.textContent = MBTI_personality_scoreA2 + '%'
  modalScoreB1.textContent = MBTI_personality_scoreB1 + '%'
  modalScoreB2.textContent = MBTI_personality_scoreB2 + '%'
  modalScoreC1.textContent = MBTI_personality_scoreC1 + '%'
  modalScoreC2.textContent = MBTI_personality_scoreC2 + '%'
  modalScoreD1.textContent = MBTI_personality_scoreD1 + '%'
  modalScoreD2.textContent = MBTI_personality_scoreD2 + '%'
  modalDescription.textContent = MBTI_personality_description
  modalCareer.textContent = MBTI_career
  modal.style.display = 'block'
}
