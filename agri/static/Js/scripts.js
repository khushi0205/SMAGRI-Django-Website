/* Your existing JavaScript functions remain unchanged */

// Modified openModal function to accept image source
function openModal(title, description, imageSrc) {
    var modal = document.getElementById("modal");
    var modalTitle = document.getElementById("modal-title");
    var modalDescription = document.getElementById("modal-description");
    var modalImage = document.getElementById("modal-image");

    modalTitle.textContent = title;
    modalDescription.textContent = description;
    modalImage.src = imageSrc;

    modal.style.display = "block";
}


// script.js

// Function to open modal with title, description, and image source
function openModal(title, description, imageSrc) {
    var modal = document.getElementById("modal");
    var modalTitle = document.getElementById("modal-title");
    var modalDescription = document.getElementById("modal-description");
    var modalImage = document.getElementById("modal-image");

    modalTitle.textContent = title;
    modalDescription.textContent = description;
    modalImage.src = imageSrc;

    modal.style.display = "block";
}

// Function to close modal
function closeModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
}