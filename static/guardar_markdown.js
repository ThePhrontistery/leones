// Script para guardar el contenido del editor Markdown usando HTMX

document.addEventListener('DOMContentLoaded', function () {
  const guardarBtn = document.getElementById('guardar-markdown-btn');
  const editor = document.getElementById('markdown-editor-content');
  const msgDiv = document.getElementById('guardar-msg');

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
});
