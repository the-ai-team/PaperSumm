// should send a post request to the server with the data
const fetchAPI = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify(data),
        });
        return response.json();
    } catch (e) {
        console.error(e);
    }
}

// async function fetchAPIWith(url, data) {
(async () => {
    const summary = await fetchAPI('http://localhost:8000/generate', {
        url: 'https://arxiv.org/abs/1512.03385',
        keyword: 'Experiments and results',
    })
console.log(summary);
})()
