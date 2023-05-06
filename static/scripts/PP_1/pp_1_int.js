fetch('/pp_1_int_results')
  .then((response) => response.json())
  .then((data) => {
    // Assign the values to the table cells by ID
    document.getElementById('size').textContent =
      'Veličina testirane populacije: ' + data[0]
    document.getElementById('high_factor_1').textContent = '- ' + data[1][0][0]
    document.getElementById('high_factor_2').textContent = '- ' + data[1][1][0]
    document.getElementById('high_factor_3').textContent = '- ' + data[1][2][0]
    document.getElementById('low_factors_1').textContent = '- ' + data[2][0][0]
    document.getElementById('low_factors_2').textContent = '- ' + data[2][1][0]
    document.getElementById('low_factors_3').textContent = '- ' + data[2][2][0]
  })
