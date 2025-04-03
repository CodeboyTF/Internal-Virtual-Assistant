const socket = io();

// Function to toggle the chat container
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    const overlay = document.getElementById('overlay');
    const chatBox = document.getElementById('chatBox'); // Static message box

    if (chatContainer.style.display === 'none' || chatContainer.style.display === '') {
        chatContainer.style.display = 'block';
        overlay.style.display = 'block';
        chatBox.style.display = 'none'; // Hide message box
    } else {
        chatContainer.style.display = 'none';
        overlay.style.display = 'none';
        chatBox.style.display = 'block'; // Show message box
        // Clear messages when chat is closed
        messages.innerHTML = '';
    }
}

// Function to send user message
function sendMessage() {
    const userInput = document.getElementById('userInput');
    const userMessage = userInput.value.trim();

    if (userMessage) {
        appendMessage('user', userMessage);
        userInput.value = '';

        // Send the message to the server
        socket.emit('user_message', { message: userMessage });
    }
}

// Function to append messages to the chat
function appendMessage(sender, message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to the latest message
}

// Function to handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

socket.on('trigger_popup', function(data) {
    if (data.show) {
        // Show your popup modal here
        alert("Would you like to provide additional feedback?"); // Replace with your actual popup
        // Or if using Bootstrap:
        // $('#feedbackModal').modal('show');
    }
});

// Function to open the modal
function openModal() {
    const modal = document.getElementById('enquiryModal');
    modal.style.display = 'block';
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('enquiryModal');
    modal.style.display = 'none';
}

// Function to submit the enquiry form
// const socket = io();

// Function to validate email
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Function to submit the enquiry form
function submitEnquiry() {
    const name = document.getElementById('nameInput').value.trim();
    const surname = document.getElementById('surnameInput').value.trim();
    const email = document.getElementById('emailInput').value.trim();
    const enquiry = document.getElementById('enquiryInput').value.trim();

    if (name && surname && email && enquiry) {
        if (!validateEmail(email)) {
            alert('Please enter a valid email address.');
            return;
        }

        // Send the enquiry data to the server
        socket.emit('user_message', {
            name: name,
            surname: surname,
            email: email,
            enquiry: enquiry,
            message: enquiry // Include the enquiry as the message for the bot
        });

        // Show overlay and success message
        const overlay = document.getElementById('overlay');
        const successMessage = document.getElementById('successMessage');

        overlay.style.display = 'block';
        successMessage.style.display = 'block';

        // Clear fields after submission
        document.getElementById('nameInput').value = '';
        document.getElementById('surnameInput').value = '';
        document.getElementById('emailInput').value = '';
        document.getElementById('enquiryInput').value = '';

        // Hide the success message and overlay after 2 seconds
        setTimeout(() => {
            successMessage.style.display = 'none';
            overlay.style.display = 'none';
        }, 2000);

        // Close the modal
        closeModal();
    } else {
        alert('Please fill in all fields.');
    }
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('enquiryModal');
    modal.style.display = 'none';
}

// Listen for bot responses
socket.on('bot_response', (data) => {
    appendMessage('bot', data.message);

    // Open modal if the bot doesn't understand the query
    if (data.message.includes("I'm sorry, I didn't understand that")) {
        openModal();
    }
});

// Function to append messages to the chat
function appendMessage(sender, message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to the latest message
}

// Slideshow functionality
let slideIndex = 0;
let timer = null; // Track the interval timer

// Initialize slideshow
showSlides();

function plusSlides(n) {
    resetTimer(); // Reset timer when user interacts
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    resetTimer(); // Reset timer when user interacts
    showSlides(slideIndex = n - 1);
}

function showSlides() {
    const slides = document.getElementsByClassName("slides");
    const dots = document.getElementsByClassName("dot");
    
    // Wrap around if at end
    if (slideIndex >= slides.length) slideIndex = 0;
    if (slideIndex < 0) slideIndex = slides.length - 1;

    // Hide all slides
    Array.from(slides).forEach(slide => slide.style.display = "none");
    
    // Update dots
    Array.from(dots).forEach(dot => dot.classList.remove("active"));
    
    // Show current slide and dot
    slides[slideIndex].style.display = "block";
    dots[slideIndex].classList.add("active");
    
    // Reset the automatic timer
    resetTimer();
    timer = setTimeout(() => {
        slideIndex++;
        showSlides();
    }, 3000);
}

function resetTimer() {
    if (timer) {
        clearTimeout(timer);
        timer = null;
    }
}

// Additional slideshow functionality
const indicators = document.querySelectorAll('.indicator div');
const slideshowContent = document.querySelector('.slideshow-content');
const slides = document.querySelectorAll('.slideshow-content a');
let currentIndex = 0;
let interval;

function showSlide(index) {
    indicators[currentIndex].classList.remove('active');
    const offset = index * 100 / slides.length;
    slideshowContent.style.transform = `translateX(-${offset}%)`;
    currentIndex = index;
    indicators[currentIndex].classList.add('active');
    resetInterval();
}

function resetInterval() {
    clearInterval(interval);
    interval = setInterval(() => {
        indicators[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % indicators.length;
        const offset = currentIndex * 100 / slides.length;
        slideshowContent.style.transform = `translateX(-${offset}%)`;
        indicators[currentIndex].classList.add('active');
    }, 10000);
}

resetInterval();