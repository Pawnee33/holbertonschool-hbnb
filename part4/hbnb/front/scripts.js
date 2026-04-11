/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

/* ============================================================
   DOM INITIALIZATION
   - Listens for DOMContentLoaded to ensure HTML is fully loaded
     before executing any code.
   - Attaches event listeners to the login form and the review form.
   - Calls checkAuthentication() and retrieves the place ID from URL.
   ============================================================ */
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
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const placeTitle = document.getElementById('place-title');

    if (placeTitle) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
                .then(r => r.json())
                .then(data => {
                    placeTitle.innerHTML = `<strong>Reviewing:</strong> ${data.title}`;
                });
        }
    }
 
    if (reviewForm) { 
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Get review text from form
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            // Make AJAX request to submit review
            // Handle the response
            if (!token) {
                alert("You must be logged in");
                return;
            }

            if (!placeId) {
                alert("Invalid place");
                return;
            }

            if (!reviewText) {
                alert("Review cannot be empty");
                return;
            }

            if (!rating) {
                alert("Please select a rating");
                return;
            }

            await submitReview(token, placeId, reviewText, rating);
        });
    }
    /* ============================================================
    INTERACTIVE STAR RATING
    - Selects all clickable star elements (.star).
    - On click: updates the hidden #rating input with the selected
      value and toggles filled/empty stars (★/☆) up to that value.
    ============================================================ */
    const stars = document.querySelectorAll('.star');
    if (stars.length > 0) {
        stars.forEach(star => {
            star.addEventListener('click', () => {
                const value = star.dataset.value;
                document.getElementById('rating').value = value;
                stars.forEach(s => {
                    s.textContent = s.dataset.value <= value ? '★' : '☆';
                    s.classList.toggle('selected', s.dataset.value <= value);
                });
            });
        });
    }
});

/* ============================================================
   PLACE IMAGE MAPPING
   - Maps each place name to an array of 3 images used
     in the image slider on the place details page.
   ============================================================ */
const placeImages = {
    'Beautiful Beach House': ['images/Beautiful-Beach_House.jpg', 'images/Beautiful-Beach_House2.jpg', 'images/Beautiful-Beach_House3.jpg'],
    'Rouna': ['images/Rouna.jpg', 'images/Rouna2.jpg', 'images/Rouna3.jpg'],
    'Golden Apple': ['images/Golden_Apple.jpg', 'images/Golden_Apple2.jpg', 'images/Golden_Apple3.jpg'],
    'Corsica': ['images/Corsica.jpg', 'images/Corsica2.jpg', 'images/Corsica3.jpg']
};

/* ============================================================
   USER LOGIN
   - Sends a POST request to the API with email and password.
   - On success: stores the JWT token in a cookie and redirects
     the user to index.html.
   - On failure: displays an alert with the error message.
   ============================================================ */
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

/* ============================================================
   AUTHENTICATION CHECK
   - Reads the "token" cookie to determine if the user is logged in.
   - Shows/hides the login link, logout button, and "add-review"
     section based on the authentication state.
   - If authenticated: triggers place list loading (index) or
     place details loading (place.html).
   - If not authenticated on add_review.html: redirects to index.html.
   - Returns the token for later use.
   ============================================================ */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
      if (document.getElementById('review-form')) {
        window.location.href = 'index.html';
      }
      if (loginLink) loginLink.style.display = 'block';
      if (logoutButton) logoutButton.style.display = 'none';
      if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'block';
        // Fetch places data if the user is authenticated
        
        
      }
      const placesList = document.getElementById('places-list');
      if (placesList) fetchPlaces(token);
      const placeId = getPlaceIdFromURL();
      if (placeId) fetchPlaceDetails(token, placeId);
      return token;
}

/* ============================================================
   LOGOUT
   - Deletes the token cookie by setting a past expiration date.
   - Redirects the user to the login page.
   ============================================================ */
function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = 'login.html';
}

/* ============================================================
   UTILITY: READ A COOKIE BY NAME
   - Iterates over all browser cookies to find the one matching
     the given name.
   - Returns its value, or null if not found.
   ============================================================ */
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    const cookie = cookies.find(cookie => cookie.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : null;
}

/* ============================================================
   FETCH PLACES LIST (API)
   - Sends an authenticated GET request to retrieve all places.
   - Passes the response data to displayPlaces() for rendering.
   ============================================================ */
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

