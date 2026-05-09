const citySelected = document.querySelector('.city__selected');
const cityList = document.querySelector('.city__list');
const selectedText = document.querySelector('.selected__text');
const cityOptions = document.querySelectorAll('.city__option');

citySelected.addEventListener('click', () => {
  citySelected.classList.toggle('city__selected--active');
  cityList.classList.toggle('city__list--active');
});

cityOptions.forEach(option => {
  option.addEventListener('click', () => {
    selectedText.textContent = option.textContent;
    
    citySelected.classList.remove('city__selected--active');
    cityList.classList.remove('city__list--active');
  });
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('.city')) {
    citySelected.classList.remove('city__selected--active');
    cityList.classList.remove('city__list--active');
  }
});
