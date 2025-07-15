const express = require('express');
const morgan = require('morgan');

const app = express();
const port = 3000;

// Middleware para logging de peticiones
app.use(morgan('dev'));

// Middleware para servir archivos estáticos (css, js, imágenes)
app.use(express.static('public'));

// Ruta principal
app.get('/', (req, res) => {
  res.send('¡Servidor corriendo!');
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});

