window.onload = function () {
    const user_mbti_data_local = sessionStorage.getItem('user_mbti_data_local');
    user_data = JSON.parse(user_mbti_data_local)
    distributeData(user_data);
    $(document).ready(function() {
        $.get('/get_user_mbti_data', function(data) {
            console.log("Received data from server:", data);
        });
    });
};


var mbti_title = document.getElementById("int_title");
var mbti_subtitle = document.getElementById("int_sub_title");
var mbti_dim1 = document.getElementById("dimEI");
var mbti_dim2 = document.getElementById("dimSN");
var mbti_dim3 = document.getElementById("dimTF");
var mbti_dim4 = document.getElementById("dimJP");

var mbti_description = document.getElementById("int_description_text");
var mbti_career = document.getElementById("int_career_text");
var mbti_strenghts = document.getElementById("str_table");

function distributeData (data) {
    mbti_title.innerHTML = data['type']
    mbti_subtitle.innerHTML = data['title']

    mbti_dim1.innerHTML = 'ekstraverzija: ' + data['dimensions']['EI'][0]*100 + '% | introverzija: ' + data['dimensions']['EI'][1]*100 + '%';
    mbti_dim2.innerHTML = 'senzornost: ' + data['dimensions']['SN'][0]*100 + '% | intuicija: ' + data['dimensions']['SN'][1]*100 + '%';
    mbti_dim3.innerHTML = 'mišljenje: ' + data['dimensions']['TF'][0]*100 + '% | emocije: ' + data['dimensions']['TF'][1]*100 + '%';
    mbti_dim4.innerHTML = 'rasuđivanje: ' + data['dimensions']['JP'][0]*100 + '% | iskustvo/zapažanje: ' + data['dimensions']['JP'][1]*100 + '%';

    mbti_description.innerHTML = data['description']
    mbti_career.innerHTML = data['career']
    populateStrengths(data['strengths'])
    populateWeaknesses(data['weaknesses'])
    populateRules(data['rules'])
}

function populateStrengths(strengths) {
    const table = document.getElementById("str_table");
  
    // Clear any existing rows in the table
    while (table.rows.length > 1) {
      table.deleteRow(-1);
    }
  
    // Add a row for each strength
    for (let i = 0; i < strengths.length; i++) {
      const row = table.insertRow(-1);
      const cell = row.insertCell(0);
      cell.textContent = '- ' + strengths[i];
    }
  }
  
  function populateWeaknesses(strengths) {
    const table = document.getElementById("weak_table");
  
    // Clear any existing rows in the table
    while (table.rows.length > 1) {
      table.deleteRow(-1);
    }
  
    // Add a row for each strength
    for (let i = 0; i < strengths.length; i++) {
      const row = table.insertRow(-1);
      const cell = row.insertCell(0);
      cell.textContent = '- ' + strengths[i];
    }
  }

  function populateRules(strengths) {
    const table = document.getElementById("sug_table");
  
    // Clear any existing rows in the table
    while (table.rows.length > 1) {
      table.deleteRow(-1);
    }
  
    // Add a row for each strength
    for (let i = 0; i < strengths.length; i++) {
      const row = table.insertRow(-1);
      const cell = row.insertCell(0);
      cell.textContent = strengths[i];
    }
  }
       
