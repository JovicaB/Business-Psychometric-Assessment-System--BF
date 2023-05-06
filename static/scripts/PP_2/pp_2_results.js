let result_table = document.getElementById('results_table')
var modal = document.getElementById('pp_2-modal')
var span = document.getElementsByClassName('pp_2-close')[0]
modal.style.display = 'none'

//POPULATE TABLE WITH RESULTS
fetch('/pp_2_results')
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
    row.cells[2].innerHTML = ''
  }

  for (var i = 0; i < data.length; i++) {
    var row = table.rows[i + 1]
    if (!row) {
      row = table.insertRow(-1)
    }
    var col1 = row.insertCell(0)
    var col2 = row.insertCell(1)
    var col3 = row.insertCell(2)
    col1.innerHTML = data[i][0]
    col2.innerHTML = data[i][1]
    col3.innerHTML = data[i][2]
  }
}

// INTERPRETATION MODAL

//Opening modal
let modalName
let modalfactor1
let modalfactor2
let modaltotal

result_table.addEventListener('dblclick', function (event) {

  if (
    event.target.cellIndex === 0 ||
    event.target.cellIndex === 1

  ) {
    var modalfactors = event.target.parentNode.cells[2].textContent.split(",").map(Number)
    modalName = event.target.parentNode.cells[0].textContent
    modalfactor1 = modalfactors[0]
    modalfactor2 = modalfactors[1]
    modaltotal = event.target.parentNode.cells[1].textContent
    openModal()
  }
})


//Two function that close modal, x and outside of modal click
span.onclick = function () {
  modal.style.display = 'none'
}

window.addEventListener("click", function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});

function openModal() {
  var modal = document.getElementById('pp_2-modal')
  var modalNameElement  = document.getElementById('pp_2-modal-name')
  var modalFactor1Element = document.getElementById('pp_2-modal-factor1')
  var modalFactor2Element = document.getElementById('pp_2-modal-factor2')
  var modalTotalElement = document.getElementById('pp_2-modal-total')

  modalNameElement.innerHTML = modalName
  modalFactor1Element.innerHTML = 'skor: ' + modalfactor1 + ' od 16'
  modalFactor2Element.innerHTML = 'skor: ' + modalfactor2+ ' od 18'
  modalTotalElement.innerHTML = interpretation(modaltotal) + ', skor: ' + modaltotal+ ' od 40'

  modal.style.display = 'block'
}

function interpretation(data) {
  if (data < 10) {
    return 'bez psihopatskih tendencija'
  } else if (data >= 10 && data <= 20) {
    return 'blagi oblik psihopatije'
  } else if (data >= 21 && data <= 30) {
    return 'umeren oblik psihopatije'
  } else if (data > 29) {
    return 'težak oblik psihopatije'
  } else {
  }
}