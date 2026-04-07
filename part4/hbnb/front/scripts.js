/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Your code to handle form submission
            const email = loginForm.elements.email.value
            const password = loginForm.elements.password.value
            loginUser(email, password);
        });
    }
    checkAuthentication();
});

async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    // Handle the response
    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
      console.log("Success:", data);
    } else {
      alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutButton) logoutButton.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'block';
        // Fetch places data if the user is authenticated
        const placesList = document.getElementById('places-list');
        if (placesList) fetchPlaces(token);

        const placeId = getPlaceIdFromURL();
        if (placeId) fetchPlaceDetails(token, placeId);
    }
}

function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = 'login.html';
}

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    const cookie = cookies.find(cookie => cookie.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : null;
}

async function fetchPlaces(token) {
    // Make a GET request to fetch places data
    try {
      const request = await fetch('http://127.0.0.1:5000/api/v1/places/', {
        method: 'GET',
        // Include the token in the Authorization header
        headers: {
            'Authorization': `Bearer ${token}`
        },
      });
      // Handle the response and pass the data to displayPlaces function
      if (request.ok) {
      let data = await request.json();
      console.log("Success:", data);
      displayPlaces(data);
    } else {
      alert('Login failed: ' + request.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function displayPlaces(places) {
    // Clear the current content of the places list
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
    // Iterate over the places data
    places.forEach(place => {
      // For each place, create a div element and set its content
      const card = document.createElement('div');
      card.classList.add('place-card');
      card.dataset.price = place.price;
      card.innerHTML = `
      <h2>${place.title}</h2>
      <p>Price per night: $${place.price}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
      `;
      // Append the created element to the places list
      placesList.appendChild(card);
      console.log(place.title);
    });
}
const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
  priceFilter.addEventListener('change', (event) => {
      // Get the selected price value
      const selectedPrice = event.target.value;
      // Iterate over the places and show/hide them based on the selected price
      document.querySelectorAll('.place-card').forEach(card => {
        if (selectedPrice === 'All') {
          card.style.display = 'block';
        } else {
          if (parseFloat(card.dataset.price) <= parseFloat(selectedPrice)) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        }
      });
  });
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
      const request = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        // Include the token in the Authorization header
        headers: {
            'Authorization': `Bearer ${token}`
        },
      });
      // Handle the response and pass the data to displayPlaces function
      if (request.ok) {
      let data = await request.json();
      console.log("Success:", data);
      displayPlaceDetails(data);
    } else {
      alert('Login failed: ' + request.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '';
    // Create elements to display the place details (name, description, price, amenities and reviews)
    const title = document.createElement('h2');
    title.textContent = place.title;
    placeDetails.appendChild(title);

    const div = document.createElement('div');
    div.classList.add('place-details');
    div.innerHTML = `
        <p class="place-info"><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
        <p class="place-info"><strong>Price per night:</strong> $${place.price}</p>
        <p class="place-info"><strong>Description:</strong> ${place.description}</p>
        <p class="place-info"><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
    `;
    placeDetails.appendChild(div);
    
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    place.reviews.forEach(review => {
        const card = document.createElement('div');
        card.classList.add('review-card');
        card.innerHTML = `
            <p><strong>${review.user_id}</strong></p>
            <p>${review.text}</p>
            <p>Rating: ${review.rating}</p>
        `;
        // Append the created elements to the place details section
        reviewsSection.appendChild(card);
});
}
