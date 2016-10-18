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
            'Accept': 'text/json'
        }
    })
    .then(res => res.json())
    .then(res => res.object)
    .then(callback)
}
