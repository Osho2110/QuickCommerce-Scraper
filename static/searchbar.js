const items = [
    { name: "Aloo Bhujia" },
    { name: "Coke" },
    { name: "Pepsi" },
    { name: "Lays" },
    { name: "Head and Shoulders" }
];

const options = {
    keys: ['name']
};

const fuse = new Fuse(items, options);

const searchInput = document.getElementById('search-input');
const results = document.getElementById('results');

searchInput.addEventListener('input', () => {
    const searchQuery = searchInput.value;
    const fuseResults = fuse.search(searchQuery);

    results.innerHTML = '';

    if (fuseResults.length > 0) {
        fuseResults.forEach(result => {
            const item = result.item;
            const listItem = document.createElement('ul'); // Changed from 'ul' to 'li'
            listItem.textContent = item.name;
            listItem.addEventListener('click', () => { // Added click event listener
                searchInput.value = item.name;
            });
            results.appendChild(listItem);
        });
    } else {
        results.textContent = 'No matching results found.';
    }
});