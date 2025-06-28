// static/exportar_markdown.js
// Gestiona la exportación del markdown a Word usando HTMX

document.addEventListener("DOMContentLoaded", () => {
  const exportBtn = document.getElementById("exportar-markdown-btn");
  const formatoCombo = document.getElementById("exportar-formato");
  const editor = document.getElementById("markdown-editor-content");

  if (exportBtn && formatoCombo && editor) {
    exportBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      exportBtn.disabled = true;
      exportBtn.textContent = "Exportando...";
      try {
        const formData = new FormData();
        formData.append("markdown_content", editor.value); // <-- nombre correcto
        formData.append("formato", formatoCombo.value);    // <-- nombre correcto
        const response = await fetch("/api/generar-funcional/exportar", {
          method: "POST",
          body: formData,
        });
        if (!response.ok) throw new Error("Error al exportar");
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = formatoCombo.value === "word" ? "funcional.docx" : "funcional.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        alert("No se pudo exportar el documento.");
      } finally {
        exportBtn.disabled = false;
        exportBtn.textContent = "Exportar";
      }
    });
  }
});
