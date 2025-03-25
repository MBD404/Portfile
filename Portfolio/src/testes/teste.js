
var radio = document.querySelector('.manual-btn')
var cont = 1;

document.getElementById('radio1').checked = true;

setInterval(() => {
    proximaImg()
}, 25000);

function proximaImg() {
    cont++


    if (cont > 6){
        cont = 1
    }

    document.getElementById('radio'+cont).checked = true;

}