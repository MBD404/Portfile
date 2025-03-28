function changePage(){
    let page = document.getElementById('pages');
    var selected = page.options[page.selectedIndex].value 

    switch (selected) {
        case 'python':
            window.location.href=`./${selected}.html`
            break;
        case 'js':
            window.location.href=`./${selected}.html`
            break;
        case 'php':
            window.location.href=`./${selected}.html`
            break;
        case 'html5':
            window.location.href=`./${selected}.html`
            break;
        case 'css3':
            window.location.href=`./${selected}.html`
            break;
    
        default:
            break;
    }
}