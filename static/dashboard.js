// Inicializa la gráfica principal usando Chart.js
const ctx = document.getElementById('grafica').getContext('2d');
let chart = new Chart(ctx, {
  type: 'line',
  data: { labels: [], datasets: [] },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    animation: {
      duration: 300,
      easing: 'easeInOutQuad'
    },
    scales: {
      x: {
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10,
          callback: function(value, index) {
            const label = this.chart.data.labels[index];
            const date = new Date(label);
            const fecha = date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
            const hora = date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
            return `${fecha} ${hora}`;
          }
        }
      },
      y: { beginAtZero: true }
    }
  }
});

// Colores para las diferentes variables
const colores = {
  temperatura: 'rgba(255, 99, 132, 0.8)',
  humedad: 'rgba(54, 162, 235, 0.8)',
  presion: 'rgba(144, 238, 144, 0.9)',
  calidad_aire: 'rgba(153, 102, 255, 0.8)'
};

// Variables de estado global
let tipoSeleccionado = 'temperatura';
let datosTotales = [];
let filtroCondicionalActivo = "";
let modoComparacionActivo = false;
let ultimoTimestamp = null;
let fechaFiltrada = null; //guarda la fecha seleccionada


async function cargarDatos(tipo = tipoSeleccionado) {
  try {
    const response = await fetch('/api/mediciones/');
    const datos = await response.json();
    datos.sort((a, b) => new Date(a.fecha_hora) - new Date(b.fecha_hora));
    datosTotales = datos;
    tipoSeleccionado = tipo;

    filtroCondicionalActivo = "";
    fechaFiltrada = null;
    modoComparacionActivo = false;
    document.getElementById("filtro-condicion").value = "";
    document.getElementById("fecha-historial-sidebar").value = "";

    // Mostrar la vista normal
    mostrarTodosEnGrafica(obtenerDatosFiltrados(), tipoSeleccionado);

  } catch (error) {
    console.error("Error al cargar los datos:", error);
  }
}



function obtenerDatosFiltrados() {
  let datos = [...datosTotales];

  // Aplicar filtro por fecha si existe
  if (fechaFiltrada) {
    const inicio = new Date(fechaFiltrada);
    const fin = new Date(fechaFiltrada);
    fin.setHours(23, 59, 59, 999);
    datos = datos.filter(d => {
      const f = new Date(d.fecha_hora);
      return f >= inicio && f <= fin;
    });
  }

  // Aplicar filtro condicional si existe
  if (filtroCondicionalActivo === "temp_gt_30") {
    datos = datos.filter(d => d.temperatura > 30);
  } else if (filtroCondicionalActivo === "hum_lt_50") {
    datos = datos.filter(d => d.humedad < 50);
  } else if (filtroCondicionalActivo === "aire_malo") {
    datos = datos.filter(d => d.calidad_aire === 0);
  }

  return datos;
}


// Muestra una única variable ambiental en el gráfico (ej. temperatura)
function mostrarTodosEnGrafica(datos, tipo) {
  const labels = datos.map(d => new Date(d.fecha_hora));
  const valores = datos.map(d => d[tipo]);

  chart.data.labels = labels;
  chart.data.datasets = [{
    label: tipo.charAt(0).toUpperCase() + tipo.slice(1),
    data: valores,
    borderColor: colores[tipo],
    pointBackgroundColor: colores[tipo],
    borderWidth: 2,
    tension: 0.2
  }];
  chart.update();
  actualizarUltimosValores();
}

// Añade un nuevo punto al gráfico en tiempo real
function añadirNuevoPunto(dato, tipo) {
  const t = new Date(dato.fecha_hora);
  const valor = dato[tipo];

  chart.data.labels.push(t);
  chart.data.datasets[0].data.push(valor);
  datosTotales.push(dato);
  ultimoTimestamp = t.getTime();

  const maxPuntos = 50;
  if (chart.data.labels.length > maxPuntos) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }

  chart.update();
  actualizarUltimosValores();
}

