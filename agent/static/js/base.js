document.querySelectorAll('.map-btn').forEach(button => {
    button.addEventListener('click', function() {
        const row = this.closest('tr');
        const address = row.cells[2].innerText;

        const mapUrl = `https://yandex.ru/maps/?text=${encodeURIComponent(address)}`;

        window.open(mapUrl, '_blank');
    });
});
