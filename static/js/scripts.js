document.getElementById('recommendForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const movieInput = document.getElementById('movieInput').value.trim();
    
    if (!movieInput) {
        alert('Please enter a movie name.');
        return;
    }
    
    fetch('/recommend_movie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'favorite_movie': movieInput
        })
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = '';  // Clear previous recommendations
        
        if (data.recommended_movies && data.recommended_movies.length > 0) {
            data.recommended_movies.forEach(movie => {
                const movieElement = document.createElement('div');
                movieElement.textContent = movie;
                movieElement.className = 'recommend-block';  // Apply CSS class for styling
                recommendationsDiv.appendChild(movieElement);
            });
        } else {
            recommendationsDiv.textContent = 'No recommendations available...Can you try using meaningfull tagname';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching recommendations. Please try again.');
    });
});