// Actualiza los valores mostrados debajo del gráfico
function actualizarUltimosValores() {
  const ultimo = datosTotales[datosTotales.length - 1];
  console.log(ultimo);
  if (!ultimo) return;

  document.getElementById("valor-temp").textContent = `${ultimo.temperatura} °C`;
  document.getElementById("valor-humedad").textContent = `${ultimo.humedad} %`;
  document.getElementById("valor-presion").textContent = `${ultimo.presion} hPa`;

  let calidadTexto = "Desconocida";
  if (ultimo.calidad_aire === 100) calidadTexto = "Buena";
  else if (ultimo.calidad_aire === 50) calidadTexto = "Media";
  else if (ultimo.calidad_aire === 0) calidadTexto = "Mala";

  document.getElementById("valor-aire").textContent = calidadTexto;
  document.getElementById("ultima-actualizacion").textContent =
    "Última actualización: " + new Date().toLocaleString('es-ES');

    if (ultimo.prediccion !== undefined) {
      document.getElementById("mensaje-prediccion").textContent =
        `Predicción futura (+1h) generada con IA: ${ultimo.prediccion.toFixed(2)} °C`;
    } else {
      document.getElementById("mensaje-prediccion").textContent =
        "Predicción no disponible.";
    }

}

function mostrarToast(mensaje, color = "bg-primary") {
  const toastEl = document.getElementById("liveToast");
  const toastBody = document.getElementById("toast-body");

  // Cambiar mensaje y color
  toastBody.textContent = mensaje;
  toastEl.className = `toast align-items-center text-white ${color} border-0`;

  // Mostrar toast usando Bootstrap
  const toast = new bootstrap.Toast(toastEl);
  toast.show();
}


// Aplica un filtro condicional (temperatura > 30, humedad < 50, calidad_aire = 0)
function aplicarFiltroCondicional() {
  const condicion = document.getElementById("filtro-condicion").value;
  filtroCondicionalActivo = condicion;

  const filtrados = obtenerDatosFiltrados();
  if (filtrados.length === 0) return alert("No hay datos que cumplan esa condición.");
  mostrarTodosEnGrafica(filtrados, tipoSeleccionado);
}


// Limpia el filtro condicional y vuelve a mostrar la vista orignal
function limpiarFiltro() {
  filtroCondicionalActivo = "";
  document.getElementById("filtro-condicion").value = "";
  mostrarTodosEnGrafica(datosTotales, tipoSeleccionado);
  modoComparacionActivo = false;
}

// Muestra dos variables en la misma gráfica para compararlas
function compararVariables() {
  modoComparacionActivo = true;
  const v1 = document.getElementById("variable1").value;
  const v2 = document.getElementById("variable2").value;

  if (v1 === v2) return alert("Selecciona dos variables diferentes para comparar.");

  const datos = obtenerDatosFiltrados();
  const labels = datos.map(d => new Date(d.fecha_hora));
  const datos1 = datos.map(d => d[v1]);
  const datos2 = datos.map(d => d[v2]);

  chart.data.labels = labels;
  chart.data.datasets = [
    {
      label: v1.charAt(0).toUpperCase() + v1.slice(1),
      data: datos1,
      borderColor: colores[v1],
      pointBackgroundColor: colores[v1],
      borderWidth: 2,
      tension: 0.2
    },
    {
      label: v2.charAt(0).toUpperCase() + v2.slice(1),
      data: datos2,
      borderColor: colores[v2],
      pointBackgroundColor: colores[v2],
      borderWidth: 2,
      tension: 0.2
    }
  ];
  chart.update();
}


