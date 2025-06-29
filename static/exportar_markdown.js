// static/exportar_markdown.js
// Nueva funcionalidad: exportar markdown a Word

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
        formData.append("markdown_text", editor.value);
        formData.append("format", formatoCombo.value);
        const response = await fetch("/api/export/", {
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
