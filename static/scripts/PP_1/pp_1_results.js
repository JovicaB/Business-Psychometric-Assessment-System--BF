let results
let suggestions
let chart_data
let result_table = document.getElementById('results_table')
let suggestion_table = document.getElementById('suggestion_table')
var chart_results = document.getElementById('line-chart')

//FETCH RESULTS
fetch('/pp_1_results')
  .then((response) => response.json())
  .then((data) => {
    results = data.data
    suggestions = data.data_sug
    chart_data = [
        results[0],
        results[1],
        results[2],
        results[3],
        results[4],
        results[5],
        results[6],
        results[7],
        results[8],
        results[9],
        results[10],
        results[11],
        results[12],
        results[13],
        results[14],
        results[15],
        results[16],
        results[17],
        results[18],
        results[19],
        results[20],
    ]
    populateResultsTable(result_table, results)
    populateSuggestionTable(suggestion_table, suggestions)
    updateChartData(results)
  })

//reload results (clear and populate)
  function populateResultsTable(table, data) {
    for (var i = 1; i < table.rows.length; i++) {
      var row = table.rows[i]
      row.cells[1].innerHTML = ''
    }
  
    for (var i = 0; i < data.length; i++) {
      var row = table.rows[i + 1]
      var col2 = row.cells[1]
      col2.innerHTML = Number(data[i]).toFixed(2)
    }
  }

  //clear results
  function populateSuggestionTable(table, data) {
    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];
        row.cells[0].innerHTML = '';
    }
    for (var i = 0; i < data.length; i++) {
        var row = table.rows[i + 1];
        if (!row) {
            row = table.insertRow(-1);
        }
        var col1 = row.insertCell(0);
        col1.innerHTML = data[i];
    }
}

// chart settings
var data = {
  labels: [
    '#1',
    '#2',
    '#3',
    '#4',
    '#5',
    '#6',
    '#7',
    '#8',
    '#9',
    '#10',
    '#11',
    '#12',
    '#13',
    '#14',
    '#15',
    '#16',
    '#17',
    '#18',
    '#19',
    '#20',
  ],
  datasets: [
    {
      label: 'prosečna ocena: ',
      data: chart_data,
      backgroundColor: 'rgba(201, 203, 207, 0.2)',
      borderColor: 'rgba(0, 0, 0, 1)',
      borderWidth: 1,
      pointHoverBackgroundColor: 'rgba(0, 0, 0, 1)',
      pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
      lineTension: 0,
    },
  ],

  options: {
    legend: {
      display: false,
    },
    scales: {
      yAxes: [
        {
          gridLines: {
            color: 'rgba(80, 255, 80, 0.1)',
          },
        },
      ],
      xAxes: [
        {
          gridLines: {
            display: false,
          },
        },
      ],
    },
  },
}

var ctx = document.getElementById('line-chart').getContext('2d')
var chart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            suggestedMin: 0,
            suggestedMax: 5,
          },
          gridLines: {
            //display: false,
          },
        },
      ],
      xAxes: [
        {
          gridLines: {
            display: false,
          },
        },
      ],
    },
  },
})

function updateChartData(newData) {
  chart.options.legend.display = false
  chart.data.datasets[0].data = newData

  // Minimum value
  const minVal = Math.min(...newData.slice(0, 20))

  // minimum value indexes
  const minIndices = newData
    .map((value, index) => ({ value, index })) // Add the index to each value
    .filter(({ value }) => value === minVal) // Filter values that are equal to the minimum
    .map(({ index }) => index) // Extract the indices

  const maxVal = Math.max(...newData.slice(0, 20))

  const maxIndices = newData
    .map((value, index) => ({ value, index })) // Add the index to each value
    .filter(({ value }) => value === maxVal) // Filter values that are equal to the minimum
    .map(({ index }) => index) // Extract the indices

  // Set the color of each data point
  const colors = newData.map((value, index) => {
    if (minIndices.includes(index)) {
      return 'rgba(179, 80, 80, 0.3)' // Red color for minimum values
    } else if (maxIndices.includes(index)) {
      return 'rgba(134, 180, 116, 0.3)' // Green color for maximum values
    } else {
      return 'rgba(201, 203, 207, 0.2)' // Default color for other values
    }
  })

  // Update the dataset with the new colors
  chart.data.datasets[0].backgroundColor = colors

  // Update the chart
  chart.update()
}