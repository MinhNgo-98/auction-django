var menu = document.querySelector('.nav-flyout-menu');
var mobile_menu = document.querySelector('.nav-list');
var burger = document.querySelector('.hamburger-menu');

function toggleFlyoutMenu(){
	if (menu.style.display === 'none' || menu.style.display === '') {
		menu.style.display = 'block';
	} else {
		menu.style.display = 'none';
	}
}

function toggleHamburgerMenu(){
	burger.addEventListener('click', () => {
		mobile_menu.classList.toggle('nav-active');
	});
}

toggleHamburgerMenu();
