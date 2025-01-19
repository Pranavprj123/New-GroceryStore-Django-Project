document.addEventListener("DOMContentLoaded", function () {
    // For video container hover play/pause functionality
    const videoContainers = document.querySelectorAll(".video-container");

    videoContainers.forEach((container) => {
        const video = container.querySelector("video");

        if (video) {
            // Play video on hover
            container.addEventListener("mouseenter", () => video.play());
            container.addEventListener("mouseleave", () => video.pause());
        } else {
            // Remove hover effects for containers without video
            container.classList.remove("has-video");
        }
    });

    // Replace feather icons
    feather.replace();

    // Add to Cart functionality
    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach((button) => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const productId = this.dataset.productId;

            // Assuming an AJAX endpoint or a POST form submission
            fetch(`/add_to_cart/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken(), // Use your CSRF token function
                },
                body: JSON.stringify({ quantity: 1 }),
            })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error("Failed to add to cart");
                    }
                })
                .then((data) => {
                    alert(`Added ${data.productName} to cart`);
                    updateCartBadge(data.cartItemCount); // Update cart badge
                })
                .catch((error) => {
                    console.error(error);
                    alert("Error adding to cart");
                });
        });
    });

    // Sorting functionality
    const sortSelect = document.getElementById("sort_by");

    if (sortSelect) {
        sortSelect.addEventListener("change", function () {
            const sortValue = this.value;
            const urlParams = new URLSearchParams(window.location.search);
            const category = urlParams.get("category") || "All";
            const newUrl = `?category=${category}&sort_by=${sortValue}`;
            window.location.href = newUrl;
        });
    }

    // Helper: Update cart badge count
    function updateCartBadge(count) {
        const cartBadge = document.querySelector(".cart-badge");
        if (cartBadge) {
            cartBadge.textContent = count;
        }
    }

    // Helper: Get CSRF token
    function getCsrfToken() {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
        return csrfToken ? csrfToken.value : "";
    }
});