// Carga el mapa y muestra la ubicación de la Raspberry Pi
let mapa = null;
async function inicializarMapa() {
  try {
    const res = await fetch("/api/ubicacion/");
    const data = await res.json();
    const lat = data.lat || 40.4168;
    const lon = data.lon || -3.7038;
    const ciudad = data.ciudad || "Ubicación desconocida";
    const pais = data.pais || "";

    mapa = L.map('mapa').setView([lat, lon], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(mapa);

    marcadorSensor = L.marker([lat, lon])
      .addTo(mapa)
      .bindPopup(`Raspberry Pi<br>${ciudad}, ${pais}`)
      .openPopup();
  } catch (error) {
    console.error("Error al cargar el mapa:", error);
  }
}

// Centra el mapa en la ubicación actual del usuario (geolocalización navegador)
let marcadorSensor = null;
function centrarEnMiUbicacion() {
  if (!navigator.geolocation || !mapa) return;

  navigator.geolocation.getCurrentPosition(pos => {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;

    mapa.setView([lat, lon], 15);

    if (marcadorSensor) {
      marcadorSensor.setLatLng([lat, lon]);
    } else {
      marcadorSensor = L.marker([lat, lon])
        .addTo(mapa)
        .bindPopup("Tu ubicación actual")
        .openPopup();
    }
  });
}

// Filtra los datos mostrados por una fecha específica desde el sidebar
function filtrarPorFechaDesdeSidebar() {
  const fechaStr = document.getElementById("fecha-historial-sidebar").value;
  if (!fechaStr) return alert("Selecciona una fecha para ver el historial.");

  fechaFiltrada = fechaStr;

  const filtrados = obtenerDatosFiltrados();
  if (filtrados.length === 0) return alert("No hay datos para esa fecha.");

  // Solo ejecuta una de las dos formas de mostrar datos
  if (modoComparacionActivo) {
    compararVariables(); // mantiene la comparación con los nuevos datos filtrados
  } else {
    mostrarTodosEnGrafica(filtrados, tipoSeleccionado); // muestra una sola variable
  }
}




// Alterna entre modo claro y modo oscuro
function alternarModo() {
  const body = document.body;
  const btn = document.getElementById("btn-modo");

  body.classList.toggle('dark');
  btn.textContent = body.classList.contains('dark') ? "Modo día" : "Modo noche";

  localStorage.setItem("modoOscuro", modoOscuro ? "true" : "false");
}

// Muestra u oculta un submenú lateral
function toggleSubmenu(id) {
  document.querySelectorAll('.submenu').forEach(el => {
    if (el.id !== id) el.classList.add('oculto');
  });
  const target = document.getElementById(id);
  if (target) target.classList.toggle('oculto');
}

async function refrescarVistaActual() {
  try {
    const response = await fetch('/api/mediciones/');
    const datos = await response.json();
    datos.sort((a, b) => new Date(a.fecha_hora) - new Date(b.fecha_hora));
    datosTotales = datos;

    const filtrados = obtenerDatosFiltrados();

    if (modoComparacionActivo) {
      compararVariables();
    } else {
      mostrarTodosEnGrafica(filtrados, tipoSeleccionado);
    }
  } catch (error) {
    console.error("Error actualizando datos:", error);
  }
}



// Manejo del intervalo de actualización automática
let intervaloActual = null;

function lanzarActualizacion() {
  if (!intervaloActual) {
    refrescarVistaActual();
    intervaloActual = setInterval(refrescarVistaActual, 10000);
    mostrarToast("Actualización lanzada", "bg-success");
  } else {
    mostrarToast("La actualización ya está activa", "bg-secondary");
  }
}

function pausarActualizacion() {
  if (intervaloActual) {
    clearInterval(intervaloActual);
    intervaloActual = null;
    mostrarToast("Actualización pausada", "bg-warning");
  }
}

function detenerActualizacion() {
  if (intervaloActual) {
    clearInterval(intervaloActual);
    intervaloActual = null;
  }
  chart.data.labels = [];
  chart.data.datasets = [];
  chart.update();
  mostrarToast("Actualización detenida", "bg-danger");
}


// Muestra un panel lateral y oculta los demás (Comparar, Filtrar, Historial)
function mostrarPanel(nombre) {
  const paneles = ['comparar', 'filtrar', 'historial'];
  paneles.forEach(p => {
    const el = document.getElementById(`panel-${p}`);
    if (el) {
      el.style.display = (p === nombre) ? 'block' : 'none';
    }
  });
}

// Inicializa el sistema al cargar la página
window.addEventListener("DOMContentLoaded", async () => {
  const modoGuardado = localStorage.getItem("modoOscuro");
  const body = document.body;
  const btn = document.getElementById("btn-modo");

  if (modoGuardado === "true") {
    body.classList.add("dark");
    if (btn) btn.textContent = "Modo día";
  } else {
    if (btn) btn.textContent = "Modo noche";
  }

  tipoSeleccionado = "temperatura";

  // ✅ Cargar los datos desde la API al iniciar
  try {
    const response = await fetch('/api/mediciones/');
    const datos = await response.json();
    datos.sort((a, b) => new Date(a.fecha_hora) - new Date(b.fecha_hora));
    datosTotales = datos;
    refrescarVistaActual(); // ✅ Mostrar los datos iniciales
  } catch (error) {
    console.error("Error al cargar datos iniciales:", error);
  }

  // Luego se lanza el refresco automático
  lanzarActualizacion();

  await inicializarMapa();

  if (btn) {
    btn.addEventListener("click", () => {
      body.classList.toggle("dark");
      const esOscuro = body.classList.contains("dark");
      btn.textContent = esOscuro ? "Modo día" : "Modo noche";
      localStorage.setItem("modoOscuro", esOscuro ? "true" : "false");
    });
  }
});



