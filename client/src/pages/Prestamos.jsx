import { useEffect, useState } from 'react'

import { Alert } from '../components/ui/Alert'
import { DataTable } from '../components/ui/DataTable'
import { PageHeader } from '../components/ui/PageHeader'
import { StatusBadge } from '../components/ui/StatusBadge'
import { getErrorMessage } from '../services/api'
import { getMateriales, sendMaterialToMantenimiento } from '../services/materialService'
import {
  createPrestamo,
  devolverPrestamo,
  getPrestamos,
} from '../services/prestamoService'

export function Prestamos() {
  const [materiales, setMateriales] = useState([])
  const [prestamos, setPrestamos] = useState([])
  const [form, setForm] = useState({ material_id: '', solicitante: '' })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function loadData() {
    try {
      const [materialesData, prestamosData] = await Promise.all([
        getMateriales(),
        getPrestamos(),
      ])
      setMateriales(materialesData)
      setPrestamos(prestamosData)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    Promise.all([getMateriales(), getPrestamos()])
      .then(([materialesData, prestamosData]) => {
        if (isMounted) {
          setMateriales(materialesData)
          setPrestamos(prestamosData)
        }
      })
      .catch((requestError) => {
        if (isMounted) {
          setError(getErrorMessage(requestError))
        }
      })
      .finally(() => {
        if (isMounted) {
          setLoading(false)
        }
      })

    return () => {
      isMounted = false
    }
  }, [])

  const disponibles = materiales.filter((material) => material.estado === 'Disponible')
  const prestamosActivos = prestamos.filter((prestamo) => prestamo.estado === 'activo')

  async function handleSubmit(event) {
    event.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')

    try {
      await createPrestamo(form)
      setForm({ material_id: '', solicitante: '' })
      setSuccess('Prestamo registrado correctamente')
      await loadData()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSaving(false)
    }
  }

  async function handleDevolver(prestamoId) {
    setError('')
    setSuccess('')

    try {
      await devolverPrestamo(prestamoId)
      setSuccess('Devolucion registrada correctamente')
      await loadData()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  async function handleMantenimiento(materialId) {
    setError('')
    setSuccess('')

    try {
      await sendMaterialToMantenimiento(materialId)
      setSuccess('Material enviado a mantenimiento')
      await loadData()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  const prestamoColumns = [
    { key: 'material_nombre', header: 'Material' },
    { key: 'solicitante', header: 'Solicitante' },
    {
      key: 'estado',
      header: 'Estado',
      render: (row) => <StatusBadge value={row.estado} />,
    },
    {
      key: 'acciones',
      header: 'Acciones',
      render: (row) => (
        <button
          className="button button-secondary"
          type="button"
          onClick={() => handleDevolver(row.id)}
        >
          Devolver
        </button>
      ),
    },
  ]

  const disponibleColumns = [
    { key: 'nombre', header: 'Material' },
    { key: 'tipo', header: 'Tipo' },
    {
      key: 'acciones',
      header: 'Acciones',
      render: (row) => (
        <button
          className="button button-secondary"
          type="button"
          onClick={() => handleMantenimiento(row.id)}
        >
          Mantenimiento
        </button>
      ),
    },
  ]

  return (
    <>
      <PageHeader
        eyebrow="Command"
        title="Prestamos y devoluciones"
        description="Ejecuta comandos para prestar, devolver y enviar materiales a mantenimiento."
      />

      <Alert>{error}</Alert>
      <Alert type="success">{success}</Alert>

      <section className="content-grid">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <h3>Registrar prestamo</h3>

          <label>
            Material disponible
            <select
              name="material_id"
              required
              value={form.material_id}
              onChange={(event) =>
                setForm((current) => ({ ...current, material_id: event.target.value }))
              }
            >
              <option value="">Selecciona un material</option>
              {disponibles.map((material) => (
                <option key={material.id} value={material.id}>
                  {material.nombre} · {material.tipo}
                </option>
              ))}
            </select>
          </label>

          <label>
            Solicitante
            <input
              required
              minLength="2"
              value={form.solicitante}
              onChange={(event) =>
                setForm((current) => ({ ...current, solicitante: event.target.value }))
              }
            />
          </label>

          <button className="button" disabled={saving || disponibles.length === 0} type="submit">
            {saving ? 'Registrando...' : 'Registrar prestamo'}
          </button>
        </form>

        <section className="panel table-panel">
          <div className="section-title">
            <h3>Prestamos activos</h3>
            <span>{loading ? 'Cargando...' : `${prestamosActivos.length} activos`}</span>
          </div>
          <DataTable
            columns={prestamoColumns}
            rows={prestamosActivos}
            emptyMessage="No hay prestamos activos"
          />
        </section>
      </section>

      <section className="panel table-panel wide-panel">
        <div className="section-title">
          <h3>Materiales disponibles</h3>
          <span>{disponibles.length} disponibles</span>
        </div>
        <DataTable
          columns={disponibleColumns}
          rows={disponibles}
          emptyMessage="No hay materiales disponibles"
        />
      </section>
    </>
  )
}
