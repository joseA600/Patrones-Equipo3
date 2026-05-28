import { Route, Routes } from 'react-router-dom'

import { AppLayout } from '../components/layout/AppLayout'
import { Home } from '../pages/Home'
import { Materiales } from '../pages/Materiales'
import { Prestamos } from '../pages/Prestamos'
import { Reportes } from '../pages/Reportes'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Home />} />
        <Route path="materiales" element={<Materiales />} />
        <Route path="prestamos" element={<Prestamos />} />
        <Route path="reportes" element={<Reportes />} />
      </Route>
    </Routes>
  )
}
