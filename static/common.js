/**
 * Fetching data from API on the server with a GET request.
 * 
 * @param {string} url The url to get from.
 * @param {function} callback The function to recieve the async data.
 */
function getData (url, callback) {
    fetch(url, {
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(function(res) { return res.json() })
    .then(function(res) { return res.object })
    .then(callback)
}

/**
 * Fetching data from Spotify API from id of a band on the server with a GET request.
 * 
 * @param {string} id The id to get spotify_artist_id from.
 * @param {function} callback The function to recieve the async data.
 */
function getSpotifyDataFromBand (id, callback) {
    getData('/band/' + id + '/', function(data) {
        fetch('https://api.spotify.com/v1/artists/' + data.spotify_artist_id + '/')
        .then(function(res) { return res.json() })
        .then(callback)
    })
}
