import { Route, Routes } from 'react-router-dom'

import { AppLayout } from '../components/layout/AppLayout'
import { Home } from '../pages/Home'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Home />} />
      </Route>
    </Routes>
  )
}
