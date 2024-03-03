document.addEventListener('DOMContentLoaded', function() {
	const infoPopup = document.getElementById('popup-info');
	const contactPopup = document.getElementById('popup-contact');
	const contactUsLink = document.getElementById('contact-us-link');
	const closePopupInfo = document.getElementById('popup-close-info');
	const closePopupContact = document.getElementById('popup-close-contact');
	const contactSend = document.getElementById('contact-send');
	const popupDoneInfo = document.getElementById('popup-done-info');
	const popupOpen = document.getElementById('popup-open');
	const contactMessage = document.getElementById('contact-message');
	const contactEmail = document.getElementById('contact-email');

	document.addEventListener('click', function(e) {
		if (contactPopup.classList.contains('popup-show') && !contactPopup.contains(e.target)) {
			contactPopup.classList.remove('popup-show');
			popupOpen.style.display = 'none';

		}
		if (infoPopup.classList.contains('popup-show') && !infoPopup.contains(e.target)) {
			infoPopup.classList.remove('popup-show');
			popupOpen.style.display = 'none';

		}
	});

	contactUsLink.addEventListener('click', function(e) {
		e.preventDefault();
		e.stopPropagation();
		popupOpen.style.display = 'block';
		contactPopup.classList.add('popup-show');
	});

	closePopupInfo.addEventListener('click', function(e) {
		e.stopPropagation();
		infoPopup.classList.remove('popup-show');
		popupOpen.style.display = 'none';

	});

	closePopupContact.addEventListener('click', function(e) {
		e.stopPropagation();
		contactPopup.classList.remove('popup-show');
		popupOpen.style.display = 'none';

	});

	contactSend.addEventListener('click', function(e) {
		if (!contactMessage.value) {
			contactMessage.style.border = "2px solid #FF6666";
		}
		if (!contactEmail.value) {
			contactEmail.style.border = "2px solid #FF6666";
		}
		if (contactMessage.value && contactEmail.value) {
			e.stopPropagation();
			contactPopup.classList.remove('popup-show');
			infoPopup.classList.add('popup-show');

			contactEmail.style.border = "2px solid transparent";
			contactMessage.style.border = "2px solid transparent";

			contactEmail.value = '';
			contactMessage.value = '';
		}
	});

	popupDoneInfo.addEventListener('click', function(e) {
		e.stopPropagation();
		infoPopup.classList.remove('popup-show');
		popupOpen.style.display = 'none';

	});
});
