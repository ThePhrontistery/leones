document.addEventListener('htmx:afterOnLoad', function(evt) {
  if (evt.detail.elt && evt.detail.elt.id === 'upload-result') {
    // Dispara un evento personalizado para recargar la lista de documentos
    document.body.dispatchEvent(new Event('documentUploaded'));
  }
});

function renderPreview() {
  const textarea = document.getElementById('markdown-input');
  const preview = document.getElementById('markdown-preview');
  if (textarea && preview && window.marked) {
    preview.innerHTML = window.marked.parse(textarea.value);
  }
}

document.addEventListener('DOMContentLoaded', renderPreview);
document.body.addEventListener('input', function(evt) {
  if (evt.target && evt.target.id === 'markdown-input') {
    renderPreview();
  }
});
document.body.addEventListener('htmx:afterSwap', function(evt) {
  if (document.getElementById('markdown-input') && document.getElementById('markdown-preview')) {
    renderPreview();
  }
});

// El backend ahora controla los mensajes de estado paso a paso con hx-swap-oob
// No es necesario simular pasos en el frontend

document.body.addEventListener('htmx:afterRequest', function(evt) {
  // El backend pone el OK o el error, no limpiar aquí
});
