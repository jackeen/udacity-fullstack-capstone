import Fetch from "./fetch.mjs";

class MovieActorForm {
	
	id = 'movie_actor_form_' + new Date().getTime();
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

	lunch(mid) {

		let tpl = `
			<h3>Add Actor For Movie</h3>
			<form method="dialog">
				<input type="hidden" name="mid" value="${mid}"/>
				<input type="text" name="aid" placeholder="actor id"/>
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
		Fetch.patch(`/api/movies/${fd.get('mid')}/actors`, {
			actor_id: fd.get('aid'),
			attach_state: true,
		}, () => {
			this.onSubmit(fd.get('mid'));
		});
	}


}

export default MovieActorForm;