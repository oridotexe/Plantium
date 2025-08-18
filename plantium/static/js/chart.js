document.addEventListener('DOMContentLoaded', () => {
  const measurements = JSON.parse(
    document.getElementById('measurements-data').textContent
  );
  console.log("hola");
    let dateStr = Object.values(measurements).map(m => m.date);
    const date = new Date(dateStr.replace(" ", "T")); 


    const day = date.getDate().toString().padStart(2, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0");

    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");

  const labels = `${day}/${month}\n${hours}:${minutes}`;
  console.log(labels);
  
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
  
