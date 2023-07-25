const BASE = "form";
const CORRECT = "green";
const INCORRECT = "red";

function check() {
    let correct = 0;
    let total = ANSWERS.length;
    
    for (let i = 0; i < total; ++i) {
        let field = document.getElementById(BASE + i);
        
        if (field.value === ANSWERS[i]) {
            ++correct;
            field.style.background = CORRECT;
        }
        
        else {
            field.style.background = INCORRECT;
        }
    }
    
    window.alert(correct + "/" + total);
}

function checkKey(e) {
    if (e.key === "Enter") {
        check();
    }
}