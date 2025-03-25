const carouselInner = document.querySelector('.carousel-inner');
const carouselItems = document.querySelectorAll('.carousel-item');
const overlay = document.querySelector('.overlay');
const prevButton = document.querySelector('.carousel-control.prev');
const nextButton = document.querySelector('.carousel-control.next');


const link = document.createElement("a");
link.href = "#"
link.target = "_blank";

let projects = ["python","js","php","html5","css"]
let currentIndex = 0;
function getThePage() {
    console.log(`indo para pagina do ${projects[currentIndex]}`)
    //let pagepath = `src/pages/${projects[currentIndex]}.html`
    if (pagepath) {
      //window.location.href = pagepath
    } else {
      //window.location.href = `src/pages/notfound.html`
    }
    
}

function updateCarousel() {
  // Remove todas as classes de estado
  carouselItems.forEach((item) => {
    item.classList.remove('active', 'prev', 'next');
    item.removeEventListener('click', getThePage)
  });

  // Adiciona a classe 'active' ao item central
  carouselItems[currentIndex].classList.add('active');
  carouselItems[currentIndex].addEventListener('click', getThePage, false);
  overlay.style.display='block';     
  
  //carouselItems[currentIndex]


  // Adiciona a classe 'prev' ao item anterior
  if (currentIndex > 0) {
    carouselItems[currentIndex - 1].classList.add('prev');
  }

  // Adiciona a classe 'next' ao próximo item
  if (currentIndex < carouselItems.length - 1) {
    carouselItems[currentIndex + 1].classList.add('next');
  }

  // Move o carrossel para o item atual
  const offset = -currentIndex * 25; // 25% por item (igual ao flex-basis)
  carouselInner.style.transform = `translateX(${offset}%)`;
  document.querySelector(".project-label").innerHTML = projects[currentIndex]
}

prevButton.addEventListener('click', () => {
  
  if (currentIndex > 0) {
    currentIndex--;
  } else {
    currentIndex = carouselItems.length - 1;
  }
  updateCarousel();
});

nextButton.addEventListener('click', () => {
    
  if (currentIndex < carouselItems.length - 1) {
    currentIndex++;
  } else {
    currentIndex = 0;
  }
  updateCarousel();
});

// Inicializa o carrossel
updateCarousel();