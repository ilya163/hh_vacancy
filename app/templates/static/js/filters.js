function createList(items) {
    const ul = document.createElement('ul');
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item.name;
        li.classList.add(item.areas && item.areas.length > 0 ? 'parent' : 'child');
        li.addEventListener('click', () => {
            if (!item.areas || item.areas.length === 0) {
                document.getElementById('filterInput').value = item.name
                document.getElementById('filterInput').setAttribute('data-id', item.id)
            }
        });
        ul.appendChild(li);
        if (item.areas && item.areas.length > 0) {
            const subList = createList(item.areas);
            ul.appendChild(subList);
        }
    });
    return ul;
}

function filterList() {
    const filter = document.getElementById('filterInput').value.toLowerCase();
    const items = document.querySelectorAll('#dropdown-content li');
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? '' : 'none';
    });
}

function toggleDropdown(show) {
    const dropdown = document.getElementById("dropdown-content");
    dropdown.style.display = show ? 'block' : 'none';
}

document.getElementById('filterInput').addEventListener('focus', () => {
    toggleDropdown(true);
});

document.getElementById('filterInput').addEventListener('blur', () => {
    // Задержка перед скрытием, чтобы обработать нажатие на элемент списка
    setTimeout(() => {
        toggleDropdown(false);
    }, 200);
});

document.getElementById('filterInput').addEventListener('input', filterList);

document.addEventListener('DOMContentLoaded', () => {
    const dropdownList = document.getElementById('dropdownList');

    fetch('/static/areas.json')
      .then(response => response.json()) 
      .then(data => {
        dropdownList.appendChild(createList(data));
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });



});