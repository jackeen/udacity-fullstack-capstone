import MovieList from './components/movie_list.mjs';
import ActorList from './components/actor_list.mjs';
import MovieForm from './components/movie_form.mjs';
import ActorForm from './components/actor_form.mjs';

let State = {
	currentDataList: 'movie'
};

function loadMovies(content) {
	const movieList = new MovieList();
	content.appendChild(movieList);
	movieList.load();
}

function loadActors(content) {
	const actorList = new ActorList();
	content.appendChild(actorList);
	actorList.load();
}

function loadContent() {
	let content = document.getElementById('content');
	content.innerHTML = '';
	switch (State.currentDataList) {
		case 'movie':
			loadMovies(content);
			break;
		case 'actor':
			loadActors(content);
			break;
	}
}

document.getElementById('content_tab').addEventListener('click', (e) => {
	let target = e.target;
	let dataType = target.dataset.type;
	
	if (!dataType) {
		return;
	}

	State.currentDataList = dataType;

	let selectedTab = document.querySelector('#content_tab .selected');
	if (selectedTab) {
		selectedTab.classList.remove('selected');
	}
	target.classList.add('selected');

	loadContent();
});

// load default data
document.getElementById('content_tab').firstElementChild.click();

let movieForm = new MovieForm({
	onSubmit: () => {
		alert('The new movie is added, please click the movie tab to view.');
		// loadContent();
	}
});
document.getElementById('post_movie').addEventListener('click', () => {
	movieForm.lunch(null);
});

let actorForm = new ActorForm({
	onSubmit: () => {
		alert('The new actor is added, please click the actor tab to view.');
	}
});
document.getElementById('post_actor').addEventListener('click', () => {
	actorForm.lunch(null);
});
