var question = document.getElementById('question')
var question_title = document.getElementById('question_title')
var leftA = document.getElementById('left_a')
var rightA = document.getElementById('right_a')

let counter = 1
let test_data = {}

window.onload = function () {
  question_title.innerHTML = 'PITANJE #' + counter
  question.innerHTML = 'NA ZABAVI:'
  leftA.innerHTML = 'komunicirate s mnogo ljudi, uključujući nepoznate osobe'
  rightA.innerHTML = 'komunicirate s nekoliko ljudi koje poznajete'
}

function updateHTML(elmId, value) {
  var elem = document.getElementById(elmId)
  if (typeof elem !== 'undefined' && elem !== null) {
    elem.innerHTML = value
  }
}

document.getElementById('left_a').addEventListener('click', testAnswerClick)
document.getElementById('right_a').addEventListener('click', testAnswerClick)

var question = document.getElementById('question')
var leftA = document.getElementById('left_a')
var rightA = document.getElementById('right_a')



function testAnswerClick(event) {
  if (event.target.id === 'left_a') {
    counter++
    question_title.innerHTML = 'PITANJE #' + counter
    getQuestion(counter - 1)
      .then(function (data) {
        question.innerHTML = data['Q']
        leftA.innerHTML = data['A']
        rightA.innerHTML = data['B']
        test_data[counter - 1] = 'A'

        if (counter == 71) {

          question_title.innerHTML = ''
          leftA.style.display = 'none';
          rightA.style.display = 'none';
          question.innerHTML = 'Sačekajte interpretaciju rezultata';

          sendResults(test_data)
        }
      })
      .catch(function (error) {
        console.log('Error getting question from Flask endpoint')
      })
  } else if (event.target.id === 'right_a') {
    counter++
    question_title.innerHTML = 'PITANJE #' + counter
    getQuestion(counter - 1)
      .then(function (data) {
        question.innerHTML = data['Q']
        leftA.innerHTML = data['A']
        rightA.innerHTML = data['B']
        test_data[counter - 1] = 'B'
        if (counter == 71) {

          question_title.innerHTML = ''
          leftA.style.display = 'none';
          rightA.style.display = 'none';
          question.innerHTML = 'Sačekajte interpretaciju rezultata';

          sendResults(test_data)
        }
      })
      .catch(function (error) {
        console.log('Error getting question from Flask endpoint')
      })
  }
}

function getQuestion(question_index) {
  return $.ajax({
    type: 'POST',
    url: '/pp0_QA',
    data: { integer_value: question_index },
    success: function (response) {
      console.log('Request for the question sent to Flask endpoint')
    },
    error: function (error) {
      console.log('Error sending test counter value to Flask endpoint')
    },
  })
}

function sendResults(hash_map) {
  data = JSON.stringify(hash_map)
  $.post('/pp_0_zavrseno', { results: data }, function (response) {
    sessionStorage.setItem('user_mbti_data_local', JSON.stringify(response))
    window.location.href = '/pp_0_zavrseno_render_page'
  }).fail(function () {
    console.log('Error submitting test results')
  })
}


