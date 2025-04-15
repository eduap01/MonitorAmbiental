// static/js/dashboard.js

const ctx = document.getElementById('grafica').getContext('2d');
let chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Dato ambiental',
      data: [],
      borderWidth: 2,
      fill: false,
      tension: 0.2
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Fecha y Hora' } },
      y: { beginAtZero: true }
    }
  }
});

async function cargarDatos(tipo) {
  const url = `http://192.168.1.41:8000/datos?tipo=${tipo}`;
  try {
    const response = await fetch(url);
    const datos = await response.json();

    const labels = datos.map(d => new Date(d.fecha).toLocaleString());
    const valores = datos.map(d => d.valor);

    chart.data.labels = labels;
    chart.data.datasets[0].label = tipo;
    chart.data.datasets[0].data = valores;
    chart.update();
  } catch (error) {
    console.error("Error al cargar los datos:", error);
  }
}
