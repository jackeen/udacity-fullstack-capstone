import {retrieveToken} from './token.mjs';

class Fetch {

	static checkToken() {
		let token = retrieveToken();
		if (token === null) {
			alert('The token is expired or missing, please to login.');
			return false;
		}
		return true;
	}

	static get(url, fn) {
		this.checkToken();
		fetch(url, {
			method: 'GET',
			cache: 'no-cache',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + retrieveToken()
			}
		}).then(data => data.json()).then(json => {
			if (json.success) {
				fn(json);
			} else {
				alert(json.message);
			}
		});
	}

	static post(url, data, fn) {
		this.checkToken();
		fetch(url, {
			method: 'POST',
			cache: 'no-cache',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + retrieveToken()
			},
			body: JSON.stringify(data)
		}).then(data => data.json()).then(json => {
			if (json.success) {
				fn(json);
			} else {
				alert(json.message);
			}
		});
	}

	static patch(url, data, fn) {
		this.checkToken();
		fetch(url, {
			method: 'PATCH',
			cache: 'no-cache',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + retrieveToken()
			},
			body: JSON.stringify(data)
		}).then(data => data.json()).then(json => {
			if (json.success) {
				fn(json);
			} else {
				alert(json.message);
			}
		});
	}

	static delete(url, fn) {
		this.checkToken();
		fetch(url, {
			method: 'DELETE',
			cache: 'no-cache',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + retrieveToken()
			}
		}).then(data => data.json()).then(json => {
			if (json.success) {
				fn(json);
			} else {
				alert(json.message);
			}
		});
	}

}

export default Fetch;