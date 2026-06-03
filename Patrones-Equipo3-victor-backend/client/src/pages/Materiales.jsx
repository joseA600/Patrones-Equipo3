import { useEffect, useState } from 'react'

import { Alert } from '../components/ui/Alert'
import { DataTable } from '../components/ui/DataTable'
import { PageHeader } from '../components/ui/PageHeader'
import { StatusBadge } from '../components/ui/StatusBadge'
import { getErrorMessage } from '../services/api'
import {
  createMaterial,
  darDeBajaMaterial,
  getMateriales,
  sendMaterialToMantenimiento,
  updateMaterialEstado,
} from '../services/materialService'
import { createPrestamo } from '../services/prestamoService'

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
  const [prestandoId, setPrestandoId] = useState(null)
  const [solicitante, setSolicitante] = useState('')

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

  async function handleRestaurar(materialId) {
    setError('')
    setSuccess('')

    try {
      await updateMaterialEstado(materialId, 'Disponible')
      setSuccess('Material restaurado a disponible')
      await loadMateriales()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  async function handleDarDeBaja(materialId) {
    setError('')
    setSuccess('')

    try {
      await darDeBajaMaterial(materialId)
      setSuccess('Material dado de baja y eliminado')
      await loadMateriales()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  async function handlePrestar(materialId) {
    if (!solicitante.trim()) {
      setError('Ingresa el nombre del solicitante')
      return
    }
    setError('')
    setSuccess('')

    try {
      await createPrestamo({ material_id: materialId, solicitante: solicitante.trim() })
      setSuccess('Material prestado correctamente')
      setPrestandoId(null)
      setSolicitante('')
      await loadMateriales()
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }

  function renderAcciones(row) {
    if (row.estado === 'Disponible') {
      if (prestandoId === row.id) {
        return (
          <div className="acciones-inline">
            <input
              className="input-inline"
              placeholder="Nombre del solicitante"
              value={solicitante}
              onChange={(e) => setSolicitante(e.target.value)}
            />
            <button
              className="button button-sm"
              type="button"
              onClick={() => handlePrestar(row.id)}
            >
              Confirmar
            </button>
            <button
              className="button button-secondary button-sm"
              type="button"
              onClick={() => { setPrestandoId(null); setSolicitante('') }}
            >
              Cancelar
            </button>
          </div>
        )
      }
      return (
        <div className="acciones-group">
          <button
            className="button button-sm"
            type="button"
            onClick={() => { setPrestandoId(row.id); setSolicitante('') }}
          >
            Prestar
          </button>
          <button
            className="button button-secondary button-sm"
            type="button"
            onClick={() => handleMantenimiento(row.id)}
          >
            Mantenimiento
          </button>
          <button
            className="button button-danger button-sm"
            type="button"
            onClick={() => handleDarDeBaja(row.id)}
          >
            Dar de Baja
          </button>
        </div>
      )
    }

    if (row.estado === 'EnMantenimiento') {
      return (
        <div className="acciones-group">
          <button
            className="button button-sm"
            type="button"
            onClick={() => handleRestaurar(row.id)}
          >
            Restaurar
          </button>
          <button
            className="button button-danger button-sm"
            type="button"
            onClick={() => handleDarDeBaja(row.id)}
          >
            Dar de Baja
          </button>
        </div>
      )
    }

    return <span style={{ color: '#aaa' }}>—</span>
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
      render: renderAcciones,
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
