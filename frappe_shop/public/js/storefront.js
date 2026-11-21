// Storefront polish (specs/002-storefront-polish, US5): a "Browse books" button in empty states.
// Webshop renders the cart empty state on the server and the product list empty state in JS.
(function () {
	function add_browse_button(container) {
		if (!container || container.querySelector(".browse-books")) return;
		const link = document.createElement("a");
		link.className = "btn btn-primary browse-books ml-2";
		link.href = "/all-products";
		link.style.fontSize = "16px";
		link.textContent = __("Browse books");
		container.appendChild(link);
	}

	function apply() {
		document
			.querySelectorAll(".cart-empty, .empty-apps-state")
			.forEach((el) => add_browse_button(el));
	}

	document.addEventListener("DOMContentLoaded", apply);
	new MutationObserver(apply).observe(document.documentElement, {
		childList: true,
		subtree: true,
	});
})();
