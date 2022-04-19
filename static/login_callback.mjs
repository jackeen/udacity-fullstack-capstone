import {storeToken} from './components/token.mjs';

let url = location.href.split('#')[1];
let param = new URLSearchParams(url);

let token = param.get('access_token');
let expires = param.get('expires_in');

storeToken(token, expires);

// back to home page
location.href = `${location.protocol}//${location.host}`;
