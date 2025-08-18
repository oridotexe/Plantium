document.addEventListener('DOMContentLoaded', () => {
  const measurements = JSON.parse(
    document.getElementById('measurements-data').textContent
  );
  let labels = Object.values(measurements).map(m => {
  let d = new Date(m.date);
  let day = String(d.getDate()).padStart(2, '0');
  let month = String(d.getMonth() + 1).padStart(2, '0');
  let hours = String(d.getHours()).padStart(2, '0');
  let minutes = String(d.getMinutes()).padStart(2, '0');
  return [`${day}-${month}`, `${hours}:${minutes}`];
  });
  
  const temps = Object.values(measurements).map(m => m.temp);
  const hums = Object.values(measurements).map(m => m.hum);
new Chart(document.getElementById('comboChart'), {
  type: 'bar',
  data: {
    labels,
    datasets: [
      {
        type: 'line',
        label: 'Temperatura',
        data: temps,
        borderColor: '#ff6384',
        backgroundColor: '#ff6384',
        yAxisID: 'y',
      },
      {
        type: 'bar',
        label: 'Humedad',
        data: hums,
        backgroundColor: '#36a2eb',
        yAxisID: 'y1',
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        position: 'left',
        ticks: {
          color: '#ff6384'  // color de los números del eje izquierdo
        },
        title: {
          display: true,
          text: 'Temperatura (°C)',
          color: '#ff6384'  // color del título del eje izquierdo
        }
      },
      y1: {
        position: 'right',
        ticks: {
          color: '#36a2eb'  // color de los números del eje derecho
        },
        title: {
          display: true,
          text: 'Humedad (%)',
          color: '#36a2eb'  // color del título del eje derecho
        }
      }
    }
  }
});
});
  
