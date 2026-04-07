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
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        loginLink.style.display = 'block';
        logoutButton.style.display = 'none';
    } else {
        loginLink.style.display = 'none';
        logoutButton.style.display = 'block';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
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

document.getElementById('price-filter').addEventListener('change', (event) => {
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