import Fetch from "./fetch.mjs";

class ActorForm {
	
	id = 'actor_form_' + new Date().getTime();
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

		let id = '', name = '', age = '', gender = true;

		if (data) {
			this.isPost = false;
			id = data.id;
			name = data.name;
			age = data.age;
			gender = data.gender;
		} else {
			this.isPost = true;
		}
		
		let header = 'Create New Actor';
		if (id) {
			header = `Edit Actor: ${id}`;
		}

		let genderChecked = gender ? 'checked': '';

		let tpl = `
			<h3>${header}</h3>
			<form method="dialog">
				<input type="hidden" name="id" value="${id}"/>
				<input type="text" name="name" value="${name}" placeholder="name"/>
				<input type="number" min="0" name="age" value="${age}"/>
				<label>
				<input type="checkbox" name="gender" ${genderChecked}/> is female
				</label>
			</form>
			<p class="btn">
				<button data-btn="submit">Submit</button>
				<button data-btn="cancel">Cancel</button>
			</p>
		`;

		this.instance.innerHTML = tpl;
		this.instance.showModal();
	}

	close() {
		this.instance.close();
	}

	postData() {
		let f = this.instance.querySelector('form');
		let fd = new FormData(f);
		
		let name = fd.get('name');
		let age = parseInt(fd.get('age'));
		let gender = fd.get('gender') === 'on' ? true: false;

		if (this.isPost) {
			Fetch.post('/api/actors', {
				name: name,
				age: age,
				gender: gender,
			}, () => {
				this.onSubmit();
			})
		} else {
			Fetch.patch('/api/actors/' + fd.get('id'), {
				name: name,
				age: age,
				gender: gender,
			}, () => {
				this.onSubmit();
			})
		}
	}


}

export default ActorForm;