let MBTI_results
let MBTI_code
let MBTI_personality_title
let MBTI_personality_description

window.onload = function () {
    getInterpretation("INTJ", function() {
        document.getElementById("int_title").textContent = 1;
        document.getElementById("int_sub_title").textContent = 2;
        document.getElementById("int_description").textContent = MBTI_personality_description;
    });
};

function getInterpretation(input_data, callback) {
    if (!input_data) {
        return Promise.resolve();
    } else {
        const data = input_data;
        return fetch('/pp_0_type_indicator', { //IZMENA
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((data) => {
            MBTI_results = JSON.stringify(data);
            MBTI_results = JSON.parse(MBTI_results);
            MBTI_code = MBTI_results['MBTI_code'];
            MBTI_personality_title = MBTI_results['MBTI_personality_title'];
            MBTI_personality_description = MBTI_results['MBTI_personality_description'];
            if (callback) {
                callback();
            }
        })
    }
}