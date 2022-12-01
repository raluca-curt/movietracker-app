window.onload = () => {
    // Get movie id
    let movie = document.getElementById('interactions')
    let movie_id = movie.dataset.filmid

    // Get variables
    let watchlist = document.getElementById('watchlist')
    let watched = document.getElementById('watched')
    let liked = document.getElementById('liked')

    // Keep track of variables' status for the given movie id
    let added_to_watchlist = {'watchlist': 0, 'movie_id': movie_id}
    let added_to_watched = {'watched': 0, 'movie_id': movie_id}
    let added_to_liked = {'liked': 0, 'movie_id': movie_id}

    // Watchlist trigger
    watchlist.addEventListener('click', () => {
        // If watchlist does not have the class -on, add it
        if (watchlist.classList.contains('-on') === false)
        {
            watchlist.classList.add('-on')

            // Change icon
            watchlist.classList.add('bi-stopwatch-fill')
            watchlist.classList.remove('bi-stopwatch')

            // Update server data
            added_to_watchlist['watchlist'] = 1

        } else
        {
            watchlist.classList.remove('-on')

            // Change icon
            watchlist.classList.add('bi-stopwatch')
            watchlist.classList.remove('bi-stopwatch-fill')
        }

        $.ajax({
            type: 'POST',
            url: '/process_interaction',
            data: JSON.stringify(added_to_watchlist),
            contentType: 'application/json',
            dataType: 'json' 
        });
    })


    // Watched trigger
    watched.addEventListener('click', () => {
        // If watched does not have the class -on, add it
        if (watched.classList.contains('-on') === false)
        {
            watched.classList.add('-on')

            // Change icon
            watched.classList.add('bi-eye-fill')
            watched.classList.remove('bi-eye')

            // Update server data
            added_to_watched['watched'] = 1

        } else
        {
            watched.classList.remove('-on')

            // Change icon
            watched.classList.add('bi-eye')
            watched.classList.remove('bi-eye-fill')
        }

        $.ajax({
            type: 'POST',
            url: '/process_interaction',
            data: JSON.stringify(added_to_watched),
            contentType: 'application/json',
            dataType: 'json' 
        });
    })


    // Liked trigger
    liked.addEventListener('click', () => {
        // If liked does not have the class -on, add it
        if (liked.classList.contains('-on') === false)
        {
            liked.classList.add('-on')

            // Change icon
            liked.classList.add('bi-heart-fill')
            liked.classList.remove('bi-heart')

            // Update server data
            added_to_liked['liked'] = 1

        } else
        {
            liked.classList.remove('-on')

            // Change icon
            liked.classList.add('bi-heart')
            liked.classList.remove('bi-heart-fill')
        }

        $.ajax({
            type: 'POST',
            url: '/process_interaction',
            data: JSON.stringify(added_to_liked),
            contentType: 'application/json',
            dataType: 'json' 
        });
    })
}
