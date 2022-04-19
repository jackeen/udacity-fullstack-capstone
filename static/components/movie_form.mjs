import Fetch from "./fetch.mjs";

class MovieForm {
	
	id = 'movie_form_' + new Date().getTime();
	isPost = true;
	instance = null;
	onSubmit = () => {};

	constructor({onSubmit}) {
		let dialog = document.createElement('dialog');
		dialog.id = this.id;
		document.body.append(dialog);
		this.instance = dialog;
		
		let form = this;
		dialog.addEventListener('click', (e) => {
			let target = e.target;
			let btn = target.dataset.btn;
			if (btn) {
				switch (btn) {
					case 'submit':
						form.postData();
						form.close();
						break;
					case 'cancel':
						form.close();
						break;
				}
			}
		});

		this.onSubmit = onSubmit;
	}

	lunch(data) {

		let id = '', title = '', release_date = '';

		if (data) {
			this.isPost = false;
			id = data.id;
			title = data.title;
			release_date = data.release_date;
		} else {
			this.isPost = true;
		}
		
		let header = 'Create New Movie';
		if (id) {
			header = `Edit Movie: ${id}`;
		}

		let tpl = `
			<h3>${header}</h3>
			<form method="dialog">
				<input type="hidden" name="id" value="${id}"/>
				<input type="text" name="title" value="${title}" placeholder="title"/>
				<input type="date" name="release_date" value="${release_date}"/>
			</form>
			<p class="btn">
				<button data-btn="submit">Submit</button>
				<button data-btn="cancel">Cancel</button>
			</p>
		`
		this.instance.innerHTML = tpl;
		this.instance.showModal();
	}

	close() {
		this.instance.close();
	}

	postData() {
		let f = this.instance.querySelector('form');
		let fd = new FormData(f);
		
		if (this.isPost) {
			Fetch.post('/api/movies', {
				title: fd.get('title'),
				release_date: fd.get('release_date'),
			}, () => {
				this.onSubmit();
			})
		} else {
			Fetch.patch('/api/movies/' + fd.get('id'), {
				title: fd.get('title'),
				release_date: fd.get('release_date'),
			}, () => {
				this.onSubmit();
			})
		}
	}


}

export default MovieForm;