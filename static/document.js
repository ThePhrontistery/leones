document.addEventListener('htmx:afterOnLoad', function(evt) {
  if (evt.detail.elt && evt.detail.elt.id === 'upload-result') {
    // Dispara un evento personalizado para recargar la lista de documentos
    document.body.dispatchEvent(new Event('documentUploaded'));
  }
});
