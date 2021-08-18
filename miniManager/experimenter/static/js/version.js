const BASE_URL = window.location.origin;
const ROUND_ENDPOINT = "/rodada";

const getDefaultHeaderToRequest = () => {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;;
    const headers = new Headers();
    headers.append('X-CSRFToken', csrfToken);
    return headers;
}

const postRound = async (versionID) => {
    const url = `${BASE_URL}${ROUND_ENDPOINT}`;
    const headers = getDefaultHeaderToRequest();

    const response = await fetch(url, {
        method: 'post',
        body: {
            version: versionID
        },
        headers: headers,
        credentials: 'include'
    });

    if(!response.ok){
        throw response.statusText
    }
}

const executeRound = async () => {
    try {     
        await postRound(1);
    } catch(err) {
        console.error(`Error: ${err}`);
    }
};

// Managing DOM elements
/*
const executeRoundButton = document.getElementById('execute-round-button');
executeRoundButton.addEventListener('click', executeRound);
*/