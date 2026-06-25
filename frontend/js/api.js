const BASE_URL = "http://127.0.0.1:8018";

async function callAPI(method) {

    const response = await fetch(
        `${BASE_URL}/api/method/${method}`
    );

    const data = await response.json();

    return data.message;
}