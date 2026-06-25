document.addEventListener('DOMContentLoaded', function() {
    
    const alertElements = document.querySelectorAll('.alert');
    alertElements.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(function(input) {
            input.addEventListener('invalid', function(e) {
                e.preventDefault();
                this.classList.add('is-invalid');
            });
            input.addEventListener('input', function() {
                this.classList.remove('is-invalid');
            });
        });
    });

    const otpInputs = document.querySelectorAll('.otp-input');
    otpInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length >= 6) {
                this.value = this.value.substring(0, 6);
            }
        });
    });

    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(function(input) {
        input.setAttribute('min', today);
    });

    const citySelects = document.querySelectorAll('select[name="city"]');
    citySelects.forEach(function(select) {
        select.addEventListener('change', function() {
            const cityId = this.value;
            if (cityId) {
                fetchHotels(cityId);
                fetchRestaurants(cityId);
            }
        });
    });

    function fetchHotels(cityId) {
        const hotelSelect = document.querySelector('select[name="hotel"]');
        if (!hotelSelect) return;
        
        fetch(`/api/hotels/?city=${cityId}`)
            .then(response => response.json())
            .then(data => {
                hotelSelect.innerHTML = '<option value="">Select Hotel</option>';
                data.results.forEach(function(hotel) {
                    const option = document.createElement('option');
                    option.value = hotel.id;
                    option.textContent = `${hotel.name} - ₹${hotel.price_per_night}/night`;
                    hotelSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching hotels:', error));
    }

    function fetchRestaurants(cityId) {
        const restaurantSelect = document.querySelector('select[name="restaurant"]');
        if (!restaurantSelect) return;
        
        fetch(`/api/restaurants/?city=${cityId}`)
            .then(response => response.json())
            .then(data => {
                restaurantSelect.innerHTML = '<option value="">Select Restaurant</option>';
                data.results.forEach(function(restaurant) {
                    const option = document.createElement('option');
                    option.value = restaurant.id;
                    option.textContent = `${restaurant.name} (${restaurant.price_range})`;
                    restaurantSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching restaurants:', error));
    }

    const searchInputs = document.querySelectorAll('input[type="search"]');
    searchInputs.forEach(function(input) {
        let timeout = null;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                const form = input.closest('form');
                if (form) {
                    form.submit();
                }
            }, 500);
        });
    });

    const cancelButtons = document.querySelectorAll('.cancel-booking');
    cancelButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to cancel this booking?')) {
                e.preventDefault();
            }
        });
    });

    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            console.log('User logging out');
        });
    }

    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }

    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    } else {
        lazyImages.forEach(function(img) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }

    console.log('Tour & Travel - JavaScript initialized');
});
