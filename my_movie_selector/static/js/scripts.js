// Example JavaScript code for your Flask application

// Example function to handle a form submission via AJAX
function handleFormSubmission(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    // Get the values from the form fields
    var username = document.getElementById('username').value;
    var genre = document.getElementById('genre').value;

    // Make an AJAX POST request to Flask endpoint '/get_random_movie'
    fetch('/get_random_movie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, genre: genre })
    })
    .then(response => response.json())
    .then(data => {
        // Update the HTML with the response data
        document.getElementById('movieTitle').innerText = data.title;
        document.getElementById('tmdbLink').innerHTML = `<a href="${data.tmdblink}">${data.tmdblink}</a>`;

        // Optionally update an image (ensure correct image path and ID)
        var imgElement = document.getElementById('moviePoster');
        imgElement.src = `/static/img.png?${new Date().getTime()}`;  // Add timestamp to force reload
        imgElement.alt = 'Movie Poster';

    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listener to form submission
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('movieForm');
    form.addEventListener('submit', handleFormSubmission);
});
