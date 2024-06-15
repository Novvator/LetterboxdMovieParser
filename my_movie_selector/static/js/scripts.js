document.getElementById('movie-form').onsubmit = function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);
    fetch('/get_movies', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var moviesDiv = document.getElementById('movies');
        moviesDiv.innerHTML = '';
        for (var movie in data) {
            var div = document.createElement('div');
            div.innerText = movie;
            moviesDiv.appendChild(div);
        }
    });
};