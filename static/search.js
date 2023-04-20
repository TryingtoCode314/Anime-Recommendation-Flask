// Get DOM elements
const animeInput = document.querySelector('#anime');
const animeList = document.querySelector('#anime-list');
const addBtn = document.querySelector('#add-btn');
const anilist = document.querySelector('#anilist');
const animeListInput = document.querySelector('#anime-list-input');
const submitBtn = document.querySelector('#submit-btn');



// Initialize anime list
let animeListData = [];

//check for entered ratings
function checkRating(ratingInput) {
    const rating = parseInt(ratingInput.value);
    if (rating < 1) {
      ratingInput.value = 1;
    }
    if (rating > 10) {
        ratingInput.value = 10;
      }
    
  }

// Add anime to list
function addAnimeToList() {
  // Get selected anime
  const selectedAnime = animeList.querySelector(`[value="${animeInput.value}"]`);

  // Check if anime is already in list
  if (animeListData.some(anime => anime.id === selectedAnime.dataset.id)) {
    alert('Anime is already in the list!');
    return;
  }

  // Add anime to list
  const anime = {
    id: selectedAnime.dataset.id,
    idx: selectedAnime.dataset.index,
    name: selectedAnime.value,
    rating: -1
  };
  animeListData.push(anime);

  // Create anime item
  const animeItem = document.createElement('div');
  animeItem.classList.add('anime-item');
  animeItem.dataset.id = anime.id;
  animeItem.dataset.index = anime.index;
  animeItem.innerHTML = `
    <span>${anime.name}</span>
    <input type="number" min="1" max="10" placeholder="Rating" oninput="checkRating(this)" onchange="updateAnimeRating('${anime.id}', this.value)">
    <button onclick="removeAnimeFromList('${anime.id}','${anime.idx}')">Remove</button>
  `;

  // Append anime item to Anilist
  anilist.appendChild(animeItem);

  // Remove anime from datalist
  selectedAnime.remove();

  // Update anime list input
  updateAnimeListInput();

  // Clear input field
  animeInput.value = '';
}

// Remove anime from list
function removeAnimeFromList(id, idx) {
    // Remove anime from list
    animeListData = animeListData.filter(anime => anime.id !== id);
  
    // Remove anime item from Anilist
    const animeItem = anilist.querySelector(`[data-id="${id}"]`);
    animeItem.remove();
  
    // Insert anime back to datalist at original position
    const animeName = animeItem.querySelector('span').textContent;
    const animeOption = document.createElement('option');
    animeOption.value = animeName;
    animeOption.dataset.id = id;
    animeOption.dataset.index = idx;  // set original index
    const options = animeList.querySelectorAll('option');
    const nextOption = options[idx];
    animeList.insertBefore(animeOption, nextOption);
  
    // Update anime list input
    updateAnimeListInput();
  }
  
  
  

// Update anime rating
function updateAnimeRating(id, rating) {
    
  // Update anime rating in list
  const anime = animeListData.find(anime => anime.id === id);
  anime.rating = rating;

  // Update anime list input
  updateAnimeListInput();
}

// Update anime list input
function updateAnimeListInput() {
  animeListInput.value = animeListData.map(anime => `(${anime.id},${anime.rating})`).join(',');
}

// Submit anime list
function submitAnimeList() {
  // Check if anime list is empty
  if (animeListData.length === 0) {
    alert('Anilist is empty!');
    return;
  }

  // Submit anime list
  submitBtn.disabled = true;
  animeListInput.disabled = false;
  submitBtn.form.submit();
}

// Add event listeners
addBtn.addEventListener('click', addAnimeToList);
submitBtn.addEventListener('click', submitAnimeList);

