// Script para guardar el contenido del editor Markdown usando HTMX

document.addEventListener('DOMContentLoaded', function () {
  const guardarBtn = document.getElementById('guardar-markdown-btn');
  const editor = document.getElementById('markdown-editor-content');
  const msgDiv = document.getElementById('guardar-msg');
  const preview = document.getElementById('markdown-preview');

  async function renderPreviewFromBackend() {
    // Obtiene el markdown guardado y lo renderiza en la vista previa
    if (preview) {
      const resp = await fetch('/api/markdown/get');
      if (resp.ok) {
        const text = await resp.text();
        // Extrae el contenido del textarea
        const match = text.match(/<textarea[^>]*>([\s\S]*)<\/textarea>/);
        const markdown = match ? match[1] : '';
        // Renderiza el markdown guardado
        fetch('/api/markdown/preview', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: markdown })
        })
        .then(res => res.text())
        .then(html => { preview.innerHTML = html; });
      }
    }
  }

  if (guardarBtn && editor) {
    guardarBtn.addEventListener('click', async function () {
      guardarBtn.disabled = true;
      msgDiv.textContent = 'Guardando...';
      try {
        const resp = await fetch('/api/markdown/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: editor.value })
        });
        if (resp.ok) {
          msgDiv.textContent = '¡Cambios guardados!';
          msgDiv.className = 'mt-2 text-green-600 text-sm';
          setTimeout(() => { msgDiv.textContent = ''; }, 1500);
          await renderPreviewFromBackend(); // Recarga la vista previa con el markdown guardado
        } else {
          msgDiv.textContent = 'Error al guardar.';
          msgDiv.className = 'mt-2 text-red-600 text-sm';
        }
      } catch (e) {
        msgDiv.textContent = 'Error de red.';
        msgDiv.className = 'mt-2 text-red-600 text-sm';
      } finally {
        guardarBtn.disabled = false;
      }
    });
  }

  // También recarga la vista previa tras HTMX swap si el panel se ha actualizado
  document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (document.getElementById('markdown-editor-content') && document.getElementById('markdown-preview')) {
      renderPreviewFromBackend();
    }
  });
});
