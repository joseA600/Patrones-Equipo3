import { NavLink, Outlet } from 'react-router-dom'

const navItems = [{ to: '/', label: 'Inicio' }]

export function AppLayout() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <span className="eyebrow">Patrones de diseno</span>
          <h1>Equipo 3</h1>
        </div>

        <nav aria-label="Navegacion principal">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to}>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main>
        <Outlet />
      </main>
    </div>
  )
}
