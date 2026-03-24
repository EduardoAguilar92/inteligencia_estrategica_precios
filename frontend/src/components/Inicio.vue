<template>
  <div class="home-container">
    <!-- Sección Hero (Bienvenida) -->
    <header class="hero">
      <h1>Bienvenido al Panel de Inteligencia Estratégica</h1>
      <p class="subtitle">Optimización de precios y análisis competitivo en tiempo real para Gran Chapur.</p>
    </header>

    <!-- Sección de Introducción -->
    <section class="intro-grid">
      <div class="card">
        <div class="icon">📊</div>
        <h3>Análisis de Datos</h3>
        <p>Visualiza tendencias de mercado y el comportamiento de la competencia de manera centralizada.</p>
      </div>

      <div class="card">
        <div class="icon">⚡</div>
        <h3>Decisiones Rápidas</h3>
        <p>Herramientas diseñadas para ajustar márgenes y precios con base en datos precisos.</p>
      </div>

      <div class="card">
        <div class="icon">🎯</div>
        <h3>Objetivos Estratégicos</h3>
        <p>Alinea los precios de cada categoría con las metas comerciales de la temporada.</p>
      </div>
    </section>

    <!-- Footer de la sección -->
    <footer class="home-footer">
      <p>Selecciona una opción en el menú superior para comenzar el análisis.</p>
    </footer>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Segoe UI', Roboto, sans-serif;
  color: #333;
}

.hero {
  text-align: center;
  margin-bottom: 60px;
}

.hero h1 {
  font-size: 2.5rem;
  color: #E30613; /* Rojo Chapur */
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
}

.intro-grid {
  display: flex;
  gap: 30px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.card {
  flex: 1;
  min-width: 250px;
  background: #f9f9f9;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  border-top: 4px solid #E30613;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.card h3 {
  margin-bottom: 15px;
  color: #2c2c2c;
}

.card p {
  line-height: 1.6;
  color: #555;
  font-size: 0.95rem;
}

.home-footer {
  margin-top: 60px;
  text-align: center;
  border-top: 1px solid #eee;
  padding-top: 20px;
  color: #999;
  font-style: italic;
}
</style>
