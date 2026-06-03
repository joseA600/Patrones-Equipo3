const labels = {
  Disponible: 'Disponible',
  Prestado: 'Prestado',
  EnMantenimiento: 'Mantenimiento',
  DadoDeBaja: 'Baja',
  activo: 'Activo',
  devuelto: 'Devuelto',
}

export function StatusBadge({ value }) {
  return (
    <span className={`status-badge status-${value}`}>
      {labels[value] ?? value}
    </span>
  )
}
