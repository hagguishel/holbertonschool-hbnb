const currentPage = window.location.pathname;
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname;

    if (currentPage.includes('login.html')) {
        const form = document.getElementById('login-form');
        if (form) {
            form.addEventListener('submit', async (event) => {
                event.preventDefault();

                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;

                try {
                    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email, password }),
                        credentials: 'include'
                    });

                    if (!response.ok) {
                        const data = await response.json();
                        alert('❌ ' + (data.error || response.statusText));
                        return;
                    }

                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } catch (error) {
                    console.error("❌ Erreur de connexion :", error);
                    alert('Impossible de se connecter au serveur.');
                }
            });
        }
    }

    if (currentPage.includes('index.html')) {
        checkAuthentication();

        const filter = document.getElementById('price-filter');
        if (filter) {
            filter.addEventListener('change', (event) => {
                const selectedPrice = event.target.value;
                const cards = document.querySelectorAll('.place-card');

                cards.forEach(card => {
                    const price = parseFloat(card.getAttribute('data-price'));
                    if (selectedPrice === 'All' || price <= parseFloat(selectedPrice)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }
    }
});

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Erreur lors de la récupération des lieux');

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Erreur fetch places :', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';

    places.forEach(place => {
        const div = document.createElement('div');
        div.className = 'place-card';
        div.setAttribute('data-price', place.price);

        div.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p>Price: $${place.price}</p>
            <p>Location: ${place.latitude}, ${place.longitude}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(div);
    });
}

if (currentPage.includes('place.html')) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    fetchPlaceDetails(token, placeId);
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error('Erreur lors de la récupération des détails du lieu');

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error('Erreur fetch place details :', error);
    }
}

function displayPlaceDetails(place) {
    const details = document.getElementById('place-details');
    if (!details) return;

    details.innerHTML = `
        <h2>${place.title}</h2>
        <p>${place.description}</p>
        <p>Price: $${place.price}</p>
        <p>Location: ${place.latitude}, ${place.longitude}</p>
        <h4>Amenities</h4>
        <ul>${(place.amenities || []).map(a => `<li>${a}</li>`).join('')}</ul>
        <h4>Reviews</h4>
        <ul>${(place.reviews || []).map(r => `<li>${r.user}: ${r.text}</li>`).join('')}</ul>
    `;
}
if (currentPage.includes('add_review.html')) {
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();
  const form = document.querySelector('.form');

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            text: reviewText,
            rating: rating,
            place_id: placeId
          })
        });
        if (response.ok) {
          alert('✅ Review submitted!');
        form.reset();
      } else {
        const data = await response.json();
        alert('❌ Error: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Submit review error:', error);
      alert('❌ Server error while submitting review.');
    }
  });
}}
