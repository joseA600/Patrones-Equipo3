import { useEffect, useState } from 'react'

import { getServerStatus } from '../services/healthService'

export function Home() {
  const [serverStatus, setServerStatus] = useState('Pendiente')

  useEffect(() => {
    let isMounted = true

    // Consulta inicial para confirmar que el frontend puede comunicarse con la API.
    getServerStatus()
      .then((data) => {
        if (isMounted) {
          setServerStatus(data.message)
        }
      })
      .catch(() => {
        if (isMounted) {
          setServerStatus('Servidor no disponible')
        }
      })

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <section className="home-page">
      <div className="intro">
        <p className="eyebrow">Base inicial</p>
        <h2>Sistema preparado para crecer con arquitectura limpia.</h2>
        <p>
          La aplicacion queda lista para incorporar modelos, rutas, servicios y
          patrones sin acoplar la interfaz con la logica del backend.
        </p>
      </div>

      <div className="status-panel">
        <span>Estado API</span>
        <strong>{serverStatus}</strong>
      </div>
    </section>
  )
}
