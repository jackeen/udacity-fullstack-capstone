import Fetch from "./fetch.mjs";
import MovieForm from "./movie_form.mjs";
import ActorList from "./actor_list.mjs";
import MovieActorForm from "./movie_actor_form.mjs";

class MovieList extends HTMLElement {

	loadingMassage = null;
	movieForm = null;
	movieActorForm = null;
	dataCache = {};

	constructor(tpl) {
		super();

		let msg = document.createElement('p');
		msg.className = 'loading';
		msg.innerText = 'loading movies ... ';
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
				case 'actors':
					list.showActors(id);
					break;
				case 'add-actors':
					list.addActorForMovie(id);
					break;
				case 'remove-actor':
					list.deleteActorFromMovie(target, id, target.dataset.aid);
					break;
			}
		});

		this.movieForm = new MovieForm({
			onSubmit: () => {
				this.load();
			}
		});

		this.movieActorForm = new MovieActorForm({
			onSubmit: (mid) => {
				this.showActors(mid);
			}
		});
	}

	deleteActorFromMovie(btn, mid, aid) {
		btn.disable = true;
		btn.innerText = 'Removing';
		Fetch.patch(`/api/movies/${mid}/actors`, {
			actor_id: aid,
			attach_state: false,
		}, () => {
			this.showActors(mid);
		});
	}

	addActorForMovie(id) {
		this.movieActorForm.lunch(id);
	}

	showActors(id) {
		let content = document.getElementById(`movie_${id}_actors`);
		content.innerHTML = 'loading...';
		
		Fetch.get(`/api/movies/${id}`, (json) => {
			let actors = json.actors;
			let f = '';
			actors.forEach((actor) => {
				let tpl = `
					<div class="actor-item">
						<p>
							<b>${actor.id}:</b>
							<span>${actor.name}</span>
							<span>${actor.age}</span>
							<span>${ActorList.genderString(actor.gender)}</span>
						</p>
						<button data-id="${id}" data-aid="${actor.id}" data-btn="remove-actor">Remove</button>
					</div>
				`;

				f += tpl;
			});

			content.innerHTML = f;
		});
	}

	deleteItem(id) {
		if (confirm('Do you confirm to delete?')) {
			Fetch.delete(`/api/movies/${id}`, () => {
				this.load();
			})
		}
	}

	editItem(id) {
		this.movieForm.lunch(this.dataCache[id]);
	}

	showLoading() {
		this.loadingMassage.style.display = 'block';
	}

	hideLoading() {
		this.loadingMassage.style.display = 'none';
	}

	load() {
		this.showLoading();
		Fetch.get('/api/movies', (json) => {
			this.hideLoading();
			this.updateView(json);
		});
	}

	updateView(json) {

		let content = document.createElement('ul');
		let parser = new DOMParser();
		
		let list = json.movies;
		list.forEach(movie => {
			let {id, title, release_date} = movie;
			let itemTemplate = `
				<li>
					<div class="item-header">
						<p>ID: ${id}</p>
						<p>
							<button data-id="${id}" data-btn="edit">Edit</button>
							<button data-id="${id}" data-btn="delete">Delete</button>
							<button data-id="${id}" data-btn="actors">Show Actors</button>
							<button data-id="${id}" data-btn="add-actors">Add Actor</button>
						</p>
					</div>
					<h3>${title}</h3>
					<p class="date">${release_date}</p>
					<div id="movie_${id}_actors" class="actors"></div>
				</li>
			`;
			let doc = parser.parseFromString(itemTemplate, 'text/html')
			content.appendChild(doc.body.firstChild);
			this.dataCache[movie.id] = movie;
		});

		let exist = this.querySelector('ul');
		if (exist) {
			this.removeChild(exist);
		}
		this.appendChild(content);
	}

}

customElements.define('movie-list', MovieList);

export default MovieList;