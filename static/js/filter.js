// static/js/filter.js
function filtrarProductos() {
    const searchInput = document.getElementById('search').value.toLowerCase();
    const productos = document.querySelectorAll('.producto');
    
    productos.forEach(producto => {
      const nombre = producto.querySelector('td:first-child').textContent.toLowerCase();
      const descripcion = producto.querySelector('td:nth-child(2)').textContent.toLowerCase();
      
      if (nombre.includes(searchInput) || descripcion.includes(searchInput)) {
        producto.style.display = '';
      } else {
        producto.style.display = 'none';
      }
    });
  }
  