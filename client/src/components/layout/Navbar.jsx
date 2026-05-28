import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Inicio' },
  { to: '/materiales', label: 'Materiales' },
  { to: '/prestamos', label: 'Prestamos' },
  { to: '/reportes', label: 'Reportes' },
]

export function Navbar() {
  return (
    <header className="navbar">
      <div>
        <span className="eyebrow">Patrones de diseno</span>
        <h1>Inventario academico</h1>
      </div>

      <nav aria-label="Navegacion principal">
        {navItems.map((item) => (
          <NavLink key={item.to} to={item.to}>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </header>
  )
}
