import { useEffect, useState } from 'react'

import { PageHeader } from '../components/ui/PageHeader'
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
    <>
      <PageHeader
        eyebrow="Panel principal"
        title="Gestion de materiales con patrones de diseno"
        description="Sistema academico conectado a FastAPI y MongoDB para registrar materiales, prestamos, devoluciones, mantenimiento y bitacora."
      />

      <section className="home-grid">
        <article className="metric">
          <span>Backend</span>
          <strong>{serverStatus}</strong>
        </article>
        <article className="metric">
          <span>Arquitectura</span>
          <strong>Factory · State · Observer · Command</strong>
        </article>
        <article className="metric">
          <span>Base de datos</span>
          <strong>MongoDB</strong>
        </article>
      </section>
    </>
  )
}
