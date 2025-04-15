
const ctx = document.getElementById('grafica').getContext('2d');
let chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: []
  },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    animation: {
      duration: 300, // Muy corta duración
      easing: 'easeInOutQuad' // Suave, sin rebote ni sobresalto
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
      y: {
        beginAtZero: true
      }
    }
  }
});


const colores = {
  temperatura: 'rgba(255, 99, 132, 0.8)',
  humedad: 'rgba(54, 162, 235, 0.8)',
  presion: 'rgba(75, 192, 192, 0.8)',
  calidad_aire: 'rgba(153, 102, 255, 0.8)'
};

let tipoSeleccionado = 'temperatura';
let datosTotales = [];
let filtroCondicionalActivo = "";
let modoComparacionActivo = false;
let ultimoTimestamp = null;


async function cargarDatos(tipo) {
  tipoSeleccionado = tipo;

  try {
    const response = await fetch('/api/mediciones/');
    const datos = await response.json();
    datos.sort((a, b) => new Date(a.fecha_hora) - new Date(b.fecha_hora));

    // Primera carga: dibujar todos
    if (!ultimoTimestamp) {
      datosTotales = datos;
      ultimoTimestamp = new Date(datos[datos.length - 1].fecha_hora).getTime();
      mostrarTodosEnGrafica(datosTotales, tipoSeleccionado);
      return;
    }

    // Carga incremental: buscar nuevos
    const nuevos = datos.filter(d => new Date(d.fecha_hora).getTime() > ultimoTimestamp);

    if (nuevos.length > 0) {
      nuevos.forEach(dato => {
        añadirNuevoPunto(dato, tipoSeleccionado);
      });
    }

  } catch (error) {
    console.error("Error al cargar los datos:", error);
  }
}



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



function actualizarUltimosValores() {
  if (datosTotales.length === 0) return;
  const ultimo = datosTotales[datosTotales.length - 1];
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
}

function aplicarFiltroCondicional() {
  const condicion = document.getElementById("filtro-condicion").value;
  filtroCondicionalActivo = condicion;

  let filtrados = [...datosTotales];

  if (condicion === "temp_gt_30") {
    filtrados = filtrados.filter(d => d.temperatura > 30);
  } else if (condicion === "hum_lt_50") {
    filtrados = filtrados.filter(d => d.humedad < 50);
  } else if (condicion === "aire_malo") {
    filtrados = filtrados.filter(d => d.calidad_aire === 0);
  }

  if (filtrados.length === 0) {
    alert("No hay datos que cumplan esa condición.");
    return;
  }

  mostrarEnGrafica(filtrados, tipoSeleccionado);
}

function limpiarFiltro() {
  filtroCondicionalActivo = "";
  document.getElementById("filtro-condicion").value = "";
  mostrarEnGrafica(datosTotales, tipoSeleccionado);

  modoComparacionActivo = false;

}

function compararVariables() {

  modoComparacionActivo = true;

  const v1 = document.getElementById("variable1").value;
  const v2 = document.getElementById("variable2").value;

  if (v1 === v2) {
    alert("Selecciona dos variables diferentes para comparar.");
    return;
  }

  const labels = datosTotales.map(d => new Date(d.fecha_hora));
  const datos1 = datosTotales.map(d => d[v1]);
  const datos2 = datosTotales.map(d => d[v2]);

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

    L.marker([lat, lon])
      .addTo(mapa)
      .bindPopup(`Raspberry Pi<br>${ciudad}, ${pais}`)
      .openPopup();
  } catch (error) {
    console.error("Error al cargar el mapa:", error);
  }
}

function centrarEnMiUbicacion() {
  if (!navigator.geolocation || !mapa) return;
  navigator.geolocation.getCurrentPosition(pos => {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    mapa.setView([lat, lon], 15);
  });
}

function analizarTendencias() {
  if (datosTotales.length < 6) {
    document.getElementById("mensaje-prediccion").textContent = "Datos insuficientes para predicción.";
    return;
  }

  const ultimos = datosTotales.slice(-24); // últimas 24 lecturas (ultimo minuto)
  const t0 = ultimos[0];
  const tN = ultimos[ultimos.length - 1];

  const tempSube = tN.temperatura > t0.temperatura;
  const presionBaja = tN.presion < t0.presion;
  const humedadAlta = tN.humedad > 60;

  let mensaje = "Sin cambios relevantes.";

  if (tempSube && presionBaja) {
    mensaje = "Posibilidad de lluvia próxima (temperatura sube, presión baja).";
  } else if (humedadAlta && presionBaja) {
    mensaje = "Humedad alta y presión baja. Podría haber niebla o lluvias débiles.";
  } else if (tempSube) {
    mensaje = "Temperatura en ascenso – posible calor en próximas horas.";
  } else if (tN.temperatura < t0.temperatura) {
    mensaje = "Temperatura descendiendo – posibles condiciones frescas.";
  }

  document.getElementById("mensaje-prediccion").textContent = mensaje;
}

function filtrarPorFecha() {
  const fechaStr = document.getElementById("fecha-historial").value;
  if (!fechaStr) {
    alert("Selecciona una fecha para ver el historial.");
    return;
  }

  const inicio = new Date(fechaStr);
  const fin = new Date(fechaStr);
  fin.setHours(23, 59, 59, 999);

  const filtrados = datosTotales.filter(d => {
    const fecha = new Date(d.fecha_hora);
    return fecha >= inicio && fecha <= fin;
  });

  if (filtrados.length === 0) {
    alert("No hay datos para esa fecha.");
    return;
  }

  modoComparacionActivo = false;
  filtroCondicionalActivo = "";

  mostrarEnGrafica(filtrados, tipoSeleccionado);
}

function alternarModo() {
  const body = document.body;
  const btn = document.querySelector('.sidebar-app .menu button:last-child');

  body.classList.toggle('dark');

  if (body.classList.contains('dark')) {
    btn.textContent = "Modo día";
  } else {
    btn.textContent = "Modo noche";
}
}


function toggleMenu() {
  const menu = document.getElementById('sidebar');
  menu.classList.toggle('oculto');
}

function mostrarPanel(nombre) {
  const ids = ['panel-comparar', 'panel-filtrar', 'panel-historial'];

  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.style.display = (id === `panel-${nombre}`) ? 'block' : 'none';
    }
  });
}


window.addEventListener("load", async () => {
  cargarDatos("temperatura");
  setInterval(() => cargarDatos(tipoSeleccionado), 10000);
  await inicializarMapa();
});