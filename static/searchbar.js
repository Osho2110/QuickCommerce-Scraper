

const items = [
    { name: "Aloo Bhujia" },
    { name: "Coke" },
    { name: "Pepsi" },
    { name: "Lays" },
    { name: "Head and Shoulders" },
    { name: "Haldiram's Aloo bhujia" }
];

const options = {
    keys: ['name']
};

const fuse = new Fuse(items, options);

const searchInput = document.getElementById('search-input');
const results = document.getElementById('results');
const searchbutton = document.getElementById('search-submit');



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
    } else {// modified content because of display issues
        const listItem = document.createElement('ul'); 
        listItem.textContent = "No results found";
        results.appendChild(listItem);
    }
});

searchbutton.addEventListener('click',() => {
    searchterm=searchInput.value;
    $.ajax({ 
        url: '/searchbar', 
        type: 'POST', 
        data: { 'searchterm': searchterm }, 
        success: function(response) { 
            document.getElementById('output').innerHTML = response; 
        }, 
        error: function(error) { 
            console.log(error); 
        } 
    }); 
});