/* ============================================================
   DISPLAY PLACES LIST (DOM)
   - Clears the #places-list container.
   - For each place, creates a card with an image, title, price,
     and a "View Details" button linking to place.html?id=...
   - Stores the price in a data-price attribute for client-side filtering.
   ============================================================ */
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
      <img src="${placeImages[place.title] ? placeImages[place.title][0] : ''}" alt="${place.title}" style="width:100%; border-radius:10px;">
      <h2>${place.title}</h2>
      <p>Price per night: $${place.price}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
      `;
      // Append the created element to the places list
      placesList.appendChild(card);
      console.log(place.title);
    });
}

/* ============================================================
   CLIENT-SIDE PRICE FILTER
   - Listens for changes on the #price-filter dropdown.
   - Shows or hides place cards based on whether their price
     is within the selected range.
   - Selecting "All" removes the filter and shows every card.
   ============================================================ */
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

/* ============================================================
   UTILITY: GET PLACE ID FROM URL
   - Reads the "id" query parameter from the current page URL.
   - Returns its value, or null if absent.
   ============================================================ */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/* ============================================================
   FETCH PLACE DETAILS (API)
   - Sends an authenticated GET request for a specific place.
   - Passes the response data to displayPlaceDetails() for rendering.
   ============================================================ */
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

/* ============================================================
   DISPLAY PLACE DETAILS (DOM)
   - Clears the #place-details container.
   - Builds an image slider with previous/next navigation buttons.
   - Displays host name, price, description, and amenities with icons.
   - Generates review cards with star ratings inside #reviews.
   ============================================================ */
function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '';
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Place title
    const title = document.createElement('h2');
    title.textContent = place.title;
    placeDetails.appendChild(title);

    // --- Image slider ---
    const images = placeImages[place.title] || [];
    let currentIndex = 0;

    const sliderDiv = document.createElement('div');
    sliderDiv.style.position = 'relative';
    sliderDiv.style.textAlign = 'center';
    sliderDiv.style.maxWidth = '900px';
    sliderDiv.style.margin = '0 auto';

    const img = document.createElement('img');
    img.src = images[0] || '';
    img.alt = place.title;
    img.style.width = '100%';
    img.style.borderRadius = '10px';
    img.style.maxHeight = '900px';
    img.style.objectFit = 'cover';

    // Previous image button
    const prevBtn = document.createElement('button');
    prevBtn.textContent = '◀';
    prevBtn.style.position = 'absolute';
    prevBtn.style.left = '10px';
    prevBtn.style.top = '50%';
    prevBtn.style.transform = 'translateY(-50%)';
    prevBtn.style.background = 'rgba(0,0,0,0.5)';
    prevBtn.style.color = '#fff';
    prevBtn.style.border = 'none';
    prevBtn.style.borderRadius = '50%';
    prevBtn.style.cursor = 'pointer';
    prevBtn.style.padding = '10px';
    prevBtn.onclick = () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        img.src = images[currentIndex];
    };

    // Next image button
    const nextBtn = document.createElement('button');
    nextBtn.textContent = '▶';
    nextBtn.style.position = 'absolute';
    nextBtn.style.right = '10px';
    nextBtn.style.top = '50%';
    nextBtn.style.transform = 'translateY(-50%)';
    nextBtn.style.background = 'rgba(0,0,0,0.5)';
    nextBtn.style.color = '#fff';
    nextBtn.style.border = 'none';
    nextBtn.style.borderRadius = '50%';
    nextBtn.style.cursor = 'pointer';
    nextBtn.style.padding = '10px';
    nextBtn.onclick = () => {
        currentIndex = (currentIndex + 1) % images.length;
        img.src = images[currentIndex];
    };

    sliderDiv.appendChild(prevBtn);
    sliderDiv.appendChild(img);
    sliderDiv.appendChild(nextBtn);
    placeDetails.appendChild(sliderDiv);
    
    // --- Amenity icon mapping ---
    const amenityIcons = {
    'WiFi': 'images/icon_wifi.png',
    'Pool': 'images/icon_pool.png',
    'Air Conditioning': 'images/icon_air-conditioner.png',
    'Bathtub': 'images/icon_bath.png',
    'King Size Bed': 'images/icon_bed.png'
  };

    // Main place information block
    const div = document.createElement('div');
    div.classList.add('place-details');
    div.innerHTML = `
        <p class="place-info"><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
        <p class="place-info"><strong>Price per night:</strong> $${place.price}</p>
        <p class="place-info"><strong>Description:</strong> ${place.description}</p>
        <p class="place-info"><strong>Amenities:</strong> ${place.amenities.map(a => `<img src="${amenityIcons[a.name] || ''}" width="20"> ${a.name}`).join(', ')}</p>
    `;
    placeDetails.appendChild(div);

    // Bouton Add a Review
    const token = getCookie('token');
    const addReviewBtn = document.createElement('a');

    if (token) {
        addReviewBtn.href = `add_review.html?id=${place.id}`;
        addReviewBtn.textContent = 'Add a Review';
    } else {
        addReviewBtn.href = '#';
        addReviewBtn.textContent = 'Add a Review';
        addReviewBtn.onclick = (e) => {
            e.preventDefault();
            alert('You must be logged in to add a review!');
        };
    }

    addReviewBtn.classList.add('details-button');
    addReviewBtn.style.display = 'block';
    addReviewBtn.style.textAlign = 'center';
    addReviewBtn.style.margin = '20px auto';
    addReviewBtn.style.maxWidth = '200px';
    placeDetails.appendChild(addReviewBtn);
    
    // --- Reviews section ---
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    place.reviews.forEach(review => {
        const card = document.createElement('div');
        card.classList.add('review-card');
        card.innerHTML = `
            <p><strong>${review.user_name}:</strong></p>
            <p>${review.text}</p>
            <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
        `;
        // Append the created elements to the place details section
        reviewsSection.appendChild(card);
});
}

/* ============================================================
   SUBMIT A REVIEW (API)
   - Sends an authenticated POST request with the review text,
     rating, and place ID.
   - Delegates response handling to handleResponse().
   ============================================================ */
async function submitReview(token, placeId, reviewText, rating) {
    try {
        // Make a POST request to submit review data
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Include the token in the Authorization header
                'Authorization': `Bearer ${token}`
            },
            // Send placeId and reviewText in the request body
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating, 10),
                place_id: placeId
            })
        });
        // Handle the response
        const data = await response.json();
        handleResponse(response, data,placeId);
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Network error. Please try again.');
    }
}

/* ============================================================
   HANDLE REVIEW SUBMISSION RESPONSE
   - On success: shows a confirmation alert, resets the form,
     and redirects to the place details page.
   - On failure: displays an error alert.
   ============================================================ */
function handleResponse(response, data, placeId) {
    if (response.ok) {
        alert('Review submitted successfully!');
        // Clear the form
        document.getElementById('review-form').reset();
        // Redirect back to the place page
        window.location.href = `place.html?id=${placeId}`;
    } else {
        alert(data.message || 'Failed to submit review');
    }
}
