import Fetch from "./fetch.mjs";
import ActorForm from "./actor_form.mjs";

class ActorList extends HTMLElement {

	loadingMassage = null;
	dataCache = {};
	actorForm = null;

	constructor(tpl) {
		super();

		let msg = document.createElement('p');
		msg.className = 'loading';
		msg.innerText = 'loading actors ... ';
		this.appendChild(msg);
		this.loadingMassage = msg;

		let list = this;
		this.addEventListener('click', (e) => {
			let target = e.target;
			let btn = target.dataset.btn;
			if (!btn) {
				return;
			}

			let id = target.dataset.id;
			switch (btn) {
				case 'edit':
					list.editItem(id);
					break;
				case 'delete':
					list.deleteItem(id);
					break;
			}
		});

		this.actorForm = new ActorForm({
			onSubmit: () => {
				this.load();
			}
		})
	}

	deleteItem(id) {
		if (confirm('Do you confirm to delete?')) {
			Fetch.delete(`/api/actors/${id}`, () => {
				this.load();
			})
		}
	}

	editItem(id) {
		this.actorForm.lunch(this.dataCache[id]);
	}

	showLoading() {
		this.loadingMassage.style.display = 'block';
	}

	hideLoading() {
		this.loadingMassage.style.display = 'none';
	}

	load() {
		this.showLoading();
		Fetch.get('/api/actors', (json) => {
			this.hideLoading();
			this.updateView(json);
		});
	}

	static genderString(state) {
		if (state) {
			return 'female';
		} else {
			return 'male';
		}
	}

	updateView(json) {
		let content = document.createElement('ul');
		let parser = new DOMParser();
		
		let list = json.actors;
		list.forEach(actor => {
			let {id, name, age, gender} = actor;
			let itemTemplate = `
				<li>
					<div class="item-header">
						<p>ID: ${id}</p>
						<p>
							<button data-id="${id}" data-btn="edit">Edit</button>
							<button data-id="${id}" data-btn="delete">Delete</button>
						</p>
					</div>
					<h3>${name}</h3>
					<p>${age}, ${ActorList.genderString(gender)}</p>
				</li>
			`;
			let doc = parser.parseFromString(itemTemplate, 'text/html')
			content.appendChild(doc.body.firstChild);

			this.dataCache[actor.id] = actor;
		});
		
		let exist = this.querySelector('ul');
		if (exist) {
			this.removeChild(exist);
		}
		this.appendChild(content);
	}

}

customElements.define('actor-list', ActorList);

export default ActorList;