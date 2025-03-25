const carouselInner = document.querySelector('.carousel-inner');
const carouselItems = document.querySelectorAll('.carousel-item');
const carousel = document.querySelector('.carousel');
const overlay = document.querySelector('.overlay');
const images = document.querySelectorAll('.image');
const prevButton = document.querySelector('.carousel-control.prev');
const nextButton = document.querySelector('.carousel-control.next');


const transitionanimate = [
  { background: "rgba(0, 0, 0, 0)" },
  { background: "rgba(0, 0, 0, 1)" },
];

const transitionTiming = {
  duration: 1200,
  iterations: 1,
}


document.addEventListener("DOMContentLoaded", function () {
carouselItems.forEach(item => {
  item.addEventListener('click', function () {
    if (item.classList.contains("active"))
      {
      window.scroll({
        top: 750,
        behavior: "smooth"
      })
      carouselItems.forEach(i => { 
        i.classList.remove('active');
      });
      this.classList.add('active');

      if (item.classList.contains('active')) {[
        this.style.opacity = '1'
      ]}
      carousel.classList.add('active')
      
      
    }
  });
});
images.forEach(image => {
  image.addEventListener('click', function() {
      carouselItems
      images.forEach(img => {
        img.classList.remove('active');
        img.classList.add("off")
      });

      this.classList.add('active');
      if (image.classList.contains("active")) {
          this.style.opacity='1'
          

          overlay.style.display = 'block'
          overlay.animate(transitionanimate, transitionTiming)
          prevButton.style.opacity='0'
          nextButton.style.opacity='0'
      }
      
  });
});
overlay.addEventListener("click", function () {
  this.style.display = 'none';

  carouselItems.forEach(item=> item.classList.remove('active'));
})

const link = document.createElement("a");
link.href = "#"
link.target = "_blank";

let projects = ["python","js","php","html5","css"]
let currentIndex = 0;


function getThePage() {
    console.log(`indo para pagina do ${projects[currentIndex]}`)
    let pagepath = `src/pages/${projects[currentIndex]}.html`

    if (pagepath) {
     
      //overlay.style.display = 'block';
      carouselItems[currentIndex].classList.add('ativo');
      setTimeout(()=>{window.location.href = pagepath},800)
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
  carouselItems[currentIndex].addEventListener('click', getThePage, false)     

 
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

})