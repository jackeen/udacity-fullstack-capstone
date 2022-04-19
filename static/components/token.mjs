
const config = {
	tokenName: 'token',
	tokenExpiresName: 'expires'
}

function storeToken(token, expires) {
	let t = new Date().getTime();
	expires = parseInt(expires)*1000 + t;
	localStorage.setItem(config.tokenName, token);
	localStorage.setItem(config.tokenExpiresName, expires);
}

function retrieveToken() {
	let token = localStorage.getItem(config.tokenName);
	let expires = localStorage.getItem(config.tokenExpiresName);
	let t = new Date().getTime();
	if (parseInt(expires) > t) {
		return token;
	}
	return null;
}

function cleanToken() {
	localStorage.removeItem(config.tokenName);
	localStorage.removeItem(config.tokenExpiresName);
}

export {storeToken, retrieveToken, cleanToken};