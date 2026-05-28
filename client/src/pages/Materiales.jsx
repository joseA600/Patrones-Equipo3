import { useEffect, useState } from 'react'

import { Alert } from '../components/ui/Alert'
import { DataTable } from '../components/ui/DataTable'
import { PageHeader } from '../components/ui/PageHeader'
import { StatusBadge } from '../components/ui/StatusBadge'
import { getErrorMessage } from '../services/api'
import {
  createMaterial,
  getMateriales,
  sendMaterialToMantenimiento,
} from '../services/materialService'

const initialForm = {
  nombre: '',
  tipo: 'Laptop',
  descripcion: '',
  estado: 'Disponible',
}

const tipos = ['Laptop', 'Router', 'Proyector', 'Adaptador', 'Cable']

export function Materiales() {
  const [materiales, setMateriales] = useState([])
  const [form, setForm] = useState(initialForm)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function loadMateriales() {
    try {
      setMateriales(await getMateriales())
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    getMateriales()
      .then((data) => {
        if (isMounted) {
          setMateriales(data)
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

  function handleChange(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')

    try {
      await createMaterial({
        ...form,
        descripcion: form.descripcion || null,
      })
      setForm(initialForm)
      setSuccess('Material registrado correctamente')
      await loadMateriales()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSaving(false)
    }
  }

  async function handleMantenimiento(materialId) {
    setError('')
    setSuccess('')

    try {
      await sendMaterialToMantenimiento(materialId)
      setSuccess('Material enviado a mantenimiento')
      await loadMateriales()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  const columns = [
    { key: 'nombre', header: 'Material' },
    { key: 'tipo', header: 'Tipo' },
    {
      key: 'estado',
      header: 'Estado',
      render: (row) => <StatusBadge value={row.estado} />,
    },
    {
      key: 'descripcion',
      header: 'Descripcion',
      render: (row) => row.descripcion || 'Sin descripcion',
    },
    {
      key: 'acciones',
      header: 'Acciones',
      render: (row) => (
        <button
          className="button button-secondary"
          disabled={row.estado === 'EnMantenimiento' || row.estado === 'DadoDeBaja'}
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
        eyebrow="Inventario"
        title="Materiales"
        description="Registra y consulta materiales administrados por MongoDB y Factory Method."
      />

      <Alert>{error}</Alert>
      <Alert type="success">{success}</Alert>

      <section className="content-grid">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <h3>Nuevo material</h3>

          <label>
            Nombre
            <input
              name="nombre"
              required
              minLength="2"
              value={form.nombre}
              onChange={handleChange}
            />
          </label>

          <label>
            Tipo
            <select name="tipo" value={form.tipo} onChange={handleChange}>
              {tipos.map((tipo) => (
                <option key={tipo} value={tipo}>
                  {tipo}
                </option>
              ))}
            </select>
          </label>

          <label>
            Descripcion
            <textarea
              name="descripcion"
              rows="4"
              value={form.descripcion}
              onChange={handleChange}
            />
          </label>

          <button className="button" disabled={saving} type="submit">
            {saving ? 'Guardando...' : 'Registrar material'}
          </button>
        </form>

        <section className="panel table-panel">
          <div className="section-title">
            <h3>Listado</h3>
            <span>{loading ? 'Cargando...' : `${materiales.length} registros`}</span>
          </div>
          <DataTable
            columns={columns}
            rows={materiales}
            emptyMessage="No hay materiales registrados"
          />
        </section>
      </section>
    </>
  )
}
