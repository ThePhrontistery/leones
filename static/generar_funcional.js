// Script para mostrar iconos de estado en el botón "Generar Funcional"
import { reloj, ok } from './generar_funcional_icons.js';

window.mostrarReloj = function () {
  const indicador = document.getElementById('generar-funcional-indicador');
  if (indicador) {
    indicador.innerHTML = reloj;
  }
};

document.body.addEventListener('htmx:afterRequest', function (evt) {
  if (
    evt.detail &&
    evt.detail.elt &&
    evt.detail.elt.id === 'generar-funcional-btn' &&
    evt.detail.requestConfig.verb === 'post'
  ) {
    const indicador = document.getElementById('generar-funcional-indicador');
    if (evt.detail.xhr.status === 200) {
      indicador.innerHTML = ok;
    } else {
      indicador.innerHTML = '';
    }
  }
});
