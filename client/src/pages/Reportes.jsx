import { useEffect, useState } from 'react'

import { Alert } from '../components/ui/Alert'
import { DataTable } from '../components/ui/DataTable'
import { PageHeader } from '../components/ui/PageHeader'
import { StatusBadge } from '../components/ui/StatusBadge'
import { getErrorMessage } from '../services/api'
import { getBitacora } from '../services/bitacoraService'
import { getMateriales } from '../services/materialService'

function formatDate(value) {
  return new Intl.DateTimeFormat('es-MX', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export function Reportes() {
  const [materiales, setMateriales] = useState([])
  const [bitacora, setBitacora] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadReportes() {
      try {
        const [materialesData, bitacoraData] = await Promise.all([
          getMateriales(),
          getBitacora(),
        ])
        setMateriales(materialesData)
        setBitacora(bitacoraData)
      } catch (requestError) {
        setError(getErrorMessage(requestError))
      } finally {
        setLoading(false)
      }
    }

    loadReportes()
  }, [])

  const disponibles = materiales.filter((material) => material.estado === 'Disponible')
  const prestados = materiales.filter((material) => material.estado === 'Prestado')
  const mantenimiento = materiales.filter(
    (material) => material.estado === 'EnMantenimiento',
  )

  const materialColumns = [
    { key: 'nombre', header: 'Material' },
    { key: 'tipo', header: 'Tipo' },
    {
      key: 'estado',
      header: 'Estado',
      render: (row) => <StatusBadge value={row.estado} />,
    },
  ]

  const bitacoraColumns = [
    { key: 'tipo_evento', header: 'Evento' },
    { key: 'material_nombre', header: 'Material' },
    { key: 'descripcion', header: 'Descripcion' },
    {
      key: 'fecha',
      header: 'Fecha',
      render: (row) => formatDate(row.fecha),
    },
  ]

  return (
    <>
      <PageHeader
        eyebrow="Reportes"
        title="Estado general e historial"
        description="Consulta disponibles, prestados, mantenimiento, historial y bitacora generada por Observer."
      />

      <Alert>{error}</Alert>

      <section className="home-grid">
        <article className="metric">
          <span>Disponibles</span>
          <strong>{loading ? '...' : disponibles.length}</strong>
        </article>
        <article className="metric">
          <span>Prestados</span>
          <strong>{loading ? '...' : prestados.length}</strong>
        </article>
        <article className="metric">
          <span>Mantenimiento</span>
          <strong>{loading ? '...' : mantenimiento.length}</strong>
        </article>
        <article className="metric">
          <span>Bitacora</span>
          <strong>{loading ? '...' : bitacora.length}</strong>
        </article>
      </section>

      <section className="report-grid">
        <div className="panel table-panel">
          <h3>Disponibles</h3>
          <DataTable
            columns={materialColumns}
            rows={disponibles}
            emptyMessage="Sin materiales disponibles"
          />
        </div>
        <div className="panel table-panel">
          <h3>Prestados</h3>
          <DataTable
            columns={materialColumns}
            rows={prestados}
            emptyMessage="Sin materiales prestados"
          />
        </div>
        <div className="panel table-panel">
          <h3>Mantenimiento</h3>
          <DataTable
            columns={materialColumns}
            rows={mantenimiento}
            emptyMessage="Sin materiales en mantenimiento"
          />
        </div>
        <div className="panel table-panel">
          <h3>Historial y bitacora</h3>
          <DataTable
            columns={bitacoraColumns}
            rows={bitacora}
            emptyMessage="Sin eventos registrados"
          />
        </div>
      </section>
    </>
  )
}
