const button = document.getElementById("pp0_button");
const url_label = document.getElementById("link");

button.addEventListener("click", () => {
    fetch("/pp_0_gen_but")
      .then(response => response.text())
      .then(data => {
        url_label.innerHTML = 'http://127.0.0.1:5000/' + data; //IZMENA
        navigator.clipboard.writeText('http://127.0.0.1:5000/' + data); //IZMENA
      });
  });
